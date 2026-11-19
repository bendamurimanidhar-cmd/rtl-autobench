# Pre-Silicon Hardware Verification Audit
## Certificate of Functional Verification: `alu_pipelined`
**Status:** 🟢 READY FOR TAPE-OUT  
**Date of Audit:** 2026-11-19 11:19:00 UTC  
**Auditor Engine:** `RTL-AutoBench v2.0 Enterprise`  

---

### 1. Pre-Silicon Verification Summary
* **Device Under Test (DUT):** `alu_pipelined`
* **Verilator Static Lint:** `PASSED` (0 warnings, 0 errors)
* **Cycle-Accurate Icarus Simulation:** `PASSED`
* **Yosys Logic Synthesis:** `158 cells` (0 wires)
* **NextPnR Timing Closure:** `MET (TIMING PASSED)` (Fmax: `188.7 MHz`, Slack: `4.7 ns`)

---

### 2. Interface Specification
* **Clock Domains:** `clk`
* **Reset Domains:** `rst_n (active_low)`
* **Inputs (5):** `clk[1], rst_n[1], opcode[2], op_a[4], op_b[4]`
* **Outputs (2):** `result[4], carry_out[1]`
* **FSM States Detected:** `None (Datapath-only)`

---

### 3. NextPnR Physical Layout & Placement Metrics
* **Target Architecture:** `1.2V Silicon Core / Lattice iCE40 Architecture`
* **LUT4 Utilization:** `25 / 1280 (2.0%)`
* **Flip-Flop (DFF) Utilization:** `0 / 1280 (0.0%)`
* **IO Pad Utilization:** `0 / 96 (0.0%)`
* **Physical Bounding Box:** `8 x 8 Slices` (Routing Density: `31.2%`)

---

### 4. NextPnR Static Timing Analysis (STA)
* **Target Clock Frequency:** `100.0 MHz` (Target Period: `10.0 ns`)
* **Maximum Achievable Clock (Fmax):** `188.7 MHz`
* **Critical Path Propagation Delay:** `5.3 ns`
  * *Internal Logic Gate Delay:* `2.9 ns`
  * *Interconnect Routing Wire Delay:* `1.6 ns`
* **Setup Timing Slack:** `4.7 ns` -> **MET (TIMING PASSED)**

---

