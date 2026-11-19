#!/usr/bin/env python3
"""
RTL-AutoBench CLI: Autonomous Pre-Silicon Hardware Verification Suite.
One-shot execution: Testbench + Simulation + Yosys Synthesis + NextPnR Physical Layout & STA.
"""

import sys
import os
import time
import argparse
from typing import Dict, Any

# Ensure autoverif is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from autoverif.parser.verilog_ast import VerilogModuleParser
from autoverif.generator.sva_generator import SVAGenerator
from autoverif.generator.tb_synthesizer import TestbenchSynthesizer
from autoverif.sim.verilator_runner import VerilatorRunner
from autoverif.sim.iverilog_runner import IcarusRunner
from autoverif.sim.yosys_synth import YosysSynthesizer
from autoverif.sim.pnr_engine import NextPnREngine
from autoverif.report.cert_generator import CertificateGenerator

def generate_testbench_only(verilog_path: str, cycles: int = 100, output_file: str = None) -> str:
    """Parses any Verilog source code and synthesizes a complete self-checking testbench."""
    if not os.path.exists(verilog_path):
        print(f"[ERROR] Source file not found: {verilog_path}")
        sys.exit(1)

    with open(verilog_path, "r", encoding="utf-8") as f:
        code = f.read()

    parser = VerilogModuleParser(code)
    meta = parser.parse()
    mod = meta["module_name"]

    tb_code = TestbenchSynthesizer.synthesize_testbench(meta, sim_cycles=cycles)

    if output_file:
        out_dir = os.path.dirname(os.path.abspath(output_file))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(tb_code)
        print(f"\n[SUCCESS] Generated self-checking testbench for '{mod}' saved to:")
        print(f"          {output_file}\n")
    else:
        print(tb_code)

    return tb_code

def run_verification_flow(verilog_path: str, cycles: int = 50, output_dir: str = None) -> Dict[str, Any]:
    if not os.path.exists(verilog_path):
        print(f"[ERROR] Source file not found: {verilog_path}")
        return {"status": "FILE_NOT_FOUND"}

    with open(verilog_path, "r", encoding="utf-8") as f:
        code = f.read()

    out_dir = output_dir or os.path.join(os.path.dirname(os.path.abspath(verilog_path)), "verification_out")
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n[1/6] Parsing Hardware Topology: {os.path.basename(verilog_path)}...")
    parser = VerilogModuleParser(code)
    meta = parser.parse()
    mod = meta["module_name"]
    print(f"      Module: {mod} | Inputs: {len(meta['inputs'])} | Outputs: {len(meta['outputs'])} | Reset: {meta.get('reset_polarity')}")

    print(f"[2/6] Synthesizing SVA Properties & Self-Checking Testbench...")
    sva_code = SVAGenerator.generate_assertions(meta)
    tb_code = TestbenchSynthesizer.synthesize_testbench(meta, sim_cycles=cycles)

    tb_path = os.path.join(out_dir, f"{mod}_tb.sv")
    with open(tb_path, "w", encoding="utf-8") as f:
        f.write(tb_code)
    print(f"      Generated Testbench: {os.path.basename(tb_path)} ({cycles:,} cycles)")

    print(f"[3/6] Running Verilator Static Lint Check...")
    linter = VerilatorRunner()
    lint_res = linter.run_lint(verilog_path)
    print(f"      Status: {lint_res['status']} ({lint_res.get('warning_count', 0)} warnings)")

    print(f"[4/6] Executing Cycle-Accurate Icarus Simulation ({cycles:,} vectors)...")
    sim_runner = IcarusRunner()
    sim_res = sim_runner.run_simulation(verilog_path, tb_path)
    print(f"      Simulation: {sim_res['status']}")

    print(f"[5/6] Executing Yosys Gate-Level Logic Synthesis...")
    synth_runner = YosysSynthesizer()
    synth_res = synth_runner.synthesize(verilog_path, mod, out_dir=out_dir)
    if synth_res.get("status") == "PASSED":
        print(f"      Synthesis : PASSED ({synth_res.get('total_cells', 0)} physical cells, {synth_res.get('total_wires', 0)} wires)")
        print(f"      Netlist   : Gate-level Verilog -> {os.path.basename(synth_res.get('netlist_verilog_path', ''))}")
        print(f"      PnR Target: JSON Netlist       -> {os.path.basename(synth_res.get('pnr_json_netlist_path', ''))}")
    else:
        print(f"      Synthesis : {synth_res.get('status')}")

    print(f"[6/6] Executing NextPnR Physical Layout & Static Timing Analysis (STA)...")
    pnr_engine = NextPnREngine()
    pnr_res = pnr_engine.run_pnr(synth_res.get("pnr_json_netlist_path", ""), mod, synth_res)
    
    pnr_util = pnr_res.get("utilization", {})
    pnr_timing = pnr_res.get("timing", {})
    pnr_layout = pnr_res.get("layout", {})

    print(f"      Target Silicon: {pnr_res.get('target_device')}")
    print(f"      Placement     : {pnr_util.get('lut4_used', 0)}/{pnr_util.get('lut4_total', 1280)} LUT4s ({pnr_util.get('lut4_pct', 0)}%) | {pnr_util.get('dff_used', 0)}/{pnr_util.get('dff_total', 1280)} DFFs ({pnr_util.get('dff_pct', 0)}%) | {pnr_util.get('io_used', 0)} IOs")
    print(f"      Layout Grid   : {pnr_layout.get('bounding_box')} (Routing Density: {pnr_layout.get('routing_density_pct') }%)")
    print(f"      Static Timing : Critical Path = {pnr_timing.get('critical_path_ns')} ns (Logic: {pnr_timing.get('logic_delay_ns')}ns, Wire Routing: {pnr_timing.get('routing_delay_ns')}ns)")
    print(f"      Max Clock Freq: {pnr_timing.get('fmax_mhz')} MHz (Fmax)")
    print(f"      Timing Closure: {pnr_timing.get('closure')} [Slack: {pnr_timing.get('slack_ns')} ns @ 100MHz]")

    audit_data = {
        **meta,
        "lint": lint_res,
        "sim": sim_res,
        "synth": synth_res,
        "pnr": pnr_res
    }

    cert_md = CertificateGenerator.generate_markdown(audit_data)
    cert_path = os.path.join(out_dir, f"{mod}_CERTIFICATE.md")
    with open(cert_path, "w", encoding="utf-8") as f:
        f.write(cert_md)

    print(f"\n[SUCCESS] Pre-Silicon Verification & PnR complete! Audit Certificate written to:")
    print(f"          {cert_path}\n")
    return audit_data

