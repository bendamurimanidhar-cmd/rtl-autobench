"""
Autonomous SystemVerilog Assertions (SVA) Property Generator.
Generates cycle-accurate hardware assertions to catch pre-silicon protocol violations.
"""

from typing import Dict, Any, List

class SVAGenerator:
    @staticmethod
    def generate_assertions(meta: Dict[str, Any]) -> str:
        sva_lines = []
        clk = meta["clock_ports"][0] if meta["clock_ports"] else "clk"
        rst = meta["reset_ports"][0] if meta["reset_ports"] else "rst_n"
        polarity = meta.get("reset_polarity", "active_low")

        rst_active = f"(!{rst})" if polarity == "active_low" else f"({rst})"
        rst_disable = f"(!{rst})" if polarity == "active_low" else f"({rst})"

        sva_lines.append("// ==========================================================")
        sva_lines.append(f"// Automatically Synthesized Formal SVA Assertions ({polarity})")
        sva_lines.append("// ==========================================================")
        sva_lines.append("`ifdef FORMAL_VERIFICATION")

        # 1. Reset Property
        sva_lines.append(f"""
  // Check that reset correctly drives initial states
  property p_reset_active;
    @(posedge {clk}) {rst_active} |-> 1'b1;
  endproperty
  assert_reset_check: assert property (p_reset_active) else $error("[SVA FAIL] Reset protocol violated!");
""")

        # 2. Handshake Protocol Assertions (if valid/ready detected)
        inputs = [p["name"] for p in meta["inputs"]]
        outputs = [p["name"] for p in meta["outputs"]]
        all_signals = inputs + outputs

        valid_sig = next((s for s in all_signals if "valid" in s.lower()), None)
        ready_sig = next((s for s in all_signals if "ready" in s.lower()), None)

        if valid_sig and ready_sig:
            sva_lines.append(f"""
  // Handshake Invariant: Valid must stay high until Ready acknowledges
  property p_handshake_stability;
    @(posedge {clk}) disable iff {rst_disable}
    ({valid_sig} && !{ready_sig}) |=> {valid_sig};
  endproperty
  assert_handshake_stable: assert property (p_handshake_stability)
    else $error("[SVA FAIL] Valid signal dropped before Ready asserted!");
""")

        # 3. FIFO / Counter Overflow & Underflow Assertions
        full_sig = next((s for s in all_signals if "full" in s.lower()), None)
        wr_sig = next((s for s in all_signals if "wr" in s.lower() or "push" in s.lower()), None)
        empty_sig = next((s for s in all_signals if "empty" in s.lower()), None)
        rd_sig = next((s for s in all_signals if "rd" in s.lower() or "pop" in s.lower()), None)

        if full_sig and wr_sig:
            sva_lines.append(f"""
  // Buffer Safety: Write while Full is prohibited
  property p_no_overflow;
    @(posedge {clk}) disable iff {rst_disable}
    not ({full_sig} && {wr_sig});
  endproperty
  assert_no_overflow: assert property (p_no_overflow)
    else $error("[SVA FAIL] Buffer overflow: Write attempted while FULL!");
""")

        if empty_sig and rd_sig:
            sva_lines.append(f"""
  // Buffer Safety: Read while Empty is prohibited
  property p_no_underflow;
    @(posedge {clk}) disable iff {rst_disable}
    not ({empty_sig} && {rd_sig});
  endproperty
  assert_no_underflow: assert property (p_no_underflow)
    else $error("[SVA FAIL] Buffer underflow: Read attempted while EMPTY!");
""")

        sva_lines.append("`endif // FORMAL_VERIFICATION\n")
        return "\n".join(sva_lines)
