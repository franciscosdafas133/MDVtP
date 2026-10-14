#!/usr/bin/env python3
"""Evalúa la parte determinista del catálogo E01–E18 (semilla B18).

No sustituye observación en Cursor/Claude (B19). No autoaprueba agentes.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLOW = ROOT / "scripts" / "product_flow.py"
VALIDATE = ROOT / "scripts" / "validate_workflow.py"
INSTALL = ROOT / "scripts" / "install_metodo.py"
INTEGRIDAD = ROOT / "scripts" / "run_integridad.py"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)


def main() -> int:
    # Reutiliza batería B17 + demos clave
    checks: list[tuple[str, list[str], int, str]] = [
        ("E08", [sys.executable, str(FLOW), "demo-b13"], 0, "verificar sin evidencia falla; depurar×3"),
        ("E05", [sys.executable, str(FLOW), "demo-b12"], 0, "dividir + bloqueo parcial"),
        ("E11", [sys.executable, str(FLOW), "demo-b11"], 0, "checkpoint + worktree"),
        ("E14", [sys.executable, str(INSTALL), "demo"], 0, "instalación smoke"),
        ("E15", [sys.executable, str(VALIDATE), "--self-test"], 0, "fixture sano + defectos conocidos"),
        ("E17", [sys.executable, str(FLOW), "recorrido-simple"], 0, "producto mínimo cableado"),
        ("E12", [sys.executable, str(INTEGRIDAD)], 0, "batería integridad completa"),
    ]
    resultados = []
    for eid, cmd, expect, nota in checks:
        print(f"→ {eid} …", flush=True)
        r = run(cmd)
        ok = r.returncode == expect
        resultados.append(
            {
                "id": eid,
                "ok": ok,
                "exit": r.returncode,
                "esperado_exit": expect,
                "nota": nota,
                "tail": (r.stdout + r.stderr)[-400:],
            }
        )
        print(f"  [{'OK' if ok else 'FALLA'}] {eid}", flush=True)

    # Escenarios solo observación: quedan pendientes (no inventar OK)
    solo_obs = ["E01", "E02", "E03", "E09", "E13", "E16", "E18"]
    for eid in solo_obs:
        resultados.append(
            {
                "id": eid,
                "ok": None,
                "exit": None,
                "esperado_exit": None,
                "nota": "observación de agente — pendiente B18/B19 (no autojuzgar)",
                "tail": "",
            }
        )

    det = [r for r in resultados if r["ok"] is not None]
    passed = sum(1 for r in det if r["ok"])
    informe = {
        "bateria": "B18-determinista",
        "ts": now_iso(),
        "deterministas_ok": passed,
        "deterministas_total": len(det),
        "observacion_pendiente": solo_obs,
        "veredicto_determinista": "ok" if passed == len(det) else "falla",
        "veredicto_agente": "pendiente",
        "casos": resultados,
        "regla": "El mismo agente no se autoaprueba. Hosts reales = B19.",
    }
    out = ROOT / "tests" / "scenarios" / "evaluacion" / "ultimo-informe.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"\n=== B18 determinista: {passed}/{len(det)} → {informe['veredicto_determinista']} ==="
    )
    print(f"Observación agente: pendiente ({', '.join(solo_obs)})")
    print(f"Informe: {out}")
    return 0 if passed == len(det) else 1


if __name__ == "__main__":
    sys.exit(main())
