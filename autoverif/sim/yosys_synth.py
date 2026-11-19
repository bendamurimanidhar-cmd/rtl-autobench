"""
Yosys Open Synthesis Suite Runner & PnR Netlist Exporter.
Performs RTLIL synthesis, technology cell mapping, gate-level hardware area estimation,
and generates PnR-ready netlists (.v and .json) for nextpnr / OpenROAD.
"""

import subprocess
import shutil
import os
import re
from typing import Dict, Any

class YosysSynthesizer:
    def __init__(self):
        self.yosys_bin = shutil.which("yosys") or "/opt/homebrew/bin/yosys"
        self.nextpnr_bin = shutil.which("nextpnr-ice40") or shutil.which("nextpnr-generic") or shutil.which("nextpnr-ecp5")

    def synthesize(self, rtl_path: str, top_module: str, out_dir: str = None) -> Dict[str, Any]:
        if not os.path.exists(self.yosys_bin):
            return {"status": "SKIPPED", "message": "Yosys binary not found on host."}

        target_dir = out_dir or os.path.join(os.path.dirname(os.path.abspath(rtl_path)), "verification_out")
        os.makedirs(target_dir, exist_ok=True)

        netlist_v = os.path.join(target_dir, f"{top_module}_netlist.v")
        netlist_json = os.path.join(target_dir, f"{top_module}_pnr.json")

        # Complete Synthesis Script:
        # 1. Ingest SystemVerilog
        # 2. Hierarchy elaboration
        # 3. Optimization & FSM extraction
        # 4. Tech mapping to logic primitives
        # 5. Export Gate-Level Verilog & PnR JSON
        script = (
            f"read_verilog -sv {rtl_path}; "
            f"hierarchy -top {top_module}; "
            f"proc; opt; fsm; opt; memory; opt; techmap; opt; "
            f"write_verilog {netlist_v}; "
            f"synth_ice40 -top {top_module} -json {netlist_json}; "
            f"stat;"
        )

        res = subprocess.run([self.yosys_bin, "-p", script], capture_output=True, text=True)
        if res.returncode != 0:
            # Fallback to standard generic synthesis if synth_ice40 fails
            fallback_script = (
                f"read_verilog -sv {rtl_path}; "
                f"hierarchy -top {top_module}; "
                f"proc; opt; fsm; opt; memory; opt; techmap; opt; "
                f"write_verilog {netlist_v}; "
                f"write_json {netlist_json}; "
                f"stat;"
            )
            res = subprocess.run([self.yosys_bin, "-p", fallback_script], capture_output=True, text=True)
            if res.returncode != 0:
                return {
                    "status": "SYNTH_ERROR",
                    "returncode": res.returncode,
                    "error": res.stderr.strip()[:400]
                }

        # Parse stat output
        stdout = res.stdout[res.stdout.rfind("Printing statistics"):]  # synth_ice40 prints its own earlier stats

        def stat_count(label):
            m = re.search(rf'^\s*(?:Number of {label}:\s+(\d+)|(\d+)\s+{label})\s*$', stdout, re.M)
            return int(m.group(1) or m.group(2)) if m else 0

        # Extract cell breakdown (LUTs, Flip-Flops, Gates)
        cell_breakdown = {}
        for line in stdout.splitlines():
            # Match cell lines like: "   27   SB_LUT4" or "   8   $_SDFFE_PP0P_"
            m = re.match(r'^\s*(\d+)\s+([A-Za-z0-9_\$]+)\s*$', line)
            if m and not line.strip().endswith("cells") and not line.strip().endswith("wires") and not line.strip().endswith("bits") and not line.strip().endswith("ports"):
                cell_breakdown[m.group(2)] = int(m.group(1))
            else:
                m2 = re.match(r'^\s*([A-Za-z0-9_\$]+)\s+(\d+)\s*$', line)
                if m2 and not line.strip().startswith("Number of"):
                    cell_breakdown[m2.group(1)] = int(m2.group(2))

        total_cells_val = sum(cell_breakdown.values()) if cell_breakdown else stat_count("cells")

        # Check if nextpnr is available to run automated Place & Route
        pnr_status = "NETLIST_GENERATED"
        pnr_metrics = {}
        if self.nextpnr_bin and os.path.exists(netlist_json):
            try:
                pnr_cmd = [self.nextpnr_bin, "--json", netlist_json, "--run", "--quiet"]
                pnr_res = subprocess.run(pnr_cmd, capture_output=True, text=True, timeout=15)
                if pnr_res.returncode == 0:
                    pnr_status = "PNR_PASSED"
                    # Extract Max Frequency (Fmax) from nextpnr output if present
                    fmax_m = re.search(r'Max frequency.*?: ([\d\.]+\s*MHz)', pnr_res.stdout)
                    if fmax_m:
                        pnr_metrics["fmax"] = fmax_m.group(1)
            except Exception:
                pass

        return {
            "status": "PASSED",
            "top_module": top_module,
            "total_cells": total_cells_val,
            "total_wires": stat_count("wires"),
            "public_wires": stat_count("public wires"),
            "port_bits": stat_count("port bits"),
            "cell_breakdown": cell_breakdown,
            "netlist_verilog_path": netlist_v,
            "pnr_json_netlist_path": netlist_json,
            "pnr_status": pnr_status,
            "pnr_metrics": pnr_metrics,
            "raw_stat": "\n".join([l for l in stdout.splitlines() if "Number of" in l or "SB_" in l or "$_" in l])
        }
