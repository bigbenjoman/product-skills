"""
Pricing toolkit.

  van_westendorp(too_cheap, cheap, expensive, too_expensive) -> PMC, OPP, IDP, PME (+ validation report)
  nms_curves(cheap_price, cheap_likelihood, exp_price, exp_likelihood, grid) -> demand & revenue curves
  gabor_granger(prices, max_wtp)          -> CUMULATIVE demand (monotonic) + revenue index
  gg_from_segments(prices, shares_by_max) -> same curve from "share whose max price is X" tables
  net_revenue(price, vat, store_fee, variable_cost) -> what you actually keep per sale
  ltv(monthly_margin, monthly_churn), payback_months(cac, monthly_margin)
  arc_elasticity(p1, q1, p2, q2)
  wilson(successes, n) / n_for_margin(p, margin)  -> proportion CI and sample size (fake doors, surveys)

Usage:
  python pricing_toolkit.py demo
"""
import sys, math
import numpy as np


# ---------------------------------------------------------------- Van Westendorp
def _share_at_or_above(values, grid):
    v = np.sort(np.asarray(values, float))
    return 1 - np.searchsorted(v, grid, side="left") / len(v)


def _share_at_or_below(values, grid):
    v = np.sort(np.asarray(values, float))
    return np.searchsorted(v, grid, side="right") / len(v)


def _cdf_at(values, grid, ascending=True):
    """Back-compat helper."""
    v = np.sort(np.asarray(values, float))
    frac = np.searchsorted(v, grid, side="right") / len(v)
    return frac if ascending else 1 - frac


def _cross(grid, a, b):
    """First price where curve a crosses curve b. Returns None if they never cross."""
    d = a - b
    idx = np.where(np.diff(np.sign(d)) != 0)[0]
    if len(idx) == 0:
        return None
    i = idx[0]
    if d[i] == d[i + 1]:
        return float(grid[i])
    return float(grid[i] + (grid[i + 1] - grid[i]) * d[i] / (d[i] - d[i + 1]))


def validate_vw(too_cheap, cheap, expensive, too_expensive):
    """Keep respondents whose answers are ordered too_cheap < cheap < expensive < too_expensive."""
    a = np.array([too_cheap, cheap, expensive, too_expensive], float).T
    ok = (a[:, 0] < a[:, 1]) & (a[:, 1] < a[:, 2]) & (a[:, 2] < a[:, 3])
    return a[ok], {"respondents": int(len(a)), "kept": int(ok.sum()), "dropped_for_bad_order": int((~ok).sum())}


def van_westendorp(too_cheap, cheap, expensive, too_expensive, step=0.01, validate=True):
    """
    Standard crossings:
      PMC = 'too cheap' x 'not cheap'           (point of marginal cheapness)
      OPP = 'too cheap' x 'too expensive'       (optimal price point)
      IDP = 'cheap'     x 'expensive'           (indifference price point)
      PME = 'not expensive' x 'too expensive'   (point of marginal expensiveness)
    Any crossing that does not exist is returned as None (never crashes).
    """
    report = {}
    if validate:
        a, report = validate_vw(too_cheap, cheap, expensive, too_expensive)
        too_cheap, cheap, expensive, too_expensive = a.T
    hi = float(max(np.max(too_cheap), np.max(cheap), np.max(expensive), np.max(too_expensive)))
    grid = np.arange(0, hi + step, step)
    tc = _share_at_or_above(too_cheap, grid)      # % who call this price "too cheap" or cheaper threshold above it
    ch = _share_at_or_above(cheap, grid)
    ex = _share_at_or_below(expensive, grid)
    te = _share_at_or_below(too_expensive, grid)
    pts = {
        "PMC": _cross(grid, tc, 1 - ch),
        "OPP": _cross(grid, tc, te),
        "IDP": _cross(grid, ch, ex),
        "PME": _cross(grid, 1 - ex, te),
    }
    return {"points": pts, "validation": report}


# Assumption, documented: stated purchase likelihood overstates real purchase.
# Calibration weights translate a 5-point scale into an expected purchase probability.
NMS_WEIGHTS = {5: 0.70, 4: 0.30, 3: 0.0, 2: 0.0, 1: 0.0}


