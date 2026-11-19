# Stage 1 Review: Hardware AST Ingestion & Topology Mapping
**Lead Documentarians:** AST Analysis Squad  
**Target:** RTL-AutoBench Core Parser  

### What Was Done in This Stage:
1. Built the zero-dependency regularized tokenizer that ingests both classic Verilog-2001 and SystemVerilog IEEE 1800 designs.
2. Extracted port definitions, bus widths, and input/output directions.
3. Automatically isolated clock nets and reset pins (handling active-low asynchronous resets).
4. Discovered FSM state encodings (`typedef enum` and `localparam STATE_*`).

### Human English Summary:
Before running tests, the system needs to "read the blueprint." This parser reads the code just like a senior engineer, cataloging every wire, switch, and state machine so that subsequent agents know exactly what signals need to be driven and measured.
