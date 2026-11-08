"""
MaxDiff + Kano toolkit.

  design(n_items, per_set, n_sets, n_versions)   balanced, position-randomised questionnaire versions
  export_design_csv / load_responses_csv          move data in and out of survey tools
  simulate(...)                                   teaching data only (label it SIMULATED)
  analyse(responses, n_items, sequential=True)    count scores, logit utilities, share of preference
  bootstrap_ci(responses, n_items)                95% intervals on share of preference (resample respondents)
  segment_cuts(responses, n_items, segment_of)    analyse per segment
  anchor_share(anchor_answers, n_items)           % saying "yes, I'd pay / it's essential" per item
  turf(anchor_answers, n_items, k)                best k-item bundle by reach
  kano_classify(functional, dysfunctional)        Kano category per answer pair (A/O/M/I/R/Q)
  kano_summary(pairs_by_item)                     category shares + Better/Worse coefficients

Usage:  python maxdiff_toolkit.py demo
"""
import itertools, random, sys, csv, json
import numpy as np


# ------------------------------------------------------------------ design
def _pair_counts(versions, n_items):
    c = np.zeros((n_items, n_items))
    for v in versions:
        for s in v:
            for a, b in itertools.combinations(s, 2):
                c[a, b] += 1; c[b, a] += 1
    return c


def design(n_items, per_set, n_sets, n_versions=10, seed=1, tries=600):
    """
    Each version: every item shown equally often (n_sets*per_set/n_items times), items placed in random
    positions within each set, sets in random order. Versions are built one after another, each minimising
    the spread of pair co-occurrence ACROSS ALL versions so far (zero-count pairs included).
    """
    rng = random.Random(seed)
    versions = []
    for _ in range(n_versions):
        best, best_score = None, None
        for _ in range(tries):
            shown = [0] * n_items
            sets = []
            for _ in range(n_sets):
                order = sorted(range(n_items), key=lambda i: (shown[i], rng.random()))
                s = rng.sample(order[: per_set + 2], per_set)
                rng.shuffle(s)                       # random position within the set
                sets.append(tuple(s))
                for i in s: shown[i] += 1
            pc = _pair_counts(versions + [sets], n_items)
            off = pc[np.triu_indices(n_items, 1)]   # includes pairs that never met (zeros)
            score = (max(shown) - min(shown)) * 100 + off.std()
            if best_score is None or score < best_score:
                best, best_score = sets, score
        rng.shuffle(best)                            # random set order
        versions.append(best)
    return versions


def export_design_csv(versions, items, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["version", "set", "position", "item_id", "item_text"])
        for vi, v in enumerate(versions):
            for si, s in enumerate(v):
                for pi, it in enumerate(s):
                    w.writerow([vi, si, pi, it, items[it]])


def load_responses_csv(path):
    """Columns: resp, segment (optional), set_items (semicolon-separated ids), best, worst."""
    out = []
    with open(path) as f:
        for r in csv.DictReader(f):
            out.append({"resp": r["resp"], "segment": r.get("segment", ""), "set": [int(x) for x in r["set_items"].split(";")],
                        "best": int(r["best"]), "worst": int(r["worst"])})
    return out


def save_responses_csv(responses, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["resp", "segment", "set_items", "best", "worst"])
        for t in responses:
            w.writerow([t["resp"], t.get("segment", ""), ";".join(map(str, t["set"])), t["best"], t["worst"]])


# ------------------------------------------------------------------ simulate (teaching only)
def simulate(versions, true_utils, n_resp, seed=7, segment_shift=None):
    rng = np.random.default_rng(seed)
    out = []
    for r in range(n_resp):
        seg = "A" if r % 2 == 0 else "B"
        u = np.array(true_utils, float) + rng.normal(0, 0.6, len(true_utils))
        if segment_shift and seg == "B": u = u + np.array(segment_shift)
        for s in versions[r % len(versions)]:
            s = list(s)
            g = u[s] + rng.gumbel(size=len(s)); best = s[int(np.argmax(g))]
            rest = [i for i in s if i != best]
            g2 = -u[rest] + rng.gumbel(size=len(rest)); worst = rest[int(np.argmax(g2))]
            out.append({"resp": r, "segment": seg, "set": s, "best": int(best), "worst": int(worst)})
    return out


