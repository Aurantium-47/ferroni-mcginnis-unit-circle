"""Independent exact subset-cycle DP and Sturm unit-circle certificates.

No weighted-Lah recurrence, determinant identity, or polarization theorem is
used to construct or certify these polynomials. Integer coefficient arithmetic
constructs P(c,k); a reciprocal-to-real transform followed by square-free
factorization and exact Sturm counts certifies its roots, with multiplicity.
"""

from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass
from functools import lru_cache
from itertools import combinations_with_replacement
from math import factorial

import sympy as sp

if __package__:
    from ._validation import parameters, require
else:
    from _validation import parameters, require


x, y = sp.symbols("x y")
ASYMMETRIC_CAPACITIES = (
    (1, 1, 2, 3, 5, 8),
    (1, 2, 3, 4, 5, 6, 7),
    (2, 2, 2, 3, 3, 3, 5, 5),
    (1, 2, 4, 8, 16),
)


def _add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    result = list(a) + [0] * max(0, len(b) - len(a))
    for i, coefficient in enumerate(b):
        result[i] += coefficient
    return tuple(result)


def _multiply_interval(a: tuple[int, ...], length: int, scale: int) -> tuple[int, ...]:
    result = [0] * (len(a) + length - 1)
    for i, coefficient in enumerate(a):
        for j in range(length):
            result[i + j] += scale * coefficient
    return tuple(result)


def cycle_polynomial(values: Iterable[int], k: int) -> sp.Poly:
    """Compute P(c,k) by choosing the cycle containing the least unused label.

    Each chosen label set C has (|C|-1)! cyclic orders and contributes
    [sum(c_i for i in C)]_x. Recursing on its complement counts each permutation
    exactly once. Cached states contain integer coefficient tuples only.
    """
    c, k = parameters(values, k)
    n = len(c)

    @lru_cache(maxsize=None)
    def dp(mask: int, remaining_cycles: int) -> tuple[int, ...]:
        if mask == 0:
            return (1,) if remaining_cycles == 0 else ()
        if remaining_cycles <= 0 or remaining_cycles > mask.bit_count():
            return ()
        first = mask & -mask
        rest = mask ^ first
        answer: tuple[int, ...] = ()
        subset = rest
        while True:
            cycle = first | subset
            tail = dp(mask ^ cycle, remaining_cycles - 1)
            if tail:
                capacity = sum(c[i] for i in range(n) if cycle & (1 << i))
                answer = _add(answer, _multiply_interval(
                    tail, capacity, factorial(cycle.bit_count() - 1)
                ))
            if subset == 0:
                break
            subset = (subset - 1) & rest
        return answer

    coefficients = dp((1 << n) - 1, k)
    return sp.Poly.from_list(list(reversed(coefficients)), x, domain=sp.ZZ)


def reciprocal_transform(polynomial: sp.Poly) -> tuple[sp.Poly, int]:
    """Return R(y) and epsilon such that

    P(x) = (x+1)^epsilon x^h R(x+x^-1), epsilon in {0,1}, h=degree(R).
    Inputs must be nonzero univariate reciprocal polynomials over QQ or ZZ.
    A nonzero constant is valid. The zero polynomial is deliberately rejected.
    """
    if not isinstance(polynomial, sp.Poly):
        raise TypeError("polynomial must be a SymPy Poly")
    if len(polynomial.gens) != 1:
        raise ValueError("polynomial must be univariate")
    if polynomial.domain not in (sp.ZZ, sp.QQ):
        raise ValueError("polynomial must have exact rational coefficients")
    if polynomial.is_zero:
        raise ValueError("the zero polynomial cannot be certified")
    coefficients = polynomial.all_coeffs()
    if coefficients != list(reversed(coefficients)):
        raise ValueError("polynomial must be reciprocal (palindromic coefficients)")
    epsilon = int(polynomial.degree() % 2)
    if epsilon:
        variable = polynomial.gens[0]
        polynomial, remainder = polynomial.div(sp.Poly(variable + 1, variable))
        require(remainder.is_zero, "odd reciprocal polynomial lacks its forced -1 root")
    h = polynomial.degree() // 2
    a = list(reversed(polynomial.all_coeffs()))
    # C_j(y) = x^j+x^(-j), with y=x+x^(-1). This elementary transform
    # recurrence is not the candidate proof's weighted-Lah recurrence.
    chebyshev = [sp.Integer(2), y]
    for j in range(2, h + 1):
        chebyshev.append(sp.expand(y * chebyshev[-1] - chebyshev[-2]))
    transformed = sp.Poly(a[h] + sum(a[h + j] * chebyshev[j] for j in range(1, h + 1)),
                          y, domain=sp.QQ)
    require(transformed.degree() == h, "reciprocal transform lost degree")
    return transformed, epsilon


