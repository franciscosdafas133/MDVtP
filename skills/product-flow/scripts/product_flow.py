#!/usr/bin/env python3
"""Coordinador product-flow (pasos 9–10).

Acciones mecánicas: iniciar, continuar, estado, anotar, impactar.
El agente (skill) interpreta lenguaje natural y llama a este script;
las puertas de producto las responde el usuario.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def _resolve_roots() -> tuple[Path, Path, Path]:
    """Repo del método, skill empaquetada o .metodo/."""
    here = Path(__file__).resolve().parent
    parent = here.parent
    if (parent / "templates").is_dir() and (parent / "scripts").is_dir():
        return parent, parent / "templates", parent / "scripts" / "validate_workflow.py"
    repo = here.parent
    if (repo / "core" / "templates").is_dir():
        return (
            repo,
            repo / "core" / "templates",
            repo / "scripts" / "validate_workflow.py",
        )
    return parent, parent / "templates", parent / "scripts" / "validate_workflow.py"


ROOT, TEMPLATES, VALIDATE = _resolve_roots()
ID_RE = re.compile(r"^(OBJ|REQ|DEC|TASK|CHECK|EVID|ASK|NOTE)-[0-9]{2,}$")

AREAS = [
    ("ASK-01", "Usuarios y permisos", "¿Quién usa el producto y con qué permisos?"),
    ("ASK-02", "Datos y recuperación", "¿Qué datos guarda y cómo se recuperan si fallan?"),
    ("ASK-03", "Integraciones y credenciales", "¿Con qué sistemas externos habla y qué secretos necesita?"),
    ("ASK-04", "Procesos asíncronos", "¿Hay trabajos en segundo plano, colas o esperas largas?"),
    ("ASK-05", "Concurrencia", "¿Pueden dos personas pisarse el mismo dato a la vez?"),
    ("ASK-06", "Experiencia de uso", "¿Cuál es el recorrido feliz mínimo del usuario?"),
    ("ASK-07", "Calidad / pruebas", "¿Cómo sabremos que una versión está bien?"),
    ("ASK-08", "Entornos", "¿Dónde corre (local, staging, prod) y qué cambia entre ellos?"),
    ("ASK-09", "Costes y operación", "¿Qué hay que vigilar en producción (coste, alertas, backups)?"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def atomic_write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def append_event(workflow: Path, event: dict) -> None:
    path = workflow / "eventos.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def render(name: str, **kwargs: str) -> str:
    text = (TEMPLATES / name).read_text(encoding="utf-8")
    for k, v in kwargs.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def informe(
    *,
    objetivo: str,
    actividad: str,
    confirmado: list[str],
    propuesto: list[str],
    rechazado: list[str],
    dudas: list[str],
    archivos: list[str],
    comprobaciones: list[str],
    checkpoint: str,
    siguiente: str,
) -> str:
    def bullets(items: list[str]) -> str:
        return "\n".join(f"  - {i}" for i in items) if items else "  - (nada)"

    return "\n".join(
        [
            "Objetivo actual:",
            f"  {objetivo}",
            "Actividad en curso:",
            f"  {actividad}",
            "Lo confirmado:",
            bullets(confirmado),
            "Lo propuesto:",
            bullets(propuesto),
            "Lo rechazado o aplazado:",
            bullets(rechazado),
            "Dudas y bloqueos:",
            bullets(dudas),
            "Archivos actualizados:",
            bullets(archivos),
            "Comprobaciones y pendientes:",
            bullets(comprobaciones),
            "Punto de recuperación disponible:",
            f"  {checkpoint}",
            "Siguiente paso y por qué:",
            f"  {siguiente}",
            "",
        ]
    )


def run_validator(workflow: Path) -> tuple[bool, str]:
    r = subprocess.run(
        [sys.executable, str(VALIDATE), str(workflow), "--json"],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0, r.stdout or r.stderr


def load_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def next_id(prefix: str, existing: set[str]) -> str:
    n = 1
    while True:
        cand = f"{prefix}-{n:02d}"
        if cand not in existing:
            return cand
        n += 1


def git_uncommitted(proyecto: Path) -> list[str]:
    """Archivos sin commit (hecho real, no memoria). Vacío si no hay git."""
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=proyecto,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return []
    if r.returncode != 0:
        return []
    return [ln[3:] for ln in r.stdout.splitlines() if ln.strip()]


def dependents(relaciones: dict, changed: str) -> list[str]:
    """Nodos que dependen del cambiado (aristas que apuntan a él o salen implementando)."""
    out: set[str] = set()
    for edge in relaciones.get("aristas") or []:
        if edge.get("a") == changed:
            out.add(edge["de"])
        # también quien implementa/verifica algo que deriva del cambiado (1 salto)
        if edge.get("de") == changed and edge.get("tipo") in (
            "deriva_de",
            "condiciona",
            "implementa",
            "verifica",
            "evidencia_de",
        ):
            out.add(edge["a"])
    out.discard(changed)
    return sorted(out)


def cmd_iniciar(proyecto: Path, idea: str, fuerza: bool) -> int:
    wf = proyecto / "workflow"
    if wf.exists() and any(wf.iterdir()) and not fuerza:
        print(f"Ya existe {wf}. Usa --fuerza para recrear (borra workflow/).", file=sys.stderr)
        return 2

    if wf.exists() and fuerza:
        shutil.rmtree(wf)

    entrega = "E01"
    idea_corta = idea.strip().split("\n")[0][:120]
    preguntas_md = "\n".join(
        f"- **{aid}** ({area}): {preg}" for aid, area, preg in AREAS
    )

    (wf / "decisiones").mkdir(parents=True)
    (wf / "entregas" / entrega).mkdir(parents=True)
    (wf / "checkpoints").mkdir(parents=True)

    files_written = [
        "workflow/producto.md",
        "workflow/descubrimiento.md",
        "workflow/requisitos.md",
        "workflow/sistema.md",
        "workflow/verificacion.md",
        "workflow/operacion.md",
        f"workflow/entregas/{entrega}/plan.md",
        f"workflow/entregas/{entrega}/tareas.md",
        "workflow/relaciones.json",
        "workflow/evidencias.json",
        "workflow/apuntes.json",
        "workflow/estado.json",
        "workflow/eventos.jsonl",
        "workflow/tablero.md",
    ]

    (wf / "producto.md").write_text(
        render("producto.md", idea=idea.strip(), idea_corta=idea_corta),
        encoding="utf-8",
    )
    (wf / "descubrimiento.md").write_text(
        render("descubrimiento.md", preguntas=preguntas_md),
        encoding="utf-8",
    )
    (wf / "requisitos.md").write_text(render("requisitos.md"), encoding="utf-8")
    (wf / "sistema.md").write_text(render("sistema.md"), encoding="utf-8")
    (wf / "verificacion.md").write_text(render("verificacion.md"), encoding="utf-8")
    (wf / "operacion.md").write_text(
        render(
            "operacion.md",
            checklist_antes="(generar con `operar` cuando toque entregar)",
            checklist_durante="(generar con `operar`)",
            checklist_despues="(generar con `operar`)",
            pendientes_reales="- (aún no hay plan de entrega)",
            recuperacion_prod=(
                "- Definir al operar: datos, APIs y pagos no se deshacen con git"
            ),
        ),
        encoding="utf-8",
    )
    (wf / "entregas" / entrega / "plan.md").write_text(
        render(
            "plan.md",
            entrega_id=entrega,
            objetivo="Primer incremento usable a partir de la idea inicial.",
        ),
        encoding="utf-8",
    )
    (wf / "entregas" / entrega / "tareas.md").write_text(
        render(
            "tareas.md",
            entrega_id=entrega,
            tarea_1="Cerrar descubrimiento mínimo (áreas que aplican + 3 preguntas prioritarias)",
            termino_1="Hay respuestas o 'no aplica' en ASK prioritarias y OBJ-01 revisado",
        ),
        encoding="utf-8",
    )

    nodos = {
        "OBJ-01": {
            "tipo": "OBJ",
            "estado_afirmacion": "hipotesis",
            "archivo": "producto.md",
        },
        "TASK-01": {
            "tipo": "TASK",
            "archivo": f"entregas/{entrega}/tareas.md",
        },
    }
    for aid, area, _ in AREAS:
        nodos[aid] = {"tipo": "ASK", "archivo": "descubrimiento.md", "area": area}

    aristas = [{"de": "TASK-01", "tipo": "implementa", "a": "OBJ-01"}]
    for aid, _, _ in AREAS:
        aristas.append({"de": aid, "tipo": "comenta", "a": "OBJ-01"})

    atomic_write_json(
        wf / "relaciones.json",
        {"contrato_version": "0.1.0", "nodos": nodos, "aristas": aristas},
    )
    atomic_write_json(
        wf / "evidencias.json",
        {"contrato_version": "0.1.0", "items": {}},
    )
    atomic_write_json(
        wf / "apuntes.json",
        {"contrato_version": "0.1.0", "items": {}},
    )

    estado = {
        "contrato_version": "0.1.0",
        "paquete_version": (
            (ROOT / "VERSION").read_text(encoding="utf-8").strip()
            if (ROOT / "VERSION").is_file()
            else "0.1.0-rc1"
        ),
        "actualizado": now_iso(),
        "actividad": {
            "id": "descubrir",
            "nombre": "Descubrir (idea → preguntas)",
            "estado": "en_curso",
        },
        "tareas": {
            "TASK-01": {
                "id": "TASK-01",
                "titulo": "Cerrar descubrimiento mínimo",
                "estado": "en_curso",
                "depende_de": [],
                "enlaces": ["OBJ-01"],
                "evidencia": [],
                "comprobacion": None,
                "bloqueo": None,
            }
        },
        "bloqueos": [],
        "siguiente_preparada": None,
        "idea_inicial": idea_corta,
        "entrega_actual": entrega,
    }
    atomic_write_json(wf / "estado.json", estado)
    (wf / "eventos.jsonl").write_text("", encoding="utf-8")
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "sesion.reanudar",
            "actor": "agente",
            "sujeto": "OBJ-01",
            "de": None,
            "a": "hipotesis",
            "detalle": {"accion": "iniciar", "idea": idea_corta},
        },
    )
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "tarea.transicion",
            "actor": "agente",
            "sujeto": "TASK-01",
            "de": "pendiente",
            "a": "preparada",
            "detalle": {},
        },
    )
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "tarea.transicion",
            "actor": "agente",
            "sujeto": "TASK-01",
            "de": "preparada",
            "a": "en_curso",
            "detalle": {},
        },
    )

    ok, raw = run_validator(wf)
    (wf / "tablero.md").write_text(
        f"# Tablero (regenerable)\n\nActividad: descubrir\nTarea en curso: TASK-01\n"
        f"Validador: {'OK' if ok else 'FALLA'}\n",
        encoding="utf-8",
    )

    if not ok:
        print("ADVERTENCIA: el workflow recién creado no pasó el validador:", file=sys.stderr)
        print(raw, file=sys.stderr)

    # Propuestas de profundidad: 3 preguntas prioritarias tipicas
    prioritarias = ["ASK-01", "ASK-06", "ASK-02"]
    propuesto = [
        f"{aid}: {next(p for a, _, p in AREAS if a == aid)}" for aid in prioritarias
    ]

    print(
        informe(
            objetivo=idea_corta,
            actividad="Descubrir — convertir la idea en preguntas y hechos",
            confirmado=["Idea inicial registrada como OBJ-01 (hipótesis)"],
            propuesto=[
                "Recorrer áreas de descubrimiento; priorizar usuarios, recorrido y datos",
                *propuesto,
            ],
            rechazado=[],
            dudas=[f"{a}: {p}" for a, _, p in AREAS],
            archivos=files_written,
            comprobaciones=[
                "Validador: " + ("OK" if ok else "FALLA — ver JSON"),
                "Puerta humana: el usuario responde o marca 'no aplica' en preguntas prioritarias",
            ],
            checkpoint="(aún no — se crea al cerrar actividad comprobada; paso 11)",
            siguiente=(
                "Responder ASK-01, ASK-06 y ASK-02 (o decir 'no aplica'). "
                "No hace falta elegir skills: sigue con product-flow continuar."
            ),
        )
    )
    print(f"Proyecto: {proyecto.resolve()}")
    print(f"Workflow: {wf.resolve()}")
    return 0 if ok else 1


def load_estado(wf: Path) -> dict:
    return json.loads((wf / "estado.json").read_text(encoding="utf-8"))


def ruta_siguiente(estado: dict, val_ok: bool, hallazgos: list) -> str:
    """Tabla de rutas mínima sobre hechos (inspiración X11)."""
    if not val_ok:
        codigos = ", ".join(sorted({h.get("codigo", "?") for h in hallazgos})) or "error"
        return f"Reparar integridad del workflow (validador: {codigos}) antes de avanzar."

    if estado.get("bloqueos"):
        b = estado["bloqueos"][0]
        return f"Resolver bloqueo {b.get('id')}: {b.get('motivo')}"

    tareas = estado.get("tareas") or {}
    en_curso = [t for t, v in tareas.items() if v.get("estado") == "en_curso"]
    en_rev = [t for t, v in tareas.items() if v.get("estado") == "en_revision"]
    prep = [t for t, v in tareas.items() if v.get("estado") == "preparada"]

    act = (estado.get("actividad") or {}).get("id")
    if en_rev:
        return f"Puerta humana: revisar {en_rev[0]} y aceptar/rechazar."
    if en_curso:
        if act == "descubrir":
            return (
                f"Seguir descubrimiento en {en_curso[0]}: "
                "contestar preguntas ASK o anotar; luego product-flow decidir si hay alternativas."
            )
        return f"Continuar trabajo técnico de {en_curso[0]} dentro del alcance autorizado."
    if prep:
        return f"Empezar tarea preparada {prep[0]} (ya tiene dependencias listas)."
    return "Proponer siguiente actividad (requisitos / sistema / plan) según docs y puertas pendientes."


def pendientes_apuntes(wf: Path) -> list[str]:
    items = (load_json(wf / "apuntes.json", {"items": {}}) or {}).get("items") or {}
    out = []
    for nid, note in items.items():
        if note.get("pendiente"):
            out.append(f"{nid} → {note.get('enlaza')}: {note.get('texto')}")
    return out


def cmd_estado(proyecto: Path) -> int:
    wf = proyecto / "workflow"
    if not (wf / "estado.json").is_file():
        print("No hay workflow/. Ejecuta: product_flow.py iniciar …", file=sys.stderr)
        return 2
    estado = load_estado(wf)
    ok, raw = run_validator(wf)
    hallazgos = []
    try:
        hallazgos = json.loads(raw).get("hallazgos") or []
    except json.JSONDecodeError:
        pass

    tareas = estado.get("tareas") or {}
    resumen_t = [f"{k}: {v.get('estado')}" for k, v in tareas.items()]
    dudas = [f"{b.get('id')}: {b.get('motivo')}" for b in estado.get("bloqueos") or []]
    dudas.extend(pendientes_apuntes(wf))
    print(
        informe(
            objetivo=estado.get("idea_inicial") or "(sin idea)",
            actividad=(estado.get("actividad") or {}).get("nombre") or "?",
            confirmado=resumen_t,
            propuesto=[],
            rechazado=[],
            dudas=dudas,
            archivos=["workflow/estado.json"],
            comprobaciones=["Validador: " + ("OK" if ok else "FALLA")],
            checkpoint="(ver workflow/checkpoints/)",
            siguiente=ruta_siguiente(estado, ok, hallazgos),
        )
    )
    if not ok and raw:
        print(raw)
    return 0 if ok else 1


def cmd_continuar(proyecto: Path) -> int:
    """Reanuda: contrasta validador + apuntes + git; imprime ruta (R08, R13)."""
    wf = proyecto / "workflow"
    if not (wf / "estado.json").is_file():
        print("No hay workflow/. Ejecuta: product_flow.py iniciar …", file=sys.stderr)
        return 2

    print("=== Contraste al retomar ===")
    ok, raw = run_validator(wf)
    print(f"- Validador: {'OK' if ok else 'FALLA'}")
    if not ok:
        try:
            for h in json.loads(raw).get("hallazgos") or []:
                print(f"  · [{h.get('codigo')}] {h.get('mensaje')}")
        except json.JSONDecodeError:
            print(raw)

    ap = pendientes_apuntes(wf)
    print(f"- Apuntes pendientes: {len(ap)}")
    for line in ap[:10]:
        print(f"  · {line}")

    dirty = git_uncommitted(proyecto)
    print(f"- Archivos sin commit (git): {len(dirty)}")
    for f in dirty[:15]:
        print(f"  · {f}")
    if dirty:
        print("  (No descartar en silencio — E11 / R13)")

    docs = [
        "producto.md",
        "descubrimiento.md",
        "requisitos.md",
        "sistema.md",
        "estado.json",
    ]
    print("- Docs workflow presentes:")
    for d in docs:
        p = wf / d
        print(f"  · {d}: {'sí' if p.is_file() else 'FALTA'}")

    print()
    code = cmd_estado(proyecto)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "sesion.reanudar",
            "actor": "agente",
            "sujeto": "actividad",
            "de": None,
            "a": None,
            "detalle": {
                "accion": "continuar",
                "validador_ok": ok,
                "apuntes_pendientes": len(ap),
                "sin_commit": len(dirty),
            },
        },
    )
    print(
        "Nota: continuar no salta puertas humanas ni marca tareas verificadas. "
        "El validador y los apuntes pendientes mandan sobre la memoria del chat."
    )
    return code


def cmd_anotar(proyecto: Path, enlaza: str, texto: str, pendiente: bool) -> int:
    """Registra NOTE enlazado a ASK/DEC/REQ/… (R06)."""
    wf = proyecto / "workflow"
    if not (wf / "estado.json").is_file():
        print("No hay workflow/.", file=sys.stderr)
        return 2
    if not ID_RE.match(enlaza):
        print(f"Id inválido: {enlaza}", file=sys.stderr)
        return 2

    rel = load_json(wf / "relaciones.json", {"nodos": {}, "aristas": []})
    if enlaza not in (rel.get("nodos") or {}):
        print(f"{enlaza} no existe en relaciones.nodos", file=sys.stderr)
        return 2

    apuntes = load_json(wf / "apuntes.json", {"contrato_version": "0.1.0", "items": {}})
    items = apuntes.setdefault("items", {})
    existing = set(items) | set(rel.get("nodos") or {})
    nid = next_id("NOTE", existing)
    items[nid] = {
        "id": nid,
        "texto": texto.strip(),
        "enlaza": enlaza,
        "ts": now_iso(),
        "pendiente": pendiente,
    }
    rel.setdefault("nodos", {})[nid] = {
        "tipo": "NOTE",
        "archivo": "apuntes.json",
    }
    rel.setdefault("aristas", []).append(
        {"de": nid, "tipo": "comenta", "a": enlaza}
    )
    atomic_write_json(wf / "apuntes.json", apuntes)
    atomic_write_json(wf / "relaciones.json", rel)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "nota.anadir",
            "actor": "usuario",
            "sujeto": nid,
            "de": None,
            "a": None,
            "detalle": {"enlaza": enlaza, "pendiente": pendiente},
        },
    )
    ok, _ = run_validator(wf)
    print(f"Apunte {nid} → {enlaza}: {texto.strip()}")
    print(f"Pendiente visible: {pendiente}")
    print(f"Validador: {'OK' if ok else 'FALLA'}")
    return 0 if ok else 1


def cmd_impactar(proyecto: Path, cambiado: str, motivo: str) -> int:
    """Invalida dependientes mecánicamente (R11): tareas verificadas→en_revision, EVID→stale."""
    wf = proyecto / "workflow"
    if not (wf / "estado.json").is_file():
        print("No hay workflow/.", file=sys.stderr)
        return 2
    if not ID_RE.match(cambiado):
        print(f"Id inválido: {cambiado}", file=sys.stderr)
        return 2

    rel = load_json(wf / "relaciones.json", {"nodos": {}, "aristas": []})
    if cambiado not in (rel.get("nodos") or {}):
        print(f"{cambiado} no está en relaciones", file=sys.stderr)
        return 2

    deps = dependents(rel, cambiado)
    estado = load_estado(wf)
    evidencias = load_json(wf / "evidencias.json", {"items": {}})
    items_ev = evidencias.setdefault("items", {})
    afectados: list[str] = []

    # Expandir: si un TASK depende del cambiado vía enlaces en estado
    for tid, tarea in (estado.get("tareas") or {}).items():
        if cambiado in (tarea.get("enlaces") or []):
            if tid not in deps:
                deps.append(tid)

    for dep in deps:
        if dep.startswith("TASK-"):
            tarea = (estado.get("tareas") or {}).get(dep)
            if not tarea:
                continue
            prev = tarea.get("estado")
            if prev == "verificada":
                tarea["estado"] = "en_revision"
                afectados.append(f"{dep}: verificada → en_revision")
                append_event(
                    wf,
                    {
                        "ts": now_iso(),
                        "tipo": "tarea.transicion",
                        "actor": "validador",
                        "sujeto": dep,
                        "de": "verificada",
                        "a": "en_revision",
                        "detalle": {"motivo": motivo, "por": cambiado},
                    },
                )
            for evid in tarea.get("evidencia") or []:
                if evid in items_ev and items_ev[evid].get("estado") == "vigente":
                    items_ev[evid]["estado"] = "stale"
                    items_ev[evid]["motivo_stale"] = f"Cambio en {cambiado}: {motivo}"
                    afectados.append(f"{evid}: vigente → stale")
                    append_event(
                        wf,
                        {
                            "ts": now_iso(),
                            "tipo": "evidencia.marcar",
                            "actor": "validador",
                            "sujeto": evid,
                            "de": "vigente",
                            "a": "stale",
                            "detalle": {"por": cambiado, "motivo": motivo},
                        },
                    )
        if dep.startswith("EVID-") and dep in items_ev:
            if items_ev[dep].get("estado") == "vigente":
                items_ev[dep]["estado"] = "stale"
                items_ev[dep]["motivo_stale"] = f"Cambio en {cambiado}: {motivo}"
                afectados.append(f"{dep}: vigente → stale")
                append_event(
                    wf,
                    {
                        "ts": now_iso(),
                        "tipo": "evidencia.marcar",
                        "actor": "validador",
                        "sujeto": dep,
                        "de": "vigente",
                        "a": "stale",
                        "detalle": {"por": cambiado, "motivo": motivo},
                    },
                )

    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "estado.json", estado)
    atomic_write_json(wf / "evidencias.json", evidencias)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "reconciliar",
            "actor": "agente",
            "sujeto": cambiado,
            "de": None,
            "a": None,
            "detalle": {"accion": "impactar", "motivo": motivo, "deps": deps},
        },
    )

    ok, raw = run_validator(wf)
    # Tras invalidar, una tarea en_revision con evidencias stale es coherente;
    # si quedó verificada sin vigente, el validador lo dirá.
    print(f"Impacto por cambio de {cambiado}: {motivo}")
    print(f"Dependientes considerados: {', '.join(deps) if deps else '(ninguno)'}")
    if afectados:
        for a in afectados:
            print(f"  - {a}")
    else:
        print("  - (nada que invalidar todavía)")
    print(f"Validador: {'OK' if ok else 'FALLA'}")
    if not ok:
        print(raw)
    print(
        informe(
            objetivo=estado.get("idea_inicial") or "(sin idea)",
            actividad="Impacto de cambio (R11)",
            confirmado=[f"Origen del cambio: {cambiado}"],
            propuesto=["Revisar artefactos en_revision antes de volver a verificar"],
            rechazado=[],
            dudas=afectados,
            archivos=["workflow/estado.json", "workflow/evidencias.json", "workflow/eventos.jsonl"],
            comprobaciones=["Evidencias históricas se conservan pero ya no cuentan como vigentes"],
            checkpoint="(sin tocar código automáticamente)",
            siguiente=ruta_siguiente(estado, ok, []),
        )
    )
    return 0 if ok else 1


def git_root(proyecto: Path) -> Path | None:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=proyecto,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if r.returncode != 0:
        return None
    return Path(r.stdout.strip())


def git_head(proyecto: Path) -> str | None:
    r = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=proyecto,
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def git_worktree_available(proyecto: Path) -> bool:
    r = subprocess.run(
        ["git", "worktree", "list"],
        cwd=proyecto,
        capture_output=True,
        text=True,
        check=False,
    )
    return r.returncode == 0


def list_checkpoints(wf: Path) -> list[Path]:
    d = wf / "checkpoints"
    if not d.is_dir():
        return []
    return sorted(d.glob("CP-*.json"))


def cmd_checkpoint(
    proyecto: Path,
    nombre: str,
    alcance: str,
    pendientes: str,
    commit_workflow: bool,
) -> int:
    """Guarda un punto de recuperación (metadatos + snapshot; commit opcional)."""
    wf = proyecto / "workflow"
    if not (wf / "estado.json").is_file():
        print("No hay workflow/.", file=sys.stderr)
        return 2

    dirty = git_uncommitted(proyecto)
    if dirty and commit_workflow:
        print(
            "Hay archivos sin commit. No se hará commit automático de todo el repo.\n"
            "Opciones: confirma tú el commit, o usa --sin-commit (solo snapshot documental).",
            file=sys.stderr,
        )
        for f in dirty[:20]:
            print(f"  · {f}", file=sys.stderr)
        return 2

    estado = load_estado(wf)
    existing = {p.stem for p in list_checkpoints(wf)}
    cid = next_id("CP", existing)
    snap_dir = wf / "checkpoints" / cid / "snapshot"
    if snap_dir.exists():
        shutil.rmtree(snap_dir)
    snap_dir.parent.mkdir(parents=True, exist_ok=True)

    # Copia documental (sin secretos a propósito: solo workflow/)
    for item in wf.iterdir():
        if item.name == "checkpoints":
            continue
        dest = snap_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    root = git_root(proyecto)
    docs = sorted(
        str(p.relative_to(wf))
        for p in wf.rglob("*")
        if p.is_file() and "checkpoints" not in p.parts
    )
    meta = {
        "id": cid,
        "nombre": nombre,
        "creado": now_iso(),
        "commit": None,
        "modo": "documental",
        "paquete_version": estado.get("paquete_version") or "0.0.0-dev",
        "documentos": docs,
        "tareas": list((estado.get("tareas") or {}).keys()),
        "comprobaciones": [alcance],
        "pendientes": [p.strip() for p in pendientes.split(";") if p.strip()],
        "dependencias_externas": [],
        "alcance_comprobado": alcance,
        "snapshot": f"checkpoints/{cid}/snapshot",
    }
    atomic_write_json(wf / "checkpoints" / f"{cid}.json", meta)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "checkpoint.crear",
            "actor": "agente",
            "sujeto": cid,
            "de": None,
            "a": None,
            "detalle": {"nombre": nombre},
        },
    )

    commit = git_head(proyecto) if root else None
    modo = "git" if commit else "documental"
    if root and commit_workflow:
        subprocess.run(["git", "add", "workflow"], cwd=proyecto, check=False)
        r = subprocess.run(
            ["git", "commit", "-m", f"checkpoint {cid}: {nombre}"],
            cwd=proyecto,
            capture_output=True,
            text=True,
            check=False,
        )
        if r.returncode != 0:
            print(
                "No se pudo crear commit git. Se guarda checkpoint documental.",
                file=sys.stderr,
            )
            print(r.stderr or r.stdout, file=sys.stderr)
        else:
            commit = git_head(proyecto)
            modo = "git"
            meta["commit"] = commit
            meta["modo"] = modo
            atomic_write_json(wf / "checkpoints" / f"{cid}.json", meta)
            subprocess.run(
                ["git", "add", f"workflow/checkpoints/{cid}.json"],
                cwd=proyecto,
                check=False,
            )
            subprocess.run(
                ["git", "commit", "-m", f"checkpoint {cid}: sha {commit[:7]}"],
                cwd=proyecto,
                capture_output=True,
                check=False,
            )
            # El commit de recuperación es el del contenido del checkpoint (primer sha).
    else:
        meta["commit"] = commit
        meta["modo"] = modo
        atomic_write_json(wf / "checkpoints" / f"{cid}.json", meta)

    print(f"Checkpoint {cid}: {nombre}")
    print(f"  Modo: {modo}")
    print(f"  Commit: {commit or '(ninguno — solo documental)'}")
    print(f"  Snapshot: {snap_dir}")
    print(f"  Alcance comprobado: {alcance}")
    print("  Recuperar con: product_flow.py recuperar --proyecto … --checkpoint", cid)
    return 0


def cmd_recuperar(
    proyecto: Path,
    checkpoint_id: str,
    destino: Path | None,
    forzar_rama: bool,
) -> int:
    """Abre worktree (o rama) desde el commit del checkpoint; no toca la línea actual."""
    wf = proyecto / "workflow"
    meta_path = wf / "checkpoints" / f"{checkpoint_id}.json"
    if not meta_path.is_file():
        print(f"No existe {meta_path}", file=sys.stderr)
        return 2
    meta = load_json(meta_path, {})
    commit = meta.get("commit")
    snap = meta.get("snapshot")
    root = git_root(proyecto)

    dirty = git_uncommitted(proyecto)
    if dirty:
        print("Aviso: hay cambios sin commit en el proyecto actual (no se descartan):")
        for f in dirty[:15]:
            print(f"  · {f}")

    if not root or not commit or meta.get("modo") == "documental":
        # Solo copia documental a carpeta nueva
        dest = destino or (proyecto.parent / f"{proyecto.name}-{checkpoint_id}")
        if dest.exists():
            print(f"Destino ya existe: {dest}", file=sys.stderr)
            return 2
        dest.mkdir(parents=True)
        src = wf / snap if snap else None
        if src and src.is_dir():
            shutil.copytree(src, dest / "workflow")
        else:
            print("Sin snapshot documental usable.", file=sys.stderr)
            return 2
        print(
            f"Recuperación DOCUMENTAL en {dest}\n"
            "(Sin git: no hay aislamiento de código; solo docs del checkpoint.)"
        )
        return 0

    branch = f"recuperar/{checkpoint_id}"
    dest = destino or (proyecto.parent / f"{proyecto.name}-{checkpoint_id}")

    if not forzar_rama and git_worktree_available(proyecto):
        if dest.exists():
            print(f"Destino worktree ya existe: {dest}", file=sys.stderr)
            return 2
        # crear rama en el commit si no existe
        subprocess.run(
            ["git", "branch", branch, commit],
            cwd=proyecto,
            capture_output=True,
            check=False,
        )
        r = subprocess.run(
            ["git", "worktree", "add", str(dest), branch],
            cwd=proyecto,
            capture_output=True,
            text=True,
            check=False,
        )
        if r.returncode != 0:
            print("Falló worktree; prueba --rama:", r.stderr or r.stdout, file=sys.stderr)
            return 1
        print(f"Worktree aislado en: {dest}")
        print(f"  Rama: {branch}")
        print(f"  Commit: {commit}")
        print(f"  Checkpoint: {checkpoint_id} — {meta.get('nombre')}")
        print("  El trabajo en el proyecto original se conserva intacto.")
        return 0

    # Fallback: solo crear rama (usuario hace checkout cuando quiera)
    r = subprocess.run(
        ["git", "branch", branch, commit],
        cwd=proyecto,
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0 and "already exists" not in (r.stderr or ""):
        print(r.stderr or r.stdout, file=sys.stderr)
        return 1
    print(f"Rama creada (sin cambiar tu checkout actual): {branch} @ {commit}")
    print("  Para trabajar ahí: git switch", branch)
    print("  (Preferible: worktree; aquí se usó modo rama.)")
    return 0


def cmd_evidenciar(
    proyecto: Path,
    tarea: str,
    origen: str,
    valor: str,
    cubre: str,
) -> int:
    """Registra EVID vigente y la enlaza a la tarea (R14)."""
    wf = proyecto / "workflow"
    if not (wf / "estado.json").is_file():
        print("No hay workflow/.", file=sys.stderr)
        return 2
    estado = load_estado(wf)
    tareas = estado.get("tareas") or {}
    if tarea not in tareas:
        print(f"{tarea} no existe", file=sys.stderr)
        return 2
    if origen not in ("commit", "hash_archivo", "comando", "manual"):
        print("origen debe ser commit|hash_archivo|comando|manual", file=sys.stderr)
        return 2

    evidencias = load_json(wf / "evidencias.json", {"contrato_version": "0.1.0", "items": {}})
    rel = load_json(wf / "relaciones.json", {"nodos": {}, "aristas": []})
    existing = set(evidencias.get("items") or {}) | set(rel.get("nodos") or {})
    eid = next_id("EVID", existing)
    items = evidencias.setdefault("items", {})
    items[eid] = {
        "id": eid,
        "estado": "vigente",
        "origen": origen,
        "valor": valor,
        "cubre": [c.strip() for c in cubre.split(",") if c.strip()],
        "registrado": now_iso(),
        "motivo_stale": None,
        "tarea": tarea,
    }
    tareas[tarea].setdefault("evidencia", []).append(eid)
    rel.setdefault("nodos", {})[eid] = {"tipo": "EVID"}
    rel.setdefault("aristas", []).append(
        {"de": eid, "tipo": "evidencia_de", "a": tarea}
    )
    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "evidencias.json", evidencias)
    atomic_write_json(wf / "relaciones.json", rel)
    atomic_write_json(wf / "estado.json", estado)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "evidencia.marcar",
            "actor": "agente",
            "sujeto": eid,
            "de": None,
            "a": "vigente",
            "detalle": {"tarea": tarea, "origen": origen, "valor": valor},
        },
    )
    ok, _ = run_validator(wf)
    print(f"Evidencia {eid} → {tarea} [{origen}] {valor}")
    print(f"Validador: {'OK' if ok else 'FALLA'}")
    return 0 if ok else 1


def cmd_presentar(proyecto: Path, tarea: str) -> int:
    """en_curso → en_revision (listo para puerta humana / cierre)."""
    wf = proyecto / "workflow"
    estado = load_estado(wf)
    tareas = estado.get("tareas") or {}
    if tarea not in tareas:
        print(f"{tarea} no existe", file=sys.stderr)
        return 2
    prev = tareas[tarea].get("estado")
    if prev not in ("en_curso", "preparada"):
        print(f"{tarea} está {prev}; presenta solo desde preparada/en_curso", file=sys.stderr)
        return 2
    # preparada → en_curso → en_revision si hace falta
    if prev == "preparada":
        append_event(
            wf,
            {
                "ts": now_iso(),
                "tipo": "tarea.transicion",
                "actor": "agente",
                "sujeto": tarea,
                "de": "preparada",
                "a": "en_curso",
                "detalle": {"accion": "presentar"},
            },
        )
        prev = "en_curso"
    tareas[tarea]["estado"] = "en_revision"
    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "estado.json", estado)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "tarea.transicion",
            "actor": "agente",
            "sujeto": tarea,
            "de": prev,
            "a": "en_revision",
            "detalle": {"accion": "presentar"},
        },
    )
    ok, _ = run_validator(wf)
    print(f"{tarea}: {prev} → en_revision (esperando verificar / puerta)")
    print(f"Validador: {'OK' if ok else 'FALLA'}")
    return 0 if ok else 1


def cmd_verificar(proyecto: Path, tarea: str, fallo: str | None) -> int:
    """Cierra en_revision→verificada solo con evidencia vigente; o registra fallo."""
    wf = proyecto / "workflow"
    estado = load_estado(wf)
    tareas = estado.get("tareas") or {}
    if tarea not in tareas:
        print(f"{tarea} no existe", file=sys.stderr)
        return 2
    if tareas[tarea].get("estado") != "en_revision":
        print(f"{tarea} debe estar en_revision (usa presentar antes)", file=sys.stderr)
        return 2

    if fallo:
        tareas[tarea]["estado"] = "en_curso"
        tareas[tarea]["ultimo_fallo"] = fallo
        estado["actualizado"] = now_iso()
        atomic_write_json(wf / "estado.json", estado)
        append_event(
            wf,
            {
                "ts": now_iso(),
                "tipo": "tarea.transicion",
                "actor": "agente",
                "sujeto": tarea,
                "de": "en_revision",
                "a": "en_curso",
                "detalle": {"accion": "verificar_fallo", "fallo": fallo},
            },
        )
        print(f"NO verificada {tarea}: {fallo}")
        print("Siguiente: depurar (máx. 3) o ajustar pruebas.")
        return 1

    evidencias = load_json(wf / "evidencias.json", {"items": {}})
    items = evidencias.get("items") or {}
    eids = tareas[tarea].get("evidencia") or []
    vigentes = [e for e in eids if (items.get(e) or {}).get("estado") == "vigente"]
    omitidas = [
        e
        for e in eids
        if (items.get(e) or {}).get("estado") in ("omitida", "bloqueada")
    ]
    if not vigentes and not (omitidas and tareas[tarea].get("comprobacion")):
        print(
            "Prohibido marcar verificada sin EVID vigente "
            "(ni omitida/bloqueada justificada en comprobacion).",
            file=sys.stderr,
        )
        return 1

    tareas[tarea]["estado"] = "verificada"
    tareas[tarea]["depurar_intentos"] = 0
    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "estado.json", estado)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "tarea.transicion",
            "actor": "usuario",
            "sujeto": tarea,
            "de": "en_revision",
            "a": "verificada",
            "detalle": {"evidencia": vigentes or omitidas},
        },
    )
    ok, raw = run_validator(wf)
    print(f"Verificada {tarea} con {vigentes or omitidas}")
    print(f"Validador: {'OK' if ok else 'FALLA'}")
    if not ok:
        print(raw)
    return 0 if ok else 1


def cmd_depurar(
    proyecto: Path,
    tarea: str,
    hipotesis: str,
    resultado: str,
) -> int:
    """Registra un intento de depuración; al 3er fallo bloquea y pide al usuario (DEC-05)."""
    wf = proyecto / "workflow"
    estado = load_estado(wf)
    tareas = estado.get("tareas") or {}
    if tarea not in tareas:
        print(f"{tarea} no existe", file=sys.stderr)
        return 2
    if resultado not in ("fallo", "ok"):
        print("--resultado debe ser fallo|ok", file=sys.stderr)
        return 2

    t = tareas[tarea]
    intentos = int(t.get("depurar_intentos") or 0)
    historial = t.setdefault("depurar_historial", [])

    if resultado == "ok":
        t["depurar_intentos"] = 0
        historial.append(
            {"ts": now_iso(), "hipotesis": hipotesis, "resultado": "ok"}
        )
        estado["actualizado"] = now_iso()
        atomic_write_json(wf / "estado.json", estado)
        print(f"Depuración OK en {tarea}. Siguiente: presentar → verificar.")
        return 0

    intentos += 1
    t["depurar_intentos"] = intentos
    historial.append(
        {"ts": now_iso(), "hipotesis": hipotesis, "resultado": "fallo"}
    )
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "reconciliar",
            "actor": "agente",
            "sujeto": tarea,
            "de": None,
            "a": None,
            "detalle": {
                "accion": "depurar",
                "intento": intentos,
                "hipotesis": hipotesis,
                "resultado": "fallo",
            },
        },
    )

    if intentos >= 3:
        prev = t.get("estado")
        t["estado"] = "bloqueada"
        bid = f"bloqueo-debug-{intentos}"
        t["bloqueo"] = bid
        estado.setdefault("bloqueos", []).append(
            {
                "id": bid,
                "motivo": (
                    f"3 depuraciones fallidas. Última hipótesis: {hipotesis}. "
                    "Parar y preguntar al usuario (DEC-05)."
                ),
                "afecta": [tarea],
                "marca": "MANUAL_VERIFY_REQUIRED",
            }
        )
        if prev != "bloqueada":
            append_event(
                wf,
                {
                    "ts": now_iso(),
                    "tipo": "tarea.transicion",
                    "actor": "validador",
                    "sujeto": tarea,
                    "de": prev,
                    "a": "bloqueada",
                    "detalle": {"accion": "depurar_tope", "intentos": intentos},
                },
            )
        estado["actualizado"] = now_iso()
        atomic_write_json(wf / "estado.json", estado)
        print(f"TOPE 3/3 en {tarea}. No sigas parcheando a ciegas.")
        print("Pregunta al usuario con las hipótesis probadas:")
        for i, h in enumerate(historial, 1):
            print(f"  {i}. {h.get('hipotesis')} → {h.get('resultado')}")
        return 1

    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "estado.json", estado)
    print(f"Intento {intentos}/3 fallido en {tarea}: {hipotesis}")
    print("Reproduce, una hipótesis nueva, test, arreglo mínimo.")
    return 1


_CRITERIOS_DIVIDIR = {
    "varios_resultados_verificables",
    "varias_fronteras",
    "duda_determinante",
    "una_evidencia_no_basta",
}
_VAGO = re.compile(
    r"^(implementar|cablear|wire|soportar|handle|arreglar|mejorar)(\s|$)",
    re.I,
)


def cmd_dividir(
    proyecto: Path,
    padre: str,
    hijas_raw: str,
    motivo: str,
    porque: str,
) -> int:
    """Parte una tarea solo si hay criterio (R09 / X05). Hijas cadena o paralelo.

    --hijas: 'titulo|condicion|cadena;titulo2|condicion2|paralelo;...'
    Modo omitido = cadena. Paralelo = misma oleada (mismas deps; no se esperan entre sí).
    --porque: uno de los ids de core/contracts/reglas-division.json
    """
    wf = proyecto / "workflow"
    if not (wf / "estado.json").is_file():
        print("No hay workflow/.", file=sys.stderr)
        return 2
    if not ID_RE.match(padre) or not padre.startswith("TASK-"):
        print(f"Padre inválido: {padre}", file=sys.stderr)
        return 2
    if porque not in _CRITERIOS_DIVIDIR:
        print(
            "Hay que decir --porque con un criterio válido:\n  - "
            + "\n  - ".join(sorted(_CRITERIOS_DIVIDIR)),
            file=sys.stderr,
        )
        return 2

    partes = [p.strip() for p in hijas_raw.split(";") if p.strip()]
    if len(partes) < 2:
        print(
            "No se divide por capricho: hacen falta ≥2 hijas con resultados distintos.",
            file=sys.stderr,
        )
        return 2

    # (titulo, termino, paralelo: bool)
    hijas_spec: list[tuple[str, str, bool]] = []
    for p in partes:
        bits = [b.strip() for b in p.split("|")]
        if len(bits) < 2:
            print(
                f"Formato: titulo|condicion_observable[|cadena|paralelo] — recibí: {p}",
                file=sys.stderr,
            )
            return 2
        tit, term = bits[0], bits[1]
        modo = (bits[2] if len(bits) > 2 else "cadena").lower()
        if modo not in ("cadena", "paralelo", "seq", "par", "p"):
            print(f"Modo inválido '{modo}' (usa cadena o paralelo): {p}", file=sys.stderr)
            return 2
        paralelo = modo in ("paralelo", "par", "p")
        if not tit or not term:
            print(f"Título y condición obligatorios: {p}", file=sys.stderr)
            return 2
        if re.search(r"\b\d+\s*h(oras?)?\b", f"{tit} {term}", re.I):
            print(
                "Prohibido tamaño en horas (criterio de las fuentes, sin horas). "
                "Di qué se verá hecho.",
                file=sys.stderr,
            )
            return 2
        if _VAGO.search(term) and len(term.split()) < 5:
            print(
                f"Condición demasiado vaga: «{term}». "
                "Di un resultado observable (API, UI, test, dato guardado…).",
                file=sys.stderr,
            )
            return 2
        hijas_spec.append((tit, term, paralelo))

    estado = load_estado(wf)
    tareas = estado.setdefault("tareas", {})
    if padre not in tareas:
        print(f"{padre} no existe en estado.json", file=sys.stderr)
        return 2

    rel = load_json(wf / "relaciones.json", {"nodos": {}, "aristas": []})
    existing = set(tareas) | set(rel.get("nodos") or {})
    created: list[str] = []
    # Oleada de la que depende lo siguiente (al inicio: deps del padre)
    last_wave = list(tareas[padre].get("depende_de") or [])
    current_parallel: list[str] = []

    for tit, term, paralelo in hijas_spec:
        if paralelo:
            deps = list(last_wave)
        else:
            if current_parallel:
                last_wave = list(current_parallel)
                current_parallel = []
            deps = list(last_wave)

        tid = next_id("TASK", existing)
        existing.add(tid)
        tareas[tid] = {
            "id": tid,
            "titulo": tit,
            "estado": "pendiente",
            "depende_de": deps,
            "enlaces": list(tareas[padre].get("enlaces") or []),
            "evidencia": [],
            "comprobacion": term,
            "bloqueo": None,
            "padre": padre,
            "paralelo": paralelo,
            "simulacion": False,
        }
        rel.setdefault("nodos", {})[tid] = {
            "tipo": "TASK",
            "archivo": f"entregas/{estado.get('entrega_actual') or 'E01'}/tareas.md",
        }
        for link in tareas[tid]["enlaces"]:
            if link in (rel.get("nodos") or {}):
                rel.setdefault("aristas", []).append(
                    {"de": tid, "tipo": "implementa", "a": link}
                )
        for d in deps:
            rel.setdefault("aristas", []).append(
                {"de": tid, "tipo": "deriva_de", "a": d}
            )
        created.append(tid)
        if paralelo:
            current_parallel.append(tid)
        else:
            last_wave = [tid]

        append_event(
            wf,
            {
                "ts": now_iso(),
                "tipo": "tarea.transicion",
                "actor": "agente",
                "sujeto": tid,
                "de": None,
                "a": "pendiente",
                "detalle": {
                    "accion": "dividir",
                    "padre": padre,
                    "porque": porque,
                    "paralelo": paralelo,
                    "termino": term,
                },
            },
        )

    if current_parallel:
        last_wave = list(current_parallel)

    prev_est = tareas[padre].get("estado")
    tareas[padre]["estado"] = "bloqueada"
    tareas[padre]["bloqueo"] = f"dividida→{','.join(created)}"
    tareas[padre]["comprobacion"] = (
        f"Dividida ({porque}) en {', '.join(created)}. {motivo}"
    )
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "tarea.transicion",
            "actor": "agente",
            "sujeto": padre,
            "de": prev_est,
            "a": "bloqueada",
            "detalle": {
                "accion": "dividir",
                "hijas": created,
                "porque": porque,
                "motivo": motivo,
            },
        },
    )

    # Preparar hijas cuya deps ya están verificadas (oleada inicial)
    preparadas = []
    for tid in created:
        deps = tareas[tid].get("depende_de") or []
        deps_ok = all(
            (tareas.get(d) or {}).get("estado") == "verificada" for d in deps
        )
        if deps_ok or not deps:
            tareas[tid]["estado"] = "preparada"
            preparadas.append(tid)
            append_event(
                wf,
                {
                    "ts": now_iso(),
                    "tipo": "tarea.transicion",
                    "actor": "agente",
                    "sujeto": tid,
                    "de": "pendiente",
                    "a": "preparada",
                    "detalle": {},
                },
            )
    if preparadas:
        estado["siguiente_preparada"] = preparadas[0]

    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "estado.json", estado)
    atomic_write_json(wf / "relaciones.json", rel)

    entrega = estado.get("entrega_actual") or "E01"
    tpath = wf / "entregas" / entrega / "tareas.md"
    if tpath.is_file():
        lines = [
            "",
            f"## División de {padre}",
            f"Criterio (`porque`): `{porque}`",
            f"Motivo: {motivo}",
            "",
            "| Id | Título | Modo | Depende de | Condición observable |",
            "|---|---|---|---|---|",
        ]
        for tid in created:
            t = tareas[tid]
            deps = ", ".join(t.get("depende_de") or []) or "—"
            modo = "paralelo" if t.get("paralelo") else "cadena"
            lines.append(
                f"| {tid} | {t['titulo']} | {modo} | {deps} | {t.get('comprobacion')} |"
            )
        with tpath.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    ok, raw = run_validator(wf)
    print(f"Dividida {padre} → {', '.join(created)}")
    print(f"Criterio: {porque}")
    print(f"Motivo: {motivo}")
    for tid in created:
        t = tareas[tid]
        modo = "paralelo" if t.get("paralelo") else "cadena"
        print(
            f"  - {tid} ({modo}): {t['titulo']} [{t['estado']}] "
            f"deps={t.get('depende_de') or []} → {t['comprobacion']}"
        )
    print(f"Validador: {'OK' if ok else 'FALLA'}")
    if not ok:
        print(raw)
    return 0 if ok else 1


def cmd_bloquear(proyecto: Path, tarea: str, motivo: str, marca: str) -> int:
    """Bloquea solo una tarea (R10); el resto puede seguir si no depende de ella."""
    wf = proyecto / "workflow"
    if not (wf / "estado.json").is_file():
        print("No hay workflow/.", file=sys.stderr)
        return 2
    estado = load_estado(wf)
    tareas = estado.get("tareas") or {}
    if tarea not in tareas:
        print(f"{tarea} no existe", file=sys.stderr)
        return 2

    bid = f"bloqueo-{len(estado.get('bloqueos') or []) + 1:02d}"
    prev = tareas[tarea].get("estado")
    if prev == "verificada":
        print("No se bloquea una tarea ya verificada; usa impactar si cambió el requisito.")
        return 2
    tareas[tarea]["estado"] = "bloqueada"
    tareas[tarea]["bloqueo"] = bid
    if marca in ("simulacion", "integracion_real", "MANUAL_VERIFY_REQUIRED"):
        tareas[tarea]["marca"] = marca
    estado.setdefault("bloqueos", []).append(
        {
            "id": bid,
            "motivo": motivo,
            "afecta": [tarea],
            "marca": marca or None,
        }
    )
    # Quién queda bloqueado en cascada (solo dependientes directos/indirectos)
    afectados = [tarea]
    changed = True
    while changed:
        changed = False
        for tid, t in tareas.items():
            if tid in afectados:
                continue
            deps = t.get("depende_de") or []
            if any(d in afectados for d in deps) and t.get("estado") not in (
                "verificada",
                "bloqueada",
            ):
                # R10: no bloquear automáticamente a todos — solo informar
                pass
    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "estado.json", estado)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "tarea.transicion",
            "actor": "agente",
            "sujeto": tarea,
            "de": prev,
            "a": "bloqueada",
            "detalle": {"motivo": motivo, "marca": marca, "bloqueo": bid},
        },
    )
    # Tareas que NO dependen de esta siguen
    libres = [
        tid
        for tid, t in tareas.items()
        if tid != tarea
        and tarea not in (t.get("depende_de") or [])
        and t.get("estado") not in ("bloqueada", "verificada")
    ]
    ok, _ = run_validator(wf)
    print(f"Bloqueada {tarea}: {motivo}")
    if marca:
        print(f"  Marca: {marca}")
    print(f"  Otras tareas que pueden seguir (no dependen de ella): {', '.join(libres) or '(ninguna)'}")
    print(f"Validador: {'OK' if ok else 'FALLA'}")
    return 0 if ok else 1


def cmd_desbloquear(proyecto: Path, tarea: str, evidencia: str) -> int:
    """Quita bloqueo si hay evidencia de resolución; vuelve a preparada o pendiente."""
    wf = proyecto / "workflow"
    estado = load_estado(wf)
    tareas = estado.get("tareas") or {}
    if tarea not in tareas or tareas[tarea].get("estado") != "bloqueada":
        print(f"{tarea} no está bloqueada", file=sys.stderr)
        return 2
    # Si fue dividida, no desbloquear así
    if str(tareas[tarea].get("bloqueo") or "").startswith("dividida"):
        print("Esta tarea fue dividida; trabaja las hijas, no la desbloquees.")
        return 2
    bid = tareas[tarea].get("bloqueo")
    deps = tareas[tarea].get("depende_de") or []
    deps_ok = all((tareas.get(d) or {}).get("estado") == "verificada" for d in deps)
    nuevo = "preparada" if deps_ok or not deps else "pendiente"
    tareas[tarea]["estado"] = nuevo
    tareas[tarea]["bloqueo"] = None
    estado["bloqueos"] = [
        b for b in (estado.get("bloqueos") or []) if b.get("id") != bid
    ]
    if nuevo == "preparada":
        estado["siguiente_preparada"] = tarea
    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "estado.json", estado)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "tarea.transicion",
            "actor": "usuario",
            "sujeto": tarea,
            "de": "bloqueada",
            "a": nuevo,
            "detalle": {"evidencia_resolucion": evidencia},
        },
    )
    ok, _ = run_validator(wf)
    print(f"Desbloqueada {tarea} → {nuevo}")
    print(f"Evidencia: {evidencia}")
    print(f"Validador: {'OK' if ok else 'FALLA'}")
    return 0 if ok else 1


def _bullets_from_semi(text: str) -> str:
    parts = [p.strip() for p in text.split(";") if p.strip()]
    if not parts:
        return "- (ninguna declarada — revisar con honestidad)"
    return "\n".join(f"- {p}" for p in parts)


def cmd_operar(
    proyecto: Path,
    resumen: str,
    pendientes: str,
    recuperacion: str = "",
) -> int:
    """Genera plan contextual de entrega/operación (R18); pendientes reales explícitos."""
    wf = proyecto / "workflow"
    if not wf.is_dir():
        print(f"No hay {wf}. Ejecuta iniciar primero.", file=sys.stderr)
        return 2
    resumen = resumen.strip()
    if not resumen:
        print("--resumen es obligatorio", file=sys.stderr)
        return 2
    if not pendientes.strip():
        print(
            "--pendientes es obligatorio (lista con ; o texto 'ninguna' si aplica)",
            file=sys.stderr,
        )
        return 2

    antes = (
        f"Checkpoint del incremento «{resumen}» con alcance real comprobado; "
        "ciclos de código ya cerrados (escanear→planificar→evaluar→reemplazar); "
        "evidencia vigente en tareas a publicar"
    )
    durante = (
        "Publicar solo el alcance del incremento; "
        "anotar cualquier paso manual (migraciones, secretos, DNS); "
        "no marcar como hecho lo no ejecutado"
    )
    despues = (
        "Smoke en el entorno destino; "
        "actualizar operacion.md si cambió la realidad; "
        "registrar comprobaciones reales que sigan pendientes"
    )
    pend_md = _bullets_from_semi(pendientes)
    if recuperacion.strip():
        recup_md = _bullets_from_semi(recuperacion)
    else:
        recup_md = "\n".join(
            [
                "- Código/docs: checkpoint + worktree/rama (no borrar trabajo posterior)",
                "- Producción: procedimiento aparte para datos, pagos y APIs ya ejecutadas",
                f"- Contexto de este incremento: {resumen}",
            ]
        )

    (wf / "operacion.md").write_text(
        render(
            "operacion.md",
            checklist_antes=antes,
            checklist_durante=durante,
            checklist_despues=despues,
            pendientes_reales=pend_md,
            recuperacion_prod=recup_md,
        ),
        encoding="utf-8",
    )

    estado = load_estado(wf)
    estado["operacion"] = {
        "resumen": resumen,
        "pendientes_reales": [
            p.strip() for p in pendientes.split(";") if p.strip()
        ],
        "actualizado": now_iso(),
    }
    estado["actualizado"] = now_iso()
    atomic_write_json(wf / "estado.json", estado)
    append_event(
        wf,
        {
            "ts": now_iso(),
            "tipo": "reconciliar",
            "actor": "agente",
            "sujeto": "operacion",
            "de": None,
            "a": None,
            "detalle": {
                "accion": "operar",
                "resumen": resumen,
                "pendientes": estado["operacion"]["pendientes_reales"],
            },
        },
    )

    print(
        informe(
            objetivo=resumen,
            actividad="operar / entregar (R18)",
            confirmado=[
                "Plan en workflow/operacion.md",
                "Comprobaciones reales pendientes registradas",
            ],
            propuesto=[
                "Revisar checklist antes/durante/después",
                "No confundir recuperación git con recuperación en producción",
            ],
            rechazado=[],
            dudas=estado["operacion"]["pendientes_reales"],
            archivos=["workflow/operacion.md", "workflow/estado.json"],
            comprobaciones=["pendientes reales listados — no inventar que ya pasaron"],
            checkpoint="(crear checkpoint si el alcance ya está comprobado)",
            siguiente="Publicar solo con checklist y pendientes a la vista",
        )
    )
    return 0


def cmd_recorrido_simple() -> int:
    """Recorrido automático de un producto mínimo con el método (semilla B18).

    No sustituye a un agente real (Grok/Cursor/Claude): demuestra el cableado
    mecánico idea → código → evidencia → verificar → operar. Un agente externo
    puede seguir tests/scenarios/producto-simple/PLAYBOOK.md.
    """
    demo = ROOT / "tests" / "fixtures" / "demo-recorrido"
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir(parents=True)
    idea = "Contador CLI: al ejecutar imprime 'visitas: N' y guarda el número en un archivo"
    print("=== RECORRIDO: iniciar ===\n")
    if cmd_iniciar(demo, idea, fuerza=True) != 0:
        return 1

    wf = demo / "workflow"
    # Producto mínimo (el “código” del incremento)
    app = demo / "app"
    app.mkdir()
    (app / "contador.py").write_text(
        '#!/usr/bin/env python3\n'
        '"""Producto mínimo del recorrido-simple."""\n'
        "from pathlib import Path\n"
        "\n"
        "STATE = Path(__file__).with_name(\"visitas.txt\")\n"
        "\n"
        "def leer() -> int:\n"
        "    if not STATE.is_file():\n"
        "        return 0\n"
        "    return int(STATE.read_text(encoding=\"utf-8\").strip() or \"0\")\n"
        "\n"
        "def main() -> None:\n"
        "    n = leer() + 1\n"
        "    STATE.write_text(str(n), encoding=\"utf-8\")\n"
        "    print(f\"visitas: {n}\")\n"
        "\n"
        'if __name__ == \"__main__\":\n'
        "    main()\n",
        encoding="utf-8",
    )
    (app / "comprobar.sh").write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "cd \"$(dirname \"$0\")\"\n"
        "rm -f visitas.txt\n"
        "out=$(python3 contador.py)\n"
        "test \"$out\" = \"visitas: 1\"\n"
        "out=$(python3 contador.py)\n"
        "test \"$out\" = \"visitas: 2\"\n"
        "echo OK\n",
        encoding="utf-8",
    )
    (app / "comprobar.sh").chmod(0o755)

    print("\n=== RECORRIDO: ciclo código (escanear→planificar→evaluar→reemplazar) ===\n")
    print("Escaneo: carpeta app/ vacía → hace falta contador.py + prueba.")
    print("Plan: un archivo CLI + script comprobar.sh (2 visitas).")
    print("Evaluación: sin pagos ni red; comprobable en local.")
    print("Reemplazo: archivos escritos en app/.")

    # Tarea de implementación
    estado = load_estado(wf)
    rel = load_json(wf / "relaciones.json", {})
    rel["nodos"]["TASK-10"] = {"tipo": "TASK"}
    estado["tareas"]["TASK-10"] = {
        "id": "TASK-10",
        "titulo": "CLI contador de visitas",
        "estado": "en_curso",
        "depende_de": [],
        "enlaces": ["OBJ-01"],
        "evidencia": [],
        "comprobacion": "comprobar.sh imprime OK (visitas 1 y 2)",
        "bloqueo": None,
    }
    for de, a in [("pendiente", "preparada"), ("preparada", "en_curso")]:
        append_event(
            wf,
            {
                "ts": now_iso(),
                "tipo": "tarea.transicion",
                "actor": "agente",
                "sujeto": "TASK-10",
                "de": de,
                "a": a,
                "detalle": {"accion": "recorrido_simple"},
            },
        )
    atomic_write_json(wf / "estado.json", estado)
    atomic_write_json(wf / "relaciones.json", rel)

    print("\n=== RECORRIDO: ejecutar prueba real ===\n")
    r = subprocess.run(
        ["bash", str(app / "comprobar.sh")],
        cwd=app,
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        print(r.stdout, r.stderr, file=sys.stderr)
        print("FALLA: la prueba del producto mínimo no pasó", file=sys.stderr)
        return 1
    print(r.stdout.strip() or "OK")

    print("\n=== RECORRIDO: evidenciar → presentar → verificar ===\n")
    cmd = f"bash {app / 'comprobar.sh'}"
    if cmd_evidenciar(demo, "TASK-10", "comando", cmd, "app/contador.py,app/comprobar.sh") != 0:
        return 1
    if cmd_presentar(demo, "TASK-10") != 0:
        return 1
    if cmd_verificar(demo, "TASK-10", fallo=None) != 0:
        return 1

    print("\n=== RECORRIDO: operar (entrega + pendientes honestos) ===\n")
    if (
        cmd_operar(
            demo,
            "Contador CLI v1 (solo local)",
            "No hay despliegue web; no hay usuarios reales; no hay persistencia en nube",
            recuperacion=(
                "Borrar visitas.txt regenera el contador; "
                "código: volver al checkpoint del workflow"
            ),
        )
        != 0
    ):
        return 1

    estado = load_estado(wf)
    ok_val, _ = run_validator(wf)
    ok = (
        estado["tareas"]["TASK-10"]["estado"] == "verificada"
        and bool(estado.get("operacion"))
        and ok_val
        and (app / "contador.py").is_file()
    )
    resultado = {
        "escenario": "producto-simple",
        "clase": "determinista_paquete",
        "veredicto": "ok" if ok else "falla",
        "host": "script",
        "version_paquete": estado.get("paquete_version"),
        "entrada": idea,
        "acciones": [
            "iniciar",
            "escribir app/contador.py",
            "bash app/comprobar.sh",
            "evidenciar",
            "presentar",
            "verificar",
            "operar",
        ],
        "evidencia": {
            "tarea": "TASK-10",
            "estado_tarea": estado["tareas"]["TASK-10"]["estado"],
            "pendientes_operacion": estado.get("operacion", {}).get("pendientes_reales"),
            "validador": "OK" if ok_val else "FALLA",
            "proyecto": str(demo),
        },
        "nota": (
            "Recorrido mecánico. Un agente (Cursor/Claude/Grok) debe usar el "
            "PLAYBOOK y no autojuzgarse: el veredicto lo da este JSON + el usuario."
        ),
        "ts": now_iso(),
    }
    out = ROOT / "tests" / "scenarios" / "producto-simple" / "ultimo-resultado.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(out, resultado)
    print(
        f"\n=== RECORRIDO: veredicto={resultado['veredicto']} "
        f"TASK-10={estado['tareas']['TASK-10']['estado']} "
        f"validador={'OK' if ok_val else 'FALLA'} ==="
    )
    print(f"Resultado: {out}")
    return 0 if ok else 1


def cmd_demo_b14() -> int:
    """Demo: operar genera plan + pendientes reales; no inventa comprobaciones."""
    demo = ROOT / "tests" / "fixtures" / "demo-operar"
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir(parents=True)
    print("=== DEMO B14: base ===\n")
    if cmd_iniciar(demo, "Demo entrega y operación", fuerza=True) != 0:
        return 1

    print("\n=== DEMO B14: operar ===\n")
    if (
        cmd_operar(
            demo,
            "Primera versión de reservas online",
            "Pago real no probado; SMS del salón sin credenciales; staging sin datos de clientes reales",
            recuperacion=(
                "Rollback de app vía worktree desde CP comprobado; "
                "pagos ya cobrados: reembolso manual en pasarela; "
                "migración BD: script inverso documentado o restore backup"
            ),
        )
        != 0
    ):
        return 1

    op = (demo / "workflow" / "operacion.md").read_text(encoding="utf-8")
    estado = load_estado(demo / "workflow")
    ok = (
        "Primera versión de reservas" in op
        and "Pago real no probado" in op
        and "git" in op.lower()
        and "pendientes_reales" in (estado.get("operacion") or {})
        and "Pago real no probado" in (estado["operacion"]["pendientes_reales"][0])
    )
    print(
        f"\n=== Comprobación B14: plan={'OK' if 'Plan de entrega' in op else 'FALLA'}, "
        f"pendientes={estado.get('operacion', {}).get('pendientes_reales')} → "
        f"{'OK' if ok else 'FALLA'} ==="
    )
    return 0 if ok else 1


def cmd_demo_b13() -> int:
    """Demo: sin evidencia no verifica; con evidencia sí; depurar para a los 3."""
    demo = ROOT / "tests" / "fixtures" / "demo-verificar"
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir(parents=True)
    print("=== DEMO B13: base ===\n")
    if cmd_iniciar(demo, "Demo verificar/depurar", fuerza=True) != 0:
        return 1
    wf = demo / "workflow"
    estado = load_estado(wf)
    rel = load_json(wf / "relaciones.json", {})
    # TASK-02 en_curso lista para presentar
    rel["nodos"]["TASK-02"] = {"tipo": "TASK"}
    estado["tareas"]["TASK-02"] = {
        "id": "TASK-02",
        "titulo": "Listar peluqueros",
        "estado": "en_curso",
        "depende_de": [],
        "enlaces": ["OBJ-01"],
        "evidencia": [],
        "comprobacion": "GET /peluqueros → 200",
        "bloqueo": None,
    }
    for de, a in [("pendiente", "preparada"), ("preparada", "en_curso")]:
        append_event(
            wf,
            {
                "ts": now_iso(),
                "tipo": "tarea.transicion",
                "actor": "agente",
                "sujeto": "TASK-02",
                "de": de,
                "a": a,
                "detalle": {},
            },
        )
    atomic_write_json(wf / "estado.json", estado)
    atomic_write_json(wf / "relaciones.json", rel)

    print("\n=== DEMO B13: presentar + verificar SIN evidencia (debe fallar) ===\n")
    if cmd_presentar(demo, "TASK-02") != 0:
        return 1
    if cmd_verificar(demo, "TASK-02", fallo=None) == 0:
        print("ERROR: verificó sin evidencia", file=sys.stderr)
        return 1
    print("(bloqueo sin evidencia — OK)")

    print("\n=== DEMO B13: evidenciar + verificar ===\n")
    if (
        cmd_evidenciar(
            demo,
            "TASK-02",
            "comando",
            "pytest -q tests/test_peluqueros.py",
            "src/peluqueros.py",
        )
        != 0
    ):
        return 1
    # sigue en_revision tras el intento fallido? verificar_fallo no; sin fallo dejó en_revision
    # cmd_verificar sin evidencia no cambió estado (return 1 early) — sigue en_revision
    if cmd_verificar(demo, "TASK-02", fallo=None) != 0:
        return 1

    print("\n=== DEMO B13: depurar hasta tope ===\n")
    # nueva tarea para debug
    estado = load_estado(wf)
    rel = load_json(wf / "relaciones.json", {})
    rel["nodos"]["TASK-03"] = {"tipo": "TASK"}
    estado["tareas"]["TASK-03"] = {
        "id": "TASK-03",
        "titulo": "Bug de slots",
        "estado": "en_curso",
        "depende_de": [],
        "enlaces": ["OBJ-01"],
        "evidencia": [],
        "comprobacion": None,
        "bloqueo": None,
        "depurar_intentos": 0,
    }
    for de, a in [("pendiente", "preparada"), ("preparada", "en_curso")]:
        append_event(
            wf,
            {
                "ts": now_iso(),
                "tipo": "tarea.transicion",
                "actor": "agente",
                "sujeto": "TASK-03",
                "de": de,
                "a": a,
                "detalle": {},
            },
        )
    atomic_write_json(wf / "estado.json", estado)
    atomic_write_json(wf / "relaciones.json", rel)

    for i, hip in enumerate(
        ["param mal leído", "zona horaria", "índice BD"], 1
    ):
        code = cmd_depurar(demo, "TASK-03", hip, "fallo")
        if i < 3 and code != 1:
            return 1
        if i == 3 and code != 1:
            return 1

    estado = load_estado(wf)
    ok = (
        estado["tareas"]["TASK-02"]["estado"] == "verificada"
        and estado["tareas"]["TASK-03"]["estado"] == "bloqueada"
        and int(estado["tareas"]["TASK-03"].get("depurar_intentos") or 0) >= 3
    )
    print(
        f"\n=== Comprobación B13: TASK-02={estado['tareas']['TASK-02']['estado']}, "
        f"TASK-03={estado['tareas']['TASK-03']['estado']}, "
        f"intentos={estado['tareas']['TASK-03'].get('depurar_intentos')} → "
        f"{'OK' if ok else 'FALLA'} ==="
    )
    return 0 if ok else 1


def cmd_demo_b12() -> int:
    """Demo: tarea gorda → dividir; una hija bloqueada no frena a otra independiente."""
    demo = ROOT / "tests" / "fixtures" / "demo-tareas"
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir(parents=True)
    print("=== DEMO B12: iniciar ===\n")
    if cmd_iniciar(demo, "Reservas peluquería — demo tareas", fuerza=True) != 0:
        return 1
    wf = demo / "workflow"
    # Añadir TASK-BIG sobredimensionada
    estado = load_estado(wf)
    rel = load_json(wf / "relaciones.json", {})
    rel["nodos"]["TASK-99"] = {"tipo": "TASK"}
    estado["tareas"]["TASK-99"] = {
        "id": "TASK-99",
        "titulo": "Hacer toda la app de reservas",
        "estado": "en_curso",
        "depende_de": [],
        "enlaces": ["OBJ-01"],
        "evidencia": [],
        "comprobacion": None,
        "bloqueo": None,
    }
    for de, a in [("pendiente", "preparada"), ("preparada", "en_curso")]:
        append_event(
            wf,
            {
                "ts": now_iso(),
                "tipo": "tarea.transicion",
                "actor": "agente",
                "sujeto": "TASK-99",
                "de": de,
                "a": a,
                "detalle": {},
            },
        )
    atomic_write_json(wf / "estado.json", estado)
    atomic_write_json(wf / "relaciones.json", rel)

    print("\n=== DEMO B12: dividir TASK-99 (criterio + paralelo/cadena) ===\n")
    # Dos en paralelo (misma oleada), luego confirmar en cadena
    hijas = (
        "Listar peluqueros|La API GET /peluqueros responde 200 con lista JSON|paralelo;"
        "Página de horarios|Existe vista /horarios con slots vacíos o reales|paralelo;"
        "Elegir y confirmar reserva|El usuario confirma y el registro queda en BD|cadena"
    )
    if (
        cmd_dividir(
            demo,
            "TASK-99",
            hijas,
            "Mezcla listado, UI y confirmación (varios resultados)",
            "varios_resultados_verificables",
        )
        != 0
    ):
        return 1

    estado = load_estado(wf)
    hijas_ids = [
        t
        for t, v in estado["tareas"].items()
        if v.get("padre") == "TASK-99"
    ]
    if len(hijas_ids) < 2:
        print("FALLA: no hay hijas", file=sys.stderr)
        return 1

    # Tarea independiente TASK-80 + bloquear una hija
    rel = load_json(wf / "relaciones.json", {})
    rel["nodos"]["TASK-80"] = {"tipo": "TASK"}
    estado["tareas"]["TASK-80"] = {
        "id": "TASK-80",
        "titulo": "Página de contacto del salón",
        "estado": "preparada",
        "depende_de": [],
        "enlaces": ["OBJ-01"],
        "evidencia": [],
        "comprobacion": "Hay página /contacto con teléfono",
        "bloqueo": None,
    }
    atomic_write_json(wf / "estado.json", estado)
    atomic_write_json(wf / "relaciones.json", rel)

    print("\n=== DEMO B12: bloquear una hija (parcial) ===\n")
    hija_bloqueada = hijas_ids[1]
    if (
        cmd_bloquear(
            demo,
            hija_bloqueada,
            "Falta acceso a la BD de staging",
            "MANUAL_VERIFY_REQUIRED",
        )
        != 0
    ):
        return 1

    estado = load_estado(wf)
    t80 = estado["tareas"]["TASK-80"]["estado"]
    t99 = estado["tareas"]["TASK-99"]["estado"]
    ok = (
        t99 == "bloqueada"
        and estado["tareas"][hija_bloqueada]["estado"] == "bloqueada"
        and t80 == "preparada"
        and len(hijas_ids) >= 3
    )
    print(
        f"\n=== Comprobación B12: padre_dividido={t99}, "
        f"hija_bloqueada={estado['tareas'][hija_bloqueada]['estado']}, "
        f"independiente_sigue={t80}, hijas={len(hijas_ids)} → "
        f"{'OK' if ok else 'FALLA'} ==="
    )
    return 0 if ok else 1


def cmd_demo() -> int:
    """Demo reproducible: idea vaga → workflow válido + informe."""
    demo = ROOT / "tests" / "fixtures" / "demo-iniciar"
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir(parents=True)
    idea = (
        "Una app para que clientes de una peluquería reserven hora "
        "con el peluquero que quieran."
    )
    print("=== DEMO product-flow iniciar ===\n")
    code = cmd_iniciar(demo, idea, fuerza=True)
    print("\n=== DEMO product-flow estado ===\n")
    code2 = cmd_estado(demo)
    return 0 if code == 0 and code2 == 0 else 1


def _force_rm_tree(path: Path) -> None:
    """Borra carpeta incluso si un worktree/git dejó el árbol 'busy'."""
    if not path.exists():
        return
    if (path / ".git").exists() or (path / ".git").is_file():
        subprocess.run(
            ["git", "worktree", "prune"],
            cwd=path,
            capture_output=True,
            check=False,
        )
        listed = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
        )
        for line in (listed.stdout or "").splitlines():
            if line.startswith("worktree "):
                other = Path(line.split(" ", 1)[1].strip())
                if other.resolve() != path.resolve():
                    subprocess.run(
                        ["git", "worktree", "remove", "--force", str(other)],
                        cwd=path,
                        capture_output=True,
                        check=False,
                    )
        subprocess.run(
            ["git", "worktree", "prune"],
            cwd=path,
            capture_output=True,
            check=False,
        )
    trash = path.with_name(f"{path.name}.trash-{os.getpid()}")
    try:
        if trash.exists():
            shutil.rmtree(trash, ignore_errors=True)
        path.rename(trash)
        shutil.rmtree(trash, ignore_errors=True)
    except OSError:
        shutil.rmtree(path, ignore_errors=True)


def cmd_demo_b11() -> int:
    """Demo aislada: repo git de prueba → checkpoint → más commits → worktree al CP."""
    demo = ROOT / "tests" / "fixtures" / "demo-recuperacion"
    wt = ROOT / "tests" / "fixtures" / "demo-recuperacion-CP-01"
    fixtures = ROOT / "tests" / "fixtures"
    for old in fixtures.glob("demo-recuperacion*.trash-*"):
        shutil.rmtree(old, ignore_errors=True)
    if demo.exists():
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(wt)],
            cwd=demo,
            capture_output=True,
            check=False,
        )
        _force_rm_tree(demo)
    if wt.exists():
        _force_rm_tree(wt)
    demo.mkdir(parents=True)

    subprocess.run(["git", "init"], cwd=demo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "demo@example.com"],
        cwd=demo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Demo B11"],
        cwd=demo,
        check=True,
        capture_output=True,
    )

    print("=== DEMO B11: iniciar ===\n")
    if cmd_iniciar(demo, "Reservas peluquería — demo recuperación", fuerza=True) != 0:
        return 1

    subprocess.run(["git", "add", "workflow"], cwd=demo, check=True)
    subprocess.run(
        ["git", "commit", "-m", "demo: workflow inicial"],
        cwd=demo,
        check=True,
        capture_output=True,
    )

    print("\n=== DEMO B11: checkpoint ===\n")
    # árbol limpio → permitir --commit
    if (
        cmd_checkpoint(
            demo,
            nombre="Después del descubrimiento inicial",
            alcance="Solo creación de workflow y validador OK; sin pruebas de producto",
            pendientes="Preguntas ASK sin responder",
            commit_workflow=True,
        )
        != 0
    ):
        return 1

    cps = list_checkpoints(demo / "workflow")
    if not cps:
        print("No se creó CP", file=sys.stderr)
        return 1
    cid = cps[-1].stem

    # Trabajo posterior en la línea principal
    (demo / "workflow" / "producto.md").write_text(
        (demo / "workflow" / "producto.md").read_text(encoding="utf-8")
        + "\n\n## Cambio posterior al checkpoint\n\nEsto NO debe aparecer en el worktree recuperado.\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "workflow/producto.md"], cwd=demo, check=True)
    subprocess.run(
        ["git", "commit", "-m", "demo: cambio después del checkpoint"],
        cwd=demo,
        check=True,
        capture_output=True,
    )

    print("\n=== DEMO B11: recuperar (worktree) ===\n")
    if cmd_recuperar(demo, cid, destino=wt, forzar_rama=False) != 0:
        return 1

    recuperado = (wt / "workflow" / "producto.md").read_text(encoding="utf-8")
    original = (demo / "workflow" / "producto.md").read_text(encoding="utf-8")
    ok_iso = (
        "Cambio posterior al checkpoint" not in recuperado
        and "Cambio posterior al checkpoint" in original
        and wt.is_dir()
    )
    print(
        f"\n=== Comprobación demo B11: aislado_sin_cambio_posterior="
        f"{ 'Cambio posterior' not in recuperado }, "
        f"original_conserva_cambio={ 'Cambio posterior' in original } → "
        f"{'OK' if ok_iso else 'FALLA'} ==="
    )
    return 0 if ok_iso else 1


def cmd_demo_b10() -> int:
    """Demo: apunte + requisito cambia → tarea verificada pasa a en_revision y EVID stale."""
    demo = ROOT / "tests" / "fixtures" / "demo-continuidad"
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir(parents=True)
    print("=== DEMO B10: iniciar base ===\n")
    if cmd_iniciar(demo, "Reservas de peluquería", fuerza=True) != 0:
        return 1

    wf = demo / "workflow"
    # Enriquecer: REQ-01, TASK-02 verificada con EVID-01
    rel = load_json(wf / "relaciones.json", {})
    rel["nodos"]["REQ-01"] = {
        "tipo": "REQ",
        "estado_afirmacion": "confirmada",
        "archivo": "requisitos.md",
    }
    rel["nodos"]["TASK-02"] = {"tipo": "TASK", "archivo": "entregas/E01/tareas.md"}
    rel["nodos"]["CHECK-01"] = {"tipo": "CHECK"}
    rel["nodos"]["EVID-01"] = {"tipo": "EVID"}
    rel["aristas"].extend(
        [
            {"de": "REQ-01", "tipo": "deriva_de", "a": "OBJ-01"},
            {"de": "TASK-02", "tipo": "implementa", "a": "REQ-01"},
            {"de": "CHECK-01", "tipo": "verifica", "a": "TASK-02"},
            {"de": "EVID-01", "tipo": "evidencia_de", "a": "CHECK-01"},
        ]
    )
    atomic_write_json(wf / "relaciones.json", rel)
    atomic_write_json(
        wf / "evidencias.json",
        {
            "contrato_version": "0.1.0",
            "items": {
                "EVID-01": {
                    "id": "EVID-01",
                    "estado": "vigente",
                    "origen": "comando",
                    "valor": "pytest -q",
                    "cubre": ["src/reservas.py"],
                    "registrado": now_iso(),
                    "motivo_stale": None,
                }
            },
        },
    )
    estado = load_estado(wf)
    estado["tareas"]["TASK-02"] = {
        "id": "TASK-02",
        "titulo": "Listar horarios",
        "estado": "verificada",
        "depende_de": [],
        "enlaces": ["REQ-01"],
        "evidencia": ["EVID-01"],
        "comprobacion": None,
        "bloqueo": None,
    }
    # eventos para TASK-02 hasta verificada
    for de, a in [
        ("pendiente", "preparada"),
        ("preparada", "en_curso"),
        ("en_curso", "en_revision"),
        ("en_revision", "verificada"),
    ]:
        append_event(
            wf,
            {
                "ts": now_iso(),
                "tipo": "tarea.transicion",
                "actor": "agente",
                "sujeto": "TASK-02",
                "de": de,
                "a": a,
                "detalle": {},
            },
        )
    atomic_write_json(wf / "estado.json", estado)

    print("\n=== DEMO B10: anotar ===\n")
    if cmd_anotar(demo, "ASK-03", "Todavía no tengo acceso al router del salón", True) != 0:
        return 1

    print("\n=== DEMO B10: impactar REQ-01 ===\n")
    code = cmd_impactar(
        demo,
        "REQ-01",
        "Ahora también hay que elegir servicios, no solo hora",
    )
    print("\n=== DEMO B10: continuar (contraste) ===\n")
    code2 = cmd_continuar(demo)

    estado2 = load_estado(wf)
    t2 = estado2["tareas"]["TASK-02"]["estado"]
    ev = load_json(wf / "evidencias.json", {})["items"]["EVID-01"]["estado"]
    notes = load_json(wf / "apuntes.json", {})["items"]
    ok = t2 == "en_revision" and ev == "stale" and len(notes) >= 1 and code == 0
    print(
        f"\n=== Comprobación demo B10: TASK-02={t2}, EVID-01={ev}, "
        f"apuntes={len(notes)} → {'OK' if ok else 'FALLA'} ==="
    )
    return 0 if ok and code2 in (0, 1) else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Coordinador product-flow (B09–B10)")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_ini = sub.add_parser("iniciar", help="Crear workflow/ desde una idea")
    p_ini.add_argument("--proyecto", type=Path, required=True)
    p_ini.add_argument("--idea", required=True)
    p_ini.add_argument("--fuerza", action="store_true")

    p_st = sub.add_parser("estado", help="Informe de estado + ruta")
    p_st.add_argument("--proyecto", type=Path, required=True)

    p_co = sub.add_parser("continuar", help="Reanudar con contraste (validador/apuntes/git)")
    p_co.add_argument("--proyecto", type=Path, required=True)

    p_an = sub.add_parser("anotar", help="Apunte enlazado a un id")
    p_an.add_argument("--proyecto", type=Path, required=True)
    p_an.add_argument("--enlaza", required=True, help="ASK-/DEC-/REQ-/…")
    p_an.add_argument("--texto", required=True)
    p_an.add_argument(
        "--resuelto",
        action="store_true",
        help="Marcar el apunte como no pendiente",
    )

    p_im = sub.add_parser("impactar", help="Invalidar dependientes tras un cambio (R11)")
    p_im.add_argument("--proyecto", type=Path, required=True)
    p_im.add_argument("--cambiado", required=True, help="Id que cambió")
    p_im.add_argument("--motivo", required=True)

    p_cp = sub.add_parser("checkpoint", help="Guardar punto de recuperación")
    p_cp.add_argument("--proyecto", type=Path, required=True)
    p_cp.add_argument("--nombre", required=True)
    p_cp.add_argument(
        "--alcance",
        default="Alcance no detallado — revisar antes de confiar",
        help="Qué se comprobó de verdad",
    )
    p_cp.add_argument(
        "--pendientes",
        default="",
        help="Lista separada por ; de lo no verificado",
    )
    p_cp.add_argument(
        "--commit",
        action="store_true",
        help="Crear commit git del workflow (exige árbol limpio fuera de lo a commitear)",
    )

    p_re = sub.add_parser("recuperar", help="Worktree/rama desde un checkpoint")
    p_re.add_argument("--proyecto", type=Path, required=True)
    p_re.add_argument("--checkpoint", required=True, help="CP-01 …")
    p_re.add_argument("--destino", type=Path, default=None)
    p_re.add_argument(
        "--rama",
        action="store_true",
        help="Solo crear rama (no worktree)",
    )

    p_ev = sub.add_parser("evidenciar", help="Registrar evidencia vigente (R14)")
    p_ev.add_argument("--proyecto", type=Path, required=True)
    p_ev.add_argument("--tarea", required=True)
    p_ev.add_argument("--origen", required=True, help="commit|hash_archivo|comando|manual")
    p_ev.add_argument("--valor", required=True)
    p_ev.add_argument("--cubre", default="", help="rutas o ids separados por coma")

    p_pr = sub.add_parser("presentar", help="Pasar tarea a en_revision")
    p_pr.add_argument("--proyecto", type=Path, required=True)
    p_pr.add_argument("--tarea", required=True)

    p_ve = sub.add_parser("verificar", help="Cerrar con evidencia o registrar fallo")
    p_ve.add_argument("--proyecto", type=Path, required=True)
    p_ve.add_argument("--tarea", required=True)
    p_ve.add_argument("--fallo", default=None, help="Si la prueba falló, texto del fallo")

    p_de = sub.add_parser("depurar", help="Intento de depuración (tope 3)")
    p_de.add_argument("--proyecto", type=Path, required=True)
    p_de.add_argument("--tarea", required=True)
    p_de.add_argument("--hipotesis", required=True)
    p_de.add_argument("--resultado", required=True, choices=("fallo", "ok"))

    p_div = sub.add_parser("dividir", help="Partir tarea sobredimensionada (R09)")
    p_div.add_argument("--proyecto", type=Path, required=True)
    p_div.add_argument("--padre", required=True, help="TASK-… a dividir")
    p_div.add_argument(
        "--hijas",
        required=True,
        help="titulo|condicion|cadena|paralelo;… (mín. 2; sin horas)",
    )
    p_div.add_argument("--motivo", required=True)
    p_div.add_argument(
        "--porque",
        required=True,
        help="varios_resultados_verificables|varias_fronteras|duda_determinante|una_evidencia_no_basta",
    )

    p_bl = sub.add_parser("bloquear", help="Bloqueo parcial de una tarea (R10)")
    p_bl.add_argument("--proyecto", type=Path, required=True)
    p_bl.add_argument("--tarea", required=True)
    p_bl.add_argument("--motivo", required=True)
    p_bl.add_argument(
        "--marca",
        default="",
        help="simulacion | integracion_real | MANUAL_VERIFY_REQUIRED",
    )

    p_db = sub.add_parser("desbloquear", help="Quitar bloqueo con evidencia")
    p_db.add_argument("--proyecto", type=Path, required=True)
    p_db.add_argument("--tarea", required=True)
    p_db.add_argument("--evidencia", required=True)

    p_op = sub.add_parser(
        "operar",
        help="Plan de entrega/operación + pendientes reales (R18)",
    )
    p_op.add_argument("--proyecto", type=Path, required=True)
    p_op.add_argument("--resumen", required=True, help="Qué se entrega ahora")
    p_op.add_argument(
        "--pendientes",
        required=True,
        help="Comprobaciones reales aún no hechas (separadas por ;)",
    )
    p_op.add_argument(
        "--recuperacion",
        default="",
        help="Pasos de recuperación en prod (separados por ;); si vacío, texto base",
    )

    sub.add_parser("demo", help="Demo paso 9: idea vaga → incremento")
    sub.add_parser("demo-b10", help="Demo paso 10: apunte + impacto + continuar")
    sub.add_parser("demo-b11", help="Demo paso 11: checkpoint + worktree aislado")
    sub.add_parser("demo-b12", help="Demo paso 12: dividir + bloqueo parcial")
    sub.add_parser("demo-b13", help="Demo paso 13: evidencia + verificar + depurar×3")
    sub.add_parser("demo-b14", help="Demo paso 14: operar / plan de entrega")
    sub.add_parser(
        "recorrido-simple",
        help="Recorrido automático producto mínimo (semilla B18 / playbook agentes)",
    )

    args = p.parse_args(argv)
    if args.cmd == "iniciar":
        return cmd_iniciar(args.proyecto, args.idea, args.fuerza)
    if args.cmd == "estado":
        return cmd_estado(args.proyecto)
    if args.cmd == "continuar":
        return cmd_continuar(args.proyecto)
    if args.cmd == "anotar":
        return cmd_anotar(args.proyecto, args.enlaza, args.texto, pendiente=not args.resuelto)
    if args.cmd == "impactar":
        return cmd_impactar(args.proyecto, args.cambiado, args.motivo)
    if args.cmd == "checkpoint":
        return cmd_checkpoint(
            args.proyecto,
            args.nombre,
            args.alcance,
            args.pendientes,
            commit_workflow=args.commit,
        )
    if args.cmd == "recuperar":
        return cmd_recuperar(
            args.proyecto,
            args.checkpoint,
            args.destino,
            forzar_rama=args.rama,
        )
    if args.cmd == "evidenciar":
        return cmd_evidenciar(
            args.proyecto, args.tarea, args.origen, args.valor, args.cubre
        )
    if args.cmd == "presentar":
        return cmd_presentar(args.proyecto, args.tarea)
    if args.cmd == "verificar":
        return cmd_verificar(args.proyecto, args.tarea, args.fallo)
    if args.cmd == "depurar":
        return cmd_depurar(
            args.proyecto, args.tarea, args.hipotesis, args.resultado
        )
    if args.cmd == "dividir":
        return cmd_dividir(
            args.proyecto, args.padre, args.hijas, args.motivo, args.porque
        )
    if args.cmd == "bloquear":
        return cmd_bloquear(args.proyecto, args.tarea, args.motivo, args.marca)
    if args.cmd == "desbloquear":
        return cmd_desbloquear(args.proyecto, args.tarea, args.evidencia)
    if args.cmd == "operar":
        return cmd_operar(
            args.proyecto,
            args.resumen,
            args.pendientes,
            recuperacion=args.recuperacion,
        )
    if args.cmd == "demo":
        return cmd_demo()
    if args.cmd == "demo-b10":
        return cmd_demo_b10()
    if args.cmd == "demo-b11":
        return cmd_demo_b11()
    if args.cmd == "demo-b12":
        return cmd_demo_b12()
    if args.cmd == "demo-b13":
        return cmd_demo_b13()
    if args.cmd == "demo-b14":
        return cmd_demo_b14()
    if args.cmd == "recorrido-simple":
        return cmd_recorrido_simple()
    return 2


if __name__ == "__main__":
    sys.exit(main())

