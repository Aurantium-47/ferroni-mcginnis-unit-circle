# A determinant and polarization proof of the unit-circle assertion

**Ferroni–McGinnis Conjecture 4.5 · manuscript dated 4 November 2026**

This is an AI-assisted analytic proof manuscript. Two separate AI reviews found no mathematical gap; there has been no human peer review or proof-assistant verification. Novelty and priority are unresolved. The [source register](SOURCES.md) records a specific potentially relevant earlier solution, as well as the established antecedents used here.

The proof below derives its algebraic identities and its determinant lemma. Its external classical inputs are Gauss–Lucas and the explicitly stated open-disk Grace–Walsh–Szegő theorem. Thus “self-contained” here means that no unpublished intermediate claim or computational result is needed, not that these classical theorems are reproved.

## 1. Statement and source identification

Let $`n\ge1`$, let $`1\le k\le n`$, and let $`\mathbf c=(c_1,\ldots,c_n)\in\mathbb Z_{>0}^n`$. For an integer $`a\ge1`$, write

```math
[a]_x=1+x+\cdots+x^{a-1}.
```

For a cycle $`C`$ of a permutation of $`[n]`$, put $`c(C)=\sum_{i\in C}c_i`$. Define

```math
P_{n,k,\mathbf c}(x)
=\sum_{\substack{\sigma\in S_n\\\mathrm{cyc}(\sigma)=k}}
\prod_{C\text{ cycle of }\sigma}[c(C)]_x.
\tag{1}
```

**Theorem.** Every complex zero of $`P_{n,k,\mathbf c}`$ lies on the unit circle.

In Ferroni and McGinnis's [*Lattice points in slices of prisms*](https://arxiv.org/html/2202.11808v2), Definition 3.7 allows a cycle $`C`$ precisely the integer weights $`0,\ldots,c(C)-1`$. Multiplying the cycle generating polynomials and then summing over permutations gives (1). Conjecture 4.5 uses $`m+1`$ cycles, so its polynomial is exactly (1) with $`k=m+1`$. In particular, the capacities are **strictly positive**, not merely nonnegative.

For any summand in (1), the degree is

```math
d=\sum_C(c(C)-1)=\sum_{i=1}^n c_i-k.
```

Its leading and constant coefficients are both $`1`$. Consequently $`P`$ has degree exactly $`d`$, and its constant coefficient is the positive number of permutations with $`k`$ cycles. The degree-zero case causes no difficulty because a nonzero constant has no zeros.

## 2. Unit capacities and a path determinant

Write $`P_{n,k}(x)=P_{n,k,\mathbf1}(x)`$ and set

```math
A_n(t,x)=\sum_{k=1}^n t^kP_{n,k}(x),\qquad A_0(t,x)=1.
```

A cycle on $`j`$ labels has $`(j-1)!`$ cyclic orders and weight polynomial $`[j]_x`$. Decomposing permutations into their unordered sets of labelled cycles therefore gives the formal exponential generating function

```math
G(q)=\sum_{n\ge0}A_n(t,x)\frac{q^n}{n!}
=\exp\left(t\sum_{j\ge1}[j]_x\frac{q^j}{j}\right).
\tag{2}
```

