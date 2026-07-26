from __future__ import annotations

import ast
import os
import subprocess
import sys
from dataclasses import dataclass

from app.core.exceptions import AppException

FORBIDDEN_MODULES = {
    "os",
    "sys",
    "subprocess",
    "pathlib",
    "shutil",
    "socket",
    "ctypes",
    "resource",
    "signal",
    "multiprocessing",
    "threading",
    "asyncio",
    "importlib",
    "pickle",
    "marshal",
}
FORBIDDEN_CALLS = {"eval", "exec", "compile", "open", "__import__", "globals", "locals", "vars", "breakpoint"}
MAX_MEMORY_BYTES = 64 * 1024 * 1024
MAX_OUTPUT_FILE_BYTES = 1024 * 1024
CLEAN_EXECUTION_ENV = {
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUNBUFFERED": "1",
}


@dataclass(slots=True)
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool


class CodeExecutionService:
    @staticmethod
    def validate_code_safety(code: str) -> None:
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            raise AppException(message=f"Submitted code contains a syntax error: {exc.msg}", status_code=400) from exc

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_module = alias.name.split(".")[0]
                    if root_module in FORBIDDEN_MODULES:
                        raise AppException(message=f"Import of module '{root_module}' is not allowed", status_code=400)
            elif isinstance(node, ast.ImportFrom):
                module_name = (node.module or "").split(".")[0]
                if module_name in FORBIDDEN_MODULES:
                    raise AppException(message=f"Import of module '{module_name}' is not allowed", status_code=400)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                    raise AppException(message=f"Call to '{node.func.id}' is not allowed", status_code=400)
                if isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_CALLS:
                    raise AppException(message=f"Call to '{node.func.attr}' is not allowed", status_code=400)

    @staticmethod
    def _build_preexec_fn():
        if os.name != "posix":
            return None

        def _limit_resources() -> None:
            import resource

            resource.setrlimit(resource.RLIMIT_CPU, (6, 6))
            resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY_BYTES, MAX_MEMORY_BYTES))
            resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_OUTPUT_FILE_BYTES, MAX_OUTPUT_FILE_BYTES))
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))

        return _limit_resources

    @classmethod
    def execute_python_code(
        cls,
        *,
        code: str,
        stdin_input: str | None = None,
        timeout_seconds: int = 5,
    ) -> ExecutionResult:
        cls.validate_code_safety(code)

        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-S", "-c", code],
                input=(stdin_input or ""),
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
                env=CLEAN_EXECUTION_ENV,
                close_fds=True,
                preexec_fn=cls._build_preexec_fn(),
            )
            return ExecutionResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                exit_code=completed.returncode,
                timed_out=False,
            )
        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(
                stdout=exc.stdout or "",
                stderr=(exc.stderr or "") + "\nExecution timed out",
                exit_code=-1,
                timed_out=True,
            )