@dataclass(frozen=True)
class UnitCircleCertificate:
    original_degree: int
    forced_minus_one_root: int
    transformed_degree: int
    real_roots_with_multiplicity: int
    square_free_factors: int

    def as_dict(self) -> dict[str, int]:
        return asdict(self)


def certify_unit_circle(polynomial: sp.Poly) -> UnitCircleCertificate:
    """Certify all roots by exact closed-interval Sturm counts, or raise ValueError.

    Square-free factorization makes multiplicity explicit. Endpoint roots y=2
    and y=-2 are included, since they correspond to unit-circle roots x=1,-1.
    """
    transformed, epsilon = reciprocal_transform(polynomial)
    factors = transformed.sqf_list()[1]
    count = sum(int(multiplicity * factor.count_roots(-2, 2))
                for factor, multiplicity in factors)
    h = int(transformed.degree())
    if count != h:
        raise ValueError(f"unit-circle certification failed: {count} of {h} transformed roots in [-2,2]")
    return UnitCircleCertificate(int(polynomial.degree()), epsilon, h, count, len(factors))


def run_checks(progress: Callable[[str], None] | None = print) -> dict:
    """Reproduce all 404 original exact DP/Sturm cases, with the same inputs."""
    total = 0
    rows = []
    for n in range(1, 7):
        vectors = list(combinations_with_replacement(range(1, 4), n))
        for c in vectors:
            for k in range(1, n + 1):
                polynomial = cycle_polynomial(c, k)
                require(polynomial.degree() == sum(c) - k, f"unexpected degree for c={c}, k={k}")
                certify_unit_circle(polynomial)
                total += 1
        rows.append({"n": n, "vectors": len(vectors), "polynomials": n * len(vectors)})
        if progress:
            progress(f"PASS exact DP/Sturm: n={n}, capacities=1..3 up to permutation, "
                     f"vectors={len(vectors)}, cumulative={total}")
    base_count = total
    for c in ASYMMETRIC_CAPACITIES:
        for k in range(1, len(c) + 1):
            polynomial = cycle_polynomial(c, k)
            require(polynomial.degree() == sum(c) - k, f"unexpected degree for c={c}, k={k}")
            certify_unit_circle(polynomial)
            total += 1
        if progress:
            progress(f"PASS exact DP/Sturm asymmetric vector: c={c}, k=1..{len(c)}")
    require((base_count, total) == (378, 404), "DP/Sturm coverage changed unexpectedly")
    return {
        "count": total,
        "grid": {"count": base_count, "n_inclusive": [1, 6], "capacity_values": [1, 2, 3],
                 "up_to_coordinate_permutation": True, "k": "1..n", "by_n": rows},
        "asymmetric": {"count": total - base_count, "capacities": [list(c) for c in ASYMMETRIC_CAPACITIES],
                       "k": "1..n"},
        "root_count_method": "exact Sturm counts of square-free reciprocal-transform factors, with multiplicity",
        "transformed_root_interval": "[-2,2]",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_checks(), indent=2))
