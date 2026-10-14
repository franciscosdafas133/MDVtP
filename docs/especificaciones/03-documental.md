# ESP-03 — Contrato documental

Estado: borrador 0.3 · Fuente: encargo §5 · Decisiones: DEC-02, DEC-04/05 · Contratos: B08 · Requisitos: R04, R06, R07, R11

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
| `requisitos.md` | Escenarios y condiciones de aceptación identificables. Incluye **recorridos del usuario**: los pasos que da una persona en el producto (p. ej. «abre la app → elige peluquero → elige hora → confirma»), enlazados a los escenarios que los cubren. |
| `sistema.md` | Componentes, contratos, datos y recorridos vigentes. Incluye un apartado de **flujos de conexión entre sistemas** (qué pieza llama a cuál, servicios externos, credenciales) y de **flujos de datos** (qué dato nace dónde, por dónde pasa, dónde se guarda y cómo se recupera), con diagrama. |
| `decisiones/` | Una decisión significativa por registro (ESP-05). |
| `entregas/<id>/plan.md` y `tareas.md` | Incremento actual, límites, dependencias y terminación. |
| `verificacion.md` | Estrategia y referencias a evidencia versionada. |
| `operacion.md` | Entornos, configuración necesaria, entrega y recuperación. |
| `estado.json` | Estado de navegación y ejecución (ESP-04). |
| `tablero.md` | Vista legible **regenerable**; no es autoridad. |
| `eventos.jsonl` | Historial de transiciones y decisiones (ESP-04). |
| `checkpoints/` | Metadatos de puntos de recuperación (ESP-06). |

**Lista revisada con el usuario (2026-10-12):** el usuario acepta estos documentos como los necesarios para un buen producto, con dos añadidos suyos: flujos de conexión y de datos en `sistema.md`, y recorridos del usuario en `requisitos.md`. Quedan fuera, salvo que se pidan: bocetos de pantallas, negocio y marca.

**Metadatos mínimos de cada artefacto:** identificador, versión, estado, entradas relevantes, decisiones que lo condicionan y comprobación requerida.

**Cadena de trazabilidad:** `OBJ-01 → REQ-03 → DEC-02 → TASK-05 → CHECK-07 → EVID-04`. Las relaciones pueden ramificarse; no todo requisito necesita su propia decisión.

**Hecho e hipótesis (R04):** toda afirmación lleva estado (p. ej. confirmada / hipótesis / pendiente) y procedencia. Una hipótesis no pasa a requisito confirmado sin una transición explícita.

**Apuntes (R06):** cada comentario del usuario queda vinculado a la pregunta, decisión o requisito que comenta, y los pendientes quedan visibles.

**Proyectos pequeños:** se pueden fusionar documentos de contenido, pero se mantienen los identificadores y relaciones y nunca hay dos autoridades sobre el mismo dato.

**Cambio de requisitos (R11):** al cambiar un artefacto, se consultan sus relaciones y se marca lo dependiente como pendiente de revisión. Los resultados históricos se conservan, pero no valen como comprobación del nuevo estado.

**Mapa de lectura (apunte del usuario, 2026-10-12):** cada documento declara al principio de qué documentos depende y cuáles dependen de él, para que se lea en orden y se sepa qué revisar cuando cambia. Orden de lectura propuesto:

```
producto → descubrimiento → requisitos → sistema (+ decisiones) → plan y tareas → verificación → operación
```

Las flechas también se recorren hacia atrás: un cambio en un documento marca como pendiente de revisión lo que depende de él (R11). El mapa completo se deriva de esas declaraciones; no es una segunda autoridad.

## Cómo se revisa

Validador: `scripts/validate_workflow.py` (contratos en `core/contracts/`). Detecta ids inválidos, referencias rotas, evidencia `stale` y conflictos de decisión.

## Qué permite avanzar

Prefijos, relaciones y evidencia definidos → B09 puede generar plantillas Markdown alineadas a los mismos ids.

## Cerrado en B08

| Pregunta | Resolución |
|---|---|
| ¿Formato de metadatos? | **JSON de autoridad** (`relaciones.json`, `estado.json`, `evidencias.json`, `decisiones/*.json`). Markdown de producto con plantillas en B09; no hay segunda autoridad de enlaces. |
| ¿Dónde viven las relaciones? | **`workflow/relaciones.json`** (única autoridad mecánica). |
| ¿Estados de afirmación? | `confirmada` \| `hipotesis` \| `pendiente` (`vocabulario.json`). |
| ¿Versionado de evidencia? | `origen` = commit \| hash_archivo \| comando \| manual + `valor` + `cubre[]`; cambio de hash → `stale`. |

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿OpenSpec para formalizar más R11? | Solo si B10 se queda corto (condicional F09) |
