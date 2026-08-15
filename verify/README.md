# Exact-verification supplement

This directory contains the certificate script for every finite
computation stated in the manuscript. All values are computed with
`mpmath` at 50 significant digits, and every comparison is asserted with
an explicit margin. The script prints one `PASS`/`FAIL` line per check
and exits nonzero if any check fails.

```sh
uv run python verify/verify.py    # from the repository root, 2-3 minutes
```

What is certified, keyed to the manuscript's labels:

- **Small slices (`prop-small-slices`).** For each $m \leq 5$, an
  exhaustive enumeration of the integers in $[5041, 10^7]$ by a
  smallest-prime-factor sieve locates the slice maximizer of
  $\log G(n)$ and its runner-up margin, and the tail bound
  $\sigma(n)/n < \prod_{i \leq m} p_i/(p_i - 1)$ is checked to fall
  below each maximum at $10^7$, so the enumeration is exhaustive over
  the whole tail. The certified maximizers are $2^{13}$, $2^6 3^4$,
  $2^5 3^2 5^2$, $10080$, and $55440$.
- **Boundary window (`prop-eventual-prefix`).** The maximum of
  $\log G$ over the window $[5041, 55440)$ is at $10080$, the runner-up
  $27720$ is lower by about $0.0076$, and every window integer has at
  most six distinct prime factors.
- **Slice scan and the $m = 30$ crossover
  (`prop-eventual-prefix`).** The score-ordered prefix scan evaluates
  the slice maxima $g_{\mathbf{Z}}(k)$ for $6 \leq k \leq 30$ and
  certifies $g_{\mathbf{Z}}(k) < \log G(10080)$ through $k = 29$ (the
  tightest case is $k = 29$, short by about $1.3 \times 10^{-4}$) and
  $g_{\mathbf{Z}}(30) > \log G(10080)$. This part identifies the scan
  maximum with $g_{\mathbf{Z}}(k)$ through the manuscript's
  integer-optimizer characterization (`thm-integer-prefix`); that
  theorem is proved in the paper, not re-derived here. The scan is
  cross-checked against the exhaustive enumeration at $k = 5$ and
  $k = 6$.
- **Prefix list.** The first nine score-ordered prefixes of the
  bounded-support ordering are $2, 6, 12, 60, 120, 360, 2520, 5040,
  55440$, with no score ties among the leading increments.
