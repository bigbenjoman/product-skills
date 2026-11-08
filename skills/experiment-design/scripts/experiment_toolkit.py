"""
Experiment toolkit (A/B and multivariate tests).

  sample_size_per_arm(baseline, relative_mde, alpha=0.05, power=0.8)
  duration_weeks(n_per_arm, arms, eligible_visitors_per_week, traffic_share=1.0)
  srm_check(observed_counts, expected_shares)            sample-ratio mismatch (chi-square)
  readout(conv_a, n_a, conv_b, n_b, alpha=0.05)          two-proportion z-test with CI on the difference
  mvt_cells(levels_per_factor)                           how many cells a full-factorial MVT needs
  low_traffic_advice(n_per_arm, arms, weekly_visitors)   what to do instead when an A/B test would take too long

Usage:  python experiment_toolkit.py demo
"""
import sys, math
from statistics import NormalDist

_N = NormalDist()


def sample_size_per_arm(baseline, relative_mde, alpha=0.05, power=0.80, two_sided=True):
    """Visitors per arm to detect a relative lift `relative_mde` on conversion `baseline` (two proportions)."""
    p1 = baseline; p2 = baseline * (1 + relative_mde)
    za = _N.inv_cdf(1 - alpha / (2 if two_sided else 1)); zb = _N.inv_cdf(power)
    pbar = (p1 + p2) / 2
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return int(math.ceil(num / (p2 - p1) ** 2))


def duration_weeks(n_per_arm, arms, eligible_visitors_per_week, traffic_share=1.0):
    """Whole weeks only: weekday/weekend behaviour differs, so never stop mid-week. Minimum 1 week (2 preferred)."""
    weeks = n_per_arm * arms / (eligible_visitors_per_week * traffic_share)
    return max(1, math.ceil(weeks))


def srm_check(observed, expected_shares, alpha=0.001):
    """Chi-square goodness of fit. p < 0.001 means the split is broken: don't trust the result, find the bug."""
    total = sum(observed)
    chi2 = sum((o - total * e) ** 2 / (total * e) for o, e in zip(observed, expected_shares))
    df = len(observed) - 1
    # chi-square survival via Wilson-Hilferty normal approximation (good enough for df >= 1 at these sizes)
    if df == 1:
        p = 2 * (1 - _N.cdf(math.sqrt(chi2)))          # exact for one degree of freedom
    else:
        z = ((chi2 / df) ** (1 / 3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
        p = 1 - _N.cdf(z)
    return {"chi2": round(chi2, 2), "p": round(p, 6), "srm": p < alpha}


def readout(conv_a, n_a, conv_b, n_b, alpha=0.05):
    pa, pb = conv_a / n_a, conv_b / n_b
    pp = (conv_a + conv_b) / (n_a + n_b)
    se0 = math.sqrt(pp * (1 - pp) * (1 / n_a + 1 / n_b))
    z = (pb - pa) / se0
    p = 2 * (1 - _N.cdf(abs(z)))
    se = math.sqrt(pa * (1 - pa) / n_a + pb * (1 - pb) / n_b)
    zc = _N.inv_cdf(1 - alpha / 2)
    lo, hi = (pb - pa) - zc * se, (pb - pa) + zc * se
    return {"control": round(pa, 4), "variant": round(pb, 4), "abs_lift": round(pb - pa, 4),
            "rel_lift": round((pb - pa) / pa, 4), "ci_abs": (round(lo, 4), round(hi, 4)), "p": round(p, 4),
            "significant": p < alpha}


def mvt_cells(levels_per_factor):
    cells = 1
    for l in levels_per_factor: cells *= l
    return {"cells": cells, "warning": f"A full-factorial MVT needs {cells} arms; traffic per arm falls {cells/2:.0f}x versus an A/B test."}


def low_traffic_advice(n_per_arm, arms, weekly_visitors, max_weeks=6):
    w = duration_weeks(n_per_arm, arms, weekly_visitors)
    if w <= max_weeks:
        return {"weeks": w, "advice": "Run the A/B test. Pre-register the primary metric, guardrails and stop date."}
    return {"weeks": w, "advice": ("Too little traffic for an A/B test on this metric. Instead: (1) usability test 5 users x 3 rounds; "
            "(2) fake door / painted door with a pre-set threshold and a Wilson interval; (3) test a bigger change "
            "(larger MDE); (4) measure a higher-traffic upstream metric; (5) staged rollout with a holdout group "
            "and a before/after read, accepting weaker evidence.")}


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "demo":
    n = sample_size_per_arm(0.05, 0.10)
    print("5% baseline, 10% relative MDE, alpha 0.05, power 80% ->", n, "per arm")
    assert 30500 <= n <= 31500
    n2 = sample_size_per_arm(0.05, 0.20)
    print("Same with 20% MDE ->", n2, "per arm (about a quarter)")
    assert 7500 <= n2 <= 8500
    print("Duration at 20,000 eligible visitors/week, 2 arms:", duration_weeks(n, 2, 20000), "weeks")
    assert duration_weeks(n, 2, 20000) == 4
    s = srm_check([50_800, 49_200], [0.5, 0.5]); print("SRM 50,800 vs 49,200:", s); assert s["srm"]
    s2 = srm_check([50_100, 49_900], [0.5, 0.5]); print("SRM 50,100 vs 49,900:", s2); assert not s2["srm"]
    r = readout(1550, 31000, 1736, 31000)
    print("Readout:", r); assert r["significant"] and abs(r["rel_lift"] - 0.12) < 0.001
    print(mvt_cells([2, 3, 2]))
    adv = low_traffic_advice(n, 2, 600); print(adv); assert adv["weeks"] > 6
    print("\nALL EXPERIMENT ASSERTIONS PASSED")