This generating function and the recurrence below are established weighted-Lah identities. See Ferroni, [*Hypersimplices are Ehrhart Positive*](https://arxiv.org/pdf/1911.10146v2), Remark 3.11 and Theorem 3.12. They are derived here to fix the indexing and normalization, not claimed as new.

Differentiating (2) formally, and using $`\sum_{j\ge1}[j]_xq^{j-1}=((1-q)(1-xq))^{-1}`$, yields

```math
(1-q)(1-xq)G'(q)=tG(q).
```

Comparing coefficients gives, for $`n\ge2`$,

```math
A_n=\bigl(t+(n-1)(1+x)\bigr)A_{n-1}
-x(n-1)(n-2)A_{n-2},
\tag{3}
```

with $`A_0=1`$ and $`A_1=t`$. All of this takes place in formal power series, so no convergence hypothesis is needed.

Put $`N=n-1`$. For $`N\ge1`$, let $`C_N(t,z)`$ be the symmetric tridiagonal matrix with diagonal entries

```math
t+j(1+z^2),\qquad 1\le j\le N,
```

and adjacent off-diagonal entries $`-z\sqrt{j(j+1)}`$, $`1\le j<N`$. Its determinant satisfies the last-row continuant recurrence with adjacent products $`z^2j(j+1)`$. With $`\det C_0=1`$, the initial values and (3) show that

```math
A_n(t,z^2)=t\det C_{n-1}(t,z).
```

Let $`T_N`$ be the adjacency matrix of the $`N`$-vertex path: zeros on the diagonal and ones on the adjacent off-diagonals. Let

```math
D_N=\mathrm{diag}(1,2,\ldots,N),\qquad B_N=D_N^{-1}.
```

For $`z\ne0`$ and $`y=z+z^{-1}`$, direct multiplication gives

```math
C_N(t,z)=zD_N^{1/2}\left(yI-T_N+\frac{t}{z}B_N\right)D_N^{1/2}.
```

Taking determinants, using $`\det D_N=N!`$, and extracting the coefficient of $`t^k`$ gives

```math
P_{n,k}(z^2)
=(n-1)!\,z^{n-k}Q_{n-1,k-1}(z+z^{-1}),
\tag{4}
```

where

```math
Q_{N,r}(y)=[s^r]\det(yI-T_N+sB_N).
```

For $`N=0`$, use the empty determinant $`1`$ and $`Q_{0,0}=1`$. Then (4) also covers $`n=k=1`$.

## 3. A determinant-coefficient lemma

**Lemma.** Let $`T`$ be a real symmetric $`N\times N`$ matrix whose spectrum lies in $`(a,b)`$, and let $`B`$ be a positive diagonal matrix. For $`0\le r\le N`$,

```math
q_r(y)=[s^r]\det(yI-T+sB)
```

is nonzero, has degree $`N-r`$, and has all its zeros in $`(a,b)`$. For $`N=0`$, this means the constant polynomial $`1`$.

**Proof: reality of the zeros.** Suppose $`N\ge1`$ and fix $`y`$ with $`\mathrm{Im}y>0`$. If $`\det(yI-T+sB)=0`$, there is a nonzero complex vector $`v`$ with

```math
(yI-T+sB)v=0.
```

Multiplication by the conjugate transpose $`v^*`$ and taking imaginary parts gives

```math
\mathrm{Im}s
=-\mathrm{Im}y\,\frac{v^*v}{v^*Bv}<0.
\tag{5}
```

Here $`v^*Tv`$ is real because $`T`$ is real symmetric, and $`v^*Bv>0`$. The determinant has degree $`N`$ in $`s`$, with nonzero leading coefficient $`\det B`$. Thus all its $`s`$-roots lie strictly in the lower half-plane.

By Gauss–Lucas, each derivative's roots lie in the convex hull of the original roots. A finite set of roots strictly in the lower half-plane has its convex hull strictly there too. Repeated differentiation therefore shows that every nonconstant $`s`$-derivative is nonzero at $`s=0`$. The $`N`$th derivative is the nonzero constant $`N!\det B`$. Since

```math
q_r(y)=\frac1{r!}\left.\frac{\partial^r}{\partial s^r}\det(yI-T+sB)\right|_{s=0},
```

we have $`q_r(y)\ne0`$ whenever $`\mathrm{Im}y>0`$. Its coefficients are real, so conjugation excludes zeros in the lower half-plane as well. All zeros of $`q_r`$ are real.

**Proof: degree and localization.** Expansion in the diagonal entries from $`sB`$ gives

```math
q_r(y)=\sum_{\substack{S\subseteq[N]\\|S|=r}}
\left(\prod_{i\in S}B_{ii}\right)
\det\bigl((yI-T)_{S^c,S^c}\bigr).
\tag{6}
```

The leading coefficient in $`y`$ is $`e_r(B_{11},\ldots,B_{NN})>0`$, so the degree is exactly $`N-r`$. If $`y\ge b`$, the matrix $`yI-T`$ is positive definite and every term in (6) is positive. If $`y\le a`$, it is negative definite, so every principal minor of size $`N-r`$ has the same nonzero sign $`(-1)^{N-r}`$. The positive coefficients in (6) prevent cancellation. The empty minor has determinant $`1`$, covering $`r=N`$. Thus no zero is outside $`(a,b)`$. ∎

This lemma is an elementary instance of classical polynomial stability phenomena; no novelty is claimed for the lemma itself. In particular, the proof does **not** infer real-rootedness merely from a positive sum of real-rooted principal-minor polynomials.

## 4. Finish the unit-capacity case

The eigenvalues of $`T_N`$ are

```math
2\cos\frac{j\pi}{N+1},\qquad 1\le j\le N.
```

Indeed, the vector with $`\ell`$th entry $`\sin(\ell j\pi/(N+1))`$ is an eigenvector, by the sine addition identity and the zero boundary entries. The eigenvalues are distinct, giving the full spectrum, and each lies strictly in $`(-2,2)`$.

The lemma with $`(a,b)=(-2,2)`$ now gives every zero of $`Q_{N,r}`$ in $`(-2,2)`$. If $`P_{n,k}`$ is constant, there is nothing to prove. Otherwise take a zero $`x`$ of $`P_{n,k}`$. Its positive constant coefficient implies $`x\ne0`$. Choose either square root $`z`$ of $`x`$. By (4),

```math
Q_{n-1,k-1}(z+z^{-1})=0.
```

Therefore $`y=z+z^{-1}`$ is real and satisfies $`-2<y<2`$. The equation $`z^2-yz+1=0`$ has roots

```math
z=\frac{y\pm i\sqrt{4-y^2}}2,
```

each of modulus $`1`$. Hence $`|x|=|z|^2=1`$. This proves the result for $`\mathbf c=\mathbf1`$.

## 5. Transfer to arbitrary positive capacities

Define

```math
F_{n,k}(u_1,\ldots,u_n)
=\sum_{\substack{\sigma\in S_n\\\mathrm{cyc}(\sigma)=k}}
\prod_{C\text{ cycle of }\sigma}\left(1-\prod_{i\in C}u_i\right).
\tag{7}
```

Each label belongs to one cycle, so each variable occurs with exponent at most $`1`$ in every monomial. Thus $`F_{n,k}`$ is multiaffine. Relabelling permutations shows that it is invariant under every permutation of its variables. On the diagonal,

```math
F_{n,k}(u,\ldots,u)=(1-u)^kP_{n,k}(u).\tag{8}
```

By the unit-capacity case, the right side is nonzero whenever $`|u|<1`$.

We use the following classical consequence of the **Grace–Walsh–Szegő coincidence theorem**: for a symmetric multiaffine polynomial $`F`$ and points $`u_1,\ldots,u_n`$ in the open unit disk, there is a point $`u`$ in the same disk with

```math
F(u_1,\ldots,u_n)=F(u,\ldots,u).
```

This precise open-region version is recorded in Brändén and Wagner, [*A converse to the Grace–Walsh–Szegő theorem*](https://arxiv.org/pdf/0809.3225), Proposition 1. Their statement permits open circular regions and requires either convexity of the region or full polynomial degree. The open disk is convex, so all required hypotheses hold here.

Equation (8) and that theorem imply

```math
F_{n,k}(u_1,\ldots,u_n)\ne0\quad\text{if every }|u_i|<1.\tag{9}
```

For positive integers $`c_i`$, (7) gives the polynomial identity

```math
F_{n,k}(x^{c_1},\ldots,x^{c_n})
=(1-x)^kP_{n,k,\mathbf c}(x).
\tag{10}
```

If $`|x|<1`$, positivity of every $`c_i`$ gives $`|x^{c_i}|<1`$. By (9) the left side of (10) is nonzero, and therefore $`P_{n,k,\mathbf c}(x)\ne0`$. No zero lies inside the unit circle.

Finally, $`[a]_x=x^{a-1}[a]_{1/x}`$ for $`x\ne0`$. Every summand of (1) is reciprocal of the same degree $`d=\sum_i c_i-k`$. Consequently

```math
P_{n,k,\mathbf c}(x)=x^dP_{n,k,\mathbf c}(1/x).\tag{11}
```

An exterior zero would give an interior reciprocal zero, contrary to (10). All zeros therefore lie on the unit circle. ∎

## 6. Boundary checks and a supplementary identity

- For $`n=k=1`$, the polynomial is $`[c_1]_x`$.
- For $`k=1`$, it is $`(n-1)![\sum_i c_i]_x`$.
- For $`k=n`$, it is $`\prod_i[c_i]_x`$.
- A zero at $`0`$ is impossible because the constant coefficient is positive; a zero at $`1`$ is also impossible because all summands are positive there.
- Zero capacities are outside the statement. For example, $`n=k=1`$ and $`c_1=0`$ would give the zero polynomial if the empty weight sum were allowed.

For independent algebraic checks, one can also use

```math
F_{n,k}(u_1,\ldots,u_n)
=[t^k]\sum_{S\subseteq[n]}
(-t)^{\overline{|S|}}t^{\overline{n-|S|}}\prod_{i\in S}u_i,
\tag{12}
```

where $`a^{\overline j}=a(a+1)\cdots(a+j-1)`$ and $`a^{\overline0}=1`$. In expanding (7), choose the cycles contributing their negative monomials, and call their union $`S`$. They form a permutation of $`S`$ with factor $`-t`$ per cycle; the remaining cycles form a permutation of $`S^c`$ with factor $`t`$ per cycle. The identity $`\sum_{\sigma\in S_j}t^{\mathrm{cyc}(\sigma)}=t^{\overline j}`$ follows inductively by inserting the largest label, either as a new singleton cycle or into one of $`j-1`$ positions in an existing cycle. This proves (12).

The scripts verify (4) and (12) on finite ranges and independently certify roots in 404 cases. These checks are supplementary and do not establish, or enter into, the proof above. See [verification](VERIFICATION.md).

## 7. What is and is not claimed

The argument proves the unit-circle assertion for the exact positive-capacity objects in Conjecture 4.5, subject to scholarly scrutiny of the manuscript. It makes no claim to resolve the distinct $`h^*`$-real-rootedness or interlacing conjectures in the source paper.

A [24 September 2026 MathOverflow comment by Veronica Phan](https://mathoverflow.net/questions/449688/partitions-weights-and-polynomials-with-roots-on-the-unit-circle#comment1347048_449688) links a possible earlier solution. Its linked conversation could not be read: retrieval was inaccessible and an ordinary direct request returned HTTP 403. No bypass was attempted. Its content, validity and overlap with this argument remain unknown. Neither the accessible question's lack of an answer nor a negative literature search resolves this lead. **No originality, first-proof or priority claim is made.**
