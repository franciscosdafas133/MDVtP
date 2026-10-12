# Auditoría F01 — cc-sdd

Tarea: B03 · Fecha: 2026-10-12 · Autor: agente constructor · Estado: completada (condición de B03 cumplida; las clasificaciones son propuestas para B06)

| Campo | Valor |
|---|---|
| Fuente | [gotalab/cc-sdd](https://github.com/gotalab/cc-sdd) |
| Commit | `e2a0c671aef37a482404905b409ab5c27092b25b` |
| Licencia | MIT (© 2025 gotalab), raíz leída. No se encontraron avisos específicos en las carpetas leídas. |
| Copia local | `.reference-sources/cc-sdd` (sparse: `docs/guides`, `tools/cc-sdd/templates`, `tools/cc-sdd/src`, `tools/cc-sdd/test`) |
| Ejecutado | Nada. No se ejecutó el instalador, la suite ni ninguna skill. |

## 1. Qué se leyó y con qué profundidad

Lo que no está en esta lista no se ha leído, y ninguna conclusión de la ficha se apoya en ello.

| Pieza | Lectura |
|---|---|
| `docs/guides/skill-reference.md`, `spec-driven.md`, `agent-compatibility.md` | Completa |
| `docs/guides/customization-guide.md` | Búsqueda dirigida (`rules`) |
| `command-reference.md`, `migration-guide.md`, `claude-subagents.md`, `why-cc-sdd.md` | No leídos (modo heredado o contexto general) |
| Skills Claude Code: `kiro-discovery`, `kiro-spec-init`, `kiro-spec-status`, `kiro-impl`, `kiro-verify-completion`, `kiro-review` | Completa |
| Skills Claude Code: `kiro-debug` | Hasta «Stop / Escalate» (método y salidas completos) |
| Skills Claude Code: `kiro-validate-impl`, `kiro-spec-tasks`, `kiro-spec-design`, `kiro-spec-requirements` | Estructura y búsquedas dirigidas (aprobaciones, puertas, salidas) |
| `kiro-spec-batch`, `kiro-spec-quick`, `kiro-steering*`, `kiro-validate-gap`, `kiro-validate-design` | Solo metadatos y diferencias entre hosts |
| `kiro-impl/templates/*-prompt.md` | No leídos (se usan por referencia) |
| Variante Cursor | `diff` normalizado frente a Claude Code en 9 skills; `agents/openai.yaml` completos |
| `shared/settings/templates/specs/init.json`, `tasks.md` | Completa |
| `shared/settings/rules/tasks-generation.md`, `requirements-review-gate.md` | Búsquedas dirigidas (tamaño, división, aclaración) |
| Manifiestos `claude-code-skills.json`, `cursor-skills.json` | Completa |
| Instalador `src/plan/sharedRules.ts`, `executor.ts`, `src/cli/policies.ts`, `src/agents/registry.ts` (entradas de ambos hosts) | Completa o dirigida |
| `test/` | Solo el listado de archivos |

## 2. Recorrido real

```text
[/kiro-steering] (opcional) ─► steering/product.md, tech.md, structure.md
        │
/kiro-discovery  ─► elige ruta A–E ─► escribe brief.md (+ roadmap.md) ─► SUGIERE comando y PARA
        │
/kiro-spec-init  ─► spec.json + requirements.md (plantilla) ─► PARA
/kiro-spec-requirements ─► requirements.md (EARS) ─► pregunta «¿aprobar?» ─► PARA
/kiro-spec-design ─► research.md + design.md; marca requirements.approved=true ─► PARA
/kiro-spec-tasks ─► tasks.md; marca requirements y design approved=true ─► pide aprobación ─► PARA
        │                                   (atajo: /kiro-spec-quick o -y encadena 2–5)
/kiro-impl [tareas] ─► por tarea: implementador → revisor → verify-completion → commit selectivo
        │                 └─ BLOCKED / 3.er rechazo ─► kiro-debug (máx. 2 rondas) ─► RETRY | BLOCK | STOP_FOR_HUMAN
        └─► (modo autónomo) /kiro-validate-impl ─► GO | NO-GO (≤3 rondas) | MANUAL_VERIFY_REQUIRED
/kiro-spec-status <feature> ─► informe de fase, progreso, bloqueos y vigilancia de revalidación (solo lectura)
```

**Paradas.** Cada fase de especificación termina sugiriendo el comando siguiente y se detiene. Discovery lo dice explícitamente: «Suggest the next command and stop. Do NOT automatically run downstream spec generation». Para avanzar, el usuario tiene que conocer y teclear el nombre de la skill siguiente. **Esto contradice R02**, y nuestro coordinador tiene que aportar esa continuidad (lo anticipaba el encargo §7).

**Rutas de discovery:** A (ampliar una spec existente), B (sin spec, implementación directa), C (una spec nueva), D (varias specs, a partir de «20+ tareas» o varios dominios), E (mixta).

## 3. Estado y documentos

| Artefacto | Ubicación | Contenido | Quién escribe |
|---|---|---|---|
| `spec.json` | `.kiro/specs/<feature>/` | `phase`, `approvals.{requirements,design,tasks}.{generated,approved}`, `ready_for_implementation`, idioma, marcas de tiempo | El agente, por instrucción |
| `brief.md` | ídem | Problema, estado actual, resultado, enfoque, alcance, límites, upstream/downstream | discovery |
| `roadmap.md` | `.kiro/steering/` | Enfoque elegido, alternativas rechazadas con motivo, specs en orden de dependencias | discovery |
| `requirements.md`, `design.md`, `research.md` | spec | Requisitos EARS numerados; diseño con «Boundary Commitments», «Revalidation Triggers» y «File Structure Plan»; registro de investigación | skills de fase |
| `tasks.md` | spec | Casillas `- [ ]`/`[x]`, `(P)`, `_Boundary:_`, `_Depends:_`, `_Requirements:_`, `_Blocked:_`, `## Implementation Notes` | spec-tasks / impl |
| Steering | `.kiro/steering/` | Memoria del proyecto | steering |

Observaciones:

- **No hay registro de eventos, ni escritor único, ni escrituras atómicas.** Cada skill reescribe `spec.json` y `tasks.md` directamente. La propia guía advierte: «Recorded progress is not a guarantee of interruption recovery on every host».
- **No hay validador.** Ningún script comprueba las transiciones de `spec.json`, las referencias `_Requirements:_` ni la coherencia entre fases. La suite (40 archivos de test) cubre instalador, manifiestos y renderizado, no el estado del flujo (deducido de los nombres de archivo).
- **Trazabilidad parcial.** Tarea → requisito por número (`_Requirements: 1.2, 3.1_`) y tarea → tarea (`_Depends:_`). No hay identificadores para decisiones, comprobaciones ni evidencia.
- **Decisiones.** Solo existe «Approach Decision» en `roadmap.md` (elegido, por qué y alternativas rechazadas) y notas en `research.md`. No hay estados de decisión, sustitución ni apuntes asociados.

## 4. Controles y validaciones

| Mecanismo | Tipo | Valor para nosotros |
|---|---|---|
| Aprobaciones por fase en `spec.json` | Instrucción | Concepto útil, pero ver hallazgo H3 |
| Puertas de revisión antes de escribir (requirements, design, task plan); «-y never bypasses these review gates» | Instrucción | Útil |
| `kiro-impl`: una subtarea por iteración, salida estructurada obligatoria (`STATUS`, `VERDICT`, `NEXT_ACTION`) y nunca inferida de la prosa | Instrucción con formato verificable | **Muy útil**: el formato podría validarse con un script |
| Rondas acotadas: 2 de corrección → debug; 2 de debug → `_Blocked:_`; 3 de corrección final | Instrucción | Cubre R15 |
| `kiro-verify-completion`: `VERIFIED / NOT_VERIFIED / MANUAL_VERIFY_REQUIRED`; evidencia fresca; rechaza afirmaciones más amplias que la evidencia; `FEATURE_GO` exige smoke boot | Instrucción | Cubre gran parte de R14/E08 |
| `kiro-review`: lee el `git diff` por su cuenta, no confía en el informe del implementador; detecta stubs, TODO y secretos, y revisa la frontera de la tarea | Instrucción | Útil para B13 |
| `kiro-debug`: causa raíz primero, 10 categorías, `STOP_FOR_HUMAN` ante credenciales, hardware o conflictos de spec, sin parches a ciegas | Instrucción | Cubre R15 y parte de R10 |
| Git: staging selectivo; prohibidos `git add -A`, `git checkout .` y `git reset --hard`; registra `git status` de partida | Instrucción | Coincide con N-48/N-49 |
| Revisión independiente solo con subagente real; si no, debe declararse «inline review» | Instrucción + documentación | Coincide con §6 del encargo |
| Instalador: rutas dentro del proyecto, rechazo de enlaces simbólicos, políticas `overwrite/skip/append`, copia de seguridad opcional, no sobrescribe sin `--yes` en entornos no interactivos | **Código** | Base útil para R16 |

## 5. Instalación y diferencias entre hosts

- **Destinos:** Claude Code → `.claude/skills/kiro-*/` + `CLAUDE.md` en la raíz; Cursor → `.cursor/skills/kiro-*/` + `AGENTS.md` en la raíz. Ambos → `.kiro/settings/templates/`.
- **Reglas compartidas:** cada `SKILL.md` declara `metadata.shared-rules` y el instalador copia esas reglas en `<skill>/rules/` (`src/plan/sharedRules.ts`). La misma regla queda duplicada en varias skills (`steering-principles.md` en dos). **La guía de personalización dice que viven en `{{KIRO_DIR}}/settings/rules/`; está desactualizada** (hallazgo H5).
- **Documento de memoria del proyecto (`CLAUDE.md`/`AGENTS.md`):** si ya existe, se ofrece sobrescribir (opción recomendada), añadir al final u omitir. Sobrescribir un archivo del usuario es contrario a R16, salvo con copia de seguridad explícita.
- **Sin retirada:** no hay comando de desinstalación ni registro de los archivos instalados (búsqueda de `uninstall|remove|unlink` en `src/` sin resultados). **Hueco para R16.**
- **Dos copias mantenidas a mano.** La variante Cursor no se genera desde la de Claude Code: son 17 skills duplicadas. Diferencias encontradas:
  - Mecánicas: Cursor quita `disable-model-invocation`, `allowed-tools` y `argument-hint`; usa `$1`/`$2` en lugar de `$ARGUMENTS`; habla de «spawn a sub-agent» en lugar de «Agent tool»; envuelve el texto en `<background_information>`/`<instructions>`; añade la alternativa «If multi-agent capability is available… otherwise sequentially».
  - **Deriva de contenido:** la versión Cursor de `kiro-spec-tasks` no tiene la instrucción «list numeric requirement IDs only» ni el paso de selección de skills; `kiro-validate-impl` difiere en la detección de objetivo. Son pérdidas de comportamiento, no adaptaciones al host (hallazgo H4).
  - Tres skills de Cursor (`kiro-debug`, `kiro-review`, `kiro-verify-completion`) incluyen `agents/openai.yaml` con `allow_implicit_invocation: false`. Es un formato de Codex: **sin comprobar** que Cursor lo lea.
  - En Cursor, `kiro-discovery` y `kiro-impl` no llevan el equivalente de `disable-model-invocation`. **Sin comprobar** si Cursor podría invocarlas solas.

## 6. Hallazgos

| ID | Hallazgo | Consecuencia para el paquete |
|---|---|---|
| H1 | Cada fase se detiene y espera a que el usuario escriba la skill siguiente. | La continuidad de R02 tiene que ser nuestra (coordinador). |
| H2 | No hay estado transaccional, eventos ni validador; el progreso vive en casillas de Markdown y en `spec.json`, editados por el agente. | ESP-04 no puede heredar este modelo tal cual; R13 y R19 requieren desarrollo propio. |
| H3 | **Aprobación implícita:** `kiro-spec-design` fija `approvals.requirements.approved: true` y `kiro-spec-tasks` fija la de requirements y design al generar; `-y` aprueba todo. | Contradice §4 del encargo y N-32 («una aceptación solo cubre la propuesta mostrada»). No adoptar. |
| H4 | Variantes por host duplicadas a mano y con deriva de contenido. | Confirma nuestra propuesta: un núcleo canónico y adaptadores que solo transforman lo propio del host. |
| H5 | La documentación contradice al instalador sobre dónde viven las reglas. | Una auditoría no puede fiarse solo de las guías; hay que seguir el código. |
| H6 | El tamaño de tarea se fija en «1-3 horas» (`tasks-generation.md`). | Contradice §8 del encargo y N-21. Usar sus criterios de división (un resultado verificable, una frontera), no la duración. |
| H7 | Cambiar requisitos o diseño no invalida nada: la «Revalidation Watchlist» de `kiro-spec-status` solo informa. | R11 requiere desarrollo propio (invalidación mecánica). |
| H8 | No hay puntos de recuperación ni recuperación aislada; solo commits por tarea. | R12 y ESP-06 requieren otras fuentes (GSD Core, B04) o desarrollo propio. |
| H9 | No hay entrega, operación ni mantenimiento: el flujo termina en `GO`. | R18 requiere otras piezas (B05, B14). |
| H10 | Discovery sí cubre parte de R03: preguntas secuenciales, «Ask only questions whose answers you cannot infer», 2–3 enfoques con pros y contras, y comprobación de viabilidad. No distingue hechos de hipótesis. | Conservar la estructura; añadir estados de afirmación (R04). |
| H11 | Las copias contienen `CLAUDE.md`/`AGENTS.md` de trabajo para sus propios desarrolladores, y plantillas para instalar en proyectos. | Ver R-01 del tablero. |

## 7. Evidencia de la propia fuente: qué demuestra y qué no

Según `agent-compatibility.md` (texto de la fuente, no verificado por nosotros):

- **Demuestra (según la fuente):** 199 tests y build del instalador en verde; instalación de 17 skills en Antigravity y Devin; sondas controladas en Antigravity CLI 1.1.24. En una de ellas, con un veredicto `NEEDS_FIXES` simulado, la skill no escribió `tasks.md`.
- **No demuestra:** comportamiento en Claude Code ni en Cursor reales (el documento no recoge pruebas en esos hosts); calidad del juicio del revisor («not reviewer judgment quality»); recuperación de ejecuciones largas; un ciclo completo de implementación, revisión y debug. La propia fuente lo declara: «These checks establish installation behavior, not every host workflow».
- La fuente advierte de que un código de salida 0 o `status: SUCCESS` no prueba que el flujo se completara. Es una lección útil para nuestro ESP-08.

## 8. Fichas por pieza

Clasificación: **conservar** (casi literal), **adaptar** (rehacer en nuestro contrato), **inspiración** (idea sin texto), **redundante**, **descartar**. Todas son **propuestas para B06**, no decisiones.

| Pieza | Requisitos | Entradas → Salidas | Control | Limitaciones | Propuesta |
|---|---|---|---|---|---|
| `kiro-discovery` | R03, R09, R17 | idea + metadatos del proyecto → `brief.md`, `roadmap.md`, siguiente comando | Instrucción; `disable-model-invocation` en Claude | Se para (H1); sin hechos/hipótesis; «20+ tareas» como umbral | **Adaptar** como procedimiento interno del coordinador |
| `kiro-spec-init/requirements` | R03, R04 | brief → `requirements.md` EARS | Puerta de revisión (instrucción) | Aprobación por `spec.json` (H3) | **Adaptar** la puerta de revisión; **inspiración** para EARS |
| `kiro-spec-design` + reglas de diseño | R07, R17 | requisitos → `research.md`, `design.md` | Puerta de revisión | Aprobación implícita (H3); plantilla de 13 KB | **Inspiración** (Boundary Commitments, Revalidation Triggers) |
| `kiro-spec-tasks` + `tasks-generation.md` | R09, R10 | diseño → `tasks.md` | Puerta del plan de tareas + sanity check | Tamaño por horas (H6); deriva en Cursor (H4) | **Adaptar** los criterios de división y la «condición observable de terminación» |
| `kiro-impl` | R09, R14, R15 | `tasks.md` aprobado → código, commits, notas | Salidas estructuradas, rondas acotadas, staging selectivo | Depende de subagentes; estado en casillas | **Adaptar** el bucle y los límites; el estado pasa a ESP-04 |
| `kiro-review` | R14 | diff + spec → `APPROVED/REJECTED` | Comprobaciones mecánicas + juicio | Revisión del mismo agente si no hay subagente | **Conservar** el protocolo (con aviso de procedencia) |
| `kiro-debug` | R15, R10 | fallo + diff → `ROOT_CAUSE`, `NEXT_ACTION` | Formato estructurado | Comparar con superpowers (B05) antes de elegir | **Candidato**; decidir en B05/B06 |
| `kiro-verify-completion` | R14 | afirmación + salida fresca → `VERIFIED/…` | Formato estructurado | Comparar con superpowers (B05) | **Candidato fuerte**; decidir en B05/B06 |
| `kiro-validate-impl` | R14, R18 (parcial) | feature → `GO/NO-GO/MANUAL_VERIFY_REQUIRED` | Mecánico + juicio | Solo integración local; sin despliegue | **Adaptar** para B13/B20 |
| `kiro-spec-status` | R08 | archivos de spec → informe | Solo lectura | Sin bloqueos estructurados ni siguiente paso preparado | **Inspiración**; nuestro `estado` sale de ESP-04 |
| Instalador (`src/`) | R16, R01 | manifiesto → archivos | **Código** con seguridad de rutas | Sin retirada ni registro; Node + npm; sobrescribe el doc de memoria | **Inspiración** (seguridad de rutas, políticas); runtime a decidir en B07 |
| `spec.json` / aprobaciones | R05, R19 | — | Ninguno mecánico | H2, H3 | **Descartar** como modelo de estado |

## 9. Huecos frente a R01–R20

| Req. | Cobertura de cc-sdd | Hueco |
|---|---|---|
| R01 | Variantes para ambos hosts | Duplicadas con deriva (H4); sin evidencia propia en Claude Code ni Cursor |
| R02 | Discovery como entrada recomendada | Para avanzar hay que conocer 17 skills (H1) |
| R03 | Discovery: preguntas, enfoques, viabilidad | Falta registrar por qué importa cada pregunta y cómo responderla, según las áreas de §2 |
| R04 | — | Sin estados de hecho/hipótesis ni procedencia |
| R05 | Alternativas rechazadas en `roadmap.md` | Sin identificadores, estados ni sustitución; aprobación implícita (H3) |
| R06 | — | Los apuntes del usuario no tienen lugar ni enlace |
| R07 | Tarea → requisito; Boundary/Revalidation en diseño | Faltan decisiones, comprobaciones y evidencia en la cadena |
| R08 | `kiro-spec-status` | No propone la siguiente actividad preparada |
| R09 | Reglas de división; ruta D | Umbral por horas (H6) |
| R10 | `_Blocked:_`, `STOP_FOR_HUMAN`, `EXTERNAL_DEPENDENCY` | No distingue simulación de integración real de forma explícita (solo detecta stubs en revisión) |
| R11 | Vigilancia de revalidación (informativa) | Sin invalidación (H7) |
| R12 | Commits por tarea | Sin checkpoints ni recuperación aislada (H8) |
| R13 | `brief.md`, `tasks.md` en disco | Sin reconciliación tras interrupción (H2) |
| R14 | verify-completion, review, validate-impl | Bien cubierto como instrucción; falta un control mecánico |
| R15 | Rondas acotadas, debug por causa raíz | Bien cubierto como instrucción |
| R16 | Instalador con seguridad de rutas y políticas | Sin retirada ni registro; puede sobrescribir `CLAUDE.md`/`AGENTS.md` |
| R17 | Rutas A–E (sin spec, una, varias) | Falta graduar la profundidad del análisis según el riesgo |
| R18 | Smoke boot en `FEATURE_GO` | Sin entrega, operación ni mantenimiento (H9) |
| R19 | — | Sin validación mecánica del estado (H2) |
| R20 | `migration-guide.md` (no leído) y CHANGELOG | Revisar en B06 si su política de migración sirve |

## 10. Preguntas para B04–B06

1. ¿GSD Core o Spec Kit aportan el estado transaccional y la recuperación que faltan (H2, H8)? → B04.
2. ¿Qué protocolo elegir para depuración y verificación: el de cc-sdd o el de superpowers? → B05.
3. ¿Usar cc-sdd como base (copiar y adaptar skills) o como inspiración y escribir nuestro núcleo? Las aprobaciones implícitas, la deriva entre hosts y el estado sin validación pesan hacia la segunda opción, conservando review, verify-completion y debug. → B06.
4. ¿Lee Cursor `disable-model-invocation`, `agents/openai.yaml` y los argumentos `$1`/`$2`? → B15 (en el host real).