def nms_curves(cheap_price, cheap_likelihood, exp_price, exp_likelihood, grid, weights=NMS_WEIGHTS):
    """
    Newton-Miller-Smith extension. Each respondent gives a likelihood (1-5) at their own 'cheap' and
    'expensive' price. We calibrate likelihood -> probability with `weights` (an ASSUMPTION; change it if
    you have back-test data), interpolate linearly between the two prices, assume 0 above 'too expensive'
    style prices (here: beyond the expensive answer, probability falls to 0 at 1.5x expensive), and average.
    Returns demand (share) and revenue per 1,000 addressable people at each grid price.
    """
    cp, ep = np.asarray(cheap_price, float), np.asarray(exp_price, float)
    cl = np.array([weights[int(x)] for x in cheap_likelihood])
    el = np.array([weights[int(x)] for x in exp_likelihood])
    demand = []
    for p in grid:
        prob = np.where(p <= cp, cl,
               np.where(p <= ep, cl + (el - cl) * (p - cp) / np.maximum(ep - cp, 1e-9),
               np.where(p <= 1.5 * ep, el * (1.5 * ep - p) / (0.5 * ep), 0.0)))
        demand.append(prob.mean())
    demand = np.array(demand)
    return {"price": np.asarray(grid), "demand": demand, "revenue_per_1000": np.asarray(grid) * demand * 1000}


# ---------------------------------------------------------------- Gabor-Granger (corrected)
def gabor_granger(prices, max_wtp):
    """
    Correct adaptive Gabor-Granger analysis.
    max_wtp: one value per respondent = the highest tested price they said YES to (None = no to every price).
    demand(p) = share of ALL respondents whose max accepted price >= p. Monotonic by construction.
    (Dividing yeses by the number of people *shown* a price is wrong in an adaptive ladder: people only
    see high prices after saying yes to lower ones, so that group is pre-filtered.)
    """
    prices = np.asarray(sorted(prices), float)
    m = np.array([-np.inf if x is None else x for x in max_wtp], float)
    demand = np.array([(m >= p - 1e-9).mean() for p in prices])
    rev = prices * demand
    return {"price": prices.tolist(), "demand": demand.round(4).tolist(), "revenue_index": rev.round(2).tolist(),
            "revenue_max_price": float(prices[int(np.argmax(rev))])}


def gg_from_segments(prices, shares_by_max):
    """shares_by_max: {max_price_or_None: share}. Builds the same cumulative curve from a segment table."""
    prices = sorted(prices)
    demand = [sum(s for mp, s in shares_by_max.items() if mp is not None and mp >= p - 1e-9) for p in prices]
    rev = [p * d for p, d in zip(prices, demand)]
    return {"price": prices, "demand": [round(d, 4) for d in demand], "revenue_index": [round(r, 2) for r in rev],
            "revenue_max_price": prices[int(np.argmax(rev))]}


# ---------------------------------------------------------------- Economics
def net_revenue(price, vat=0.20, store_fee=0.0, variable_cost=0.0):
    """UK consumer prices include VAT. Strip VAT first, then the app-store/platform fee (0, 0.15 or 0.30), then cost."""
    ex_vat = price / (1 + vat)
    return round(ex_vat * (1 - store_fee) - variable_cost, 4)


def ltv(monthly_margin, monthly_churn):
    """Simple lifetime value = monthly contribution / monthly churn (geometric lifetime = 1/churn months)."""
    return round(monthly_margin / monthly_churn, 2)


def payback_months(cac, monthly_margin):
    return round(cac / monthly_margin, 1)


def arc_elasticity(p1, q1, p2, q2):
    """Midpoint (arc) elasticity: %change in quantity / %change in price, using averages as the base."""
    return ((q2 - q1) / ((q1 + q2) / 2)) / ((p2 - p1) / ((p1 + p2) / 2))


