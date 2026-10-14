#!/usr/bin/env python3
"""Batería B17: integridad, interrupciones y recuperación (determinista).

Salida: código 0 solo si todos los casos esperados pasan.
Informe JSON en tests/scenarios/integridad/ultimo-informe.json
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "scripts" / "validate_workflow.py"
FLOW = ROOT / "scripts" / "product_flow.py"
INSTALL = ROOT / "scripts" / "install_metodo.py"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def case(nombre: str, ok: bool, detalle: str, esperado: str) -> dict:
    return {
        "caso": nombre,
        "ok": ok,
        "esperado": esperado,
        "detalle": detalle.strip()[:500],
    }


def test_self_fixtures() -> dict:
    r = run([sys.executable, str(VALIDATE), "--self-test"])
    ok = r.returncode == 0
    return case(
        "fixtures_validador",
        ok,
        r.stdout + r.stderr,
        "workflow-ok pasa; ref-rota/transicion/stale/conflicto fallan con código esperado",
    )


def test_estado_invalido() -> dict:
    with tempfile.TemporaryDirectory(prefix="b17-estado-") as tmp:
        wf = Path(tmp) / "workflow"
        wf.mkdir()
        (wf / "relaciones.json").write_text(
            '{"contrato_version":"0.1.0","nodos":{},"aristas":[]}\n',
            encoding="utf-8",
        )
        (wf / "evidencias.json").write_text(
            '{"contrato_version":"0.1.0","items":{}}\n',
            encoding="utf-8",
        )
        # Falta campos requeridos
        (wf / "estado.json").write_text('{"contrato_version":"0.1.0"}\n', encoding="utf-8")
        r = run([sys.executable, str(VALIDATE), str(wf)])
        ok = r.returncode == 1 and "esquema" in (r.stdout + r.stderr)
        return case(
            "estado_invalido",
            ok,
            r.stdout + r.stderr,
            "validador exit=1 y código esquema",
        )


def test_escritura_interrumpida() -> dict:
    with tempfile.TemporaryDirectory(prefix="b17-tmp-") as tmp:
        wf = Path(tmp) / "workflow"
        # Base mínima válida luego corromper
        r0 = run(
            [
                sys.executable,
                str(FLOW),
                "iniciar",
                "--proyecto",
                tmp,
                "--idea",
                "b17 interrupcion",
                "--fuerza",
            ]
        )
        if r0.returncode != 0:
            return case("escritura_interrumpida", False, r0.stderr, "iniciar ok luego corromper")
        # Simula corte: estado.json truncado + .tmp huérfano
        estado = wf / "estado.json"
        estado.write_text('{"contrato_version": "0.1.0", "paquete', encoding="utf-8")
        (wf / "estado.json.tmp").write_text('{"parcial": true}\n', encoding="utf-8")
        r = run([sys.executable, str(VALIDATE), str(wf)])
        ok = r.returncode == 1 and (
            "json_invalido" in (r.stdout + r.stderr) or "FALLA" in r.stdout
        )
        return case(
            "escritura_interrumpida",
            ok,
            r.stdout + r.stderr,
            "JSON truncado → validador falla (detecta incoherencia)",
        )


def test_dirty_bloquea_checkpoint_commit() -> dict:
    with tempfile.TemporaryDirectory(prefix="b17-dirty-") as tmp:
        p = Path(tmp)
        run(["git", "init"], cwd=p)
        run(["git", "config", "user.email", "b17@test.local"], cwd=p)
        run(["git", "config", "user.name", "b17"], cwd=p)
        r0 = run(
            [
                sys.executable,
                str(FLOW),
                "iniciar",
                "--proyecto",
                str(p),
                "--idea",
                "b17 dirty",
                "--fuerza",
            ]
        )
        if r0.returncode != 0:
            return case("dirty_checkpoint", False, r0.stderr, "iniciar en repo git")
        # commit inicial limpio
        run(["git", "add", "-A"], cwd=p)
        run(["git", "commit", "-m", "init"], cwd=p)
        # ensuciar
        (p / "sucio.txt").write_text("sin commit\n", encoding="utf-8")
        r = run(
            [
                sys.executable,
                str(FLOW),
                "checkpoint",
                "--proyecto",
                str(p),
                "--nombre",
                "no debe",
                "--alcance",
                "nada",
                "--commit",
            ]
        )
        ok = r.returncode == 2 and "sin commit" in (r.stdout + r.stderr).lower()
        return case(
            "dirty_checkpoint",
            ok,
            r.stdout + r.stderr,
            "checkpoint --commit con dirty → exit 2, no borra ni force-commit",
        )


def test_recuperar_aviso_dirty() -> dict:
    """E11: con dirty, recuperar avisa y no descarta (demo-b11 cubre aislamiento)."""
    r = run([sys.executable, str(FLOW), "demo-b11"])
    ok = r.returncode == 0 and ("OK" in r.stdout or "Worktree" in r.stdout or "ok" in r.stdout.lower())
    # demo-b11 ends with comprobación
    if "→ OK" in r.stdout or "→OK" in r.stdout.replace(" ", ""):
        ok = r.returncode == 0
    else:
        ok = r.returncode == 0 and "FALLA" not in r.stdout.split("Comprobación")[-1]
    return case(
        "recuperacion_aislada",
        ok,
        r.stdout[-800:] + r.stderr,
        "demo-b11: worktree/rama desde CP sin perder trabajo posterior",
    )


def test_install_smoke() -> dict:
    r = run([sys.executable, str(INSTALL), "demo"])
    ok = r.returncode == 0
    return case(
        "instalacion_smoke",
        ok,
        (r.stdout + r.stderr)[-600:],
        "install_metodo.py demo (proyecto + global fake) OK",
    )


def test_recorrido_simple() -> dict:
    r = run([sys.executable, str(FLOW), "recorrido-simple"])
    ok = r.returncode == 0 and "veredicto=ok" in r.stdout
    return case(
        "recorrido_producto_minimo",
        ok,
        (r.stdout + r.stderr)[-400:],
        "recorrido-simple veredicto=ok",
    )


def test_atomic_sin_tmp() -> dict:
    with tempfile.TemporaryDirectory(prefix="b17-atomic-") as tmp:
        p = Path(tmp)
        run(
            [
                sys.executable,
                str(FLOW),
                "iniciar",
                "--proyecto",
                str(p),
                "--idea",
                "atomic",
                "--fuerza",
            ]
        )
        tmps = list((p / "workflow").rglob("*.tmp"))
        ok = len(tmps) == 0 and (p / "workflow" / "estado.json").is_file()
        return case(
            "escritura_atomica_limpia",
            ok,
            f"tmp huérfanos: {tmps}",
            "tras iniciar no quedan *.tmp en workflow/",
        )


def main() -> int:
    tests = [
        test_self_fixtures,
        test_estado_invalido,
        test_escritura_interrumpida,
        test_dirty_bloquea_checkpoint_commit,
        test_recuperar_aviso_dirty,
        test_atomic_sin_tmp,
        test_install_smoke,
        test_recorrido_simple,
    ]
    resultados: list[dict] = []
    for fn in tests:
        print(f"→ {fn.__name__} …", flush=True)
        try:
            resultados.append(fn())
        except Exception as e:  # noqa: BLE001 — informe de batería
            resultados.append(case(fn.__name__, False, repr(e), "sin excepción"))
        status = "OK" if resultados[-1]["ok"] else "FALLA"
        print(f"  [{status}] {resultados[-1]['caso']}", flush=True)

    passed = sum(1 for r in resultados if r["ok"])
    total = len(resultados)
    informe = {
        "bateria": "B17-integridad",
        "ts": now_iso(),
        "passed": passed,
        "total": total,
        "veredicto": "ok" if passed == total else "falla",
        "casos": resultados,
    }
    out_dir = ROOT / "tests" / "scenarios" / "integridad"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "ultimo-informe.json"
    out.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n=== B17: {passed}/{total} → {informe['veredicto']} ===")
    print(f"Informe: {out}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
