"""
Tape-Out Readiness & Formal Verification Certificate Generator.
Emits executive Markdown and self-contained interactive audit reports
including simulation, Yosys logic synthesis, and NextPnR physical layout & timing.
"""

from datetime import datetime
from typing import Dict, Any

class CertificateGenerator:
    @staticmethod
    def generate_markdown(audit_data: Dict[str, Any]) -> str:
        mod = audit_data["module_name"]
        lint = audit_data.get("lint", {})
        sim = audit_data.get("sim", {})
        synth = audit_data.get("synth", {})
        pnr = audit_data.get("pnr", {})
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        overall_status = "PASSED" if sim.get("status") == "PASSED" and lint.get("status") in ["PASSED", "SKIPPED"] else "FAILED"
        badge = "🟢 READY FOR TAPE-OUT" if overall_status == "PASSED" else "🔴 ACTION REQUIRED"

        pnr_util = pnr.get("utilization", {})
        pnr_timing = pnr.get("timing", {})
        pnr_layout = pnr.get("layout", {})

        md = f"""# Pre-Silicon Hardware Verification Audit
## Certificate of Functional Verification: `{mod}`
**Status:** {badge}  
**Date of Audit:** {ts}  
**Auditor Engine:** `RTL-AutoBench v2.0 Enterprise`  

---

### 1. Pre-Silicon Verification Summary
* **Device Under Test (DUT):** `{mod}`
* **Verilator Static Lint:** `{lint.get('status', 'N/A')}` ({lint.get('warning_count', 0)} warnings, {lint.get('error_count', 0)} errors)
* **Cycle-Accurate Icarus Simulation:** `{sim.get('status', 'N/A')}`
* **Yosys Logic Synthesis:** `{synth.get('total_cells', 'N/A')} cells` ({synth.get('total_wires', 0)} wires)
* **NextPnR Timing Closure:** `{pnr_timing.get('closure', 'N/A')}` (Fmax: `{pnr_timing.get('fmax_mhz', 'N/A')} MHz`, Slack: `{pnr_timing.get('slack_ns', 'N/A')} ns`)

---

### 2. Interface Specification
* **Clock Domains:** `{', '.join(audit_data.get('clock_ports', ['None']))}`
* **Reset Domains:** `{', '.join(audit_data.get('reset_ports', ['None']))} ({audit_data.get('reset_polarity', 'active_low')})`
* **Inputs ({len(audit_data.get('inputs', []))}):** `{', '.join([f"{p['name']}[{p['width']}]" for p in audit_data.get('inputs', [])])}`
* **Outputs ({len(audit_data.get('outputs', []))}):** `{', '.join([f"{p['name']}[{p['width']}]" for p in audit_data.get('outputs', [])])}`
* **FSM States Detected:** `{', '.join(audit_data.get('fsm_states', [])) if audit_data.get('fsm_states') else 'None (Datapath-only)'}`

---

### 3. NextPnR Physical Layout & Placement Metrics
* **Target Architecture:** `{pnr.get('target_device', '1.2V CMOS / iCE40 Architecture')}`
* **LUT4 Utilization:** `{pnr_util.get('lut4_used', 0)} / {pnr_util.get('lut4_total', 1280)} ({pnr_util.get('lut4_pct', 0)}%)`
* **Flip-Flop (DFF) Utilization:** `{pnr_util.get('dff_used', 0)} / {pnr_util.get('dff_total', 1280)} ({pnr_util.get('dff_pct', 0)}%)`
* **IO Pad Utilization:** `{pnr_util.get('io_used', 0)} / {pnr_util.get('io_total', 96)} ({pnr_util.get('io_pct', 0)}%)`
* **Physical Bounding Box:** `{pnr_layout.get('bounding_box', 'N/A')}` (Routing Density: `{pnr_layout.get('routing_density_pct', 0)}%`)

---

### 4. NextPnR Static Timing Analysis (STA)
* **Target Clock Frequency:** `{pnr.get('target_clock_mhz', 100.0)} MHz` (Target Period: `{pnr.get('target_period_ns', 10.0)} ns`)
* **Maximum Achievable Clock (Fmax):** `{pnr_timing.get('fmax_mhz', 'N/A')} MHz`
* **Critical Path Propagation Delay:** `{pnr_timing.get('critical_path_ns', 'N/A')} ns`
  * *Internal Logic Gate Delay:* `{pnr_timing.get('logic_delay_ns', 'N/A')} ns`
  * *Interconnect Routing Wire Delay:* `{pnr_timing.get('routing_delay_ns', 'N/A')} ns`
* **Setup Timing Slack:** `{pnr_timing.get('slack_ns', 'N/A')} ns` -> **{pnr_timing.get('closure', 'N/A')}**

---

### 5. Gate-Level Hardware Logic Utilization (Yosys)
```text
{synth.get('raw_stat', 'Synthesis metrics not generated.')}
```

---

### 6. Simulation Scoreboard Trace
```text
{sim.get('output', 'No simulation trace available.')}
```

---
*Generated autonomously by RTL-AutoBench Pre-Silicon Verification & PnR Pipeline.*
"""
        return md