### 5. Gate-Level Hardware Logic Utilization (Yosys)
```text
Generating RTLIL representation for module `$__div_mod_u'.
Generating RTLIL representation for module `$__div_mod_trunc'.
Generating RTLIL representation for module `$__div_mod_floor'.
Generating RTLIL representation for module `\SB_IO'.
Generating RTLIL representation for module `\SB_GB_IO'.
Generating RTLIL representation for module `\SB_GB'.
Generating RTLIL representation for module `\SB_LUT4'.
Generating RTLIL representation for module `\SB_CARRY'.
Generating RTLIL representation for module `\SB_DFF'.
Generating RTLIL representation for module `\SB_DFFE'.
Generating RTLIL representation for module `\SB_DFFSR'.
Generating RTLIL representation for module `\SB_DFFR'.
Generating RTLIL representation for module `\SB_DFFSS'.
Generating RTLIL representation for module `\SB_DFFS'.
Generating RTLIL representation for module `\SB_DFFESR'.
Generating RTLIL representation for module `\SB_DFFER'.
Generating RTLIL representation for module `\SB_DFFESS'.
Generating RTLIL representation for module `\SB_DFFES'.
Generating RTLIL representation for module `\SB_DFFN'.
Generating RTLIL representation for module `\SB_DFFNE'.
Generating RTLIL representation for module `\SB_DFFNSR'.
Generating RTLIL representation for module `\SB_DFFNR'.
Generating RTLIL representation for module `\SB_DFFNSS'.
Generating RTLIL representation for module `\SB_DFFNS'.
Generating RTLIL representation for module `\SB_DFFNESR'.
Generating RTLIL representation for module `\SB_DFFNER'.
Generating RTLIL representation for module `\SB_DFFNESS'.
Generating RTLIL representation for module `\SB_DFFNES'.
Generating RTLIL representation for module `\SB_RAM40_4K'.
Generating RTLIL representation for module `\SB_RAM40_4KNR'.
Generating RTLIL representation for module `\SB_RAM40_4KNW'.
Generating RTLIL representation for module `\SB_RAM40_4KNRNW'.
Generating RTLIL representation for module `\SB_PLL40_CORE'.
Generating RTLIL representation for module `\SB_PLL40_PAD'.
Generating RTLIL representation for module `\SB_PLL40_2_PAD'.
Generating RTLIL representation for module `\SB_PLL40_2F_CORE'.
Generating RTLIL representation for module `\SB_PLL40_2F_PAD'.
Generating RTLIL representation for module `\SB_WARMBOOT'.
Generating RTLIL representation for module `\SB_SPRAM256KA'.
Generating RTLIL representation for module `\SB_HFOSC'.
Generating RTLIL representation for module `\SB_LFOSC'.
Generating RTLIL representation for module `\SB_RGBA_DRV'.
Generating RTLIL representation for module `\SB_LED_DRV_CUR'.
Generating RTLIL representation for module `\SB_RGB_DRV'.
Generating RTLIL representation for module `\SB_I2C'.
Generating RTLIL representation for module `\SB_SPI'.
Generating RTLIL representation for module `\SB_LEDDA_IP'.
Generating RTLIL representation for module `\SB_FILTER_50NS'.
Generating RTLIL representation for module `\SB_IO_I3C'.
Generating RTLIL representation for module `\SB_IO_OD'.
Generating RTLIL representation for module `\SB_MAC16'.
Generating RTLIL representation for module `$__ICE40_RAM4K_'.
Generating RTLIL representation for module `$__ICE40_SPRAM_'.
Generating RTLIL representation for module `$__div_mod_u'.
Generating RTLIL representation for module `$__div_mod_trunc'.
Generating RTLIL representation for module `$__div_mod_floor'.
Generating RTLIL representation for module `$_DFF_N_'.
Generating RTLIL representation for module `$_DFF_P_'.
Generating RTLIL representation for module `$_DFFE_NP_'.
Generating RTLIL representation for module `$_DFFE_PP_'.
Generating RTLIL representation for module `$_DFF_NP0_'.
Generating RTLIL representation for module `$_DFF_NP1_'.
Generating RTLIL representation for module `$_DFF_PP0_'.
Generating RTLIL representation for module `$_DFF_PP1_'.
Generating RTLIL representation for module `$_DFFE_NP0P_'.
Generating RTLIL representation for module `$_DFFE_NP1P_'.
Generating RTLIL representation for module `$_DFFE_PP0P_'.
Generating RTLIL representation for module `$_DFFE_PP1P_'.
Generating RTLIL representation for module `$_SDFF_NP0_'.
Generating RTLIL representation for module `$_SDFF_NP1_'.
Generating RTLIL representation for module `$_SDFF_PP0_'.
Generating RTLIL representation for module `$_SDFF_PP1_'.
Generating RTLIL representation for module `$_SDFFCE_NP0P_'.
Generating RTLIL representation for module `$_SDFFCE_NP1P_'.
Generating RTLIL representation for module `$_SDFFCE_PP0P_'.
Generating RTLIL representation for module `$_SDFFCE_PP1P_'.
Using template $_DFF_PP0_ for cells of type $_DFF_PP0_.
Generating RTLIL representation for module `$_DLATCH_N_'.
Generating RTLIL representation for module `$_DLATCH_P_'.
Generating RTLIL representation for module `$__ICE40_CARRY_WRAPPER'.
Marked 1 switch rules as full_case in process $proc$/opt/homebrew/Cellar/yosys/0.70/bin/../share/yosys/ice40/cells_sim.v:406$556 in module SB_DFFR.
Found init rule in `\SB_DFFR.$proc$/opt/homebrew/Cellar/yosys/0.70/bin/../share/yosys/ice40/cells_sim.v:404$558'.
Found async reset \R in `\SB_DFFR.$proc$/opt/homebrew/Cellar/yosys/0.70/bin/../share/yosys/ice40/cells_sim.v:406$556'.
Creating decoders for process `\SB_DFFR.$proc$/opt/homebrew/Cellar/yosys/0.70/bin/../share/yosys/ice40/cells_sim.v:404$558'.
Creating decoders for process `\SB_DFFR.$proc$/opt/homebrew/Cellar/yosys/0.70/bin/../share/yosys/ice40/cells_sim.v:406$556'.
Creating register for signal `\SB_DFFR.\Q' using process `\SB_DFFR.$proc$/opt/homebrew/Cellar/yosys/0.70/bin/../share/yosys/ice40/cells_sim.v:406$556'.
Removing empty process `SB_DFFR.$proc$/opt/homebrew/Cellar/yosys/0.70/bin/../share/yosys/ice40/cells_sim.v:404$558'.
Removing empty process `SB_DFFR.$proc$/opt/homebrew/Cellar/yosys/0.70/bin/../share/yosys/ice40/cells_sim.v:406$556'.
Generating RTLIL representation for module `$__div_mod_u'.
Generating RTLIL representation for module `$__div_mod_trunc'.
Generating RTLIL representation for module `$__div_mod_floor'.
Optimizing module SB_DFFR.
Finding identical cells in module `\SB_DFFR'.
Computing hashes of 2 cells of `\SB_DFFR'.
Finding duplicate cells in `\SB_DFFR'.
Running muxtree optimizer on module \SB_DFFR..
  Optimizing cells in module \SB_DFFR.
