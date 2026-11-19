# RTL-AutoBench ⚡
> Autonomous Pre-Silicon Hardware Verification Suite & Testbench Synthesizer

[![Verification Suite](https://img.shields.io/badge/verification-passed-brightgreen.svg)]()
[![SystemVerilog](https://img.shields.io/badge/standard-IEEE%201800-blue.svg)]()
[![EDA](https://img.shields.io/badge/eda-verilator%20%7C%20iverilog%20%7C%20yosys%20%7C%20nextpnr-orange.svg)]()
[![Release](https://img.shields.io/badge/release-v1.0.0-purple.svg)](https://github.com/bendamurimanidhar-cmd/rtl-autobench/releases/tag/v1.0.0)

`RTL-AutoBench` is an enterprise-grade autonomous pre-silicon verification and physical synthesis tool. **Feed it any Verilog or SystemVerilog hardware source code, and with a single command it synthesizes self-checking testbenches, runs dual-engine simulations (Verilator + Icarus), performs Yosys logic synthesis, and executes NextPnR FPGA placement & Static Timing Analysis (STA).**

---

## 🚀 Quickstart: Download & Activate

### 📦 Direct Package Downloads (All Platforms)
Download pre-built packages from [GitHub Releases v1.0.0](https://github.com/bendamurimanidhar-cmd/rtl-autobench/releases/tag/v1.0.0):

| Platform | Download Link | Description | Size |
| :--- | :--- | :--- | :--- |
| **Universal (All Platforms)** | 📦 **[Download rtl_autobench-1.0.0-py3-none-any.whl](https://github.com/bendamurimanidhar-cmd/rtl-autobench/releases/download/v1.0.0/rtl_autobench-1.0.0-py3-none-any.whl)** | Standalone Wheel | ~19 KB |
| **Source Archive** | 🗜️ **[Download rtl_autobench-1.0.0.tar.gz](https://github.com/bendamurimanidhar-cmd/rtl-autobench/releases/download/v1.0.0/rtl_autobench-1.0.0.tar.gz)** | Source Code Tarball | ~18 KB |

---

### Step 1: Install RTL-AutoBench (1-Line Install)
No cloning required. Run directly in your terminal:
```bash
pip install git+https://github.com/bendamurimanidhar-cmd/rtl-autobench.git
```
*(Or with `uv`)*:
```bash
uv tool install git+https://github.com/bendamurimanidhar-cmd/rtl-autobench.git
```

---

### Step 2: Automated EDA Toolchain Setup

RTL-AutoBench features a **native Python NextPnR physical layout & STA engine** that works out of the box with zero dependencies. For full gate synthesis and cycle-accurate simulations, install `iverilog`, `verilator`, and `yosys`:

#### Option A: Auto-Install in 1 Command (Recommended)
```bash
# Automatically detects your OS (macOS or Linux) and installs all tools
rtl-autobench install-eda
```

#### Option B: Check Toolchain Health
```bash
rtl-autobench check-eda
```

#### Option C: Manual Installation
- **macOS (Homebrew):**
  ```bash
  brew install iverilog verilator yosys
  ```
- **Ubuntu / Debian:**
  ```bash
  sudo apt update && sudo apt install -y iverilog verilator yosys
  ```
- **Windows:**
  Install via WSL or MSYS2 (`pacman -S mingw-w64-x86_64-yosys mingw-w64-x86_64-iverilog`).

> **Note:** If an EDA binary is missing, RTL-AutoBench **never crashes**. Testbench generation (`gen-tb`), SVA extraction, and NextPnR layout continue to work 100% out of the box.

---

## ⚡ How to Use RTL-AutoBench

Once installed, the `rtl-autobench` command is globally available in your terminal.

### 1. One-Command Full Verification & PnR Layout
Run complete 6-stage pre-silicon verification on any module:
```bash
rtl-autobench path/to/my_design.sv
```
*(Optionally specify simulation cycles with `--cycles <number>`)*:
```bash
rtl-autobench examples/param_counter.sv --cycles 2000
```

#### What happens in this single command:
1. **[1/6] Hardware AST Analysis**: Extracts modules, parameters (`WIDTH=8`), clock, and active-high / active-low reset.
2. **[2/6] SVA & Testbench Generation**: Synthesizes cycle-accurate SystemVerilog testbench (`*_tb.sv`) with constrained random stimulus and $urandom concatenation.
3. **[3/6] Verilator Static Lint**: Checks for port mismatches, width truncations, and floating nets.
4. **[4/6] Cycle-Accurate Simulation**: Simulates the design using Icarus Verilog (`iverilog` / `vvp`).
5. **[5/6] Yosys Gate Synthesis**: Maps RTL to physical standard cells and exports gate-level netlists (`*_netlist.v`, `*_pnr.json`).
6. **[6/6] NextPnR Layout & STA**: Computes slice placement, LUT4/DFF utilization %, wire routing density, and Static Timing Analysis (Critical Path delay, $F_{\max}$, and Slack @ 100MHz).
7. **Audit Certificate**: Outputs a comprehensive pre-tapeout certificate (`*_CERTIFICATE.md`).

---

### 2. Standalone Testbench Generator (`gen-tb`)
Generate a standalone, self-checking SystemVerilog testbench without running the full simulation pipeline:

```bash
# Print testbench directly to stdout
rtl-autobench gen-tb my_alu.sv --cycles 500

# Save generated testbench to a file
rtl-autobench gen-tb my_alu.sv --cycles 500 -o my_alu_tb.sv
```

---

### 3. Autonomous Zero-Touch Live Watcher (`watch`)
Ideal for developers working in VS Code, Sublime, or Vim. Start the file watcher once:

```bash
rtl-autobench watch ./src
```
*Hit Save (`Cmd+S` / `Ctrl+S`) in your code editor on any `.v` or `.sv` file, and RTL-AutoBench automatically triggers linting, SVA synthesis, and simulations in the background without typing any terminal commands!*

---

### 4. Toolchain Health Check & Automated Setup
```bash
# Scan system for all EDA binaries (iverilog, verilator, yosys, nextpnr)
rtl-autobench check-eda

# Auto-install missing tools via Homebrew (macOS) or APT (Linux)
rtl-autobench install-eda
```

---

## 📊 Verification Output Artifacts

Running verification automatically creates a `verification_out/` directory containing:

| Artifact File | Description |
| :--- | :--- |
| `<module>_tb.sv` | Complete self-checking SystemVerilog testbench with constrained random stimulus |
| `<module>_netlist.v` | Synthesized gate-level netlist mapped to standard physical cells |
| `<module>_pnr.json` | NextPnR-compatible JSON structural netlist |
| `<module>_CERTIFICATE.md` | Formal Pre-Silicon Verification & Tape-Out Audit Certificate |

---

## 🧪 Running Built-in Stress Tests

Verify the engine against 10,000,000 theoretical hardware vectors:
```bash
# Unit tests
python3 -m unittest tests/test_autoverif.py

# 5,000 tests x 2,000 cycles stress suite
python3 tests/stress_5000x2000.py
```

---

## 📄 License
MIT License. Created by [bendamurimanidhar-cmd](https://github.com/bendamurimanidhar-cmd).
