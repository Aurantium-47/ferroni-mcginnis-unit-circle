"""Run every exact check; write a versioned JSON summary without local paths.

Usage from the repository root:
    python checks/run_all.py
    python -m checks.run_all
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import sys
from time import perf_counter
import unittest

import sympy as sp

if __package__:
    from . import check_identities, check_unit_circle, test_regressions
else:
    import check_identities
    import check_unit_circle
    import test_regressions


def run_all() -> dict:
    """Execute the complete suite, returning JSON-serializable coverage data."""
    start = perf_counter()
    summary = {
        "schema_version": 1,
        "status": "running",
        "started_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "versions": {"python": platform.python_version(), "sympy": sp.__version__},
        "python_optimization_level": sys.flags.optimize,
        "arithmetic": "exact integer and rational arithmetic; no numerical root approximations",
        "interpretation": "Finite regression checks support the analytic argument; they are not a proof.",
    }
    print("Ferroni–McGinnis exact verification suite", flush=True)
    print(f"UTC: {summary['started_at_utc']}", flush=True)
    print(f"Python {platform.python_version()}; SymPy {sp.__version__}", flush=True)
    print(f"Python optimization level: {sys.flags.optimize} (checks remain active)", flush=True)
    print("\n[1/3] Direct-permutation symbolic identities and supplemental spectral checks", flush=True)
    summary["identities"] = check_identities.run_checks()
    print("\n[2/3] Independent subset-cycle DP and exact Sturm certificates", flush=True)
    summary["unit_circle"] = check_unit_circle.run_checks()
    print("\n[3/3] Boundary, multiplicity, negative-control, and input-validation regressions", flush=True)
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_regressions)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    summary["regressions"] = {"tests": result.testsRun, "failures": len(result.failures),
                              "errors": len(result.errors), "skipped": len(result.skipped)}
    summary["status"] = "passed" if result.wasSuccessful() else "failed"
    summary["elapsed_seconds"] = round(perf_counter() - start, 3)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path,
                        default=Path(__file__).resolve().parent.parent / "results" / "summary.json",
                        help="JSON summary output (default: results/summary.json)")
    args = parser.parse_args()
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    # Replace any prior success before starting, so an interrupted or failed
    # run cannot leave a stale "passed" report masquerading as its outcome.
    summary = {"schema_version": 1, "status": "running",
               "versions": {"python": platform.python_version(), "sympy": sp.__version__}}
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    try:
        summary = run_all()
    except Exception as exc:
        summary.update(status="failed", error={"type": type(exc).__name__, "message": str(exc)})
        args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"\nFAILED: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 1
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"\n{summary['status'].upper()}: 28 symbolic identities; 10 subset identities; "
          f"28 supplemental spectral checks; 404 independent DP/Sturm cases; "
          f"{summary['regressions']['tests']} regression tests.", flush=True)
    print(f"JSON summary written: {args.summary.name}", flush=True)
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
