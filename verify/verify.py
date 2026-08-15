"""Verification for the small-support results of Paper A.

Certifies the finite computations behind two results (paper labels):

  [prop-small-slices]  For 1 <= m <= 5 the slice supremum g_Z(m) is attained
      at 2^13, 2^6 3^4, 2^5 3^2 5^2, 2^5 3^2 5*7, 2^4 3^2 5*7*11, uniquely.
      Method: exhaustive enumeration of all n in [5041, 10^7] via a smallest-
      prime-factor sieve, plus the tail bound  sigma(n)/n < P_m (P_m the
      product of p/(p-1) over the first m primes), which gives
      log G(n) < log P_m - gamma - log log log n for omega(n) = m.  The bound
      decreases in n and is checked to fall below the claimed maximum at
      n = 10^7, so the enumeration is exhaustive over the whole tail.

  [prop-eventual-prefix]  The boundary window [5041, 55440) has its maximum
      of log G at n = 10080 (runner-up 27720), every window integer has at
      most six distinct prime factors, the slice values satisfy
      g_Z(k) < log G(10080) for 5 <= k <= 29, and g_Z(30) > log G(10080).
      The slice values for k >= 6 are computed by the score-ordered prefix
      scan; their identification with g_Z(k) uses the integer-optimizer
      characterization of the paper (thm-integer-prefix), not re-proved here.

  [prefix list]  The first nine score-ordered prefixes of the bounded-support
      ordering (first exponents optional) are 2, 6, 12, 60, 120, 360, 2520,
      5040, 55440, with no score ties among the leading increments.

Run:  uv run python <path-to>/verify.py
"""

from mpmath import mp, mpf, log, euler

mp.dps = 50
ok_all = True

GAMMA = +euler
N_BRUTE = 10_000_000
LOW = 5041
WINDOW_TOP = 55440
CLAIMED = {1: 8192, 2: 5184, 3: 7200, 4: 10080, 5: 55440}


def report(name, cond, detail=""):
    global ok_all
    status = "PASS" if cond else "FAIL"
    if not cond:
        ok_all = False
    print(f"[{status}] {name}  {detail}")


def log_G(sig, n):
    """log G(n) = log sigma - log n - gamma - log log log n, exact inputs."""
    return log(mpf(sig)) - log(mpf(n)) - GAMMA - log(log(log(mpf(n))))


# ---------------------------------------------------------------- Part A
# Exhaustive enumeration over [5041, 10^7]: top-3 per slice m <= 5 (float
# preselection, mpmath re-evaluation), window top-2, window omega bound.

print("sieving and enumerating to 10^7 (takes a minute or two) ...")
spf = list(range(N_BRUTE + 1))
i = 2
while i * i <= N_BRUTE:
    if spf[i] == i:
        for j in range(i * i, N_BRUTE + 1, i):
            if spf[j] == j:
                spf[j] = i
    i += 1

import math

top = {m: [] for m in range(1, 7)}   # m -> list of (float log G, n, sigma)
window_top = []                       # over all omega, n < 55440
window_omega_max = 0
for n in range(LOW, N_BRUTE + 1):
    x = n
    sig = 1
    om = 0
    while x > 1:
        p = spf[x]
        pk = 1
        while x % p == 0:
            x //= p
            pk *= p
        om += 1
        sig *= (pk * p - 1) // (p - 1)
    if om > 6 and n >= WINDOW_TOP:
        continue
    v = math.log(sig / n) - 0.5772156649015329 - math.log(math.log(math.log(n)))
    if om <= 6:
        t = top[om]
        t.append((v, n, sig))
        if len(t) > 3:
            t.sort(reverse=True)
            t.pop()
    if n < WINDOW_TOP:
        window_omega_max = max(window_omega_max, om)
        window_top.append((v, n, sig))
        if len(window_top) > 2:
            window_top.sort(reverse=True)
            window_top.pop()

g_slice = {}         # m -> mp log G at the certified maximizer
for m in range(1, 6):
    cand = sorted(((log_G(sig, n), n) for v, n, sig in top[m]), reverse=True)
    (g1, n1), (g2, n2) = cand[0], cand[1]
    g_slice[m] = g1
    report(
        f"slice m={m} maximizer",
        n1 == CLAIMED[m] and g1 - g2 > mpf("1e-8"),
        f"n={n1} logG={mp.nstr(g1, 8)} runner-up n={n2} margin={mp.nstr(g1 - g2, 4)}",
    )

# Tail bound: log P_m - gamma - log log log(10^7) < g_Z(m) for each m <= 5.
PRIMES5 = [2, 3, 5, 7, 11]
for m in range(1, 6):
    logPm = sum(log(mpf(p)) - log(mpf(p - 1)) for p in PRIMES5[:m])
    tail = logPm - GAMMA - log(log(log(mpf(N_BRUTE))))
    report(
        f"tail bound m={m} at 10^7",
        tail < g_slice[m],
        f"bound={mp.nstr(tail, 6)} < gZ({m})={mp.nstr(g_slice[m], 6)}",
    )

