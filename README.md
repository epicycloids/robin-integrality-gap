# The integrality gap in Robin's inequality

Current tagged release: version 0.1.0 (August 2026).

This repository contains the manuscript **"The Integrality Gap in Robin's
Inequality with a Fixed Number of Prime Factors"** (Logan Bell) together
with its exact-verification supplement. Each tagged release is a stable
snapshot: its claims and supporting artifacts are those contained in that
tag.

Robin's inequality, $\sigma(n) < e^{\gamma} n \log\log n$ for
$n \geq 5041$, is equivalent to the Riemann hypothesis. The paper studies
the largest normalized divisor sum among integers with exactly $m$ distinct
prime factors, together with the relaxation obtained by allowing real
exponents. The main theorem evaluates the integrality gap between the two
optima,

$$g_{\mathbf{R}}(m) - g_{\mathbf{Z}}(m) = \frac{2\sqrt{2} + o(1)}{\sqrt{p_m}\\,\log p_m},$$

unconditionally, where $p_m$ is the $m$th prime. Combining the gap with
Nicolas's integrated explicit formula shows that the Riemann hypothesis is
equivalent to Robin's inequality holding on every sufficiently large
fixed-$\omega$ slice. The paper also settles the small-support cases
$m \leq 5$ by finite verification and proves a dichotomy for the
bounded-support problem $\omega(n) \leq m$: the maximum is attained at
$10080 = 2^5 3^2 5 \cdot 7$ for every $6 \leq m \leq 29$, and only from
$m = 30$ on do the score-ordered prefixes take over.

## Layout

- [`paper/`](paper/) — the LaTeX sources (`main.tex`, `refs.bib`,
  `sections/`).
- [`verify/`](verify/) — the exact-verification supplement; see its
  [README](verify/README.md) for exactly what is certified and by what
  method.
- [`verify.sh`](verify.sh) — checks the source manifest, replays the
  certificate, and builds the manuscript.

## Verifying

The repository's root `pyproject.toml` and `uv.lock` own one frozen Python
environment for the supplement. To replay the certificate alone
(about two to three minutes, standard hardware):

```sh
uv run python verify/verify.py
```

To check the source manifest, replay the certificate, and build the
manuscript in one pass:

```sh
./verify.sh            # pass --no-latex to skip the manuscript build
```

## Building the manuscript

The manuscript builds with [Tectonic](https://tectonic-typesetting.github.io/):

```sh
tectonic --reruns 9 paper/main.tex
```

## Licensing and citation

Licensing is dual, described in [`LICENSE`](LICENSE): the manuscript and
explanatory text are CC BY 4.0, and the verification software and
repository configuration are MIT. Citation metadata is in
[`CITATION.cff`](CITATION.cff).
