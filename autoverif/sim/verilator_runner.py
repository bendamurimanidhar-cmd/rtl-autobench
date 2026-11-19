"""
Verilator 2-State Linting & Static Analysis Runner.
Validates syntax, width mismatches, undeclared nets, and latches.
"""

import subprocess
import shutil
import os
from typing import Dict, Any

class VerilatorRunner:
    def __init__(self):
        self.bin_path = shutil.which("verilator") or "/opt/homebrew/bin/verilator"

    def run_lint(self, source_file: str) -> Dict[str, Any]:
        if not os.path.exists(self.bin_path):
            return {"status": "SKIPPED", "message": "Verilator binary not found on host."}

        cmd = [
            self.bin_path,
            "--lint-only",
            "-Wall",
            "-Wno-DECLFILENAME",
            "-Wno-PINMISSING",
            source_file
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        passed = (res.returncode == 0)
        warnings = [line for line in res.stderr.splitlines() if "%Warning" in line]
        errors = [line for line in res.stderr.splitlines() if "%Error" in line]

        return {
            "status": "PASSED" if passed else "FAILED",
            "returncode": res.returncode,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "errors": errors,
            "warnings": warnings,
            "raw_output": res.stderr.strip()
        }
