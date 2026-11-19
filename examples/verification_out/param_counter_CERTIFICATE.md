# Pre-Silicon Hardware Verification Audit
## Certificate of Functional Verification: `param_counter`
**Status:** 🟢 READY FOR TAPE-OUT  
**Date of Audit:** 2026-11-19 11:19:01 UTC  
**Auditor Engine:** `RTL-AutoBench v2.0 Enterprise`  

---

### 1. Pre-Silicon Verification Summary
* **Device Under Test (DUT):** `param_counter`
* **Verilator Static Lint:** `PASSED` (0 warnings, 0 errors)
* **Cycle-Accurate Icarus Simulation:** `PASSED`
* **Yosys Logic Synthesis:** `142 cells` (0 wires)
* **NextPnR Timing Closure:** `MET (TIMING PASSED)` (Fmax: `200.8 MHz`, Slack: `5.02 ns`)

---

### 2. Interface Specification
* **Clock Domains:** `clk`
* **Reset Domains:** `rst (active_high)`
* **Inputs (4):** `clk[1], rst[1], en[1], up_down[1]`
* **Outputs (2):** `count[8], overflow[1]`
* **FSM States Detected:** `None (Datapath-only)`

---

### 3. NextPnR Physical Layout & Placement Metrics
* **Target Architecture:** `1.2V Silicon Core / Lattice iCE40 Architecture`
* **LUT4 Utilization:** `16 / 1280 (1.2%)`
* **Flip-Flop (DFF) Utilization:** `0 / 1280 (0.0%)`
* **IO Pad Utilization:** `0 / 96 (0.0%)`
* **Physical Bounding Box:** `6 x 6 Slices` (Routing Density: `35.6%`)

---

### 4. NextPnR Static Timing Analysis (STA)
* **Target Clock Frequency:** `100.0 MHz` (Target Period: `10.0 ns`)
* **Maximum Achievable Clock (Fmax):** `200.8 MHz`
* **Critical Path Propagation Delay:** `4.98 ns`
  * *Internal Logic Gate Delay:* `2.9 ns`
  * *Interconnect Routing Wire Delay:* `1.28 ns`
* **Setup Timing Slack:** `5.02 ns` -> **MET (TIMING PASSED)**

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
Using template $_SDFFCE_PP0P_ for cells of type $_SDFFCE_PP0P_.
Using template $_SDFF_PP0_ for cells of type $_SDFF_PP0_.
Generating RTLIL representation for module `$_DLATCH_N_'.
Generating RTLIL representation for module `$_DLATCH_P_'.
Generating RTLIL representation for module `$__ICE40_CARRY_WRAPPER'.
Generating RTLIL representation for module `$__div_mod_u'.
Generating RTLIL representation for module `$__div_mod_trunc'.
Generating RTLIL representation for module `$__div_mod_floor'.
Generating RTLIL representation for module `$__ABC9_BARRIER_MAP'.
Generating RTLIL representation for module `$__ABC9_DELAY'.
Generating RTLIL representation for module `$__ABC9_BARRIER'.
Generating RTLIL representation for module `$__ABC9_SCC_BREAKER'.
Generating RTLIL representation for module `$__DFF_N__$abc9_flop'.
Generating RTLIL representation for module `$__DFF_P__$abc9_flop'.
Generating RTLIL representation for module `$__div_mod_u'.
Generating RTLIL representation for module `$__div_mod_trunc'.
Generating RTLIL representation for module `$__div_mod_floor'.
      17 $_MUX_
      24 $_OR_
      14 $_XOR_
      26 $_AND_
      11 $_NOT_
       8 SB_DFFESR
       1 SB_DFFSR
       9 $paramod$__ABC9_DELAY\DELAY=32'00000000000000000000000000010101
       9 $paramod$__ABC9_DELAY\DELAY=32'00000000000000000000000011001011
Generating RTLIL representation for module `$__DFF_x__$abc9_flop'.
Generating RTLIL representation for module `$__ABC9_SCC_BREAKER'.
Generating RTLIL representation for module `$__ABC9_BARRIER'.
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
Number of LUTs:       16
  with \SB_CARRY    (#0)    0
  with \SB_CARRY    (#1)    0
Number of LUTs:       16
  with \SB_CARRY    (#0)    0
  with \SB_CARRY    (#1)    0
Number of LUTs:       16
  with \SB_CARRY    (#0)    0
  with \SB_CARRY    (#1)    0
        8   SB_DFFESR
        1   SB_DFFSR
       16   SB_LUT4
        8   SB_DFFESR
        1   SB_DFFSR
       16   SB_LUT4
        8   SB_DFFESR
        1   SB_DFFSR
       16   SB_LUT4
```

---

### 6. Simulation Scoreboard Trace
```text
[20000] [INIT] Reset released (active_high). Beginning autonomous test vectors...

==================================================
  RTL-AutoBench Verification Scoreboard: param_counter
==================================================
  Total Test Vectors Evaluated : 5000
  Protocol / Assertion Failures: 0
  OVERALL RESULT               : [VERIFICATION PASSED]
==================================================

/Users/mohanmanidhar/.gemini/antigravity/scratch/rtl-autobench/examples/verification_out/param_counter_tb.sv:80: $finish called at 50046000 (1ps)
```

---
*Generated autonomously by RTL-AutoBench Pre-Silicon Verification & PnR Pipeline.*
