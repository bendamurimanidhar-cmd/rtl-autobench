"""
AST & Interface Parser for Verilog/SystemVerilog Hardware Modules.
Extracts module declaration, ports, widths, parameters, clocks, resets, and FSM states.
"""

import re
from typing import Dict, List, Any

class VerilogModuleParser:
    def __init__(self, verilog_code: str):
        self.code = self._strip_comments(verilog_code)
        self.parameters: Dict[str, int] = {}

    def _strip_comments(self, text: str) -> str:
        text = re.sub(r'//.*', '', text)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return text

    def _eval_expr(self, expr_str: str) -> int:
        expr = expr_str.strip()
        if not expr:
            return 0
        for param_name, param_val in self.parameters.items():
            expr = re.sub(rf'\b{param_name}\b', str(param_val), expr)
        # Safe mathematical evaluation for simple expressions (e.g. 8-1, 1<<4)
        if re.match(r'^[0-9\s\+\-\*\/\(\)\<\>]+$', expr):
            try:
                return int(eval(expr, {"__builtins__": None}, {}))
            except Exception:
                pass
        m = re.search(r'\d+', expr)
        return int(m.group(0)) if m else 0

    def parse(self) -> Dict[str, Any]:
        self.parameters = self._extract_parameters()

        mod_match = re.search(
            r'\bmodule\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:#\s*\((.*?)\))?\s*\((.*?)\)\s*;',
            self.code,
            re.DOTALL
        )
        if not mod_match:
            mod_simple = re.search(r'\bmodule\s+([A-Za-z_][A-Za-z0-9_]*)', self.code)
            mod_name = mod_simple.group(1) if mod_simple else "unknown_module"
            ports_raw = ""
        else:
            mod_name = mod_match.group(1)
            ports_raw = mod_match.group(3)

        ports = self._parse_ports(ports_raw)
        fsm_states = self._detect_fsm_states()
        clock_ports = [p["name"] for p in ports if any(c in p["name"].lower() for c in ["clk", "clock"])]
        reset_ports = [p["name"] for p in ports if any(r in p["name"].lower() for r in ["rst", "reset", "arst"])]

        # Dynamic Reset Polarity Detection
        reset_polarity = "active_low"
        if reset_ports:
            primary_rst = reset_ports[0].lower()
            if (
                any(primary_rst.endswith(suf) for suf in ["_n", "_b", "_l", "n", "low", "bar"])
                or any(primary_rst.startswith(pref) for pref in ["n_", "nreset", "nrst"])
                or any(sub in primary_rst for sub in ["rstn", "resetn", "_n_"])
            ):
                reset_polarity = "active_low"
            else:
                reset_polarity = "active_high"

        return {
            "module_name": mod_name,
            "parameters": self.parameters,
            "ports": ports,
            "inputs": [p for p in ports if p["direction"] == "input"],
            "outputs": [p for p in ports if p["direction"] == "output"],
            "clock_ports": clock_ports,
            "reset_ports": reset_ports,
            "reset_polarity": reset_polarity,
            "fsm_states": fsm_states
        }

    def _extract_parameters(self) -> Dict[str, int]:
        params = {}
        # 1. Parameter list in module #( ... )
        param_blocks = re.findall(r'#\s*\((.*?)\)', self.code, re.DOTALL)
        for block in param_blocks:
            for item in block.split(","):
                m = re.search(r'(?:parameter\s+)?(?:int\s+|integer\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z0-9_\-\+\*\/\s]+)', item)
                if m:
                    name, val_str = m.group(1).strip(), m.group(2).strip()
                    try:
                        params[name] = int(eval(val_str, {"__builtins__": None}, {}))
                    except Exception:
                        pass

        # 2. Body parameters / localparams
        body_params = re.findall(r'\b(?:parameter|localparam)\s+(?:int\s+|integer\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z0-9_\-\+\*\/\s]+);', self.code)
        for name, val_str in body_params:
            try:
                params[name.strip()] = int(eval(val_str.strip(), {"__builtins__": None}, {}))
            except Exception:
                pass

        return params

    def _parse_ports(self, ports_raw: str) -> List[Dict[str, Any]]:
        ports = []
        range_pat = r'\[\s*([A-Za-z0-9_\-\+\*\/\s]+)\s*:\s*([A-Za-z0-9_\-\+\*\/\s]+)\s*\]'

        if not ports_raw:
            body_ports = re.findall(
                rf'\b(input|output|inout)\s+(?:(?:wire|reg|logic)\s+)?(?:(?:signed|unsigned)\s+)?(?:{range_pat})?\s*([A-Za-z_][A-Za-z0-9_,\s]*)',
                self.code
            )
            for direction, msb_expr, lsb_expr, names in body_ports:
                if msb_expr and lsb_expr:
                    msb = self._eval_expr(msb_expr)
                    lsb = self._eval_expr(lsb_expr)
                    width = abs(msb - lsb) + 1
                else:
                    width = 1
                for n in names.split(","):
                    clean_name = n.strip().split(";")[0].strip()
                    if clean_name and clean_name not in ["wire", "reg", "logic"]:
                        ports.append({"name": clean_name, "direction": direction, "width": width})
            return ports

        tokens = [t.strip() for t in ports_raw.split(",") if t.strip()]
        last_dir = "input"
        last_width = 1
        for t in tokens:
            m = re.search(
                rf'\b(input|output|inout)\s+(?:(?:wire|reg|logic)\s+)?(?:(?:signed|unsigned)\s+)?(?:{range_pat})?\s*([A-Za-z_][A-Za-z0-9_]*)',
                t
            )
            if m:
                last_dir = m.group(1)
                msb_expr, lsb_expr = m.group(2), m.group(3)
                name = m.group(4)
                if msb_expr and lsb_expr:
                    msb = self._eval_expr(msb_expr)
                    lsb = self._eval_expr(lsb_expr)
                    width = abs(msb - lsb) + 1
                else:
                    width = 1
                last_width = width
                ports.append({"name": name, "direction": last_dir, "width": width})
            else:
                m_short = re.search(rf'(?:(?:wire|reg|logic)\s+)?(?:(?:signed|unsigned)\s+)?(?:{range_pat})?\s*([A-Za-z_][A-Za-z0-9_]*)', t)
                if m_short:
                    msb_expr, lsb_expr = m_short.group(1), m_short.group(2)
                    name = m_short.group(3)
                    if msb_expr and lsb_expr:
                        msb = self._eval_expr(msb_expr)
                        lsb = self._eval_expr(lsb_expr)
                        width = abs(msb - lsb) + 1
                    else:
                        width = last_width  # `input [7:0] a, b` -> b is 8 bits too
                    ports.append({"name": name, "direction": last_dir, "width": width})
        return ports

    def _detect_fsm_states(self) -> List[str]:
        states = set()
        params = re.findall(r'\b(?:parameter|localparam)\s+(?:\[\d+:\d+\]\s+)?([A-Za-z0-9_]+)\s*=\s*\d+', self.code)
        for p in params:
            if any(s in p.lower() for s in ["state", "s_", "idle", "read", "write", "done", "wait", "init"]):
                states.add(p)
        enums = re.findall(r'typedef\s+enum\s+(?:logic\s+(?:\[.*?\]\s+)?)?\{(.*?)\}', self.code, re.DOTALL)
        for e in enums:
            for item in e.split(","):
                clean = item.strip().split("=")[0].strip()
                if clean:
                    states.add(clean)
        return sorted(list(states))
