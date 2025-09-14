"""
Agents package providing a minimal multi-agent orchestration CLI for the
dissertation optimization workflow (Planner → Auditor → Executor → Verifier).

This package is intentionally lightweight and uses only the Python standard
library by default. Optional features (e.g., YAML playbook parsing) use PyYAML
if installed, but degrade gracefully when unavailable.
"""

__all__ = [
    "cli",
]

