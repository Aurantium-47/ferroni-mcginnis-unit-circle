"""Small regression tests for boundary cases and the certification machinery."""

import unittest

import sympy as sp

if __package__:
    from .check_identities import (determinant_polynomial, enumerate_polynomial,
                                   enumerate_polynomials, subset_numerator)
    from .check_unit_circle import (certify_unit_circle, cycle_polynomial,
                                    reciprocal_transform, x, y)
else:
    from check_identities import (determinant_polynomial, enumerate_polynomial,
                                  enumerate_polynomials, subset_numerator)
    from check_unit_circle import (certify_unit_circle, cycle_polynomial,
                                   reciprocal_transform, x, y)


class SourcePolynomialTests(unittest.TestCase):
    def test_empty_determinant(self):
        self.assertEqual(determinant_polynomial(1).as_expr(), 1)

    def test_single_unit_capacity(self):
        self.assertEqual(cycle_polynomial((1,), 1), sp.Poly(1, x))
        self.assertEqual(enumerate_polynomial((1,), 1), sp.Poly(1, x))

    def test_single_nonunit_capacity(self):
        self.assertEqual(cycle_polynomial((5,), 1), sp.Poly(1 + x + x**2 + x**3 + x**4, x))

    def test_one_cycle_factorial_multiplicity(self):
        expected = sp.Poly(6 * sum(x**j for j in range(10)), x)
        self.assertEqual(cycle_polynomial((1, 2, 3, 4), 1), expected)

    def test_all_singleton_cycles(self):
        expected = sp.Poly((1 + x) * (1 + x + x**2), x)
        self.assertEqual(cycle_polynomial((1, 2, 3), 3), expected)

    def test_all_unit_singletons_are_constant(self):
        self.assertEqual(cycle_polynomial((1,) * 6, 6), sp.Poly(1, x))

    def test_permutation_invariance(self):
        for k in range(1, 5):
            with self.subTest(k=k):
                self.assertEqual(cycle_polynomial((1, 2, 3, 5), k),
                                 cycle_polynomial((5, 2, 1, 3), k))

    def test_constant_coefficients_count_permutations(self):
        self.assertEqual([cycle_polynomial((1, 2, 4, 7), k).TC() for k in range(1, 5)],
                         [6, 11, 6, 1])

    def test_dp_matches_independent_permutation_enumeration(self):
        for c in ((1,), (2, 3), (1, 2, 4), (1, 2, 3, 5)):
            for k, enumerated in enumerate(enumerate_polynomials(c), start=1):
                with self.subTest(capacities=c, k=k):
                    self.assertEqual(cycle_polynomial(c, k), enumerated)

    def test_subset_identity_at_boundary_cycle_counts(self):
        for k in (1, 4):
            with self.subTest(k=k):
                c = (1, 2, 3, 5)
                self.assertEqual(subset_numerator(c, k),
                                 sp.Poly((1 - x)**k * enumerate_polynomial(c, k).as_expr(), x))

    def test_exact_integer_and_generator_inputs(self):
        expected = cycle_polynomial((1, 2, 3), 2)
        self.assertEqual(cycle_polynomial((sp.Integer(i) for i in (1, 2, 3)), sp.Integer(2)), expected)