Finding identical cells in module `\SB_DFFR'.
Computing hashes of 2 cells of `\SB_DFFR'.
Finding duplicate cells in `\SB_DFFR'.
Finding unused cells or wires in module \SB_DFFR..
Optimizing module SB_DFFR.
Generating RTLIL representation for module `$__ABC9_BARRIER_MAP'.
Using template SB_DFFR for cells of type SB_DFFR.
Generating RTLIL representation for module `$__ABC9_DELAY'.
Generating RTLIL representation for module `$__ABC9_BARRIER'.
Generating RTLIL representation for module `$__ABC9_SCC_BREAKER'.
Generating RTLIL representation for module `$__DFF_N__$abc9_flop'.
Generating RTLIL representation for module `$__DFF_P__$abc9_flop'.
Generating RTLIL representation for module `$__div_mod_u'.
Generating RTLIL representation for module `$__div_mod_trunc'.
Generating RTLIL representation for module `$__div_mod_floor'.
      30 $_OR_
      14 $_XOR_
      36 $_AND_
      13 $_NOT_
       5 SB_DFFR
       5 SB_DFFR_$abc9_byp
ABC RESULTS:   \SB_DFFR_$abc9_byp cells:        5
Generating RTLIL representation for module `$__DFF_x__$abc9_flop'.
Generating RTLIL representation for module `$__ABC9_SCC_BREAKER'.
Generating RTLIL representation for module `$__ABC9_BARRIER'.
Using template SB_DFFR_$abc9_byp for cells of type SB_DFFR_$abc9_byp.
Generating RTLIL representation for module `$_DFF_N_'.
Generating RTLIL representation for module `$_DFF_P_'.
Generating RTLIL representation for module `$_DFFE_NP_'.
Generating RTLIL representation for module `$_DFFE_PP_'.
Generating RTLIL representation for module `$_DFF_NP0_'.
Generating RTLIL representation for module `$_DFF_NP1_'.
Generating RTLIL representation for module `$_DFF_PP0_'.
Generating RTLIL representation for module `$_DFF_PP1_'.
Generating RTLIL representation for module `$_DFFE_NP0P_'.
Generating RTLIL representation for module `$_DFFE_NP1P_'.
Generating RTLIL representation for module `$_DFFE_PP0P_'.
Generating RTLIL representation for module `$_DFFE_PP1P_'.
Generating RTLIL representation for module `$_SDFF_NP0_'.
Generating RTLIL representation for module `$_SDFF_NP1_'.
Generating RTLIL representation for module `$_SDFF_PP0_'.
Generating RTLIL representation for module `$_SDFF_PP1_'.
Generating RTLIL representation for module `$_SDFFCE_NP0P_'.
Generating RTLIL representation for module `$_SDFFCE_NP1P_'.
Generating RTLIL representation for module `$_SDFFCE_PP0P_'.
Generating RTLIL representation for module `$_SDFFCE_PP1P_'.
Number of LUTs:       25
  with \SB_CARRY    (#0)    0
  with \SB_CARRY    (#1)    0
Number of LUTs:       25
  with \SB_CARRY    (#0)    0
  with \SB_CARRY    (#1)    0
Number of LUTs:       25
  with \SB_CARRY    (#0)    0
  with \SB_CARRY    (#1)    0
        5   SB_DFFR
       25   SB_LUT4
        5   SB_DFFR
       25   SB_LUT4
        5   SB_DFFR
       25   SB_LUT4
```

---

### 6. Simulation Scoreboard Trace
```text
[20000] [INIT] Reset released (active_low). Beginning autonomous test vectors...

==================================================
  RTL-AutoBench Verification Scoreboard: alu_pipelined
==================================================
  Total Test Vectors Evaluated : 5000
  Protocol / Assertion Failures: 0
  OVERALL RESULT               : [VERIFICATION PASSED]
==================================================

/Users/mohanmanidhar/.gemini/antigravity/scratch/rtl-autobench/examples/verification_out/alu_pipelined_tb.sv:84: $finish called at 50046000 (1ps)
```

---
*Generated autonomously by RTL-AutoBench Pre-Silicon Verification & PnR Pipeline.*
