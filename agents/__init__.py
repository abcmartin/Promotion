"""Agents package for the dissertation management system.

This package provides a multi-agent workflow with the following roles:
- Planner: Produces or loads a structured plan for a manuscript section
- Auditor: Audits the plan and/or draft for logic, evidence, and methodology
- Executor: Applies edits to produce a revised draft and change log
- Verifier: Validates APA-7 compliance, terminology consistency, and word counts
- Reporter: Consolidates outputs into a single report and summary

The package exposes a CLI via `python -m agents`.
"""

__all__ = [
    "__version__",
]

__version__ = "0.1.0"

