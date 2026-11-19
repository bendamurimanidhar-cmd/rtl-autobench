"""
Icarus Verilog (iverilog + vvp) 4-State Event-Driven Simulation Runner.
Compiles SystemVerilog and executes cycle-accurate testbenches.
"""

import subprocess
import shutil
import os
import tempfile
from typing import Dict, Any, List

class IcarusRunner:
    def __init__(self):
        self.iverilog_bin = shutil.which("iverilog") or "/opt/homebrew/bin/iverilog"
        self.vvp_bin = shutil.which("vvp") or "/opt/homebrew/bin/vvp"

    def run_simulation(
        self,
        rtl_path: str,
        tb_path: str,
        extra_sources: List[str] = None,
        include_dirs: List[str] = None,
        timeout_sec: int = 20
    ) -> Dict[str, Any]:
        if not os.path.exists(self.iverilog_bin) or not os.path.exists(self.vvp_bin):
            return {"status": "SKIPPED", "message": "iverilog/vvp binaries not found."}

        with tempfile.NamedTemporaryFile(suffix=".vvp", delete=False) as tmp_bin:
            sim_bin = tmp_bin.name

        try:
            # 1. Compilation
            compile_cmd = [
                self.iverilog_bin,
                "-g2012",
                "-o", sim_bin,
                rtl_path,
                tb_path
            ]
            if extra_sources:
                compile_cmd.extend(extra_sources)
            if include_dirs:
                for inc in include_dirs:
                    compile_cmd.extend(["-I", inc])

            c_res = subprocess.run(compile_cmd, capture_output=True, text=True)
            if c_res.returncode != 0:
                return {
                    "status": "COMPILATION_ERROR",
                    "returncode": c_res.returncode,
                    "error": c_res.stderr.strip(),
                    "output": ""
                }

            # 2. Execution
            sim_res = subprocess.run([self.vvp_bin, sim_bin], capture_output=True, text=True, timeout=timeout_sec)
            sim_output = sim_res.stdout.strip()
            passed = "[VERIFICATION PASSED]" in sim_output and sim_res.returncode == 0

            return {
                "status": "PASSED" if passed else "FAILED",
                "returncode": sim_res.returncode,
                "output": sim_output,
                "error": sim_res.stderr.strip()
            }
        except subprocess.TimeoutExpired:
            return {"status": "TIMEOUT", "error": f"Simulation exceeded {timeout_sec} seconds."}
        finally:
            if os.path.exists(sim_bin):
                os.remove(sim_bin)