# ------------------------------------------------------------------ analyse
def analyse(responses, n_items, sequential=True, iters=5000, lr=0.5, tol=1e-6, init=None):
    """
    Count score = (best - worst) / times shown, range -1..+1.
    Aggregate logit: best = max utility over the set; worst = min utility over the set MINUS the best item
    when sequential=True (respondents pick best first, then worst from what is left). Item 0 fixed at 0.
    Share of preference = exp(u) / sum(exp(u)) * 100 (scale-dependent: compare items, not studies).
    """
    shown = np.zeros(n_items); b = np.zeros(n_items); w = np.zeros(n_items)
    for t in responses:
        for i in t["set"]: shown[i] += 1
        b[t["best"]] += 1; w[t["worst"]] += 1
    counts = (b - w) / np.maximum(shown, 1)
    beta = np.zeros(n_items) if init is None else np.array(init, float); N = len(responses)
    converged = False
    for it in range(iters):
        grad = np.zeros(n_items)
        for t in responses:
            s = np.array(t["set"])
            e = np.exp(beta[s] - beta[s].max()); p = e / e.sum()
            grad[t["best"]] += 1; np.add.at(grad, s, -p)
            sw = s[s != t["best"]] if sequential else s
            e = np.exp(-beta[sw] - (-beta[sw]).max()); p = e / e.sum()
            grad[t["worst"]] -= 1; np.add.at(grad, sw, p)
        grad[0] = 0
        step = lr * grad / N
        beta += step
        if np.abs(step).max() < tol:
            converged = True; break
    share = np.exp(beta) / np.exp(beta).sum() * 100
    return {"shown": shown.tolist(), "best": b.tolist(), "worst": w.tolist(), "count_score": counts.round(3).tolist(),
            "utility": beta.round(3).tolist(), "share_of_preference": share.round(1).tolist(),
            "converged": converged, "iterations": it + 1}


def bootstrap_ci(responses, n_items, reps=200, seed=11, **kw):
    rng = np.random.default_rng(seed)
    by = {}
    for t in responses: by.setdefault(t["resp"], []).append(t)
    ids = list(by)
    full = analyse(responses, n_items, **kw)  # same convergence rule as the point estimate
    shares = []
    for _ in range(reps):
        sample = [t for i in rng.choice(ids, len(ids), replace=True) for t in by[i]]
        shares.append(analyse(sample, n_items, init=full["utility"], **kw)["share_of_preference"])
    a = np.array(shares)
    return {"estimate": full["share_of_preference"], "low": np.percentile(a, 2.5, axis=0).round(1).tolist(),
            "high": np.percentile(a, 97.5, axis=0).round(1).tolist()}


def segment_cuts(responses, n_items, key="segment"):
    segs = sorted({t.get(key, "") for t in responses})
    return {s: analyse([t for t in responses if t.get(key, "") == s], n_items)["share_of_preference"] for s in segs}


# ------------------------------------------------------------------ anchors + TURF
def anchor_share(anchor_answers, n_items):
    """anchor_answers: {resp: set(item ids the respondent said they'd pay for / is essential)}."""
    n = len(anchor_answers)
    return [round(100 * sum(i in a for a in anchor_answers.values()) / n, 1) for i in range(n_items)]


def turf(anchor_answers, n_items, k):
    """Exhaustive TURF: the k-item bundle reaching the most respondents (reach = has >=1 anchored item)."""
    best = (None, -1)
    for combo in itertools.combinations(range(n_items), k):
        cs = set(combo)
        reach = sum(1 for a in anchor_answers.values() if a & cs)
        if reach > best[1]: best = (combo, reach)
    return {"items": list(best[0]), "reach_pct": round(100 * best[1] / len(anchor_answers), 1)}


# ------------------------------------------------------------------ Kano
# Answers: 1 Like, 2 Expect (must-be), 3 Neutral, 4 Can live with it, 5 Dislike
# Standard Kano evaluation table: rows = functional answer, cols = dysfunctional answer.
_KANO = [
    # D:  Like Expect Neutral Live Dislike
    ["Q", "A", "A", "A", "O"],   # F = Like
    ["R", "I", "I", "I", "M"],   # F = Expect
    ["R", "I", "I", "I", "M"],   # F = Neutral
    ["R", "I", "I", "I", "M"],   # F = Can live with
    ["R", "R", "R", "R", "Q"],   # F = Dislike
]
KANO_NAMES = {"A": "Attractive (delighter)", "O": "One-dimensional (performance)", "M": "Must-be (parity)",
              "I": "Indifferent", "R": "Reverse", "Q": "Questionable"}


def kano_classify(functional, dysfunctional):
    return _KANO[functional - 1][dysfunctional - 1]


