#!/usr/bin/env python3
"""Validador determinista del workflow/ de un proyecto (paso 8 / R19).

Solo biblioteca estándar. Códigos de salida:
  0 — íntegro
  1 — violaciones de contrato
  2 — uso incorrecto / carpeta ilegible
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

def _resolve_roots() -> tuple[Path, Path]:
    """Repo del método, skill empaquetada o .metodo/."""
    here = Path(__file__).resolve().parent
    parent = here.parent
    if (parent / "contracts").is_dir():
        return parent, parent / "contracts"
    repo = here.parent
    if (repo / "core" / "contracts").is_dir():
        return repo, repo / "core" / "contracts"
    return parent, parent / "contracts"


ROOT, CONTRACTS = _resolve_roots()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_contracts() -> dict[str, Any]:
    return {
        "vocabulario": load_json(CONTRACTS / "vocabulario.json"),
        "transiciones": load_json(CONTRACTS / "transiciones.json"),
    }


class Finding:
    __slots__ = ("codigo", "mensaje", "ruta")

    def __init__(self, codigo: str, mensaje: str, ruta: str = "") -> None:
        self.codigo = codigo
        self.mensaje = mensaje
        self.ruta = ruta

    def as_dict(self) -> dict[str, str]:
        d = {"codigo": self.codigo, "mensaje": self.mensaje}
        if self.ruta:
            d["ruta"] = self.ruta
        return d


def validate_workflow(
    workflow: Path,
    huellas: dict[str, str] | None = None,
) -> list[Finding]:
    """Valida una carpeta workflow/. Devuelve lista de hallazgos (vacía = ok)."""
    c = load_contracts()
    vocab = c["vocabulario"]
    trans = c["transiciones"]
    id_re = re.compile(vocab["patron_id"])
    findings: list[Finding] = []

    def err(codigo: str, mensaje: str, ruta: str = "") -> None:
        findings.append(Finding(codigo, mensaje, ruta))

    estado_path = workflow / "estado.json"
    rel_path = workflow / "relaciones.json"
    evid_path = workflow / "evidencias.json"
    eventos_path = workflow / "eventos.jsonl"
    dec_dir = workflow / "decisiones"

    for required in (estado_path, rel_path, evid_path):
        if not required.is_file():
            err("archivo_faltante", f"Falta {required.name}", str(required))
    if findings:
        return findings

    try:
        estado = load_json(estado_path)
        relaciones = load_json(rel_path)
        evidencias = load_json(evid_path)
    except json.JSONDecodeError as e:
        err("json_invalido", str(e), str(e.doc if False else "workflow"))
        return findings

    # --- relaciones / nodos ---
    nodos: dict[str, Any] = relaciones.get("nodos") or {}
    aristas: list[dict[str, Any]] = relaciones.get("aristas") or []
    if not isinstance(nodos, dict):
        err("esquema", "relaciones.nodos debe ser objeto", str(rel_path))
        return findings

    for nid, meta in nodos.items():
        if not id_re.match(nid):
            err("id_invalido", f"Id no cumple patrón: {nid}", str(rel_path))
        if not isinstance(meta, dict):
            err("esquema", f"Nodo {nid} debe ser objeto", str(rel_path))
            continue
        tipo = meta.get("tipo")
        prefijo = nid.split("-", 1)[0]
        if tipo and tipo != prefijo:
            err("id_tipo", f"{nid}: tipo {tipo} no coincide con prefijo", str(rel_path))
        if prefijo in ("REQ", "OBJ") and "estado_afirmacion" in meta:
            if meta["estado_afirmacion"] not in vocab["estados_afirmacion"]:
                err(
                    "estado_afirmacion",
                    f"{nid}: estado_afirmacion inválido",
                    str(rel_path),
                )

    for i, edge in enumerate(aristas):
        if not isinstance(edge, dict):
            err("esquema", f"arista[{i}] no es objeto", str(rel_path))
            continue
        de, a, tipo = edge.get("de"), edge.get("a"), edge.get("tipo")
        if tipo not in vocab["tipos_relacion"]:
            err("relacion_tipo", f"Tipo de relación desconocido: {tipo}", str(rel_path))
        if de not in nodos:
            err("referencia_rota", f"Arista de={de} no existe en nodos", str(rel_path))
        if a not in nodos:
            err("referencia_rota", f"Arista a={a} no existe en nodos", str(rel_path))
        if tipo == "evidencia_de" and de and not str(de).startswith("EVID-"):
            err("relacion_forma", f"evidencia_de debe salir de EVID: {de}", str(rel_path))
        if tipo == "sustituye" and (
            not str(de).startswith("DEC-") or not str(a).startswith("DEC-")
        ):
            err("relacion_forma", "sustituye solo entre DEC", str(rel_path))

    # --- evidencias ---
    items_ev: dict[str, Any] = evidencias.get("items") or {}
    for eid, ev in items_ev.items():
        if not id_re.match(eid):
            err("id_invalido", f"Evidencia id inválido: {eid}", str(evid_path))
        if eid not in nodos:
            err("referencia_rota", f"Evidencia {eid} no está en relaciones.nodos", str(evid_path))
        if not isinstance(ev, dict):
            continue
        if ev.get("estado") not in vocab["estados_evidencia"]:
            err("estado_evidencia", f"{eid}: estado inválido", str(evid_path))
        if ev.get("origen") not in vocab["versionado_evidencia"]["origen_permitido"]:
            err("origen_evidencia", f"{eid}: origen inválido", str(evid_path))
        if (
            ev.get("origen") == "comando"
            and ev.get("estado") == "vigente"
            and ev.get("exit_code") not in (None, 0)
        ):
            err(
                "evidencia_invalida",
                f"{eid}: vigente con exit {ev.get('exit_code')}",
                str(evid_path),
            )
        # Huellas guardadas al evidenciar --ejecutar (--cubre): el código cambió → stale
        if (
            ev.get("origen") == "comando"
            and ev.get("estado") == "vigente"
            and isinstance(ev.get("huellas"), dict)
        ):
            root = workflow.parent
            for ruta, digest in (ev.get("huellas") or {}).items():
                fp = root / ruta
                if not fp.is_file():
                    continue
                actual = hashlib.sha256(fp.read_bytes()).hexdigest()
                if digest and actual != digest:
                    err(
                        "evidencia_stale",
                        f"{eid}: {ruta} cambió desde la evidencia (debería ser stale)",
                        str(evid_path),
                    )
        if huellas and ev.get("origen") == "hash_archivo" and ev.get("estado") == "vigente":
            for ruta in ev.get("cubre") or []:
                if ruta in huellas and ev.get("valor") and huellas[ruta] != ev["valor"]:
                    err(
                        "evidencia_stale",
                        f"{eid}: hash de {ruta} ya no coincide (debería ser stale)",
                        str(evid_path),
                    )

    # --- estado / tareas ---
    for campo in ("contrato_version", "paquete_version", "actualizado", "actividad", "tareas"):
        if campo not in estado:
            err("esquema", f"estado.json sin campo {campo}", str(estado_path))

    tareas: dict[str, Any] = estado.get("tareas") or {}
    if not isinstance(tareas, dict):
        err("esquema", "tareas debe ser objeto", str(estado_path))
        tareas = {}

    for tid, tarea in tareas.items():
        if not id_re.match(tid) or not tid.startswith("TASK-"):
            err("id_invalido", f"Tarea id inválido: {tid}", str(estado_path))
        if tid not in nodos:
            err("referencia_rota", f"Tarea {tid} no está en relaciones.nodos", str(estado_path))
        if not isinstance(tarea, dict):
            continue
        est = tarea.get("estado")
        if est not in vocab["estados_tarea"]:
            err("estado_tarea", f"{tid}: estado inválido {est}", str(estado_path))
        for dep in tarea.get("depende_de") or []:
            if dep not in tareas:
                err("referencia_rota", f"{tid} depende de {dep} inexistente", str(estado_path))
        for link in tarea.get("enlaces") or []:
            if link not in nodos:
                err("referencia_rota", f"{tid} enlace {link} inexistente", str(estado_path))
        for evid in tarea.get("evidencia") or []:
            if evid not in items_ev:
                err("referencia_rota", f"{tid} evidencia {evid} inexistente", str(estado_path))
        if est == "preparada":
            for dep in tarea.get("depende_de") or []:
                dep_est = (tareas.get(dep) or {}).get("estado")
                if dep_est != "verificada":
                    err(
                        "transicion_invalida",
                        f"{tid} en preparada pero dependencia {dep} está {dep_est}",
                        str(estado_path),
                    )
        if est == "verificada":
            # Padre cerrado porque todas las hijas están verificadas: sin EVID propia
            if tarea.get("cerrado_por_hijas"):
                hijas = tarea.get("hijas") or [
                    i
                    for i, x in tareas.items()
                    if isinstance(x, dict) and x.get("padre") == tid
                ]
                if hijas and all(
                    (tareas.get(h) or {}).get("estado") == "verificada" for h in hijas
                ):
                    pass  # OK sin EVID propia
                else:
                    err(
                        "evidencia_invalida",
                        f"{tid} cerrado_por_hijas pero hay hijas no verificadas",
                        str(estado_path),
                    )
            else:
                evid_ids = tarea.get("evidencia") or []
                if not evid_ids and not tarea.get("comprobacion"):
                    err(
                        "evidencia_faltante",
                        f"{tid} verificada sin evidencia ni comprobacion",
                        str(estado_path),
                    )
                vigentes = [
                    e
                    for e in evid_ids
                    if (items_ev.get(e) or {}).get("estado") == "vigente"
                ]
                if evid_ids and not vigentes:
                    err(
                        "evidencia_invalida",
                        f"{tid} verificada pero ninguna EVID vigente",
                        str(estado_path),
                    )

    siguiente = estado.get("siguiente_preparada")
    if siguiente is not None and siguiente not in tareas:
        err("referencia_rota", f"siguiente_preparada {siguiente} no existe", str(estado_path))
    elif siguiente and (tareas.get(siguiente) or {}).get("estado") != "preparada":
        err(
            "incoherencia",
            f"siguiente_preparada {siguiente} no está preparada",
            str(estado_path),
        )

    # --- decisiones ---
    aceptadas_por_asunto: dict[str, str] = {}
    if dec_dir.is_dir():
        for path in sorted(dec_dir.glob("DEC-*.json")):
            try:
                dec = load_json(path)
            except json.JSONDecodeError as e:
                err("json_invalido", str(e), str(path))
                continue
            did = dec.get("id") or path.stem
            if did not in nodos:
                err("referencia_rota", f"Decisión {did} no está en nodos", str(path))
            est = dec.get("estado")
            if est not in vocab["estados_decision"]:
                err("estado_decision", f"{did}: estado inválido", str(path))
            if est == "aceptada" and not dec.get("elegida"):
                err("decision_incompleta", f"{did} aceptada sin elegida", str(path))
            for link in dec.get("enlaces") or []:
                if link not in nodos:
                    err("referencia_rota", f"{did} enlace {link} inexistente", str(path))
            if est == "aceptada":
                asunto = (dec.get("titulo") or did).strip().lower()
                if asunto in aceptadas_por_asunto:
                    err(
                        "decision_conflicto",
                        f"{did} y {aceptadas_por_asunto[asunto]} aceptadas sobre el mismo asunto",
                        str(path),
                    )
                else:
                    aceptadas_por_asunto[asunto] = did

    # --- eventos (opcional pero si existe se valida) ---
    if eventos_path.is_file():
        last_task_state: dict[str, str] = {}
        with eventos_path.open(encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError as e:
                    err("json_invalido", f"línea {n}: {e}", str(eventos_path))
                    continue
                if ev.get("tipo") not in vocab["tipos_evento"]:
                    err("evento_tipo", f"línea {n}: tipo desconocido", str(eventos_path))
                if ev.get("tipo") == "tarea.transicion":
                    sujeto = ev.get("sujeto")
                    de, a = ev.get("de"), ev.get("a")
                    permitidas = trans["tarea"].get(de or "", [])
                    if de and a and a not in permitidas:
                        err(
                            "transicion_invalida",
                            f"línea {n}: tarea {sujeto} {de}→{a} no permitida",
                            str(eventos_path),
                        )
                    if sujeto and a:
                        last_task_state[sujeto] = a
                if ev.get("tipo") == "decision.transicion":
                    de, a = ev.get("de"), ev.get("a")
                    permitidas = trans["decision"].get(de or "", [])
                    if de and a and a not in permitidas:
                        err(
                            "transicion_invalida",
                            f"línea {n}: decisión {ev.get('sujeto')} {de}→{a} no permitida",
                            str(eventos_path),
                        )
        for tid, tarea in tareas.items():
            if tid in last_task_state and last_task_state[tid] != tarea.get("estado"):
                err(
                    "incoherencia_estado_eventos",
                    f"{tid}: estado.json={tarea.get('estado')} último evento={last_task_state[tid]}",
                    str(estado_path),
                )

    return findings


def run_self_tests() -> int:
    """Ejecuta fixtures bajo tests/fixtures/. Devuelve 0 si todo cuadra."""
    fixtures = ROOT / "tests" / "fixtures"
    cases = [
        ("workflow-ok", 0, []),
        ("workflow-ref-rota", 1, ["referencia_rota"]),
        ("workflow-transicion-invalida", 1, ["transicion_invalida"]),
        ("workflow-evidencia-stale", 1, ["evidencia_stale", "evidencia_invalida"]),
        ("workflow-decision-conflicto", 1, ["decision_conflicto"]),
    ]
    failed = 0
    for name, expect_code, expect_codes in cases:
        path = fixtures / name / "workflow"
        huellas = None
        if name == "workflow-evidencia-stale":
            huellas = {"src/app.py": "hash-nuevo-distinto"}
        findings = validate_workflow(path, huellas=huellas)
        code = 0 if not findings else 1
        got = {f.codigo for f in findings}
        ok = code == expect_code and (
            not expect_codes or any(c in got for c in expect_codes)
        )
        status = "OK" if ok else "FALLA"
        print(f"[{status}] {name}: exit={code} codigos={sorted(got)}")
        if not ok:
            failed += 1
            for f in findings:
                print(f"  - {f.codigo}: {f.mensaje}")
    return 0 if failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida workflow/ según core/contracts")
    parser.add_argument(
        "workflow",
        nargs="?",
        type=Path,
        help="Ruta a la carpeta workflow/",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Ejecuta fixtures de tests/fixtures/",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Salida JSON",
    )
    parser.add_argument(
        "--huella",
        action="append",
        default=[],
        metavar="RUTA=HASH",
        help="Huella actual de un archivo cubierto (detecta stale)",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_tests()

    if not args.workflow:
        parser.error("indica la carpeta workflow/ o usa --self-test")

    workflow = args.workflow.resolve()
    if not workflow.is_dir():
        print(f"No es un directorio: {workflow}", file=sys.stderr)
        return 2

    huellas: dict[str, str] = {}
    for item in args.huella:
        if "=" not in item:
            print(f"--huella inválida: {item}", file=sys.stderr)
            return 2
        k, v = item.split("=", 1)
        huellas[k] = v

    findings = validate_workflow(workflow, huellas=huellas or None)
    result = {
        "ok": not findings,
        "workflow": str(workflow),
        "hallazgos": [f.as_dict() for f in findings],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not findings:
            print(f"OK — {workflow}")
        else:
            print(f"FALLA — {len(findings)} hallazgo(s) en {workflow}")
            for f in findings:
                where = f" ({f.ruta})" if f.ruta else ""
                print(f"  [{f.codigo}] {f.mensaje}{where}")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