# ---------------------------------------------------------------- Proportions (fake doors, surveys)
def wilson(successes, n, z=1.96):
    """Wilson score interval for a proportion. Better than p +/- 1.96*SE when p is small or n is modest."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (round(p, 4), round(centre - half, 4), round(centre + half, 4))


def n_for_margin(p, margin, z=1.96):
    """Sample size so the 95% CI half-width is about `margin` (e.g. 0.03 = +/-3 points) at expected rate p."""
    return int(math.ceil(z * z * p * (1 - p) / (margin * margin)))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "demo":
    rng = np.random.default_rng(3)
    n = 162
    # SIMULATED, internally consistent answers: each respondent has a 'centre' price, thresholds scale around it.
    centre = rng.lognormal(np.log(22), 0.35, n)
    tc, ch, ex, te = centre * 0.40, centre * 0.70, centre * 1.35, centre * 2.0
    tc[:12] = ch[:12] * 1.2  # 12 deliberately mis-ordered respondents
    vw = van_westendorp(tc, ch, ex, te)
    print("Van Westendorp (SIMULATED):", vw["validation"])
    for k, v in vw["points"].items():
        print(f"  {k}: £{v:.2f}")
    assert vw["validation"]["dropped_for_bad_order"] == 12
    assert vw["points"]["PMC"] < vw["points"]["OPP"] <= vw["points"]["PME"]

    print("\nGabor-Granger, corrected, from a segment table (SYNTHETIC: Fernhill Coffee, n=200):")
    shares = {18: 0.18, 16: 0.10, 14: 0.34, 12: 0.08, 10: 0.14, None: 0.16}
    gg = gg_from_segments([10, 12, 14, 16, 18], shares)
    for p, d, r in zip(gg["price"], gg["demand"], gg["revenue_index"]):
        print(f"  £{p:<6} demand {d*100:5.1f}%   revenue index {r:5.2f}")
    print("  revenue-max price:", gg["revenue_max_price"])
    assert gg["demand"] == sorted(gg["demand"], reverse=True), "demand must be monotonic"
    assert abs(gg["demand"][0] - 0.84) < 1e-3 and abs(gg["demand"][2] - 0.62) < 1e-3 and abs(gg["demand"][4] - 0.18) < 1e-3
    assert gg["revenue_max_price"] == 14 and abs(gg["revenue_index"][2] - 8.68) < 0.01

    # Same answer from respondent-level data
    mw = [18] * 36 + [16] * 20 + [14] * 68 + [12] * 16 + [10] * 28 + [None] * 32
    assert gabor_granger([10, 12, 14, 16, 18], mw)["revenue_max_price"] == 14

    print("\nNMS (SIMULATED, weights 5->0.7, 4->0.3):")
    lk_c = rng.choice([3, 4, 5], n, p=[.3, .4, .3]); lk_e = rng.choice([1, 2, 3, 4], n, p=[.3, .3, .3, .1])
    nms = nms_curves(ch, lk_c, ex, lk_e, np.arange(5, 61, 5))
    best = nms["price"][int(np.argmax(nms["revenue_per_1000"]))]
    print("  revenue-max price on grid: £", best)
    assert all(np.diff(nms["demand"]) <= 1e-9), "NMS demand should not rise with price"

    print("\nNet revenue on a £14 monthly price:")
    for fee in (0.0, 0.15, 0.30):
        print(f"  store fee {int(fee*100):>2}% -> £{net_revenue(14, store_fee=fee):.2f} kept (ex VAT)")
    assert abs(net_revenue(14) - 11.6667) < 1e-3
    print("  LTV at £12 margin, 8% monthly churn:", ltv(12, 0.08), "| payback on £60 CAC:", payback_months(60, 12), "months")
    e = arc_elasticity(9.99, 1000, 10.99, 880)
    print(f"  arc elasticity £9.99->£10.99, 1000->880 buyers: {e:.2f}")
    assert -1.5 < e < -1.2

    print("\nFake door: 74 clicks from 412 visitors:", wilson(74, 412), "| n for +/-3pts at 15%:", n_for_margin(0.15, 0.03))
    p, lo, hi = wilson(74, 412)
    assert 0.14 < lo < 0.15 and 0.21 < hi < 0.22 and n_for_margin(0.15, 0.03) == 545
    print("\nALL PRICING ASSERTIONS PASSED")
