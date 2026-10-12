# ESP-03 — Contrato documental

Estado: borrador 0.1 · Fuente: encargo §5 · Requisitos: R04, R06, R07, R11

## Qué la inicia

La creación o modificación de cualquier artefacto en la carpeta `workflow/` de un proyecto de usuario.

## Qué produce

Documentos con identificador, procedencia, versión, autoridad y enlaces, de modo que un resultado de producto pueda seguirse hasta su evidencia.

## Fijado por el encargo

**Carpeta propuesta `workflow/` en el proyecto del usuario:**

| Registro | Autoridad |
|---|---|
| `producto.md` | Problema, usuarios, resultados, restricciones y alcance vigente. |
| `descubrimiento.md` | Hechos, hipótesis, preguntas y experimentos. |
| `requisitos.md` | Escenarios y condiciones de aceptación identificables. |
| `sistema.md` | Componentes, contratos, datos y recorridos vigentes. |
| `decisiones/` | Una decisión significativa por registro (ESP-05). |
| `entregas/<id>/plan.md` y `tareas.md` | Incremento actual, límites, dependencias y terminación. |
| `verificacion.md` | Estrategia y referencias a evidencia versionada. |
| `operacion.md` | Entornos, configuración necesaria, entrega y recuperación. |
| `estado.json` | Estado de navegación y ejecución (ESP-04). |
| `tablero.md` | Vista legible **regenerable**; no es autoridad. |
| `eventos.jsonl` | Historial de transiciones y decisiones (ESP-04). |
| `checkpoints/` | Metadatos de puntos de recuperación (ESP-06). |

**Metadatos mínimos de cada artefacto:** identificador, versión, estado, entradas relevantes, decisiones que lo condicionan y comprobación requerida.

**Cadena de trazabilidad:** `OBJ-01 → REQ-03 → DEC-02 → TASK-05 → CHECK-07 → EVID-04`. Las relaciones pueden ramificarse; no todo requisito necesita su propia decisión.

**Hecho e hipótesis (R04):** toda afirmación lleva estado (p. ej. confirmada / hipótesis / pendiente) y procedencia. Una hipótesis no pasa a requisito confirmado sin una transición explícita.

**Apuntes (R06):** cada comentario del usuario queda vinculado a la pregunta, decisión o requisito que comenta, y los pendientes quedan visibles.

**Proyectos pequeños:** se pueden fusionar documentos de contenido, pero se mantienen los identificadores y relaciones y nunca hay dos autoridades sobre el mismo dato.

**Cambio de requisitos (R11):** al cambiar un artefacto, se consultan sus relaciones y se marca lo dependiente como pendiente de revisión. Los resultados históricos se conservan, pero no valen como comprobación del nuevo estado.

## Cómo se revisa

Un validador determinista (B08) detecta identificadores duplicados, referencias rotas y evidencia que apunta a una versión superada.

## Qué permite avanzar

Prefijos, formato de metadatos y tipos de relación definidos → ESP-04 y ESP-05 pueden referirse a ellos sin ambigüedad.

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿Formato de metadatos: front matter YAML, bloques en Markdown o un índice JSON aparte? | B07, B08 |
| ¿Dónde viven las relaciones: en cada documento o en un índice derivado? | B07 (evitar dos autoridades) |
| ¿Vocabulario cerrado de estados de una afirmación? | B08 |
| ¿Cómo se versiona la evidencia (hash, commit, fecha)? | B07, B08 |
| ¿Qué piezas de OpenSpec (cambios frente a especificación vigente) ayudan a formalizar R11? | B05 (condicional) |
