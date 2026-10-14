#!/usr/bin/env python3
"""Regresión mínima antes de publicar / soltar versión (B22)."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(label: str, cmd: list[str]) -> dict:
    print(f"→ {label} …", flush=True)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    ok = r.returncode == 0
    print(f"  [{'OK' if ok else 'FALLA'}] {label}", flush=True)
    return {
        "label": label,
        "ok": ok,
        "exit": r.returncode,
        "tail": (r.stdout + r.stderr)[-500:],
    }


def main() -> int:
    checks = [
        ("validador_self_test", [sys.executable, "scripts/validate_workflow.py", "--self-test"]),
        ("integridad_b17", [sys.executable, "scripts/run_integridad.py"]),
        ("evaluar_determinista_b18", [sys.executable, "scripts/evaluar_determinista.py"]),
        ("integracion_b20", [sys.executable, "scripts/run_integracion_b20.py"]),
        ("build_dist", [sys.executable, "scripts/install_metodo.py", "build-dist"]),
        ("recorrido_simple", [sys.executable, "scripts/product_flow.py", "recorrido-simple"]),
    ]
    results = [run(label, cmd) for label, cmd in checks]
    passed = sum(1 for r in results if r["ok"])
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    informe = {
        "bateria": "regresion-B22",
        "version": version,
        "ts": now_iso(),
        "passed": passed,
        "total": len(results),
        "veredicto": "ok" if passed == len(results) else "falla",
        "casos": results,
    }
    out = ROOT / "tests" / "scenarios" / "regresion" / "ultimo-informe.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n=== Regresión {version}: {passed}/{len(results)} → {informe['veredicto']} ===")
    print(f"Informe: {out}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
