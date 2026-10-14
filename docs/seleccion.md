# Selección de base, extracciones y mapa de cobertura

Tarea: B06 · Fecha: 2026-10-12 · Estado: verificada (DEC-01…08 aceptadas)

## 1. Base

**Aceptada (DEC-01):** reutilizar y conectar las piezas buenas de las fuentes (X01–X21) y construir solo lo que las une: el coordinador, el registro común y los adaptadores por host. Las fuentes no se instalan tal cual; cada pieza se adapta para escribir en el registro común.

## 2. Extracciones mínimas

Cada fila es una pieza que se incorporará. «Tipo» indica: **copia adaptada** (texto reutilizado y modificado), **síntesis** (dos fuentes combinadas en un procedimiento) o **inspiración** (idea sin texto).

| ID | Pieza propia prevista | Origen (ruta en la fuente) | Tipo | Licencia | Destino | Implementa en |
|---|---|---|---|---|---|---|
| X01 | Protocolo de verificación | F01 `kiro-verify-completion/SKILL.md` + F07 `verification-before-completion/SKILL.md` | Síntesis (DEC-04) | MIT ×2 | ESP-02, ESP-08 | B13 |
| X02 | Protocolo de depuración | F07 `systematic-debugging/SKILL.md` + F01 `kiro-debug/SKILL.md` | Síntesis (DEC-05) | MIT ×2 | ESP-02 | B13 |
| X03 | Protocolo de revisión de tarea | F01 `kiro-review/SKILL.md` | Copia adaptada | MIT | ESP-02 | B13 |
| X04 | Bucle de implementación por tarea (una tarea, salida estructurada, rondas acotadas, staging selectivo, sin reset destructivo) | F01 `kiro-impl/SKILL.md` | Copia adaptada (sin `tasks.md`/`spec.json` como estado) | MIT | ESP-02, ESP-04 | B13 |
| X05 | Reglas de división de tareas y condición observable de terminación (sin horas) | F01 `shared/settings/rules/tasks-generation.md` | Copia adaptada | MIT | ESP-02, plantillas | B12 |
| X06 | Descubrimiento: rutas por tamaño, preguntas secuenciales, 2–3 enfoques, comprobación de viabilidad | F01 `kiro-discovery/SKILL.md` | Copia adaptada (sin paradas) | MIT | ESP-02 | B09 |
| X07 | Revisión de áreas de §2 y etiquetas de supuesto | F05 `bmad-prd` «Concern scan», `[ASSUMPTION]`; F04 `create_plan` «investigar antes de preguntar» | Inspiración | — | ESP-02, ESP-03 | B09 |
| X08 | Acción «profundizar» sobre una propuesta (pocos métodos: pre-mortem, red team, primeros principios; aplicar/rechazar) | F05 `bmad-advanced-elicitation` | Inspiración | — | ESP-02, ESP-05 | B09 |
| X09 | Análisis de impacto al reabrir (antiguo → nuevo con justificación; lista de comprobación) | F05 `bmad-correct-course` | Inspiración | — | ESP-05 | B10 |
| X10 | Contrato de estado: transiciones con lista permitida, escritura atómica, evento después del estado, reanudación validada | F02 `workflows/ARCHITECTURE.md`, `engine.py` (`save`, `_atomic_write_json`) | Inspiración (contrato) | — | ESP-04, validador | B08, B10 |
| X11 | Tabla de rutas ordenada para el siguiente paso | F03 `gsd-core/workflows/progress.md` | Inspiración | — | ESP-02 | B09 |
| X12 | Evidencia `stale` por cambio del código cubierto | F03 `verification.status` (descrito en `progress.md`) | Inspiración | — | ESP-03, ESP-04 | B08 |
| X13 | Puerta humana no automatizable | F03 `references/checkpoints.md` (`gate="blocking-human"`) | Inspiración | — | ESP-05 | B09 |
| X14 | Recuperación aislada: detectar aislamiento, herramienta nativa primero, `check-ignore`, línea base | F07 `using-git-worktrees/SKILL.md` | Copia adaptada (sin instaladores automáticos; desde commit de checkpoint) | MIT | ESP-06 | B11 |
| X15 | Salvaguardas de reversión: árbol limpio, dependencias aguas abajo, confirmación | F03 `gsd-core/workflows/undo.md` | Inspiración | — | ESP-06 | B11 |
| X16 | Traspaso medido: archivos sin commit sacados de un comando real, no de memoria | F03 `pause-work.md` (`uncommitted_files`) | Inspiración | — | ESP-04 | B10 |
| X17 | Manifiesto de instalación con SHA-256; retirada que conserva lo modificado | F02 `integrations/manifest.py`, `command_uninstall.py` | Inspiración | — | ESP-07 | B16 |
| X18 | Seguridad de rutas del instalador (dentro del proyecto, sin enlaces simbólicos) | F01 `src/utils/pathSafety.ts`, `plan/executor.ts` | Inspiración | — | ESP-07 | B16 |
| X19 | Criterios de éxito automáticos frente a manuales; «lo que no hacemos» | F04 `create_plan.md` | Inspiración | — | plantillas | B09, B12 |
| X20 | Evaluación: controles limpios, defectos sembrados, rutas neutras, clave fuera del espacio de trabajo, salidas 0/1/2, resultado con procedencia | F06 `docs/explanation/how-tea-is-tested.md`, `test/results/*.json` | Inspiración | — | ESP-08 | B17, B18 |
| X21 | Pruebas de presión de comportamiento | F07 `systematic-debugging/test-pressure-*.md` | Inspiración | — | ESP-08 | B18 |

