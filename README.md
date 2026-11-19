# RTL-AutoBench ⚡
> Autonomous Pre-Silicon Hardware Verification & Testbench Generator

[![Verification Suite](https://img.shields.io/badge/verification-passed-brightgreen.svg)]()
[![SystemVerilog](https://img.shields.io/badge/standard-IEEE%201800-blue.svg)]()
[![EDA](https://img.shields.io/badge/eda-verilator%20%7C%20iverilog%20%7C%20yosys-orange.svg)]()
[![Mode](https://img.shields.io/badge/mode-autonomous%20live%20watch-purple.svg)]()

`RTL-AutoBench` is an enterprise-grade autonomous pre-silicon verification engine designed for fabless semiconductor teams and chip designers. **Give it any Verilog or SystemVerilog hardware source code, and it automatically synthesizes a complete, cycle-accurate, self-checking testbench.**

---

## ⚡ 1. Generate a Testbench for ANY Source File (`gen-tb`)

If you have any Verilog module (e.g. `my_alu.sv`, `riscv_core.v`, `uart.v`), run:
```bash
# Print the generated self-checking testbench directly to terminal
rtl-autobench gen-tb my_design.sv --cycles 100

# Or save it to a testbench file directly
rtl-autobench gen-tb my_design.sv --cycles 100 -o my_design_tb.sv
```

### What the Generated Testbench Includes:
1. **Clock Generator:** 100MHz free-running clock (`10ns` period).
2. **Dynamic Reset Protocol:** Automatically asserts and deasserts reset according to detected polarity (`active_high` vs `active_low`).
3. **DUT Instantiation:** Maps all input and output ports with exact bit-widths and parameter symbols.
4. **Constrained Random Stimulus:** Uses `$urandom` and multi-chunk concatenation for wide 64-bit/128-bit buses.
5. **Floating State Monitors:** Checks for `X` and `Z` high-impedance hazards on every positive clock edge.
6. **Self-Checking Scoreboard:** Counts total vectors, logs assertion errors, and displays a pre-silicon verification pass/fail banner.

---

## ⚡ 2. Zero-Command Live Watch Daemon

```bash
# Run once: monitors the directory and auto-verifies any HDL file when saved
rtl-autobench watch ./examples
```
*Hit Save (`Cmd+S` / `Ctrl+S`) in your code editor, and RTL-AutoBench automatically compiles, lints, and simulates the design in the background.*

---

## ⚡ 3. Direct Full Verification (Linter + Simulator + Synthesizer)
```bash
# Verify a module and generate both testbench and pre-tapeout certificate
rtl-autobench examples/param_counter.sv --cycles 2000
```
