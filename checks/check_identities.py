"""Exact symbolic identities, with the source polynomials enumerated directly.

The left side is formed from actual permutations and their cycles. It does not
use the determinant, the weighted-Lah recurrence, or the subset-cycle DP.
The checks are finite regression evidence, not a proof of the conjecture.
"""

from collections.abc import Callable, Iterable
from itertools import permutations
from math import factorial

import sympy as sp

if __package__:
    from ._validation import capacities, integer, parameters, require
else:
    from _validation import capacities, integer, parameters, require


x, y, z, s, t = sp.symbols("x y z s t")
ASYMMETRIC_CAPACITIES = ((1, 2, 3), (2, 3, 5), (1, 2, 3, 4))


def _cycle_capacities(permutation: tuple[int, ...], c: tuple[int, ...]) -> list[int]:
    seen: set[int] = set()
    result = []
    for start in range(len(c)):
        if start in seen:
            continue
        current, capacity = start, 0
        while current not in seen:
            seen.add(current)
            capacity += c[current]
            current = permutation[current]
        result.append(capacity)
    return result


def enumerate_polynomials(values: Iterable[int]) -> tuple[sp.Poly, ...]:
    """Compute P(c,k) for k=1,...,n by visiting every permutation once.

    Result entry k-1 corresponds to k cycles. Polynomial products are expanded
    by direct integer convolution of their factors 1+x+...+x^(capacity-1).
    Runtime is factorial in the number of capacities, by design.
    """
    c = capacities(values)
    totals = [[0] * (sum(c) - k + 1) for k in range(1, len(c) + 1)]
    for permutation in permutations(range(len(c))):
        cycle_capacities = _cycle_capacities(permutation, c)
        coefficients = [1]
        for capacity in cycle_capacities:
            product = [0] * (len(coefficients) + capacity - 1)
            for degree, coefficient in enumerate(coefficients):
                for offset in range(capacity):
                    product[degree + offset] += coefficient
            coefficients = product
        total = totals[len(cycle_capacities) - 1]
        for degree, coefficient in enumerate(coefficients):
            total[degree] += coefficient
    return tuple(sp.Poly.from_list(list(reversed(a)), x, domain=sp.ZZ) for a in totals)


def enumerate_polynomial(values: Iterable[int], k: int) -> sp.Poly:
    """Direct permutation enumeration of one source polynomial."""
    c, k = parameters(values, k)
    return enumerate_polynomials(c)[k - 1]


def determinant_polynomial(n: int) -> sp.Poly:
    """Return det(y I - T_(n-1) + s B_(n-1)), including the empty determinant."""
    n = integer(n, "n")
    if n < 1:
        raise ValueError("n must be positive")
    size = n - 1
    matrix = sp.zeros(size)
    for i in range(size):
        matrix[i, i] = y + s / sp.Integer(i + 1)
        if i:
            matrix[i, i - 1] = matrix[i - 1, i] = -1
    return sp.Poly(matrix.det(method="domain-ge"), y, s, domain=sp.QQ)


def subset_numerator(values: Iterable[int], k: int) -> sp.Poly:
    """Compute [t^k] sum_S (-t)^rising(|S|) t^rising(n-|S|) x^c(S)."""
    c, k = parameters(values, k)
    n = len(c)
    weights = [sp.expand(sp.rf(-t, a) * sp.rf(t, n - a)).coeff(t, k)
               for a in range(n + 1)]
    expression = 0
    for mask in range(1 << n):
        exponent = sum(c[i] for i in range(n) if mask & (1 << i))
        expression += weights[mask.bit_count()] * x**exponent
    return sp.Poly(expression, x, domain=sp.ZZ)


def run_checks(progress: Callable[[str], None] | None = print) -> dict:
    """Run the original 28 + 10 identities and 28 modest spectral checks."""
    symbolic_count = spectral_count = subset_count = 0
    for n in range(1, 8):
        determinant = determinant_polynomial(n).as_expr()
        for k, polynomial in enumerate(enumerate_polynomials((1,) * n), start=1):
            q = sp.Poly(determinant.coeff(s, k - 1), y, domain=sp.QQ)
            residual = sp.cancel(
                polynomial.as_expr().subs(x, z**2)
                - factorial(n - 1) * z**(n - k) * q.as_expr().subs(y, z + 1 / z)
            )
            require(residual == 0, f"determinant identity failed for n={n}, k={k}")
            symbolic_count += 1
            # Additional, inexpensive exact check on the determinant side only.
            require(q.degree() == n - k, f"unexpected Q degree for n={n}, k={k}")
            require(q.eval(-2) != 0 and q.eval(2) != 0,
                    f"Q has an endpoint root for n={n}, k={k}")
            real_count = sum(m * f.count_roots(-2, 2) for f, m in q.sqf_list()[1])
            require(real_count == q.degree(), f"spectral check failed for n={n}, k={k}")
            spectral_count += 1
        if progress:
            progress(f"PASS determinant identities and exact Q root counts: n={n}, k=1..{n}")
    for c in ASYMMETRIC_CAPACITIES:
        for k, polynomial in enumerate(enumerate_polynomials(c), start=1):
            lhs = sp.Poly((1 - x)**k * polynomial.as_expr(), x, domain=sp.ZZ)
            require(lhs == subset_numerator(c, k), f"subset identity failed for c={c}, k={k}")
            subset_count += 1
        if progress:
            progress(f"PASS asymmetric subset identities: c={c}, k=1..{len(c)}")
    require((symbolic_count, subset_count, spectral_count) == (28, 10, 28),
            "identity coverage changed unexpectedly")
    return {
        "determinant_identities": {"count": symbolic_count, "n_inclusive": [1, 7], "k": "1..n"},
        "asymmetric_subset_identities": {
            "count": subset_count, "capacities": [list(c) for c in ASYMMETRIC_CAPACITIES], "k": "1..n"
        },
        "supplemental_determinant_root_counts": {
            "count": spectral_count, "n_inclusive": [1, 7], "k": "1..n", "interval": "(-2,2)"
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_checks(), indent=2))
