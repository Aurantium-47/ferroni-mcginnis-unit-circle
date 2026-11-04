# Exact computational checks

These are finite regression checks for the candidate analytic argument, not a
proof and not a numerical search for approximate roots. The recorded run uses
Python 3.12.14 and SymPy 1.14.0. SymPy is the only third-party dependency.

From the repository root:

```sh
python checks/run_all.py
```

The runner creates `results/` if needed and writes `results/summary.json`.
To record a plain terminal transcript
in a POSIX shell while preserving the runner's exit code:

```sh
set -o pipefail
mkdir -p results
python checks/run_all.py 2>&1 | tee results/verification.log
```

Alternatively, use `python -m checks.run_all`. Every module is importable without
running its checks. Each `check_*.py` script and `test_regressions.py` can also run
separately. All checks remain active under `python -O`.

## Coverage and independence

- `check_identities.py`: directly enumerates permutations and cycle-weight
  factors. It checks all **28** determinant identities with `1 <= n <= 7` and
  `1 <= k <= n`, plus **10** subset identities for capacities `(1,2,3)`,
  `(2,3,5)`, and `(1,2,3,4)`, with every admissible `k`. An additional **28**
  exact root counts check the determinant coefficient polynomials in `(-2,2)`.
- `check_unit_circle.py`: constructs the source polynomial independently by
  choosing the cycle containing the least unused label. A cycle on a fixed
  label set has `(size-1)!` cyclic orders. The algorithm uses neither the
  determinant nor the weighted-Lah recurrence. It checks **378** polynomials
  from capacities in `{1,2,3}`, up to coordinate permutation, with
  `1 <= n <= 6` and every `k`; then **26** more from `(1,1,2,3,5,8)`,
  `(1,2,3,4,5,6,7)`, `(2,2,2,3,3,3,5,5)`, and `(1,2,4,8,16)`, for a total of
  **404** exact certificates.
- The certificate removes one forced `x+1` factor in odd degree, transforms the
  reciprocal polynomial to `R(x+x^-1)`, and counts the roots of each square-free
  factor in `[-2,2]` by exact Sturm methods, retaining its multiplicity. This
  handles repeated roots and endpoints without floating-point root finding.
- `test_regressions.py`: covers constants, singleton and one-cycle cases,
  permutation invariance, independent enumeration/DP agreement, repeated and
  endpoint roots, exact reconstruction, counterexamples that must fail, and
  input validation. The API rejects zero polynomials and capacities outside
  the conjecture's strictly positive integer domain. It certifies reciprocal
  polynomials over the rationals, not arbitrary unit-circle polynomials.

The shared `_validation.py` contains input checks only. No mathematical
construction is shared between permutation enumeration and the subset DP.
The JSON summary records exact ranges, counts, software versions, and runtime
without recording local paths or user-specific information.
The runner exits nonzero on failure and replaces a prior summary before
starting, so a failed or interrupted run cannot leave a stale success report.