def watch_directory(watch_dir: str, cycles: int = 50):
    """Autonomous Live File Watcher: Re-verifies hardware modules on save automatically."""
    print("\n" + "=" * 65)
    print(" ⚡ RTL-AutoBench Autonomous Pre-Silicon Watch Daemon")
    print("=" * 65)
    print(f" Watching Directory : {os.path.abspath(watch_dir)}")
    print(f" Auto-Test Vectors  : {cycles:,} cycles per modification")
    print(" Status             : 🟢 ACTIVE (Zero Manual Commands Needed)")
    print(" Save any .v / .sv file and it will automatically verify!")
    print("=" * 65 + "\n")

    mtimes = {}
    try:
        while True:
            for root, _, files in os.walk(watch_dir):
                if "verification_out" in root:
                    continue
                for file in files:
                    if file.endswith((".v", ".sv")) and not file.endswith("_tb.sv"):
                        full_path = os.path.join(root, file)
                        try:
                            current_mtime = os.stat(full_path).st_mtime
                        except OSError:
                            continue

                        if full_path not in mtimes:
                            mtimes[full_path] = current_mtime
                        elif current_mtime > mtimes[full_path]:
                            mtimes[full_path] = current_mtime
                            sys_time = time.strftime("%H:%M:%S")
                            print(f"\n[{sys_time}] [CHANGE DETECTED] {file} modified. Triggering autonomous verification...")
                            run_verification_flow(full_path, cycles=cycles)
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n[RTL-AutoBench] Watch daemon stopped cleanly.")

def main():
    # If first argument is a file path rather than a subcommand, default to 'verify'
    subcommands = ["gen-tb", "watch", "verify"]
    if len(sys.argv) > 1 and sys.argv[1] not in subcommands and not sys.argv[1].startswith("-"):
        sys.argv.insert(1, "verify")

    p = argparse.ArgumentParser(
        description="RTL-AutoBench: Autonomous Pre-Silicon Hardware Verification Suite"
    )
    sub = p.add_subparsers(dest="subcommand")

    # 1. Full Verification & Synthesis (`verify` or direct file)
    verify_p = sub.add_parser("verify", help="Run full linting, SVA synthesis, simulation, Yosys synthesis, and NextPnR layout")
    verify_p.add_argument("verilog_file", help="Path to synthesizable Verilog/SystemVerilog source file")
    verify_p.add_argument("--cycles", type=int, default=50, help="Number of simulation cycles (default: 50)")
    verify_p.add_argument("--outdir", default=None, help="Output directory for testbenches and reports")

    # 2. Generate Testbench Only (`gen-tb`)
    gen_p = sub.add_parser("gen-tb", help="Generate a complete self-checking SystemVerilog testbench for any file")
    gen_p.add_argument("source_file", help="Path to Verilog/SystemVerilog source file")
    gen_p.add_argument("--cycles", type=int, default=100, help="Number of simulation cycles (default: 100)")
    gen_p.add_argument("-o", "--output", default=None, help="Save testbench to specified file path (default: print to terminal)")

    # 3. Watch Mode (`watch`)
    watch_p = sub.add_parser("watch", help="Autonomously monitor directory and auto-verify hardware files on save")
    watch_p.add_argument("directory", nargs="?", default=".", help="Directory to monitor for Verilog changes (default: current directory)")
    watch_p.add_argument("--cycles", type=int, default=50, help="Simulation vectors per test run")

    args = p.parse_args()

    if args.subcommand == "verify":
        run_verification_flow(args.verilog_file, cycles=args.cycles, output_dir=args.outdir)
    elif args.subcommand == "gen-tb":
        generate_testbench_only(args.source_file, cycles=args.cycles, output_file=args.output)
    elif args.subcommand == "watch":
        watch_directory(args.directory, cycles=args.cycles)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
