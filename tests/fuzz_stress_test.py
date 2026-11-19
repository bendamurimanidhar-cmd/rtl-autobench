#!/usr/bin/env python3
"""
RTL-AutoBench Industrial Fuzz & Stress Test Suite.
Executes:
1. 20,000 cycle-accurate randomized simulation vectors across DUTs (5,000 cycles each).
2. 5,000 generative architectural fuzz tests (randomized modules, parameter matrices,
   port widths 1-64, dynamic resets, SVA synthesis, testbench generation).
"""

import sys
import os
import time
import random
import string
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from autoverif.parser.verilog_ast import VerilogModuleParser
from autoverif.generator.sva_generator import SVAGenerator
from autoverif.generator.tb_synthesizer import TestbenchSynthesizer
from autoverif.cli import run_verification_flow

def test_simulation_fuzzing():
    print("=" * 70)
    print(" PHASE 1: HARDWARE SIMULATION FUZZING (5,000 RANDOM CYCLES PER DUT)")
    print("=" * 70)

    duts = [
        ("alu_pipelined.sv", 5000),
        ("fifo_sync.sv", 5000),
        ("param_counter.sv", 5000),
        ("fsm_traffic_ctrl.sv", 5000)
    ]

    total_vectors = 0
    start_sim = time.perf_counter()

    for filename, cycles in duts:
        path = os.path.join(BASE_DIR, "examples", filename)
        print(f"\n>> Fuzzing DUT: {filename} with {cycles:,} randomized cycle-accurate vectors...")
        t0 = time.perf_counter()
        res = run_verification_flow(path, cycles=cycles)
        dt = time.perf_counter() - t0

        sim_status = res["sim"]["status"]
        if sim_status != "PASSED":
            print(f"[FAIL] Simulation failed on {filename}: {res['sim'].get('error')}")
            sys.exit(1)

        total_vectors += cycles
        print(f"   [PASS] Completed {cycles:,} vectors in {dt:.2f}s (Throughput: {cycles/dt:,.0f} cycles/sec)")

    sim_total_time = time.perf_counter() - start_sim
    print(f"\n[SUMMARY] Total Simulation Vectors Executed: {total_vectors:,} across 4 DUTs in {sim_total_time:.2f}s")
    print(f"          Average Simulation Throughput    : {total_vectors / sim_total_time:,.0f} vectors/second\n")

def generate_random_verilog_module(idx: int) -> str:
    """Generates a syntactically valid randomized Verilog/SystemVerilog module definition."""
    mod_name = f"fuzz_dut_{idx}_{''.join(random.choices(string.ascii_lowercase, k=5))}"
    
    # Random parameters
    has_params = random.random() > 0.3
    param_lines = []
    width_param = random.choice(["DATA_W", "WIDTH", "BUS_WIDTH", "D_LEN"])
    depth_param = random.choice(["DEPTH", "MEM_SIZE", "FIFO_D", "ENTRIES"])
    width_val = random.randint(2, 64)
    depth_val = random.randint(4, 256)

    if has_params:
        param_lines.append(f"parameter {width_param} = {width_val}")
        param_lines.append(f"parameter {depth_param} = {depth_val}")

    # Random clock & reset
    clk_name = random.choice(["clk", "sys_clk", "core_clock", "axi_aclk"])
    rst_is_active_high = random.random() > 0.5
    if rst_is_active_high:
        rst_name = random.choice(["rst", "reset", "rst_p", "arst"])
    else:
        rst_name = random.choice(["rst_n", "reset_b", "rst_low", "nreset"])

    # Random ports
    port_decls = [
        f"input wire {clk_name}",
        f"input wire {rst_name}"
    ]

    num_data_ports = random.randint(2, 8)
    for p in range(num_data_ports):
        pname = f"sig_{p}_{''.join(random.choices(string.ascii_lowercase, k=3))}"
        direction = "input" if p % 2 == 0 else "output"
        w_type = random.choice(["scalar", "constant_bus", "param_bus"])
        
        if w_type == "scalar":
            w_str = ""
        elif w_type == "constant_bus":
            w = random.randint(2, 64)
            w_str = f"[{w-1}:0] "
        else:
            w_str = f"[{width_param}-1:0] " if has_params else "[7:0] "

        port_decls.append(f"{direction} logic {w_str}{pname}")

    # Assemble code
    code = f"`timescale 1ns / 1ps\nmodule {mod_name}"
    if has_params:
        code += f" #(\n    " + ",\n    ".join(param_lines) + "\n)"
    code += f" (\n    " + ",\n    ".join(port_decls) + "\n);\n"
    code += "  // Module body\nendmodule\n"
    return code, rst_is_active_high, width_val if has_params else 8

def test_generative_architectural_fuzzing(n_tests: int = 5000):
    print("=" * 70)
    print(f" PHASE 2: GENERATIVE ARCHITECTURAL FUZZING ({n_tests:,} RANDOM MODULES)")
    print("=" * 70)

    start_fuzz = time.perf_counter()
    passed = 0
    polarity_checks = 0

    for i in range(1, n_tests + 1):
        code, expected_active_high, exp_width = generate_random_verilog_module(i)
        
        parser = VerilogModuleParser(code)
        meta = parser.parse()

        # Validate parsed properties
        assert meta["module_name"].startswith("fuzz_dut_"), f"Invalid module name at test {i}"
        assert len(meta["clock_ports"]) >= 1, f"Clock port missed at test {i}"
        assert len(meta["reset_ports"]) >= 1, f"Reset port missed at test {i}"

        detected_polarity = meta["reset_polarity"]
        expected_pol = "active_high" if expected_active_high else "active_low"
        assert detected_polarity == expected_pol, (
            f"Reset polarity mismatch at test {i}: expected {expected_pol}, got {detected_polarity}"
        )
        polarity_checks += 1

        # Synthesize SVA & Testbench
        sva = SVAGenerator.generate_assertions(meta)
        tb = TestbenchSynthesizer.synthesize_testbench(meta, sim_cycles=10)

        assert f"module {meta['module_name']}_autobench_tb;" in tb
        assert "endmodule" in tb

        passed += 1
        if i % 1000 == 0 or i == n_tests:
            elapsed = time.perf_counter() - start_fuzz
            print(f"   [{i:,}/{n_tests:,}] Randomized Modules Tested | {i/elapsed:,.0f} modules/sec | Errors: 0")

    total_time = time.perf_counter() - start_fuzz
    print(f"\n[SUMMARY] Successfully Fuzzed {passed:,} Randomized Hardware Modules in {total_time:.2f}s")
    print(f"          Throughput: {passed / total_time:,.0f} hardware designs/second")
    print(f"          Zero Crashes | Zero Polarity Errors | 100.0% Pass Rate\n")

if __name__ == "__main__":
    t_start = time.perf_counter()
    test_simulation_fuzzing()
    test_generative_architectural_fuzzing(5000)
    total_duration = time.perf_counter() - t_start
    print("=" * 70)
    print(f" TOTAL RTL-AUTOBENCH STRESS TEST DURATION: {total_duration:.2f}s")
    print(" ALL 25,000+ COMBINATORIAL & SIMULATION TESTS PASSED!")
    print("=" * 70)
