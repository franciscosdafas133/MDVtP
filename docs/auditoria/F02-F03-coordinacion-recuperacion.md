# Auditoría F02 y F03 — Coordinación y recuperación

Tarea: B04 · Fecha: 2026-10-12 · Autor: agente constructor · Estado: completada (condición de B04 cumplida; las propuestas son para B06)

| | F02 Spec Kit | F03 GSD Core |
|---|---|---|
| Fuente | [github/spec-kit](https://github.com/github/spec-kit) | [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core) |
| Commit | `0443760542e7e5269724744a2ac55c4bd386d095` | `b747aca5b1dcff699c36d90c5b9fca0ec6354c1c` |
| Licencia raíz | MIT (© GitHub, Inc.) | MIT (© 2026 Open GSD) |
| Ejecutado | Nada | Nada |

Regla de esta comparación (encargo, B04): **sus modelos de estado se describen por separado y no se mezclan.** Las propuestas finales toman ideas concretas de cada uno, no su estado.

## 1. Qué se leyó

| Fuente | Pieza | Lectura |
|---|---|---|
| F02 | `workflows/ARCHITECTURE.md` | Completa |
| F02 | `workflows/speckit/workflow.yml` | Completa |
| F02 | `engine.py` (`RunState.save`, `_atomic_write_json`) | Fragmento dirigido (líneas 730–810) |
| F02 | `step/gate/__init__.py` | Cabecera y contrato (primeras 60 líneas) |
| F02 | `step/command/__init__.py` | Búsqueda dirigida (despacho a la integración) |
| F02 | `integrations/_file_changes.py`, `manifest.py`, `command_uninstall.py`, `cursor_agent/__init__.py`, `claude/__init__.py` | Leídos con `git show`, fuera de la selección sparse; búsquedas dirigidas, salvo la cabecera completa de `_file_changes.py` |
| F02 | `pyproject.toml` (dependencias) | Completa |
| F02 | `workflows/README.md`, `PUBLISHING.md`, resto de `engine.py`, `_execution.py`, `expressions.py`, `templates/` | **No leídos** |
| F03 | `commands/gsd/progress.md`, `commands/gsd/undo.md` | Completa |
| F03 | `gsd-core/workflows/progress.md` | Inicialización, carga y tabla de enrutamiento (líneas 1–124 y 320–345); resto por títulos |
| F03 | `gsd-core/workflows/undo.md` | Estructura por pasos y salvaguardas (búsqueda dirigida); conflicto y commit completos (540–600) |
| F03 | `gsd-core/workflows/pause-work.md` | Búsqueda dirigida (handoff, estado) |
| F03 | `gsd-core/references/checkpoints.md` | Visión general (líneas 1–30) |
| F03 | `docs/ARCHITECTURE.md` | Principios, estructura de archivos, instalador, matriz de runtimes, escritura de `STATE.md` (fragmentos) |
| F03 | `package.json` (engines, dependencias) | Fragmento |
| F03 | `gsd-core/bin/` (`gsd-tools.cjs`), `resume-project.md`, `next.md`, hooks, agentes | **No leídos** (fuera de la selección o no prioritarios) |

## 2. Naturaleza de cada sistema

- **Spec Kit — motor externo.** `specify workflow run` es un CLI en Python que carga un YAML, ejecuta los pasos uno a uno y **lanza al agente como subproceso** (`command` → CLI de la integración). El agente no lleva la coordinación: la lleva el motor. Las puertas (`gate`) son preguntas en el terminal; sin terminal interactivo, el motor pausa y se retoma con `specify workflow resume <run_id>`.
- **GSD Core — instrucciones con un CLI auxiliar.** Los comandos y workflows son Markdown que sigue el agente. Para el estado y el enrutamiento, el agente llama a un CLI en Node (`gsd-tools.cjs`), que devuelve JSON (`init.progress`, `roadmap.analyze`, `verification.status`, `state-snapshot`). Hay ~72 comandos, ~109 workflows y ~67 skills, más agentes y hooks propios por runtime.

## 3. Matriz de mecanismos

| Mecanismo | Spec Kit (F02) | GSD Core (F03) | Requisitos |
|---|---|---|---|
| **Quién coordina** | El motor (código). El agente es un paso. | El agente, guiado por Markdown; el CLI calcula datos | R02, R08 |
| **Estado** | `.specify/workflows/runs/<run_id>/state.json` + `inputs.json` + `log.jsonl` (eventos, solo se añade) | `.planning/STATE.md` (cuerpo autoritativo, frontmatter rederivado), `ROADMAP.md`, carpetas por fase, `HANDOFF.json` | R13, R19 |
| **Transiciones** | Estados de ejecución `CREATED → RUNNING → COMPLETED/PAUSED/FAILED/ABORTED`; `PAUSED/FAILED → resume`. Toda mutación pasa por `Execution.transition()` con listas de fases y campos permitidos; quien llama no elige la fase destino | Implícitas en archivos (planes frente a resúmenes, estado de verificación). El enrutamiento se calcula, no se almacena | R19 |
| **Escritura atómica** | Sí: archivo temporal + `os.replace`, bajo un cerrojo del run; si un checkpoint falla, esa instancia ya no puede escribir | `STATE.md.lock` con creación atómica `O_EXCL` para evitar carreras entre agentes (según la arquitectura; código no leído) | R13, R19 |
| **Eventos** | `log.jsonl`; los eventos se emiten **después** del checkpoint; al reanudar, los pasos completados se reproducen sin repetir efectos | Commits git por tarea y por pausa (`wip: … paused at X/Y`) | R13, E12 |
| **Reanudación** | Valida estructura, instantánea y offset **antes de escribir**; continúa en la ocurrencia sin terminar | `pause-work` escribe `HANDOFF.json` y `.continue-here.md`; `uncommitted_files` «measured, never asserted» (de un comando real, no de memoria) | R13, E06 |
| **Siguiente paso** | El siguiente paso del YAML (o rama `if/switch`) | **Tabla de rutas ordenada** (A–F, E.2, V.*), evaluada de arriba abajo con datos del CLI; gana la primera que coincide | R08 |
| **Verificación obsoleta** | — | `verification.status` devuelve `stale` si el código cubierto cambió después de verificar, y `missing` si falta el informe; solo `passed` cuenta como fase completa | R14, R19 |
| **Puertas humanas** | `gate`: `approve/reject`, `on_reject: abort/skip/retry`, pausa sin TTY | Checkpoints de plan: `human-verify`, `decision`; `gate="blocking-human"` **nunca** se aprueba solo, ni en modo automático | R05 |
| **Avance automático** | El YAML se ejecuta sin intervención salvo en las puertas | `--next --auto` encadena pasos; `--next --force` **salta las salvaguardas** | R02 |
| **Deshacer / recuperación** | — (reanudar un run no es recuperar código) | `undo`: `git revert --no-commit` de los commits de una fase o plan **en la rama activa**; rechaza el árbol sucio; comprueba dependencias aguas abajo; confirmación previa; un único commit de revert | R11, R12, E11 |
| **Instalación / retirada** | Manifiesto por integración con **SHA-256 por archivo**; al desinstalar solo borra lo no modificado y conserva y lista lo modificado (`--force` para todo) | `gsd-file-manifest.json` (con runtime y alcance); `--uninstall` borra archivos, hooks y ajustes; copia de seguridad de archivos modificados en `gsd-local-patches/` | R16, E14 |
| **Hosts** | Claude: `.claude/skills`; Cursor: `.cursor/skills/speckit-*`. El despacho de workflows a Cursor usa `cursor-agent -p --trust --approve-mcps --force` | Claude: global `~/.claude/skills` o local `commands/gsd`; Cursor: `~/.cursor` o `./.cursor` + `hooks.json` (sessionStart, monitor de `STATE.md`). Importaciones `@~/.claude/...` reescritas por runtime | R01 |
| **Dependencias** | Python + typer, click, rich, readchar, pyyaml, packaging, pathspec, json5, mcp, pydantic | Node ≥ 24, npm ≥ 10, `@anthropic-ai/claude-agent-sdk`, `ws`; instalador de ~10 700 líneas | §12 del encargo |
| **Tamaño** | Motor ~740 KB de Python en `workflows/` | 72 comandos, 109 workflows, 100+ referencias | — |

## 4. Hallazgos

| ID | Hallazgo | Consecuencia |
|---|---|---|
| C1 | El motor de Spec Kit es la única pieza estudiada con **garantías reales** de estado: escritura atómica, transiciones con listas permitidas, eventos después del checkpoint y reanudación validada antes de escribir. | Copiar su **contrato**, no su código: un validador pequeño puede aplicar las mismas reglas a nuestro `estado.json` y `eventos.jsonl` (ESP-04). |
| C2 | Adoptar el motor exige que **el motor lance al agente**, en modo no interactivo y con permisos amplios (`--trust --approve-mcps --force` en Cursor). Eso sustituye la conversación con el coordinador por un terminal. | Contradice R02 (conversar con un coordinador) y nuestras reglas de seguridad. **No adoptar el motor.** Resuelve la «decisión pendiente» del encargo §7 a favor de un validador pequeño (pendiente de confirmar en B06). |
| C3 | La tabla de rutas de GSD (ordenada, evaluada sobre datos que calcula un programa) es el mejor modelo para el «siguiente paso y por qué» (R08). | **Inspiración** para ESP-02: el validador calcula los datos y el coordinador aplica la tabla. |
| C4 | La detección de verificación `stale` de GSD es exactamente nuestra regla de evidencia vigente (R14, N-39). | **Inspiración** para ESP-04/ESP-08: la evidencia guarda el commit o hash que cubre y se invalida si cambia. |
| C5 | `gate="blocking-human"` resuelve un problema real: el modo automático puede «decidir por el usuario». | Adoptar la idea: las decisiones de producto siempre son `blocking-human` (R05, N-32). |
| C6 | `undo` de GSD revierte **en la rama activa**. Es seguro (árbol limpio obligatorio, dependencias, confirmación), pero no es la recuperación aislada de R12 (rama o worktree desde un checkpoint, conservando el trabajo posterior). | R12 requiere desarrollo propio. De GSD se toman la comprobación de dependencias, el árbol limpio y la confirmación. |
| C7 | La limpieza de conflictos de `undo` ejecuta `git reset HEAD` + `git restore .`. Es seguro solo porque exige árbol limpio al principio. | Si adaptamos algo parecido, la precondición debe ser comprobable, no confiar en la instrucción (N-48, N-49). |
| C8 | «Checkpoint» significa cosas distintas: en GSD, un punto de interacción humana dentro de un plan; en el encargo, un punto de recuperación. | Fijar el vocabulario en ESP-03/ESP-06: «checkpoint» = punto de recuperación; las paradas humanas se llamarán «puertas». |
| C9 | Ambos instaladores registran los archivos instalados en un manifiesto; Spec Kit además compara SHA-256 y conserva lo modificado. | **Modelo para R16** (ESP-07): manifiesto con hash y retirada que no toca lo modificado. |
| C10 | GSD instala globalmente en `~/.claude/` por defecto y escribe hooks y ajustes. | Contrario a la instalación limitada al proyecto que buscamos (R16). Por defecto, instalación local. |
| C11 | Ambos sistemas son muy grandes (motor de 740 KB; ~300 archivos de instrucciones). | Confirma el criterio del encargo §12: no introducir una dependencia para copiar una arquitectura ajena. |

## 5. Qué demuestra la evidencia de cada fuente y qué no

- Spec Kit documenta el diseño del motor; **no hemos ejecutado sus tests**. Ninguno de los fragmentos leídos prueba el comportamiento con Claude Code o Cursor en modo conversacional.
- GSD declara el cerrojo de `STATE.md`, la detección de `stale` y el instalador con manifiesto; **no hemos leído el código de `gsd-tools.cjs`** (fuera de la selección). Antes de reutilizar cualquier idea como contrato, el diseño propio debe probarse con nuestros casos (B17), no con la palabra de la fuente.

## 6. Propuesta para B06

| Necesidad | Propuesta | Origen | Tipo |
|---|---|---|---|
| Estado y transiciones (R13, R19) | Validador propio pequeño: escritura atómica (temporal + rename), transiciones con lista permitida, evento escrito después del estado y reconciliación al reanudar | Contrato de F02 | Desarrollo propio inspirado |
| Siguiente paso (R08) | El validador calcula hechos (tareas preparadas, bloqueos, evidencia obsoleta) y el coordinador aplica una tabla de rutas ordenada | F03 `progress` | Inspiración |
| Evidencia vigente (R14) | La evidencia registra el commit o el hash cubierto; un cambio la marca obsoleta | F03 `verification.status` | Inspiración |
| Puertas humanas (R05) | Las decisiones de producto nunca se aprueban en automático | F03 `blocking-human` | Inspiración |
| Recuperación (R12) | Rama o worktree desde un commit de checkpoint, con árbol limpio o cambios protegidos, dependencias revisadas y confirmación | F03 `undo` (salvaguardas) + desarrollo propio | Desarrollo propio |
| Instalación (R16) | Manifiesto con SHA-256, instalación local y retirada que conserva lo modificado | F02 `manifest.py` | Adaptar |
| Runtime del validador | Node 24 o Python 3.13 (ambos presentes; `npm` y `pip` sin confirmar). Sin dependencias externas si es posible | Entorno B01 | **Decisión de B07** |
| Motor de Spec Kit y runtime de GSD | No adoptar | C2, C11 | Descartar como dependencia |

## 7. Preguntas que quedan

1. ¿El validador lo invoca el agente (como `gsd-tools`) o un hook del host antes y después de cada acción? Depende de lo que Claude Code y Cursor permitan de verdad. → B07, B15.
2. ¿`pip` o `npm` están disponibles en el entorno de los usuarios? Para no depender de ellos, el validador debería usar solo la biblioteca estándar. → B07.
3. ¿Hace falta registrar sesiones paralelas (`workstreams`, fan-out)? El encargo no lo pide; dejarlo fuera salvo que B05 encuentre una necesidad.
