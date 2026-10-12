# Auditoría F04–F07 — Complementos

Tarea: B05 · Fecha: 2026-10-12 · Autor: agente constructor · Estado: completada (condición de B05 cumplida; las clasificaciones son propuestas para B06)

| ID | Fuente | Commit | Licencia raíz | Copia local (sparse) |
|---|---|---|---|---|
| F04 | [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) | `99abe673…` | Apache-2.0 | `.claude/commands`, `.claude/agents` |
| F05 | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | `bda3c592…` | MIT + **política de marca** (`TRADEMARK.md`) | `skills/bmad-{product-brief,prd,advanced-elicitation,architecture,correct-course}` |
| F06 | [bmad-code-org/bmad-method-test-architecture-enterprise](https://github.com/bmad-code-org/bmad-method-test-architecture-enterprise) | `a5675c35…` | MIT (ver marca de F05) | `skills/bmad-testarch-{test-design,trace,evaluate}`, `docs/explanation`, `test` |
| F07 | [obra/superpowers](https://github.com/obra/superpowers) | `bb92a777…` | MIT | `skills/{systematic-debugging,verification-before-completion,using-git-worktrees}` |

Nada se ha ejecutado. Las huellas SHA-256 de las licencias están en `sources.lock.json`.

## 1. Qué se leyó

| Fuente | Pieza | Lectura |
|---|---|---|
| F07 | `verification-before-completion/SKILL.md` | Completa |
| F07 | `systematic-debugging/SKILL.md` | Fases 1–4 y regla de 3 intentos (sin líneas vacías, ~150 líneas) |
| F07 | `systematic-debugging/CREATION-LOG.md`, `test-pressure-1.md` | Inicio (40 y 30 líneas) |
| F07 | `using-git-worktrees/SKILL.md` | Completa |
| F07 | `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting*.md`, `find-polluter.sh`, demás pruebas de presión | **No leídos** |
| F04 | `create_plan.md` | Pasos 1–4 completos; plantilla y pautas por búsqueda dirigida |
| F04 | `validate_plan.md` | Hasta el informe (80 líneas) |
| F04 | `research_codebase.md`, `.claude/agents/*` | **No leídos** (solo nombres) |
| F05 | `bmad-correct-course/SKILL.md` | Activación y pasos 1–3 (~110 líneas) |
| F05 | `bmad-correct-course/checklist.md` | Estructura (6 secciones, 23 puntos) |
| F05 | `bmad-advanced-elicitation/SKILL.md` | Completa hasta «Running a Method»; catálogo `methods.csv` (cabecera, 71 métodos) |
| F05 | `bmad-product-brief` (plantilla completa; SKILL por búsqueda), `bmad-prd` (búsqueda dirigida) | Parcial |
| F05 | `bmad-architecture` | **No leído** (solo tamaños) |
| F05 | `TRADEMARK.md` | Primeras 40 líneas |
| F06 | `docs/explanation/how-tea-is-tested.md` | Secciones 1–6 |
| F06 | `docs/explanation/how-evaluate-works.md` | Introducción y diagrama |
| F06 | `test/results/` | Listado, un resultado JSON (cabecera), recuento de agentes, modelos y versiones |
| F06 | `bmad-testarch-trace` (SKILL inicial y plantilla por búsqueda) | Parcial |
| F06 | `bmad-testarch-test-design`, `bmad-testarch-evaluate` | **Solo estructura de carpetas** |

## 2. Dependencias de entorno que traen

| Fuente | Supuestos del entorno original |
|---|---|
| F04 | Exclusiva de Claude Code: `.claude/commands`, frontmatter `model: opus`, agentes con nombre propio (`codebase-locator`, `thoughts-analyzer`…), carpeta `thoughts/` del equipo, Linear, `make check test`, TodoWrite |
| F05 | Instalación `_bmad/` en el proyecto; `uv run …/_bmad/scripts/resolve_customization.py`; `npx skills add …`; `customize.toml` en tres capas; personas («Agent communication style»); salida en `{output_folder}/{active_initiative}/` |
| F06 | Igual que F05 + `bmod-tea/knowledge`; CLI `tea-evaluate`; Node para el arnés; ejecuciones con CLIs de agentes en modo headless |
| F07 | Mínimos: Markdown + `git`. `using-git-worktrees` ejecuta instaladores de dependencias (`npm install`, `pip install`, `poetry install`) en el paso 2 |

## 3. Piezas por función

### 3.1 Verificación antes de dar por terminado (R14) — un solo protocolo

| Aspecto | cc-sdd `kiro-verify-completion` (F01) | superpowers `verification-before-completion` (F07) |
|---|---|---|
| Regla central | Evidencia fresca acorde al alcance de la afirmación | «NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE» |
| Tipos de afirmación | `TASK`, `FIX`, `TEST_OR_BUILD`, `FEATURE_GO` | Tabla por tipo (tests, linter, build, bug, regresión, agente, requisitos) |
| Resultado | `VERIFIED` / `NOT_VERIFIED` / **`MANUAL_VERIFY_REQUIRED`** | Sin formato; el agente informa del estado real |
| Entorno no disponible | Explícito → `MANUAL_VERIFY_REQUIRED` | No contemplado |
| Señales de alarma | Tabla de racionalizaciones | Más completa: lenguaje («should», «probably», «Great!»), cansancio, «just this once» |
| Regresión | `FIX` sin regresiones | Ciclo rojo-verde: revertir la reparación debe hacer fallar el test |

**Propuesta:** base cc-sdd (salida estructurada y el estado `MANUAL_VERIFY_REQUIRED`, necesario para E04, E09 y N-45), con las señales de alarma y el ciclo rojo-verde de superpowers. Un único protocolo sintetizado con las diferencias documentadas (regla H-21).

### 3.2 Depuración (R15, E10) — un solo protocolo

| Aspecto | cc-sdd `kiro-debug` (F01) | superpowers `systematic-debugging` (F07) |
|---|---|---|
| Reproducción | No exigida explícitamente | **Exigida** («If not reproducible → gather more data, don't guess») |
| Hipótesis | Causa raíz primero, plan mínimo | **Una sola hipótesis cada vez**, cambio mínimo, una variable |
| Límite de intentos | 2 rondas de debug por tarea → `_Blocked:_` | **≥ 3 reparaciones fallidas → parar y cuestionar la arquitectura** |
| Sistemas con varios componentes | — | Instrumentar cada frontera antes de reparar |
| Salida | Estructurada: `ROOT_CAUSE`, `CATEGORY` (10 categorías), `FIX_PLAN`, `NEXT_ACTION: RETRY / BLOCK / STOP_FOR_HUMAN`, `CONFIDENCE` | Prosa |
| Escalado | `STOP_FOR_HUMAN` ante credenciales, hardware o conflicto de spec | «Say "I don't understand X"… Ask for help» |
| Prueba del protocolo | Sondas en Antigravity (según la fuente) | **Pruebas de presión** con escenarios (`test-pressure-*.md`) |

**Propuesta:** método de superpowers (reproducir → patrón → hipótesis única → reparación con test que falla; parar a los 3 intentos) con el informe estructurado y las categorías de cc-sdd. Cubre R15 y E10 mejor que cualquiera de los dos por separado.

### 3.3 Recuperación aislada (R12, E11)

`using-git-worktrees` (F07) aporta:
- Detectar si ya estás en un worktree (con la salvedad de los submódulos).
- Preferir la herramienta nativa del host (por ejemplo `EnterWorktree`) en lugar de `git worktree add`, que crearía estado que el host no ve.
- Comprobar con `git check-ignore` que la carpeta de worktrees está ignorada.
- Línea base de tests antes de empezar.

Límites:
- Crea el worktree desde la rama actual, no desde el commit de un checkpoint (ampliarlo con `git worktree add <ruta> -b <rama> <commit>`).
- **Ejecuta instaladores de dependencias automáticamente**, en contra de N-06 y de nuestra prudencia con los efectos externos. No adoptar ese paso: proponerlo y pedir confirmación.

**Propuesta:** adaptar como procedimiento de ESP-06, junto con las salvaguardas de `undo` de GSD (B04: árbol limpio, dependencias, confirmación).

### 3.4 Descubrimiento, hipótesis y decisiones (R03, R04, R05, R06)

| Pieza | Aporte | Propuesta |
|---|---|---|
| F05 `bmad-product-brief` / `bmad-prd` | Etiquetas **`[ASSUMPTION]`** donde el agente infirió algo; triaje final de preguntas abiertas y supuestos («phase-blockers» de uno en uno); **`.memlog.md`** como registro de solo añadir de cada decisión, cambio y anulación; «Concern scan» (cumplimiento, integraciones, SLA, hardware, API pública); «Elicitation, not direction» (sacar la visión del usuario, no imponer la propia); camino rápido frente a camino acompañado | **Inspiración fuerte** para ESP-03 (estado de las afirmaciones), ESP-05 (registro) y R17. Ojo: `.memlog.md` y nuestro `eventos.jsonl` serían dos autoridades; usar solo el nuestro |
| F05 `bmad-advanced-elicitation` | Menú de métodos de crítica (71: pre-mortem, red team, primeros principios…); **«Never change the work unless the user accepts the proposal»**; aplicar / rechazar / redirigir | **Inspiración**: «profundizar» como acción del coordinador sobre una propuesta. El catálogo puede reducirse a unos pocos métodos sin el script `pick_methods.py` |
| F04 `create_plan` | Antes de preguntar, investigar; preguntar solo lo que el código no responde; **verificar con investigación las correcciones del usuario**; secciones «What We're NOT Doing» y criterios de éxito **automáticos frente a manuales**, con pausa para la confirmación humana de lo manual | **Inspiración** para ESP-02 y la plantilla de plan/tareas |
| F04 `validate_plan` | Comparar plan frente a implementación por fase; ejecutar las verificaciones automáticas; listar lo manual con pasos | **Redundante** con `kiro-validate-impl`; tomar solo «manual = pasos claros para el usuario» |

### 3.5 Cambio de dirección e impacto (R11, E07)

`bmad-correct-course` (F05) aporta:
- Una lista de comprobación de impacto en 6 secciones y 23 puntos: disparador, épicas, conflictos con artefactos, camino a seguir, propuesta y traspaso.
- Cada punto con estado `[x]` / `[N/A]` / `[!]`.
- Propuestas de edición en formato **antiguo → nuevo con justificación**.
- Modo incremental o en bloque.
- `HALT` si el disparador no está claro.

**Propuesta:**
- **Inspiración** para la acción `reabrir` (ESP-05).
- La lista de comprobación es manual; en nuestro paquete, el primer paso del análisis de impacto debe salir de las relaciones registradas (consulta mecánica). Después, la revisión humana con el formato antiguo → nuevo.
- No trasladar su modelo de roles ni el sprint (N-13).

### 3.6 Evaluación del propio método (ESP-08, B18)

TEA (F06) es el modelo de evaluación más completo de las fuentes:

| Mecanismo de TEA | Nuestra regla o escenario |
|---|---|
| Tres niveles: deterministas en CI, conductuales con agentes reales y evidencia registrada | ESP-08: deterministas frente a observaciones del agente |
| **Controles limpios** y **defectos sembrados** por suite | E15; casos sanos y con defecto (B18) |
| **Rutas neutras**: los directorios de fixtures no llevan palabras como `gapped`, `clean` o `control` | N-42 |
| Respuestas correctas fuera del espacio de trabajo; detector de fugas | «Evidencia independiente de la autoevaluación» (B18) |
| Citas validadas contra archivos reales; citar uno inexistente penaliza como evidencia fabricada | N-29, R14 |
| Repeticiones y techos de estabilidad declarados por suite | §10 del encargo: umbral por escenario y riesgo |
| **Salidas 0 = pasa, 1 = fallo de calidad, 2 = fallo de entorno** (sin puntuación) | N-45: un bloqueo de entorno no es defecto ni éxito |
| Resultado JSON con commit, `dirty`, huellas de fixture y prompt, agente, versión y modelo | Formato candidato para nuestra evidencia (ESP-03, ESP-08) |
| `trace`: matriz de requisitos frente a tests con cobertura FULL / PARTIAL y puerta PASS / CONCERNS / FAIL / WAIVED | Inspiración para R07 (CHECK → EVID) |

**Comprobación de la evidencia (encargo, F06):** `test/results/` contiene 78 archivos. El recuento de campos muestra 34 entradas con agente `claude` (versión `2.1.273 (Claude Code)`, modelo `sonnet`) y 30 con `codex` (`gpt-5.6-sol`). **No hay ejecuciones registradas con Cursor.** No hemos reejecutado ni auditado el evaluador, así que estos registros prueban que existen ejecuciones con esa procedencia, **no** la eficacia que se les atribuye.

**Propuesta:** **adaptar los principios y el formato de resultado**, no el sistema. El arnés de TEA (CLI `tea-evaluate`, `eval-quality`, cientos de tests) es demasiado grande para nuestras necesidades (N-14). Nuestro ESP-08 puede empezar con fixtures pequeños, rutas neutras, una clave de respuestas fuera del espacio de trabajo y la convención 0/1/2.

## 4. Hallazgos

| ID | Hallazgo | Consecuencia |
|---|---|---|
| K1 | La **marca BMad** no está cubierta por la licencia MIT: no puede aparecer en nombres de producto o de piezas. | Toda pieza adaptada de F05 o F06 se renombra; el aviso de procedencia va en `THIRD_PARTY_NOTICES.md` («inspirado en…» está permitido). |
| K2 | F04 es Apache-2.0: si adaptamos su texto, hay que conservar el aviso de licencia y declarar los cambios. | Registrar en `THIRD_PARTY_NOTICES.md`; preferir inspiración a la copia literal. |
| K3 | F05 y F06 dependen de su runtime (`uv`, `_bmad/`, scripts) en el primer paso de cada skill. | Solo sirven como referencia de procedimiento, no como piezas instalables. |
| K4 | Superpowers es la fuente más portable: Markdown + git, sin runtime. | Candidata a copia adaptada para depuración y verificación (con aviso MIT). |
| K5 | Hay una redundancia clara entre los protocolos de verificación y depuración de F01 y F07. | Se sintetiza un único protocolo por función (3.1 y 3.2). |
| K6 | `using-git-worktrees` ejecuta instaladores de dependencias sin preguntar. | Se excluye ese paso. |
| K7 | `.memlog.md` de BMAD sería una segunda autoridad frente a `eventos.jsonl`. | Una sola autoridad de eventos (N-22). |
| K8 | Las pruebas de presión de superpowers y las suites de TEA demuestran que el comportamiento del agente **se puede evaluar con escenarios**. Ninguna fuente aporta evidencia en Cursor. | R01/B19: Cursor sigue sin evidencia de terceros; dependerá de nuestras pruebas. |

## 5. Cobertura de requisitos tras B03–B05

| Req. | Mejor cobertura encontrada | Estado para B06 |
|---|---|---|
| R01 | cc-sdd (variantes), Spec Kit/GSD (adaptadores) | Desarrollo propio: núcleo + adaptadores; sin evidencia en Cursor |
| R02 | GSD `progress` (tabla de rutas) | Desarrollo propio con inspiración en F03 |
| R03 | cc-sdd discovery + BMAD «Concern scan» + HumanLayer «investigar antes de preguntar» | Síntesis propia |
| R04 | BMAD `[ASSUMPTION]` + HumanLayer «verificar correcciones» | Desarrollo propio (estado de afirmación en ESP-03) |
| R05 | GSD `blocking-human` + BMAD elicitation (aplicar/rechazar) + roadmap de cc-sdd | Desarrollo propio |
| R06 | BMAD `.memlog.md` (idea) | Desarrollo propio |
| R07 | cc-sdd `_Requirements:_` + TEA `trace` | Desarrollo propio |
| R08 | GSD `progress` | Desarrollo propio con inspiración |
| R09 | cc-sdd `tasks-generation` (sin horas) | Adaptar |
| R10 | cc-sdd `STOP_FOR_HUMAN` / `EXTERNAL_DEPENDENCY` + TEA salida 2 | Adaptar |
| R11 | BMAD correct-course + GSD `stale` | Desarrollo propio (invalidación mecánica); OpenSpec (F09) solo si hace falta formalizar más |
| R12 | superpowers worktrees + GSD `undo` (salvaguardas) | Adaptar + desarrollo propio |
| R13 | Spec Kit (contrato de estado) + GSD `HANDOFF.json` medido | Desarrollo propio |
| R14 | cc-sdd verify + superpowers verify + GSD `stale` | Síntesis (3.1) |
| R15 | superpowers debug + cc-sdd informe | Síntesis (3.2) |
| R16 | Spec Kit manifiesto SHA-256 | Adaptar |
| R17 | cc-sdd rutas A–E + BMAD rápido/acompañado | Síntesis propia |
| R18 | cc-sdd smoke boot; **nadie cubre entrega, operación ni mantenimiento** | **Ausencia**: desarrollo propio en B14; gh-aw (F10) como referencia posterior |
| R19 | Spec Kit transiciones + GSD `stale` | Desarrollo propio (validador) |
| R20 | GSD «installer migrations» (no leído), cc-sdd `migration-guide.md` (no leído) | Pendiente: revisar en B07 o B22 |

## 6. Fuentes condicionales (F08–F10)

El encargo permite que B05 las explore si detecta un hueco. **No se han obtenido**, por estos motivos:
- **F09 OpenSpec:** R11 puede resolverse con relaciones y estados propios. Se obtendrá en B08 si la formalización de cambios resulta insuficiente.
- **F10 gh-aw:** el hueco de R18 es real, pero el encargo lo marca como referencia posterior y requiere servicios propios. Se valorará en B14.
- **F08 Agent OS:** solo si nuestros recursos crecen hasta necesitar selección de contexto. No es el caso.
