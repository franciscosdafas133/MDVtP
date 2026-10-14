#!/usr/bin/env python3
"""B20: incremento con componentes que interactúan + cambio de requisito (R07/R11/R18).

1) Contador + informe (el informe lee al contador).
2) Prueba de integración real.
3) Se cambia un requisito → impactar → tareas/evidencia invalidan.
4) Se adapta el código y se vuelve a verificar.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLOW = ROOT / "scripts" / "product_flow.py"
VALIDATE = ROOT / "scripts" / "validate_workflow.py"
DEMO = ROOT / "tests" / "fixtures" / "demo-integracion"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True, check=False)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_task(wf: Path, tid: str, titulo: str, enlaces: list[str], comprobacion: str) -> None:
    estado = load(wf / "estado.json")
    rel = load(wf / "relaciones.json")
    rel["nodos"][tid] = {"tipo": "TASK"}
    estado["tareas"][tid] = {
        "id": tid,
        "titulo": titulo,
        "estado": "en_curso",
        "depende_de": [],
        "enlaces": enlaces,
        "evidencia": [],
        "comprobacion": comprobacion,
        "bloqueo": None,
    }
    estado["actualizado"] = now_iso()
    save(wf / "estado.json", estado)
    save(wf / "relaciones.json", rel)
    with (wf / "eventos.jsonl").open("a", encoding="utf-8") as f:
        for de, a in [("pendiente", "preparada"), ("preparada", "en_curso")]:
            f.write(
                json.dumps(
                    {
                        "ts": now_iso(),
                        "tipo": "tarea.transicion",
                        "actor": "agente",
                        "sujeto": tid,
                        "de": de,
                        "a": a,
                        "detalle": {"accion": "b20"},
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


def write_app_v1(app: Path) -> None:
    app.mkdir(parents=True, exist_ok=True)
    (app / "contador.py").write_text(
        "#!/usr/bin/env python3\n"
        "from pathlib import Path\n"
        "STATE = Path(__file__).with_name('visitas.txt')\n"
        "\n"
        "def leer() -> int:\n"
        "    if not STATE.is_file():\n"
        "        return 0\n"
        "    return int(STATE.read_text(encoding='utf-8').strip() or '0')\n"
        "\n"
        "def main() -> None:\n"
        "    n = leer() + 1\n"
        "    STATE.write_text(str(n), encoding='utf-8')\n"
        "    print(f'visitas: {n}')\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n",
        encoding="utf-8",
    )
    (app / "informe.py").write_text(
        "#!/usr/bin/env python3\n"
        "\"\"\"Componente 2: lee el estado del contador.\"\"\"\n"
        "from pathlib import Path\n"
        "import contador\n"
        "\n"
        "def resumen() -> str:\n"
        "    n = contador.leer()\n"
        "    return f'resumen visitas={n}'\n"
        "\n"
        "def main() -> None:\n"
        "    print(resumen())\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n",
        encoding="utf-8",
    )
    (app / "comprobar_integracion.sh").write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "cd \"$(dirname \"$0\")\"\n"
        "rm -f visitas.txt\n"
        "python3 contador.py >/dev/null\n"
        "python3 contador.py >/dev/null\n"
        "out=$(python3 informe.py)\n"
        "test \"$out\" = \"resumen visitas=2\"\n"
        "echo OK_INTEGRACION\n",
        encoding="utf-8",
    )
    (app / "comprobar_integracion.sh").chmod(0o755)


def write_app_v2(app: Path) -> None:
    """Requisito cambiado: el resumen debe incluir la palabra 'total'."""
    (app / "informe.py").write_text(
        "#!/usr/bin/env python3\n"
        "\"\"\"Componente 2 v2: formato exigido por REQ-01 actualizado.\"\"\"\n"
        "from pathlib import Path\n"
        "import contador\n"
        "\n"
        "def resumen() -> str:\n"
        "    n = contador.leer()\n"
        "    return f'resumen total={n}'\n"
        "\n"
        "def main() -> None:\n"
        "    print(resumen())\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n",
        encoding="utf-8",
    )
    (app / "comprobar_integracion.sh").write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "cd \"$(dirname \"$0\")\"\n"
        "rm -f visitas.txt\n"
        "python3 contador.py >/dev/null\n"
        "python3 contador.py >/dev/null\n"
        "out=$(python3 informe.py)\n"
        "test \"$out\" = \"resumen total=2\"\n"
        "echo OK_INTEGRACION\n",
        encoding="utf-8",
    )
    (app / "comprobar_integracion.sh").chmod(0o755)


def main() -> int:
    if DEMO.exists():
        shutil.rmtree(DEMO)
    DEMO.mkdir(parents=True)
    pasos: list[str] = []

    print("=== B20: iniciar ===\n")
    r = run(
        [
            sys.executable,
            str(FLOW),
            "iniciar",
            "--proyecto",
            str(DEMO),
            "--idea",
            "Contador + informe CLI (dos componentes que se hablan)",
            "--fuerza",
        ]
    )
    if r.returncode != 0:
        print(r.stderr)
        return 1
    pasos.append("iniciar")
    wf = DEMO / "workflow"
    app = DEMO / "app"

    # REQ-01 en relaciones + doc
    rel = load(wf / "relaciones.json")
    rel["nodos"]["REQ-01"] = {"tipo": "REQ", "archivo": "requisitos.md"}
    save(wf / "relaciones.json", rel)
    (wf / "requisitos.md").write_text(
        "# Requisitos\n\n"
        "## REQ-01\n\n"
        "El informe debe mostrar `resumen visitas=N` leyendo el contador (integración).\n",
        encoding="utf-8",
    )
    pasos.append("registrar REQ-01")

    print("\n=== B20: componentes v1 + prueba integración ===\n")
    write_app_v1(app)
    r = run(["bash", str(app / "comprobar_integracion.sh")], cwd=app)
    if r.returncode != 0:
        print("FALLA integración v1", r.stdout, r.stderr)
        return 1
    print(r.stdout.strip())
    pasos.append("prueba integración v1 OK")

    add_task(
        wf,
        "TASK-20",
        "Contador CLI",
        ["OBJ-01", "REQ-01"],
        "contador incrementa visitas.txt",
    )
    add_task(
        wf,
        "TASK-21",
        "Informe que lee el contador",
        ["OBJ-01", "REQ-01"],
        "comprobar_integracion.sh → OK_INTEGRACION",
    )

    cmd = f"bash {app / 'comprobar_integracion.sh'}"
    for tid in ("TASK-20", "TASK-21"):
        if (
            run(
                [
                    sys.executable,
                    str(FLOW),
                    "evidenciar",
                    "--proyecto",
                    str(DEMO),
                    "--tarea",
                    tid,
                    "--origen",
                    "comando",
                    "--valor",
                    cmd,
                    "--cubre",
                    "app/contador.py,app/informe.py",
                ]
            ).returncode
            != 0
        ):
            return 1
        if (
            run(
                [
                    sys.executable,
                    str(FLOW),
                    "presentar",
                    "--proyecto",
                    str(DEMO),
                    "--tarea",
                    tid,
                ]
            ).returncode
            != 0
        ):
            return 1
        if (
            run(
                [
                    sys.executable,
                    str(FLOW),
                    "verificar",
                    "--proyecto",
                    str(DEMO),
                    "--tarea",
                    tid,
                ]
            ).returncode
            != 0
        ):
            return 1
    pasos.append("TASK-20 y TASK-21 verificadas")

    print("\n=== B20: cambiar requisito + impactar ===\n")
    (wf / "requisitos.md").write_text(
        "# Requisitos\n\n"
        "## REQ-01\n\n"
        "El informe debe mostrar `resumen total=N` (cambio: visitas= → total=).\n",
        encoding="utf-8",
    )
    r = run(
        [
            sys.executable,
            str(FLOW),
            "impactar",
            "--proyecto",
            str(DEMO),
            "--cambiado",
            "REQ-01",
            "--motivo",
            "Formato del informe: visitas= pasa a total=",
        ]
    )
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
        return 1
    pasos.append("impactar REQ-01")

    estado = load(wf / "estado.json")
    evid = load(wf / "evidencias.json")
    t20 = estado["tareas"]["TASK-20"]["estado"]
    t21 = estado["tareas"]["TASK-21"]["estado"]
    stale = [
        eid
        for eid, e in (evid.get("items") or {}).items()
        if e.get("estado") == "stale"
    ]
    if t20 != "en_revision" or t21 != "en_revision" or not stale:
        print(
            f"FALLA invalidación: TASK-20={t20} TASK-21={t21} stale={stale}",
            file=sys.stderr,
        )
        return 1
    print(f"Invalidación OK: tareas en_revision, evidencias stale={stale}")
    pasos.append("tareas invalidas + evidencia stale")

    print("\n=== B20: adaptar código v2 + re-verificar ===\n")
    write_app_v2(app)
    r = run(["bash", str(app / "comprobar_integracion.sh")], cwd=app)
    if r.returncode != 0:
        print("FALLA integración v2", r.stdout, r.stderr)
        return 1
    print(r.stdout.strip())
    pasos.append("prueba integración v2 OK")

    # Nuevas evidencias (las viejas están stale)
    for tid in ("TASK-20", "TASK-21"):
        # volver a en_curso desde en_revision vía presentar? presentar solo desde preparada/en_curso
        # verificar exige en_revision — ya están en_revision tras impactar
        estado = load(wf / "estado.json")
        # evidenciar añade EVID nueva; verificar necesita en_revision
        if (
            run(
                [
                    sys.executable,
                    str(FLOW),
                    "evidenciar",
                    "--proyecto",
                    str(DEMO),
                    "--tarea",
                    tid,
                    "--origen",
                    "comando",
                    "--valor",
                    cmd + " #v2",
                    "--cubre",
                    "app/contador.py,app/informe.py",
                ]
            ).returncode
            != 0
        ):
            return 1
        if (
            run(
                [
                    sys.executable,
                    str(FLOW),
                    "verificar",
                    "--proyecto",
                    str(DEMO),
                    "--tarea",
                    tid,
                ]
            ).returncode
            != 0
        ):
            print("verificar falló", tid, file=sys.stderr)
            return 1

    if (
        run(
            [
                sys.executable,
                str(FLOW),
                "operar",
                "--proyecto",
                str(DEMO),
                "--resumen",
                "Contador+informe v2 tras cambio REQ-01",
                "--pendientes",
                "Sin UI web; sin usuarios reales",
            ]
        ).returncode
        != 0
    ):
        return 1

    r = run([sys.executable, str(VALIDATE), str(wf)])
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        return 1
    pasos.append("re-verificar + operar + validador OK")

    estado = load(wf / "estado.json")
    ok = (
        estado["tareas"]["TASK-20"]["estado"] == "verificada"
        and estado["tareas"]["TASK-21"]["estado"] == "verificada"
        and bool(estado.get("operacion"))
    )
    informe = {
        "bateria": "B20-integracion",
        "ts": now_iso(),
        "veredicto": "ok" if ok else "falla",
        "pasos": pasos,
        "proyecto": str(DEMO),
        "tareas_final": {
            "TASK-20": estado["tareas"]["TASK-20"]["estado"],
            "TASK-21": estado["tareas"]["TASK-21"]["estado"],
        },
        "nota": (
            "Dos componentes interactúan; cambio de REQ-01 invalidó y se recuperó el flujo."
        ),
    }
    out = ROOT / "tests" / "scenarios" / "integracion" / "ultimo-informe.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    save(out, informe)
    print(f"\n=== B20: {informe['veredicto']} ===")
    print(f"Informe: {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