class CertificateTests(unittest.TestCase):
    def test_nonzero_constants_are_vacuously_certified(self):
        for value in (1, -3, sp.Rational(2, 7)):
            with self.subTest(value=value):
                result = certify_unit_circle(sp.Poly(value, x))
                self.assertEqual(result.original_degree, 0)
                self.assertEqual(result.transformed_degree, 0)
                self.assertEqual(result.real_roots_with_multiplicity, 0)

    def test_odd_degree_forced_root(self):
        result = certify_unit_circle(sp.Poly(x + 1, x))
        self.assertEqual(result.forced_minus_one_root, 1)
        self.assertEqual(result.transformed_degree, 0)

    def test_even_degree_has_no_forced_root_removed(self):
        result = certify_unit_circle(sp.Poly((x + 1)**2, x))
        self.assertEqual(result.forced_minus_one_root, 0)
        self.assertEqual(result.transformed_degree, 1)

    def test_repeated_roots_and_both_endpoints(self):
        polynomial = sp.Poly((x - 1)**4 * (x + 1)**5 * (x**2 + x + 1)**3, x)
        transformed, epsilon = reciprocal_transform(polynomial)
        self.assertEqual(transformed, sp.Poly((y - 2)**2 * (y + 2)**2 * (y + 1)**3, y, domain=sp.QQ))
        result = certify_unit_circle(polynomial)
        self.assertEqual((epsilon, result.original_degree, result.transformed_degree), (1, 15, 7))
        self.assertEqual(result.real_roots_with_multiplicity, 7)

    def test_transform_identity_even_and_odd(self):
        for expression in ((x**2 + 1)**3, (x + 1)**3 * (x**2 - x + 1)**2):
            with self.subTest(expression=expression):
                transformed, epsilon = reciprocal_transform(sp.Poly(expression, x))
                h = transformed.degree()
                reconstructed = (x + 1)**epsilon * x**h * transformed.as_expr().subs(y, x + 1 / x)
                self.assertEqual(sp.cancel(expression - reconstructed), 0)

    def test_rational_coefficients_and_negative_scale(self):
        self.assertEqual(certify_unit_circle(sp.Poly(-sp.Rational(2, 3) * (x**2 + 1)**2, x)).original_degree, 4)

    def test_arbitrary_input_variable(self):
        u = sp.Symbol("u")
        self.assertEqual(certify_unit_circle(sp.Poly(u**2 + u + 1, u)).transformed_degree, 1)

    def test_reciprocal_polynomial_with_roots_outside_interval_fails(self):
        with self.assertRaisesRegex(ValueError, "certification failed"):
            certify_unit_circle(sp.Poly(x**2 - 3*x + 1, x))

    def test_reciprocal_polynomial_with_nonreal_transform_roots_fails(self):
        with self.assertRaisesRegex(ValueError, "certification failed"):
            certify_unit_circle(sp.Poly(x**4 + 3*x**2 + 1, x))


class InputValidationTests(unittest.TestCase):
    def test_empty_capacities_rejected(self):
        for function in (cycle_polynomial, enumerate_polynomial, subset_numerator):
            with self.subTest(function=function.__name__), self.assertRaises(ValueError):
                function((), 1)

    def test_zero_and_negative_capacities_rejected(self):
        for c in ((0,), (-1,), (1, 0), (2, -3)):
            for function in (cycle_polynomial, enumerate_polynomial, subset_numerator):
                with self.subTest(capacities=c, function=function.__name__), self.assertRaises(ValueError):
                    function(c, 1)

    def test_noninteger_capacities_rejected(self):
        for c in ((1.0,), (True,), (sp.Rational(3, 2),), ("2",), "123", 3):
            with self.subTest(capacities=c), self.assertRaises(TypeError):
                cycle_polynomial(c, 1)

    def test_invalid_cycle_counts_rejected(self):
        for k in (-1, 0, 3):
            for function in (cycle_polynomial, enumerate_polynomial, subset_numerator):
                with self.subTest(k=k, function=function.__name__), self.assertRaises(ValueError):
                    function((1, 2), k)

    def test_noninteger_cycle_counts_rejected(self):
        for k in (True, 1.0, "1", sp.Rational(1, 2)):
            with self.subTest(k=k), self.assertRaises(TypeError):
                cycle_polynomial((1, 2), k)

    def test_invalid_determinant_sizes_rejected(self):
        for n in (0, -1):
            with self.subTest(n=n), self.assertRaises(ValueError):
                determinant_polynomial(n)
        for n in (True, 1.0, "2"):
            with self.subTest(n=n), self.assertRaises(TypeError):
                determinant_polynomial(n)

    def test_zero_polynomial_rejected(self):
        with self.assertRaisesRegex(ValueError, "zero polynomial"):
            certify_unit_circle(sp.Poly(0, x))

    def test_nonreciprocal_polynomial_rejected(self):
        for expression in (x, x**2 + 2*x + 2, x - 1):
            with self.subTest(expression=expression), self.assertRaisesRegex(ValueError, "reciprocal"):
                certify_unit_circle(sp.Poly(expression, x))

    def test_nonexact_and_multivariate_polynomials_rejected(self):
        for polynomial in (sp.Poly(1.0*x + 1.0, x), sp.Poly(x + y, x, y),
                           sp.Poly(x**2 + sp.sqrt(2)*x + 1, x, extension=True)):
            with self.subTest(polynomial=polynomial), self.assertRaises(ValueError):
                certify_unit_circle(polynomial)

    def test_nonpoly_input_rejected(self):
        with self.assertRaises(TypeError):
            certify_unit_circle(x + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