# Window facts.
wg1, wn1, ws1 = window_top[0]
wg2, wn2, ws2 = window_top[1]
G10080 = log_G(ws1, wn1)
report(
    "window max at 10080",
    wn1 == 10080 and G10080 - log_G(ws2, wn2) > mpf("1e-8"),
    f"logG(10080)={mp.nstr(G10080, 8)} runner-up n={wn2} "
    f"margin={mp.nstr(G10080 - log_G(ws2, wn2), 4)}",
)
report("window omega <= 6", window_omega_max <= 6, f"max omega={window_omega_max}")

# ---------------------------------------------------------------- Part C
# Score-ordered prefix scan of the slices 5 <= k <= 30 (first exponents
# mandatory, increments ordered by decreasing score, all values in mpmath).

import heapq


def primes_first(k):
    ps, x = [], 2
    while len(ps) < k:
        if all(x % q for q in ps if q * q <= x):
            ps.append(x)
        x += 1
    return ps


def slice_value(k):
    ps = primes_first(k)
    logn = sum(log(mpf(p)) for p in ps)
    logsig = sum(log(mpf(p + 1)) - log(mpf(p)) for p in ps)
    h = []
    for p in ps:
        mult = (1 - mpf(p) ** -3) / (1 - mpf(p) ** -2)
        heapq.heappush(h, (-float(log(mult) / log(mpf(p))), p, 1))
    best = mpf(-100)
    limit = 3 * logn + 60
    cur = mpf(-100)
    while h and logn <= limit:
        if logn >= log(mpf(LOW)):
            cur = logsig - GAMMA - log(log(logn))
            if cur > best:
                best = cur
        _, p, a = heapq.heappop(h)
        mult = (1 - mpf(p) ** -(a + 2)) / (1 - mpf(p) ** -(a + 1))
        logsig += log(mult)
        logn += log(mpf(p))
        a += 1
        nxt = (1 - mpf(p) ** -(a + 2)) / (1 - mpf(p) ** -(a + 1))
        heapq.heappush(h, (-float(log(nxt) / log(mpf(p))), p, a))
    assert best - cur > mpf("0.01"), f"peak not interior for k={k}"
    return best

scan5, scan6 = slice_value(5), slice_value(6)
report("scan matches brute at k=5", abs(scan5 - g_slice[5]) < mpf("1e-30"),
       f"|diff|={mp.nstr(abs(scan5 - g_slice[5]), 3)}")
cand6 = sorted(((log_G(sig, n), n) for v, n, sig in top[6]), reverse=True)
report("scan matches brute at k=6", abs(scan6 - cand6[0][0]) < mpf("1e-30"),
       f"brute n={cand6[0][1]}")

worst_margin, worst_k = mpf(100), None
for k in range(5, 30):
    gk = slice_value(k) if k >= 7 else (scan5 if k == 5 else scan6)
    margin = G10080 - gk
    if margin < worst_margin:
        worst_margin, worst_k = margin, k
    if margin <= 0:
        report(f"slice k={k} below logG(10080)", False, f"gZ={mp.nstr(gk, 8)}")
report(
    "slices 5..29 below logG(10080)",
    worst_margin > mpf("1e-8"),
    f"worst k={worst_k} margin={mp.nstr(worst_margin, 4)}",
)
g30 = slice_value(30)
report(
    "slice k=30 above logG(10080)",
    g30 - G10080 > mpf("1e-8"),
    f"gZ(30)={mp.nstr(g30, 8)} margin={mp.nstr(g30 - G10080, 4)}",
)

print("gZ(29) =", mp.nstr(slice_value(29), 8))

# ---------------------------------------------------------------- Part B
# First nine score-ordered prefixes of the bounded-support ordering, where
# first-exponent increments are optional and every increment (p, a -> a+1)
# has score log(mult)/log(p).

incs = []
for p in primes_first(25):
    for a in range(0, 12):
        mult = (1 - mpf(p) ** -(a + 2)) / (1 - mpf(p) ** -(a + 1))
        incs.append((log(mult) / log(mpf(p)), p))
incs.sort(key=lambda t: -t[0])
min_gap = min(incs[i][0] - incs[i + 1][0] for i in range(11))
seq = []
n = 1
for _, p in incs[:9]:
    n *= p
    seq.append(n)
report(
    "first nine score-ordered prefixes",
    seq == [2, 6, 12, 60, 120, 360, 2520, 5040, 55440]
    and min_gap > mpf("1e-12"),
    f"sequence {seq} min score gap {mp.nstr(min_gap, 3)}",
)

print("ALL CHECKS PASSED" if ok_all else "SOME CHECKS FAILED")
raise SystemExit(0 if ok_all else 1)
