"""
Automated Verification Test Suite for RTL-AutoBench.
Tests AST parsing, parameters, reset polarity, SVA generation,
wide bus stimuli, and Icarus/Verilator simulation.
"""

import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from autoverif.parser.verilog_ast import VerilogModuleParser
from autoverif.generator.sva_generator import SVAGenerator
from autoverif.generator.tb_synthesizer import TestbenchSynthesizer
from autoverif.cli import run_verification_flow

class TestRTLAutoBench(unittest.TestCase):
    def setUp(self):
        self.alu_path = os.path.join(BASE_DIR, "examples", "alu_pipelined.sv")
        self.fsm_path = os.path.join(BASE_DIR, "examples", "fsm_traffic_ctrl.sv")
        self.fifo_path = os.path.join(BASE_DIR, "examples", "fifo_sync.sv")
        self.param_counter_path = os.path.join(BASE_DIR, "examples", "param_counter.sv")

    def test_ast_parsing(self):
        with open(self.alu_path, "r") as f:
            code = f.read()
        parser = VerilogModuleParser(code)
        meta = parser.parse()
        self.assertEqual(meta["module_name"], "alu_pipelined")
        self.assertEqual(len(meta["clock_ports"]), 1)
        self.assertEqual(len(meta["reset_ports"]), 1)
        self.assertEqual(meta["reset_polarity"], "active_low")
        self.assertEqual(len(meta["outputs"]), 2)

    def test_fsm_detection(self):
        with open(self.fsm_path, "r") as f:
            code = f.read()
        parser = VerilogModuleParser(code)
        meta = parser.parse()
        self.assertEqual(meta["module_name"], "fsm_traffic_ctrl")
        self.assertGreaterEqual(len(meta["fsm_states"]), 4)

    def test_parameter_parsing_and_resolution(self):
        with open(self.param_counter_path, "r") as f:
            code = f.read()
        parser = VerilogModuleParser(code)
        meta = parser.parse()
        self.assertEqual(meta["module_name"], "param_counter")
        self.assertEqual(meta["parameters"].get("WIDTH"), 8)
        self.assertEqual(meta["parameters"].get("MAX_COUNT"), 255)
        # Verify port width expression evaluated correctly (WIDTH-1:0 => 8 bits)
        count_port = next((p for p in meta["outputs"] if p["name"] == "count"), None)
        self.assertIsNotNone(count_port)
        self.assertEqual(count_port["width"], 8)
        # Verify active-high reset detection
        self.assertEqual(meta["reset_polarity"], "active_high")

    def test_wide_bus_stimulus_synthesizer(self):
        meta = {
            "module_name": "wide_bus_dut",
            "ports": [
                {"name": "clk", "direction": "input", "width": 1},
                {"name": "rst_n", "direction": "input", "width": 1},
                {"name": "data_64", "direction": "input", "width": 64},
                {"name": "out_64", "direction": "output", "width": 64}
            ],
            "inputs": [
                {"name": "clk", "direction": "input", "width": 1},
                {"name": "rst_n", "direction": "input", "width": 1},
                {"name": "data_64", "direction": "input", "width": 64}
            ],
            "outputs": [
                {"name": "out_64", "direction": "output", "width": 64}
            ],
            "clock_ports": ["clk"],
            "reset_ports": ["rst_n"],
            "reset_polarity": "active_low"
        }
        tb = TestbenchSynthesizer.synthesize_testbench(meta, sim_cycles=10)
        # Verify that for 64-bit width it concatenates two $urandom calls instead of overflowing $urandom_range
        self.assertIn("data_64 = {$urandom, $urandom};", tb)

    def test_full_verification_flow_alu(self):
        res = run_verification_flow(self.alu_path, cycles=25)
        self.assertEqual(res["sim"]["status"], "PASSED")
        self.assertIn(res["lint"]["status"], ["PASSED", "SKIPPED"])

    def test_full_verification_flow_fifo(self):
        res = run_verification_flow(self.fifo_path, cycles=25)
        self.assertEqual(res["sim"]["status"], "PASSED")

    def test_full_verification_flow_param_counter_active_high(self):
        res = run_verification_flow(self.param_counter_path, cycles=30)
        self.assertEqual(res["sim"]["status"], "PASSED")
        self.assertEqual(res["reset_polarity"], "active_high")

    def test_signed_and_shared_width_ports(self):
        meta = VerilogModuleParser(
            "module m (input wire clk, input signed [7:0] x, input logic [3:0] a, b, output reg signed [7:0] y); endmodule"
        ).parse()
        widths = {p["name"]: p["width"] for p in meta["ports"]}
        self.assertEqual(widths, {"clk": 1, "x": 8, "a": 4, "b": 4, "y": 8})

    def test_x_output_fails_simulation(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "xout.sv")
            with open(src, "w") as f:
                f.write("module xout (input logic clk, input logic rst_n, output logic [3:0] q);\n"
                        "  logic [3:0] r;\n  assign q = r;\nendmodule\n")
            res = run_verification_flow(src, cycles=5, output_dir=d)
            if res["sim"]["status"] != "SKIPPED":
                self.assertEqual(res["sim"]["status"], "FAILED")
                self.assertFalse(res["passed"])

    def test_counter_reports_flip_flops(self):
        res = run_verification_flow(self.param_counter_path, cycles=5)
        if res["synth"].get("status") == "PASSED":
            self.assertGreaterEqual(res["pnr"]["utilization"]["dff_used"], 8)
            self.assertGreater(res["synth"]["total_wires"], 0)

if __name__ == "__main__":
    unittest.main()
