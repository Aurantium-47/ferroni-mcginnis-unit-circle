# Reproducible verification

The analytic proof is in [PROOF.md](PROOF.md). The checks here are independent finite regression tests; none is needed as a premise of the proof.

## Environment and execution

Reference environment: Python 3.12.14, SymPy 1.14.0. `requirements.txt` pins the direct mathematical dependency. Python 3.10 or newer is required; no other Python version is claimed to have been tested in the reference run.

From the repository root:

```sh
python -m pip install -r requirements.txt
python checks/run_all.py
```

All computation runs locally after installation. The check scripts do not fetch data, contact services, use credentials or publish results.

## Identity checks

`checks/check_identities.py` constructs the polynomial from permutations and cycle weights. It compares that polynomial to the separately constructed path-matrix determinant.

- Every pair $`1\le k\le n\le7`$: **28 identities**.
- Subset/rising-factorial formula for $`(1,2,3)`$, $`(2,3,5)`$ and $`(1,2,3,4)`$, each at every admissible cycle count: **10 identities**.
- Additionally, **28 exact root counts** verify the determinant coefficient polynomials in the open interval $`(-2,2)`$ for the same $`(n,k)`$ range.
- Calculations use exact integers and rationals; no floating-point tolerance is involved.

## Independent root checks

`checks/check_unit_circle.py` starts from a subset-cycle dynamic program. Choose the cycle containing the least remaining label. A selected block $`C`$ has $`(|C|-1)!`$ cyclic orders and weight factor $`[c(C)]_x`$. Recursing on its complement counts every permutation once. This computation does not use the determinant or the recurrence in the proof.

Coverage:

1. All sorted capacity vectors with entries in $`\{1,2,3\}`$ and length $`1\le n\le6`$, all $`k`$: **378 polynomials**. Sorting removes coordinate permutations, which leave the polynomial unchanged by relabelling.
2. All $`k`$ for $`(1,1,2,3,5,8)`$, $`(1,2,3,4,5,6,7)`$, $`(2,2,2,3,3,3,5,5)`$ and $`(1,2,4,8,16)`$: **26 polynomials**.

Total: **404 polynomials**.

For a reciprocal polynomial of odd degree, the program first divides out the forced factor $`x+1`$. If the remaining degree is $`2h`$, it constructs $`R(y)`$ satisfying

```math
x^{-h}P(x)=R(x+x^{-1}).
```

The identity $`x^j+x^{-j}=y(x^{j-1}+x^{1-j})-(x^{j-2}+x^{2-j})`$ provides an exact recurrence for the transformation. Each square-free factor of $`R`$ is checked by exact Sturm root counting in the closed interval $`[-2,2]`$. Multiplicities are restored when the counts are summed. Equality with $`\deg R`$ proves that every root of that particular polynomial lies on the unit circle. Closed endpoints correctly allow the roots $`x=\pm1`$ in the general certification routine.

This is a different transform from the analytic proof's doubled substitution $`P(z^2)=z^dQ(z+z^{-1})`$. The scripts and exposition keep those variables and degrees separate.

## Regression tests

`checks/test_regressions.py` tests extreme cycle counts, constants, repeated roots, interval endpoints and invalid or false examples. The run summary reports the exact test count; it is not combined with the 404 coverage count.

## Reference results

The reference [JSON summary](../results/summary.json) and [terminal log](../results/verification.log) are in `results/`. See those records for the exact command outcomes and environment versions. A pass is a report about those inputs and that code, not a peer-review decision.

The original SVG can be regenerated with:

```sh
python scripts/make_figure.py
```

Its coordinates come from numerical roots of directly enumerated example polynomials; `assets/example-data.json` records the exact polynomial coefficients and approximate coordinates. The figure is explanatory and is never used by the exact certification suite.