def kano_summary(pairs):
    """pairs: list of (functional, dysfunctional) answers for ONE feature."""
    cats = [kano_classify(f, d) for f, d in pairs]
    n = len(cats); share = {c: round(100 * cats.count(c) / n, 1) for c in "AOMIRQ"}
    a, o, m, i = (cats.count(c) for c in "AOMI")
    denom = max(a + o + m + i, 1)
    better = round((a + o) / denom, 2)          # how much satisfaction rises if present
    worse = round(-(o + m) / denom, 2)          # how much it falls if absent (negative)
    main = max("AOMI", key=lambda c: cats.count(c))
    return {"category": main, "category_name": KANO_NAMES[main], "shares_pct": share, "better": better, "worse": worse}


DEMO_ITEMS = [
    "Same-day delivery", "Saved templates", "Automatic suggestions",
    "Bulk export", "Price alerts", "Customer reviews",
    "Calendar sync", "Team sharing", "Printed certificate",
    "Member forum", "Personal onboarding call", "Lifetime archive",
]
DEMO_TRUE = [0.4, 0.3, 0.9, 0.8, 1.0, 0.6, 0.7, 0.2, -0.8, -0.3, 1.2, -0.1]

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "demo":
    n = len(DEMO_ITEMS)
    vs = design(n, per_set=4, n_sets=9, n_versions=10)
    # positions: every item should appear in every position roughly equally
    pos = np.zeros((n, 4))
    for v in vs:
        for s in v:
            for p, i in enumerate(s): pos[i, p] += 1
    assert (pos.sum(1) == 30).all(), "each item shown 3x per version x 10 versions"
    assert pos.min() >= 2 and pos.max() <= 15, f"positions too uneven: {pos.min()}..{pos.max()}"
    pc = _pair_counts(vs, n)[np.triu_indices(n, 1)]
    print(f"Design: each item shown 30x; position counts {int(pos.min())}-{int(pos.max())} (ideal 7.5); pair co-occurrence {int(pc.min())}-{int(pc.max())}")
    assert pc.max() - pc.min() <= 8

    resp = simulate(vs, DEMO_TRUE, n_resp=300)
    res = analyse(resp, n)
    corr = np.corrcoef(res["utility"], np.array(DEMO_TRUE) - DEMO_TRUE[0])[0, 1]
    print(f"Utility recovery: correlation with true utilities = {corr:.3f}")
    assert corr > 0.95
    order = np.argsort(res["share_of_preference"])[::-1]
    ci = bootstrap_ci(resp, n, reps=60)
    print("\nSIMULATED results (n=300):")
    for i in order:
        print(f"  {DEMO_ITEMS[i]:40s} share {res['share_of_preference'][i]:5.1f}%  95% CI {ci['low'][i]:5.1f}-{ci['high'][i]:5.1f}")
    assert all(l <= s <= h for l, s, h in zip(ci["low"], res["share_of_preference"], ci["high"]))

    save_responses_csv(resp, "/tmp/md_resp_test.csv")
    back = load_responses_csv("/tmp/md_resp_test.csv")
    assert len(back) == len(resp) and back[5]["best"] == resp[5]["best"]
    export_design_csv(vs, DEMO_ITEMS, "/tmp/md_design_test.csv")
    print("\nSegments:", {k: v[:3] for k, v in segment_cuts(resp, n).items()}, "...")

    rng = np.random.default_rng(5)
    anchors = {r: {i for i in range(n) if rng.random() < 0.15 + 0.1 * DEMO_TRUE[i]} for r in range(300)}
    a = anchor_share(anchors, n)
    t = turf(anchors, n, 3)
    print("Anchor % (would pay):", a[:4], "...  TURF best 3:", [DEMO_ITEMS[i] for i in t["items"]], f"reach {t['reach_pct']}%")
    assert 0 < t["reach_pct"] <= 100

    assert kano_classify(1, 5) == "O" and kano_classify(2, 5) == "M" and kano_classify(1, 3) == "A" and kano_classify(3, 3) == "I"
    assert kano_classify(5, 1) == "R" and kano_classify(1, 1) == "Q"
    ks = kano_summary([(2, 5)] * 12 + [(1, 5)] * 5 + [(3, 3)] * 3)
    print("Kano example (12 must-be, 5 performance, 3 indifferent):", ks)
    assert ks["category"] == "M" and ks["better"] == 0.25 and ks["worse"] == -0.85
    print("\nALL MAXDIFF/KANO ASSERTIONS PASSED")
