"""Minimal tool registry for the smoke harness.

Provides a single ``python_exec`` tool that runs a snippet of Python in a subprocess sandbox with a
short timeout and small output cap. The same callable is wrapped two ways so the t0006 ReAct
delegate (which calls ``tool(**action.args)``) and the t0007 Plan-and-Solve delegate (which calls
``tool(args_str)``) can both invoke it without per-condition special-casing inside the harness.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable, Mapping
from typing import Any, Final

PYTHON_EXEC_TIMEOUT_SECONDS: Final[float] = 5.0
PYTHON_EXEC_OUTPUT_CAP_BYTES: Final[int] = 64 * 1024


def python_exec_str(code: str) -> str:
    """Run ``code`` in a fresh ``python3`` subprocess; return stdout+stderr (truncated)."""
    if not isinstance(code, str):
        return f"<error: expected string, got {type(code).__name__}>"
    if len(code) == 0:
        return "<error: empty code>"
    try:
        completed = subprocess.run(  # noqa: S603 — local trusted invocation
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=PYTHON_EXEC_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return f"<error: python_exec timed out after {PYTHON_EXEC_TIMEOUT_SECONDS}s>"
    except Exception as exc:  # noqa: BLE001 — surface errors as observation
        return f"<error: python_exec invocation failed: {type(exc).__name__}: {exc}>"
    out: str = (completed.stdout or "") + (completed.stderr or "")
    if len(out) > PYTHON_EXEC_OUTPUT_CAP_BYTES:
        return out[:PYTHON_EXEC_OUTPUT_CAP_BYTES] + "\n<...truncated>"
    if len(out) == 0:
        return "<no output>"
    return out


def _react_python_exec(**kwargs: Any) -> str:
    """t0006-shape adapter: tool is called with ``code=<str>`` keyword arg."""
    code_obj: Any = kwargs.get("code", "")
    return python_exec_str(str(code_obj))


def _planandsolve_python_exec(args_str: str) -> str:
    """t0007/t0010-shape adapter: tool is called with the raw single-argument string.

    The Plan-and-Solve / matched-mismatch executor passes the ``Action: <tool_name>(<args>)``
    payload as a single string. We treat the entire payload as the Python code to execute.
    """
    return python_exec_str(args_str)


def build_react_tool_registry() -> Mapping[str, Callable[..., Any]]:
    """Tool registry shape consumed by t0006 (kwargs)."""
    return {"python_exec": _react_python_exec}


def build_planandsolve_tool_registry() -> Mapping[str, Callable[[str], str]]:
    """Tool registry shape consumed by t0007 / t0010 (single string arg)."""
    return {"python_exec": _planandsolve_python_exec}
