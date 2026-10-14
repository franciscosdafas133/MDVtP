#!/usr/bin/env python3
"""Regresión de los fallos que encontró el probador (informe 2026-10-14)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLOW = ROOT / "scripts" / "product_flow.py"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(FLOW), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    fails = 0
    with tempfile.TemporaryDirectory(prefix="hallazgos-") as tmp:
        p = Path(tmp)
        if run(["iniciar", "--proyecto", str(p), "--idea", "sonda hallazgos", "--fuerza"]).returncode != 0:
            print("FALLA iniciar")
            return 1
        if run(["requisito", "--proyecto", str(p), "--titulo", "Nota", "--texto", "Se guarda"]).returncode != 0:
            print("FALLA requisito")
            return 1
        if (
            run(
                [
                    "tarea",
                    "--proyecto",
                    str(p),
                    "--titulo",
                    "Guardar nota",
                    "--comprobacion",
                    "python imprime ok",
                    "--enlaces",
                    "REQ-01",
                ]
            ).returncode
            != 0
        ):
            print("FALLA tarea")
            return 1

        mentira = run(
            [
                "evidenciar",
                "--proyecto",
                str(p),
                "--tarea",
                "TASK-02",
                "--origen",
                "comando",
                "--valor",
                "echo esto no se ejecuta",
            ]
        )
        if mentira.returncode == 0:
            print("FALLA: aceptó evidencia de comando sin --ejecutar")
            fails += 1
        else:
            print("OK no ejecuta texto suelto")

        rojo = run(
            [
                "evidenciar",
                "--proyecto",
                str(p),
                "--tarea",
                "TASK-02",
                "--origen",
                "comando",
                "--valor",
                "python3 -c 'import sys; sys.exit(1)'",
                "--ejecutar",
            ]
        )
        if rojo.returncode == 0:
            print("FALLA: prueba en rojo quedó como éxito")
            fails += 1
        else:
            print("OK prueba en rojo no es vigente")

        if run(["presentar", "--proyecto", str(p), "--tarea", "TASK-02"]).returncode != 0:
            print("FALLA presentar")
            fails += 1
        ver = run(["verificar", "--proyecto", str(p), "--tarea", "TASK-02"])
        if ver.returncode == 0:
            print("FALLA: verificó con la prueba en rojo")
            fails += 1
        else:
            print("OK no verifica en rojo")

        ok = run(
            [
                "evidenciar",
                "--proyecto",
                str(p),
                "--tarea",
                "TASK-02",
                "--origen",
                "comando",
                "--valor",
                "python3 -c 'print(1)'",
                "--ejecutar",
            ]
        )
        if ok.returncode != 0 or run(["verificar", "--proyecto", str(p), "--tarea", "TASK-02"]).returncode != 0:
            print("FALLA: la prueba en verde no verificó")
            print(ok.stdout, ok.stderr)
            fails += 1
        else:
            print("OK verifica solo con exit 0")

        estado = json.loads((p / "workflow" / "estado.json").read_text(encoding="utf-8"))
        if estado["tareas"]["TASK-02"]["estado"] != "verificada":
            print("FALLA estado final", estado["tareas"]["TASK-02"]["estado"])
            fails += 1

    print("HALLAZGOS", "OK" if fails == 0 else f"FALLA {fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
