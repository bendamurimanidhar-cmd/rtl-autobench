# Stage 3 Review: Verilator Linting & Icarus Verilog Simulation
**Lead Documentarians:** Simulation & Execution Squad  
**Target:** Dual-Engine Simulation Pipeline  

### What Was Done in This Stage:
1. Integrated Verilator for 2-state cycle linting, checking for implicit net declarations, width truncations, and latches.
2. Integrated Icarus Verilog (`iverilog` + `vvp`) for cycle-accurate 4-state event simulation with full time-step scheduling.
3. Added timeout watchdogs to prevent infinite loops in buggy state machines.

### Human English Summary:
This stage runs the test inside virtual hardware simulators. Verilator checks that the code is clean and adheres to standard manufacturing guidelines, while Icarus Verilog simulates every clock pulse to verify that the math, memory, and state transitions are 100% correct.
