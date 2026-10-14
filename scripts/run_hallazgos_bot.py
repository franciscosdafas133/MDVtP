#!/usr/bin/env python3
"""Regresión de los fallos que encontró el probador (informes e2e dueños 2026-10-14)."""

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

        # --- Evidencia comando / verificar ---
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
                    "bash test_nota.sh",
                    "--enlaces",
                    "REQ-01",
                ]
            ).returncode
            != 0
        ):
            print("FALLA tarea")
            return 1
        (p / "test_nota.sh").write_text(
            "#!/bin/bash\npython3 -c 'print(1)'\n", encoding="utf-8"
        )
        (p / "test_nota.sh").chmod(0o755)
        (p / "test_nota_fail.sh").write_text(
            "#!/bin/bash\nexit 1\n", encoding="utf-8"
        )
        (p / "test_nota_fail.sh").chmod(0o755)

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
                "bash test_nota_fail.sh",
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
                "bash test_nota.sh",
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

        # --- No cerrar con true / manual (sonda e2e-v2) ---
        run(
            [
                "tarea",
                "--proyecto",
                str(p),
                "--titulo",
                "Otra pieza",
                "--comprobacion",
                "bash test_nota.sh",
            ]
        )
        triv = run(
            [
                "evidenciar",
                "--proyecto",
                str(p),
                "--tarea",
                "TASK-03",
                "--origen",
                "comando",
                "--valor",
                "true",
                "--ejecutar",
            ]
        )
        if triv.returncode == 0:
            print("FALLA: aceptó evidenciar true")
            fails += 1
        else:
            print("OK rechaza comando trivial true")
        passc = run(
            [
                "evidenciar",
                "--proyecto",
                str(p),
                "--tarea",
                "TASK-03",
                "--origen",
                "comando",
                "--valor",
                'python3 -c "pass"',
                "--ejecutar",
            ]
        )
        if passc.returncode == 0:
            print("FALLA: aceptó python3 -c pass")
            fails += 1
        else:
            print("OK rechaza python3 -c pass / no alineado a comprobacion")
        man = run(
            [
                "evidenciar",
                "--proyecto",
                str(p),
                "--tarea",
                "TASK-03",
                "--origen",
                "manual",
                "--valor",
                "lo probé, va bien",
            ]
        )
        if man.returncode == 0:
            print("FALLA: aceptó origen manual con comprobacion")
            fails += 1
        else:
            print("OK rechaza manual si hay comprobacion")

        # --- Modo rápido + pistas de negocio (formular) ---
        p2 = p / "rapido"
        p2.mkdir()
        ini = run(
            [
                "iniciar",
                "--proyecto",
                str(p2),
                "--idea",
                "Consultorio médico con recepción y nota clínica",
                "--fuerza",
                "--modo",
                "rapido",
            ]
        )
        if ini.returncode != 0:
            print("FALLA iniciar --modo rapido")
            fails += 1
        else:
            est2 = json.loads((p2 / "workflow" / "estado.json").read_text(encoding="utf-8"))
            asks = est2.get("asks_activas") or []
            if not all(x in asks for x in ("ASK-01", "ASK-06", "ASK-02")):
                print("FALLA modo rapido sin ASK base", asks)
                fails += 1
            elif not any(a.startswith("ASK-1") for a in asks):
                print("FALLA pistas sin id ASK-1x", asks)
                fails += 1
            else:
                print("OK modo rapido = ASK base + pistas con id")
            desc = (p2 / "workflow" / "descubrimiento.md").read_text(encoding="utf-8")
            if "ASK-10" not in desc or "sensib" not in desc.lower():
                print("FALLA sin ASK-10 de privacidad en consultorio")
                fails += 1
            else:
                print("OK pistas de consultorio anotables")
            if "staging" in desc.lower() or "colas" in desc.lower():
                print("FALLA jerga staging/colas en descubrimiento")
                fails += 1
            else:
                print("OK lenguaje llano en descubrimiento")

        # --- continuar no insiste ASK ya respondidas ---
        for aid in asks:
            run(
                [
                    "anotar",
                    "--proyecto",
                    str(p2),
                    "--enlaza",
                    aid,
                    "--texto",
                    "respuesta dueño",
                    "--resuelto",
                ]
            )
        cont = run(["continuar", "--proyecto", str(p2)])
        if "faltan respuestas" in (cont.stdout or "").lower():
            print("FALLA continuar insiste ASK ya respondidas")
            fails += 1
        elif "ya tienen respuesta" not in (cont.stdout or "") and "requisito" not in (
            cont.stdout or ""
        ).lower():
            print("FALLA continuar no propone requisito tras ASK")
            print(cont.stdout[-500:])
            fails += 1
        else:
            print("OK continuar tras ASK respondidas")

        # --- Anti-simulación desbloquear / verificar (restaurante) ---
        p3 = p / "tarjeta"
        p3.mkdir()
        run(["iniciar", "--proyecto", str(p3), "--idea", "Restaurante comanda y caja", "--fuerza"])
        run(
            [
                "tarea",
                "--proyecto",
                str(p3),
                "--titulo",
                "Cobro con tarjeta",
                "--comprobacion",
                "pago real aceptado",
            ]
        )
        # TASK-02 es la de cobro (TASK-01 es descubrimiento)
        bl = run(
            [
                "bloquear",
                "--proyecto",
                str(p3),
                "--tarea",
                "TASK-02",
                "--motivo",
                "Sin pasarela de tarjeta",
            ]
        )
        if bl.returncode != 0:
            print("FALLA bloquear tarjeta")
            fails += 1
        est3 = json.loads((p3 / "workflow" / "estado.json").read_text(encoding="utf-8"))
        if est3["tareas"]["TASK-02"].get("marca") != "MANUAL_VERIFY_REQUIRED":
            print("FALLA bloqueo tarjeta sin marca MANUAL_VERIFY", est3["tareas"]["TASK-02"])
            fails += 1
        else:
            print("OK bloqueo tarjeta → MANUAL_VERIFY_REQUIRED")

        des = run(
            [
                "desbloquear",
                "--proyecto",
                str(p3),
                "--tarea",
                "TASK-02",
                "--evidencia",
                "Simulación de cobro OK en demo",
            ]
        )
        if des.returncode == 0:
            print("FALLA: desbloqueó cobro con simulación")
            fails += 1
        else:
            print("OK no desbloquea cobro simulado")

        # --- impactar DEC invalida TASK verificada ---
        p4 = p / "dec"
        p4.mkdir()
        run(["iniciar", "--proyecto", str(p4), "--idea", "Peluquería reservas", "--fuerza"])
        run(
            [
                "requisito",
                "--proyecto",
                str(p4),
                "--titulo",
                "Confirmación",
                "--texto",
                "Cliente confirma por WhatsApp",
            ]
        )
        run(
            [
                "tarea",
                "--proyecto",
                str(p4),
                "--titulo",
                "Enviar confirmación",
                "--comprobacion",
                "mensaje enviado",
                "--enlaces",
                "REQ-01",
            ]
        )
        run(
            [
                "decidir",
                "--proyecto",
                str(p4),
                "--titulo",
                "Canal de confirmación",
                "--motivo",
                "WhatsApp",
                "--enlaces",
                "REQ-01",
                "--aceptar",
                "--aprobado-por",
                "dueña",
            ]
        )
        # Verificación rápida de TASK-02
        run(
            [
                "evidenciar",
                "--proyecto",
                str(p4),
                "--tarea",
                "TASK-02",
                "--origen",
                "comando",
                "--valor",
                "python3 -c 'print(ok)'",
                "--ejecutar",
            ]
        )
        run(["presentar", "--proyecto", str(p4), "--tarea", "TASK-02"])
        run(["verificar", "--proyecto", str(p4), "--tarea", "TASK-02"])
        # Encontrar DEC-01
        decs = list((p4 / "workflow" / "decisiones").glob("DEC-*.json"))
        if not decs:
            print("FALLA no hay DEC para impactar")
            fails += 1
        else:
            did = decs[0].stem
            imp = run(
                [
                    "impactar",
                    "--proyecto",
                    str(p4),
                    "--cambiado",
                    did,
                    "--motivo",
                    "Ahora confirma por SMS",
                ]
            )
            est4b = json.loads((p4 / "workflow" / "estado.json").read_text(encoding="utf-8"))
            if est4b["tareas"]["TASK-02"]["estado"] != "en_revision":
                print(
                    "FALLA impactar DEC no invalidó TASK",
                    est4b["tareas"]["TASK-02"]["estado"],
                    imp.stdout,
                    imp.stderr,
                )
                fails += 1
            else:
                print("OK impactar DEC → TASK en_revision")

    print("HALLAZGOS", "OK" if fails == 0 else f"FALLA {fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
