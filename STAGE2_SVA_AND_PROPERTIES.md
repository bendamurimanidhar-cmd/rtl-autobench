# Stage 2 Review: Formal SVA Assertions & Testbench Generation
**Lead Documentarians:** SVA Synthesis Squad  
**Target:** RTL-AutoBench Generator Core  

### What Was Done in This Stage:
1. Implemented formal property synthesis (`assert property`) for reset deassertion, handshake valid-ready holding invariants, and FIFO buffer overflow/underflow boundaries.
2. Built the autonomous self-checking testbench generator which spins up a 100MHz clock, deasserts reset cleanly, and feeds randomized boundary vectors into the DUT.
3. Added floating state (`$isunknown`) detection to catch X/Z high-impedance bugs in hardware.

### Human English Summary:
This stage writes the actual "exam" for the hardware. It creates a complete simulation environment that hammers the chip with random inputs while constantly checking with strict rules (assertions) to ensure the chip never misbehaves or drops data.
