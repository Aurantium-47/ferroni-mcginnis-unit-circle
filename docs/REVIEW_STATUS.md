# Review status and limits

**Snapshot: 4 November 2026.**

## Mathematical review

Two separate AI reviews of the complete analytic argument reported no mathematical gap. Both checked:

- The match to the source's positive-capacity definition and cycle-count index.
- The generating function, recurrence, determinant normalization and empty-matrix case.
- The kernel-vector argument, use of Gauss–Lucas and principal-minor interval bounds.
- Both directions of the root-location substitution and the nonzero constant term.
- Symmetry, multiaffinity and the precise open-disk hypotheses of Grace–Walsh–Szegő.
- Positive-capacity substitution, reciprocity, and the extreme cycle counts.

The reviews also found publication-context issues: the earlier recurrence citation had to be included, and a statement implying that no MathOverflow solution lead existed had to be removed. Those corrections are reflected in this candidate.

**These are AI reviews, not human peer review.** They are fallible, may share blind spots and should not be read as endorsement by the conjecture's authors, the cited researchers, a journal or an institution. The argument has not been checked by Lean or another proof assistant. No claim of formal certification is made.

## Computational review

The finite check suite compares independent constructions and uses exact algebra for identities and root counts. Its coverage and reference output are described in [VERIFICATION.md](VERIFICATION.md).

These tests can catch normalization errors and some implementation mistakes. They cannot validate every step of an infinite-parameter proof, establish the conjecture by themselves, or establish novelty. The plot is numerical illustration rather than a test certificate.

## Novelty and priority

**Unresolved.** A specific September 2026 MathOverflow comment links a potential earlier solution that could not be inspected because its shared conversation returned HTTP 403. This is a substantive open literature lead, not an inconsequential search omission. See [SOURCES.md](SOURCES.md).

The recurrence, generating function, classical coincidence theorem and general determinant-stability mechanism are prior mathematical tools. This repository offers an explicit proof exposition connecting those tools for the stated polynomial family, without claiming that this connection was first made here.

## Scope

The manuscript concerns precisely Ferroni–McGinnis Conjecture 4.5 for positive integer capacities. It does not prove the source paper's other real-rootedness or interlacing conjectures, does not classify the roots' multiplicities, and does not establish a new general stability theorem.