**No se extrae nada de:** `spec.json`/aprobaciones de cc-sdd (H3), el motor de Spec Kit (DEC-02), el runtime y los hooks de GSD, el modelo de roles y personas de BMAD, el arnés de TEA ni los agentes y la carpeta `thoughts/` de HumanLayer.

## 3. Mapa de cobertura R01–R20

Cada requisito tiene una solución prevista: extracción (X*) o desarrollo propio explícito (P*).

| Req. | Solución prevista | Piezas | Especificación | Implementa | Riesgo / pendiente |
|---|---|---|---|---|---|
| R01 | **P01** Núcleo canónico + adaptador por host que solo transforma lo propio del host (metadatos, invocación, subagentes); modo secuencial siempre disponible | — (lección de H4) | ESP-07 | B15, B19 | Sin evidencia de terceros en Cursor (K8) |
| R02 | **P02** Skill coordinadora única con acciones iniciar, continuar, estado, decidir, anotar, reabrir, recuperar y verificar | X11 | ESP-02 | B09 | Comprobar invocación por conversación frente a argumentos en cada host |
| R03 | **P03** Descubrimiento por áreas de §2 (aplica / se sabe / falta / cómo averiguarlo) | X06, X07, X19 | ESP-02 | B09 | — |
| R04 | **P04** Estado de afirmación (confirmada, hipótesis, pendiente) con procedencia; transición explícita a requisito | X07 | ESP-03 | B08, B09 | Vocabulario cerrado en B08 |
| R05 | **P05** Registro de decisiones con estados y sustitución; aceptación explícita y acotada; puertas humanas | X08, X13 | ESP-05 | B09 | — |
| R06 | **P06** Apuntes enlazados a pregunta, decisión o requisito; pendientes visibles | — | ESP-03, ESP-05 | B10 | — |
| R07 | **P07** Identificadores y relaciones `OBJ → REQ → DEC → TASK → CHECK → EVID` con consulta mecánica | (TEA `trace` como referencia) | ESP-03 | B08 | Dónde viven las relaciones (B07) |
| R08 | **P08** Informe de estado calculado por el validador + tabla de rutas | X11, X16 | ESP-02, ESP-04 | B10 | — |
| R09 | Reglas de división sin horas | X05 | ESP-02 | B12 | — |
| R10 | **P10** Registro de dependencias reales; marca simulación frente a integración real; `MANUAL_VERIFY_REQUIRED` | X01, X02 | ESP-03, ESP-04 | B12 | — |
| R11 | **P11** Invalidación mecánica por relaciones + revisión con formato antiguo → nuevo | X09, X12 | ESP-03, ESP-05 | B10 | F09 si hace falta más formalización (B08) |
| R12 | **P12** Checkpoint (commit + metadatos) y recuperación en rama/worktree desde él | X14, X15 | ESP-06 | B11 | Proyectos sin git |
| R13 | **P13** Reconstrucción desde `estado.json`, `eventos.jsonl`, documentos y árbol de trabajo | X10, X16 | ESP-04 | B10, B17 | — |
| R14 | Protocolo único + evidencia vigente | X01, X03, X12 | ESP-04, ESP-08 | B13 | — |
| R15 | Protocolo único de depuración | X02, X04 | ESP-02 | B13 | — |
| R16 | Instalación local con manifiesto | X17, X18 | ESP-07 | B16 | Runtime del instalador (B07) |
| R17 | **P17** Profundidad por riesgo: rutas por tamaño + camino rápido o acompañado | X06 | ESP-01, ESP-02 | B09, B21 | Criterios de riesgo (B07) |
| R18 | **P18** Entrega, operación y mantenimiento propios (ninguna fuente lo cubre) | (smoke boot de X01) | ESP-02, ESP-06 | B14, B20 | **Ausencia en las fuentes**; F10 como referencia posterior |
| R19 | **P19** Validador determinista | X10, X12 | ESP-04 | B08, B17 | Runtime (B07) |
| R20 | **P20** Versionado de contratos y migración de `workflow/` | — | ESP-07 | B22 | Guías de migración de F01/F03 sin leer |

**Requisitos sin solución prevista:** ninguno. Cinco tienen poca o ninguna referencia en las fuentes y son los de mayor riesgo para B07: R01 (parte de Cursor), R06, R07, R18 y R20.

## 4. Qué permite avanzar

DEC-01 a DEC-08 aceptadas (2026-10-12). B06 verificada; B07 puede completar las especificaciones con esta selección como entrada.
