# Plan de construcción de un paquete de desarrollo guiado con IA

Documento de traspaso para trabajar en una carpeta local abierta con Claude Code en VS Code o con Cursor. Fecha: 11 de octubre de 2026.

## 1. Encargo y estado real

Construir un paquete instalable que guíe el desarrollo de productos de software mediante un flujo conectado de skills, documentos, decisiones y verificaciones. El usuario debe poder conversar con un único coordinador y comprender qué está aceptando, rechazando, dejando pendiente o cambiando.

Este documento contiene los requisitos del paquete y el tablero para construirlo. **El paquete todavía no está implementado ni probado.** Las fuentes fueron inspeccionadas para identificar rutas, documentos y comportamientos concretos; falta la auditoría completa de las piezas que se vayan a incorporar. Las rutas propuestas para nuestro paquete son diseño propio. Las rutas de los repositorios de referencia se identifican separadamente.

El objetivo de esta investigación y construcción es crear nuestro método, no desarrollar ahora una aplicación de negocio. El posterior uso del paquete debe cubrir descubrimiento, construcción y mantenimiento, ajustando su profundidad al riesgo del proyecto.

### Cómo utilizar este documento

Coloca este archivo en la carpeta donde construirás el paquete y abre esa carpeta en el editor. Entrega al agente esta instrucción:

> Lee PLAN_PAQUETE_FLUJO_IA.md como el encargo de este proyecto. Trabaja desde el tablero, empezando por B01. Examina los repositorios y las piezas indicadas, registra tu selección y diseña las especificaciones antes de implementar el paquete. Mantén actualizado el tablero, las decisiones y la evidencia. Continúa con las tareas preparadas; plantea únicamente las decisiones de producto o bloqueos que no puedas resolver con las fuentes. No instales automáticamente todos los proyectos de referencia. El resultado debe funcionar en Claude Code y Cursor mediante un núcleo común y una entrada guiada.

Esta instrucción inicia la construcción del paquete. El nombre `/product-flow` utilizado más adelante es una interfaz propuesta para el paquete futuro, no un comando que ya exista.

## 2. Conocimiento que el paquete debe encapsular

Un buen producto requiere comprobar tres cosas diferentes: que el cambio de código esté bien implementado, que el sistema completo se comporte como se espera y que las personas obtengan un resultado útil. La documentación debe conectar esas comprobaciones.

| Actividad del proceso | Resultado esperado | Si falta evidencia |
|---|---|---|
| Entender el problema | Usuarios, situación actual y resultado que les sirve. | Investigar la necesidad o reformular la propuesta. |
| Descubrir necesidades | Escenarios, límites, condiciones de aceptación y preguntas pendientes. | Precisar ejemplos y registrar dudas. |
| Investigar viabilidad | Fuentes y experimentos sobre dificultades determinantes. | Bloquear únicamente el trabajo dependiente. |
| Diseñar el sistema | Responsabilidades, datos, interfaces y decisiones fundadas. | Revisar el diseño o realizar un experimento. |
| Preparar una base | Entorno reproducible y recorrido técnico mínimo. | Resolver preparación e integración inicial. |
| Planificar incrementos | Tareas delimitadas con dependencias y comprobación de terminación. | Dividir tareas o investigar lo desconocido. |
| Implementar e integrar | Cambios acotados sobre una base conocida. | Corregir o retirar el cambio defectuoso. |
| Verificar | Evidencia pertinente al comportamiento y los riesgos. | Mantener pendientes los criterios no comprobados. |
| Diagnosticar | Reproducción, hipótesis contrastada y corrección delimitada. | Detener reparaciones sin aprendizaje y volver a investigar. |
| Entregar | Versión desplegada, comprobación posterior y recuperación prevista. | Mantener la entrega pendiente o recuperar el estado operativo. |
| Operar y mantener | Detección, respuesta, recuperación y cambios controlados. | Priorizar riesgos y fallos reales. |
| Aprender | Resultados de uso e incidentes convertidos en mejoras. | Revisar producto, requisitos o proceso. |

Estas actividades se repiten por incrementos. La seguridad, las pruebas y la operación se consideran desde el diseño. El paquete no exigirá definir de antemano todos los requisitos ni completar documentos por rellenar casillas.

El descubrimiento debe recorrer usuarios y permisos; datos y recuperación; integraciones y credenciales; procesos asíncronos; concurrencia; experiencia de uso; calidad; entornos; costes y operación. Para cada área registra si aplica, qué se conoce, qué falta y cómo averiguarlo. No debe inventar cifras, accesos, límites de una API ni afirmaciones técnicas.

## 3. Requisitos verificables del paquete

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| R01 | Compatibilidad con ambos editores/agentes | El paquete se carga y completa el mismo escenario en Claude Code y Cursor. Registrar versiones y superficies usadas. |
| R02 | Entrada guiada única | Iniciar, continuar, consultar estado y cambiar dirección mediante el mismo coordinador, sin exigir conocer las skills internas. |
| R03 | Descubrir necesidades desconocidas | Ante una idea vaga, identifica preguntas relevantes, explica por qué importan y propone cómo responderlas. |
| R04 | Distinguir hechos e hipótesis | Una afirmación no comprobada conserva su estado y procedencia; no aparece como requisito confirmado por accidente. |
| R05 | Decisiones visibles | Cada propuesta tiene identificador, alternativas, consecuencias y estado: propuesta, aceptada, rechazada, aplazada o sustituida. |
| R06 | Conservar apuntes | Los comentarios del usuario quedan asociados a la pregunta, decisión o requisito correspondiente, con pendientes visibles. |
| R07 | Conectar documentos | Puede seguirse un resultado de producto hasta requisitos, decisiones, tareas, comprobaciones y evidencia. |
| R08 | Mantener progreso | Al continuar, informa qué está en curso, qué falta, qué bloquea y cuál es la siguiente actividad preparada. |
| R09 | Dividir trabajo amplio | Una tarea con varios objetivos o dudas determinantes se divide antes de ejecutarse. |
| R10 | Gestionar dependencias reales | Credenciales, herramientas, servicios, hardware y participación externa se registran; se distingue integración real de simulación. |
| R11 | Reabrir decisiones | Cambiar una decisión produce análisis de impacto e invalida aprobaciones o evidencia afectadas. |
| R12 | Recuperación técnica | Se puede inspeccionar un punto de recuperación y continuar desde una rama creada a partir de él, sin borrar trabajo posterior. |
| R13 | Recuperación de sesión | Otra sesión reconstruye el estado desde archivos y código, sin depender del historial de chat. |
| R14 | Verificación honesta | No declara un criterio satisfecho sin evidencia pertinente y vigente; informa pruebas omitidas o bloqueadas. |
| R15 | Depuración controlada | Reproduce, comprueba hipótesis y detiene cambios cuando no convergen o amplían injustificadamente el alcance. |
| R16 | Instalación coherente | Instala solo archivos del paquete, detecta conflictos y permite retirar sus propios archivos sin eliminar los del usuario. |
| R17 | Profundidad proporcional | Un cambio pequeño usa menos detalle; un sistema con mayor incertidumbre o impacto incorpora análisis y revisión adicionales. |
| R18 | Integración y operación | El flujo contempla pruebas entre componentes, entrega, observación y recuperación; no termina al generar código. |
| R19 | Integridad de estado | Cambios de estado inválidos, referencias rotas y comprobaciones desactualizadas se detectan mecánicamente cuando sea posible. |
| R20 | Evolución del método | Cada versión registra cambios de contratos y cómo migrar proyectos que utilizaban la anterior. |

La experiencia debe ser en español. Los identificadores técnicos pueden ser estables y breves. El usuario revisará decisiones y evidencia con explicaciones comprensibles; no necesitará estudiar el funcionamiento interno de las skills para avanzar.

## 4. Flujo de interacción propuesto

El coordinador muestra al iniciar y cerrar cada actividad:

```text
Objetivo actual:
Actividad en curso:
Lo confirmado:
Lo propuesto:
Lo rechazado o aplazado:
Dudas y bloqueos:
Archivos actualizados:
Comprobaciones y pendientes:
Punto de recuperación disponible:
Siguiente paso y por qué:
```

El usuario puede hablar naturalmente: «acepto esa alternativa», «apunta esto», «eso no lo quiero», «qué falta», «continúa» o «quiero volver al diseño anterior». Si hay varias propuestas posibles, el agente debe identificar a cuál se refiere antes de modificar su estado.

Una aceptación solo cubre la propuesta mostrada. Que una sección se acepte no aprueba automáticamente decisiones nuevas o todos los documentos posteriores. Un rechazo conserva su motivo y evita que la misma alternativa vuelva a aparecer como elegida sin nueva evidencia.

La interfaz prevista es `/product-flow` con acciones de iniciar, continuar, estado, decidir, anotar, reabrir, recuperar y verificar. El adaptador puede implementar estas acciones como argumentos o conversación, según las capacidades comprobadas del host.

Los pasos técnicos dentro del alcance autorizado continúan automáticamente cuando están preparados. El coordinador pide información cuando falta una respuesta que solo el usuario o un tercero puede dar; mientras tanto puede continuar trabajo independiente. No usa preguntas para descargar toda la definición técnica en el usuario.

## 5. Documentos y contratos compartidos

Separar tres ámbitos: documentos para construir este paquete, recursos que el paquete instala y documentos que genera en un proyecto del usuario. Nunca confundir el tablero de construcción del método con las tareas de una aplicación posterior.

### Organización propuesta del repositorio del paquete

| Ruta propuesta | Contenido |
|---|---|
| `docs/encargo.md` y `docs/tablero.md` | Requisitos y progreso de construcción del paquete. |
| `docs/fuentes.md` y `sources.lock.json` | Auditoría y versiones de las referencias seleccionadas. |
| `docs/especificaciones/` | Contratos del flujo, estado, decisiones, recuperación, adaptación e instalación. |
| `core/skills/product-flow/` | Entrada coordinadora y recursos de los procedimientos internos. |
| `core/templates/` | Plantillas de los documentos que produce el paquete. |
| `core/contracts/` | Estados permitidos, referencias y reglas verificables. |
| `adapters/claude-code/` y `adapters/cursor/` | Diferencias comprobadas de carga, herramientas e invocación. |
| `scripts/` | Validación, instalación, diagnóstico y puntos de recuperación. |
| `tests/fixtures/` y `tests/scenarios/` | Casos controlados para probar el paquete. |
| `THIRD_PARTY_NOTICES.md` | Procedencia de adaptaciones y avisos necesarios. |
| `.reference-sources/` | Copias de referencia sin habilitarlas como extensiones del proyecto. Excluir del paquete distribuido. |

La forma interna exacta se resolverá en B07. Preferir una skill coordinadora con procedimientos cargados según la actividad. Si hay skills auxiliares, comparten los mismos contratos y el usuario accede a ellas a través del coordinador. El número de skills no es una meta.

### Documentación generada en cada proyecto

Propuesta de carpeta `workflow/` en el proyecto del usuario:

| Registro | Autoridad y relación |
|---|---|
| `producto.md` | Problema, usuarios, resultados, restricciones y alcance vigente. |
| `descubrimiento.md` | Hechos, hipótesis, preguntas y experimentos. |
| `requisitos.md` | Escenarios y condiciones de aceptación identificables. |
| `sistema.md` | Componentes, contratos, datos y recorridos vigentes. |
| `decisiones/` | Una decisión significativa por registro, conservando sustituciones. |
| `entregas/<id>/plan.md` y `tareas.md` | Incremento actual, límites, dependencias y terminación. |
| `verificacion.md` | Estrategia y referencias a evidencia versionada. |
| `operacion.md` | Entornos, configuración necesaria, entrega y recuperación. |
| `estado.json` | Estado de navegación y ejecución; autoridad única para esas transiciones. |
| `tablero.md` | Vista legible regenerable a partir del estado y referencias. |
| `eventos.jsonl` | Historial de transiciones y decisiones, reconciliable después de una interrupción. |
| `checkpoints/` | Metadatos de puntos de recuperación; no copias indiscriminadas de datos o secretos. |

Para un proyecto pequeño se pueden fusionar documentos de contenido. Deben mantenerse identificadores y relaciones, sin crear dos autoridades sobre el mismo dato. El formato final y la consistencia entre eventos y estado deberán diseñarse y probarse, no improvisarse mediante escrituras independientes sin recuperación.

Cada artefacto debe conocer: identificador, versión, estado, entradas relevantes, decisiones que lo condicionan y comprobación requerida. Cadena ilustrativa: `OBJ-01 → REQ-03 → DEC-02 → TASK-05 → CHECK-07 → EVID-04`. Las relaciones reales pueden ramificarse; no todos los requisitos necesitan una decisión arquitectónica propia.

Si cambia `DEC-02`, se consultan las relaciones para marcar tareas y evidencia afectadas como pendientes de revisión. Se conservan resultados históricos, pero no se reutilizan como comprobación del nuevo estado.

### Recuperación y límites

**Reabrir una decisión:** conservar la anterior, proponer un reemplazo y revisar el impacto en documentos y tareas. No modifica automáticamente el código para imitar un estado pasado.

**Recuperar código y documentos:** identificar un commit comprobado, revisar cambios actuales y crear una rama o worktree desde ese punto. Continuar allí preservando el trabajo posterior. Si se pide revertir en la rama activa, analizar dependencias y proteger cambios propios y del usuario; no utilizar borrados masivos como atajo.

**Recuperar un sistema desplegado:** seguir un procedimiento específico para datos, infraestructura e integraciones. Git no deshace una migración externa, un pago ni una acción ejecutada por una API.

Cada checkpoint registra nombre comprensible, commit, versión del paquete, documentos asociados, comprobaciones ejecutadas, aspectos pendientes y dependencias externas. Solo se etiqueta como «comprobado» para el alcance que realmente se verificó. Datos simulados o ausencia de credenciales deben aparecer explícitamente.

La actualización del estado debe soportar interrupciones, escrituras atómicas donde corresponda y un único responsable de escritura. Al retomar, contrastar estado, eventos, documentos y árbol de trabajo antes de ejecutar nuevas tareas. El agente nunca descarta silenciosamente cambios sin commit.

## 6. Compatibilidad confirmada y pendiente

La documentación oficial consultada confirma `SKILL.md` y recursos auxiliares en ambos hosts. Claude Code admite skills de proyecto en `.claude/skills/`; Cursor admite `.cursor/skills/` y otras ubicaciones compatibles. Las funciones adicionales y el comportamiento de carga no son idénticos.

Propuesta inicial: un núcleo canónico con `name` y `description`, y un instalador que materialice una sola copia activa por host. Evitar dos copias que Cursor descubra simultáneamente por compatibilidad. Los metadatos exclusivos, hooks, ejecución en agentes secundarios e importación de archivos se resuelven en los adaptadores, no se suponen portables.

Debe existir un modo secuencial funcional. Si se utiliza una revisión en contexto independiente, registrar que se realizó; una revisión del mismo agente en el mismo contexto no se presenta como independiente. La instalación correcta no demuestra ejecución correcta.

Las instrucciones son orientación al modelo. Los controles que deban impedir transiciones inválidas necesitan validadores o mecanismos comprobados del host. Antes de publicar compatibilidad, probar los dos hosts reales y registrar sus versiones. Si alguno no está disponible, declarar ese resultado pendiente.

Referencias oficiales: [Claude Code: skills](https://code.claude.com/docs/en/skills), [Claude Code: memoria e instrucciones](https://code.claude.com/docs/en/memory), [Cursor: skills](https://cursor.com/docs/skills), [Cursor: reglas](https://cursor.com/docs/rules).

## 7. Fuentes versionadas y extracción prevista

Las siguientes versiones se obtuvieron del historial de cada repositorio durante esta consulta. Los archivos seleccionados se consultaron con referencias fijadas cuando se indica una inspección concreta. **No se han ejecutado los instaladores ni las suites de estos repositorios.** Las licencias raíz se leyeron; antes de reutilizar una pieza revisar también sus avisos y licencias específicas. Esta comprobación de procedencia no reemplaza revisar los términos aplicables a la redistribución.

| ID | Repositorio original | Papel en la auditoría | Licencia raíz | Commit de referencia |
|---|---|---|---|---|
| F01 | [gotalab/cc-sdd](https://github.com/gotalab/cc-sdd) | Principal | MIT | `e2a0c671aef37a482404905b409ab5c27092b25b` |
| F02 | [github/spec-kit](https://github.com/github/spec-kit) | Comparación principal | MIT | `0443760542e7e5269724744a2ac55c4bd386d095` |
| F03 | [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core) | Comparación principal | MIT | `b747aca5b1dcff699c36d90c5b9fca0ec6354c1c` |
| F04 | [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) | Complemento | Apache-2.0 | `99abe673498cf8bdcd5f989aebe9406a27185b3b` |
| F05 | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Complemento | MIT | `bda3c5929f672019b90f39a3ea27259d35d00974` |
| F06 | [bmad-code-org/bmad-method-test-architecture-enterprise](https://github.com/bmad-code-org/bmad-method-test-architecture-enterprise) | Complemento | MIT | `a5675c354ecb781e99b5f83145bb1850f8f27e09` |
| F07 | [obra/superpowers](https://github.com/obra/superpowers) | Comparación | MIT | `bb92a77741419a4ab5f06e711a283343f1ada0c3` |
| F08 | [buildermethods/agent-os](https://github.com/buildermethods/agent-os) | Condicional | MIT | `e892e61d322759165e7d9173e92c1010406c9f4d` |
| F09 | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | Condicional | MIT | `9111a7654d7800391459431fff4eaf66e33a3d2e` |
| F10 | [github/gh-aw](https://github.com/github/gh-aw) | Condicional, posterior | MIT | `2db4dd75564e9b65e6b1d056448b429fab2efb1d` |
| F11 | [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | Descartado como base nueva | MIT | `bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815` |


F01, F02 y F03 son alternativas para estudiar coordinación; no incorporaremos sus tres sistemas de estado a la vez. Los complementos solo entran cuando mejoran una necesidad identificada. Los condicionales se estudian si queda un hueco pertinente.

### F01 — cc-sdd: candidato de base

Carpetas verificadas:
- `docs/guides/`.
- `tools/cc-sdd/templates/shared/settings/templates/specs/`.
- `tools/cc-sdd/templates/shared/settings/templates/steering/`.
- `tools/cc-sdd/templates/shared/settings/rules/`.
- `tools/cc-sdd/templates/agents/claude-code-skills/skills/`.
- `tools/cc-sdd/templates/agents/cursor-skills/skills/`.
- `tools/cc-sdd/templates/manifests/`.

Entradas prioritarias: `kiro-discovery`, `kiro-spec-requirements`, `kiro-spec-design`, `kiro-spec-tasks`, `kiro-impl`, `kiro-spec-status`, `kiro-review`, `kiro-debug`, `kiro-validate-impl` y `kiro-verify-completion`. Cada carpeta debe estudiarse con sus recursos y dependencias.

Inspección concreta: ambas variantes de `kiro-impl/SKILL.md`, `kiro-discovery/SKILL.md`, plantilla de tareas, reglas de tareas y documentación del método. Discovery escribe resultados y después sugiere el siguiente comando y se detiene. Nuestro coordinador debe proporcionar la continuidad que pide R02.

[Referencia de skills](https://github.com/gotalab/cc-sdd/blob/e2a0c671aef37a482404905b409ab5c27092b25b/docs/guides/skill-reference.md) · [Personalización](https://github.com/gotalab/cc-sdd/blob/e2a0c671aef37a482404905b409ab5c27092b25b/docs/guides/customization-guide.md).

### F02 — Spec Kit: estado y controles de ejecución

Examinar `workflows/`, `templates/` y `src/specify_cli/workflows/`. Inspeccioné `workflows/ARCHITECTURE.md`: describe un motor con persistencia y reanudación. Ese motor es software adicional, no únicamente archivos de instrucciones.

Decisión pendiente: adaptar principios y contratos a un validador pequeño o adoptar parte del motor con sus dependencias y pruebas. Justificar complejidad, instalación y compatibilidad. No copiar YAML esperando que los hosts lo ejecuten solos.

[Arquitectura del motor](https://github.com/github/spec-kit/blob/0443760542e7e5269724744a2ac55c4bd386d095/workflows/ARCHITECTURE.md) · [Motor](https://github.com/github/spec-kit/tree/0443760542e7e5269724744a2ac55c4bd386d095/src/specify_cli/workflows).

### F03 — GSD Core: navegación y recuperación

Examinar `commands/gsd/`, `gsd-core/workflows/`, `gsd-core/templates/`, `gsd-core/references/` y `docs/`. Seguir sus llamadas al runtime antes de seleccionar una implementación.

Inspección concreta: `commands/gsd/progress.md`, `commands/gsd/undo.md`, flujo `gsd-core/workflows/undo.md` y guías del ciclo y recuperación. Progreso enruta según estado; undo relaciona commits y dependencias. Sus scripts y rutas de runtime impiden tratar un comando aislado como pieza autosuficiente.

[Progreso](https://github.com/open-gsd/gsd-core/blob/b747aca5b1dcff699c36d90c5b9fca0ec6354c1c/commands/gsd/progress.md) · [Recuperación](https://github.com/open-gsd/gsd-core/blob/b747aca5b1dcff699c36d90c5b9fca0ec6354c1c/gsd-core/workflows/undo.md).

### F04 — HumanLayer: investigación y plan

Examinar `.claude/commands/research_codebase.md`, `create_plan.md`, `validate_plan.md` y las definiciones relacionadas en `.claude/agents/`. Las tres instrucciones se estudiaron en esta investigación y la validación se volvió a consultar en la versión fijada.

Aprovechar la relación entre investigación, cambios y condiciones de éxito. Adaptar sus dependencias de agentes, rutas y contexto del equipo. Está orientado principalmente a trabajo sobre código existente; el descubrimiento de una idea inicial requiere otras actividades.

[Crear plan](https://github.com/humanlayer/humanlayer/blob/99abe673498cf8bdcd5f989aebe9406a27185b3b/.claude/commands/create_plan.md) · [Validarlo](https://github.com/humanlayer/humanlayer/blob/99abe673498cf8bdcd5f989aebe9406a27185b3b/.claude/commands/validate_plan.md).

### F05 — BMAD: descubrimiento y cambios de dirección

Examinar `skills/bmad-product-brief/`, `skills/bmad-prd/`, `skills/bmad-advanced-elicitation/`, `skills/bmad-architecture/` y `skills/bmad-correct-course/`.

Inspección concreta: estructura de product-brief y archivos de elicitation y correct-course. La profundización permite revisar una propuesta; el cambio de dirección analiza documentos afectados. Revisar catálogos, configuración y runtime referenciados: no trasladar su modelo entero de roles si basta un procedimiento interno.

[Profundización](https://github.com/bmad-code-org/BMAD-METHOD/blob/bda3c5929f672019b90f39a3ea27259d35d00974/skills/bmad-advanced-elicitation/SKILL.md) · [Cambio de dirección](https://github.com/bmad-code-org/BMAD-METHOD/blob/bda3c5929f672019b90f39a3ea27259d35d00974/skills/bmad-correct-course/SKILL.md).

### F06 — TEA: pruebas del producto y del método

Examinar `skills/bmad-testarch-test-design/`, `skills/bmad-testarch-trace/`, `skills/bmad-testarch-evaluate/`, `docs/explanation/how-tea-is-tested.md` y las piezas pertinentes de `test/evaluations/`, `test/fixtures/` y `test/results/`.

Inspección concreta: guía de evaluación, estructura de test-design y directorios de pruebas. La documentación describe evaluaciones con controles y defectos introducidos deliberadamente. Comprobar los registros de ejecución y el evaluador antes de aceptar una afirmación de eficacia.

Adaptar casos representativos y criterios de evaluación; no importar todo un sistema de pruebas empresariales sin justificar sus dependencias.

[Cómo se prueba TEA](https://github.com/bmad-code-org/bmad-method-test-architecture-enterprise/blob/a5675c354ecb781e99b5f83145bb1850f8f27e09/docs/explanation/how-tea-is-tested.md).

### F07 — Superpowers: diagnóstico y terminación

Examinar las carpetas completas `skills/systematic-debugging/`, `skills/verification-before-completion/` y, si hace falta, `skills/using-git-worktrees/`.

Inspeccioné las instrucciones de depuración y verificación. Comparar con las piezas equivalentes de cc-sdd y seleccionar un único protocolo por función. Las instrucciones por sí solas no constituyen una barrera técnica obligatoria.

[Depuración](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging/SKILL.md) · [Verificación](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/verification-before-completion/SKILL.md).

### F08–F11 — Referencias condicionales e histórica

- **Agent OS:** `commands/agent-os/discover-standards.md`, `index-standards.md` e `inject-standards.md`. Investigar selección de contexto si nuestros recursos crecen; no añadir otro coordinador. Inspección concreta de inject-standards.
- **OpenSpec:** `schemas/spec-driven/` y `docs/editing-changes.md`. Investigar contratos de cambios frente a especificaciones vigentes si R11 necesita mayor formalización. Su esquema se consultó en la versión fijada.
- **GitHub Agentic Workflows:** `.github/workflows/ci-coach.md` y `deployment-incident-monitor.md`. Referencia posterior para operación en GitHub; requiere servicios, permisos y runtime propios. No reemplaza la verificación del producto. Inspección concreta del monitor.
- **GSD antiguo:** el [README fijado](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/README.md) indica el traslado a GSD Core. No seleccionarlo como otra base activa.

### Procedimiento de extracción, una pieza por vez

1. Leer esta ficha y verificar la versión. Obtener el repositorio sin ejecutar instaladores; usar sparse checkout si conviene, conservando licencia y referencias necesarias.
2. Leer la carpeta seleccionada completa y seguir rutas, importaciones, scripts, plantillas y archivos de configuración a los que remita. Ampliar la extracción si descubre dependencias.
3. Registrar entrada, salida, precondiciones, pasos, estado, verificaciones, fallos y retorno. Identificar instrucciones exclusivas de un host.
4. Vincular la pieza con requisitos R01–R20. Clasificar: conservar, adaptar, inspiración, redundante o descartar. Registrar qué demuestra su evidencia y qué no.
5. Proponer su incorporación al contrato común. Resolver nombres, estados y documentos contradictorios antes de programar.
6. Construir un caso que verifique la necesidad cubierta y un caso que deba bloquear o fallar. Solo entonces incorporar el comportamiento.
7. Actualizar trazabilidad, versiones y avisos. Mantener las fuentes originales como referencia, separadas de las instrucciones activas del paquete.

Ficha mínima: `fuente, commit, ruta, licencia, requisito cubierto, entradas, salidas, dependencias, mecanismo de control, evidencia, limitaciones, adaptación, prueba de integración, decisión`.

Ejemplo concreto para obtener la primera fuente, desde la raíz de trabajo, después de comprobar que el destino no existe:

```bash
git clone --filter=blob:none --no-checkout https://github.com/gotalab/cc-sdd.git .reference-sources/cc-sdd
git -C .reference-sources/cc-sdd sparse-checkout init --cone
git -C .reference-sources/cc-sdd sparse-checkout set docs/guides tools/cc-sdd/templates
git -C .reference-sources/cc-sdd checkout --detach e2a0c671aef37a482404905b409ab5c27092b25b
git -C .reference-sources/cc-sdd rev-parse HEAD
```

Esto obtiene referencias para estudiar, no instala cc-sdd. Los archivos raíz del repositorio se conservan en cone mode; comprobar la licencia. Para otra fuente, reemplazar URL, destino, selección y commit usando el inventario. Si ya existe el destino, comprobar su identidad y estado; no borrarlo ni sobrescribirlo.

## 8. Tablero de construcción

Estado inicial: encargo definido y referencias identificadas. Las tareas siguientes están pendientes; no marcar ninguna como realizada por el mero hecho de tener este documento. Crear una vista mantenible en `docs/tablero.md` durante B01.

Estados: `pendiente`, `preparada`, `en_curso`, `bloqueada`, `en_revision`, `verificada`. Cada tarea registra responsable, requisitos cubiertos, evidencia, checkpoint y siguiente actividad. Solo empezar tareas con dependencias verificadas. El descubrimiento de una dependencia cambia el tablero de manera explícita.

| ID | Trabajo | Depende de | Condición observable de terminación |
|---|---|---|---|
| B01 | Inspeccionar carpeta, herramientas y archivos existentes; conservar encargo y crear tablero. | — | Se conoce el entorno y existe un registro del estado inicial sin sobrescribir trabajo previo. |
| B02 | Obtener referencias principales y guardar versiones, rutas y licencias. | B01 | El inventario reproduce los commits consultados y distingue fuentes originales de archivos propios. |
| B03 | Auditar cc-sdd, incluyendo sus dos hosts y dependencias de recursos. | B02 | Hay una ficha del recorrido real, sus paradas, estado, documentos, validaciones y huecos frente a R01–R20. |
| B04 | Comparar coordinación y recuperación de Spec Kit y GSD Core. | B02 | Matriz con mecanismos, dependencias, costes y límites; sin mezclar sus estados. |
| B05 | Auditar complementos de producto, investigación, pruebas y diagnóstico. | B02 | Cada pieza propuesta tiene ficha y requisito; redundancias y ausencias quedan visibles. |
| B06 | Elegir base y extracciones mínimas; producir mapa de cobertura. | B03–B05 | Cada requisito tiene una solución prevista o un desarrollo propio explícito. Decisiones fundadas, no selección por popularidad. |
| B07 | Elaborar especificaciones del paquete y análisis de alternativas. | B06 | Se describen flujo, estado, decisiones, trazabilidad, recuperación, dos adaptadores, instalación y verificaciones. |
| B08 | Diseñar contratos y comprobaciones de integridad. | B07 | Referencias y estados válidos definidos; cambios incompatibles o evidencia inválida producen un resultado verificable. |
| B09 | Construir prototipo de documentación guiada con una única entrada. | B08 | Una idea vaga llega a un incremento preparado con decisiones y preguntas registradas; no exige que el usuario elija skills. |
| B10 | Añadir continuidad, anotaciones e impacto de cambios. | B09 | Una sesión nueva retoma el punto correcto y un requisito modificado invalida las partes afectadas. |
| B11 | Añadir puntos de recuperación y recuperación aislada. | B10 | Puede abrirse una rama/worktree desde un checkpoint y seguir allí, conservando el trabajo posterior. |
| B12 | Implementar división, asignación y control de tareas. | B09 | Una tarea sobredimensionada se divide; las dependencias sin resolver bloquean solo el trabajo pertinente. |
| B13 | Integrar implementación, revisión, verificación y diagnóstico. | B11–B12 | Un fallo y una reparación se gestionan con evidencia; el agente no marca éxito ante pruebas fallidas u omitidas. |
| B14 | Incorporar preparación de entrega, operación y mantenimiento. | B13 | El flujo genera un plan contextual de entrega y recuperación; registra comprobaciones reales pendientes. |
| B15 | Implementar adaptadores Claude Code y Cursor. | B09 | Ambos cargan el núcleo y sus recursos desde ubicaciones correctas; diferencias de herramientas registradas. |
| B16 | Implementar instalación, actualización y retirada. | B15 | Instalación en carpeta de prueba, detección de conflictos, rutas válidas y retirada limitada a archivos propios. |
| B17 | Probar integridad, interrupciones y recuperación. | B10–B11, B16 | Pruebas de referencias rotas, escritura interrumpida, estado inválido y cambios sin commit con resultados esperados. |
| B18 | Evaluar el comportamiento del agente sobre casos controlados. | B12–B14, B17 | Casos sanos y casos con defectos; evidencia independiente de la autoevaluación del agente. |
| B19 | Ejecutar escenarios en Claude Code y Cursor reales. | B15–B18 | Resultados por host y versión. Si falta un host o acceso, R01 permanece parcialmente pendiente. |
| B20 | Probar un incremento con componentes interactuando y un cambio posterior. | B19 | Se verifica integración real en fixture/proyecto de prueba, se modifica un requisito y se comprueba la recuperación del flujo. |
| B21 | Preparar versión candidata y guía breve de usuario. | B20 | Paquete reproducible con requisitos satisfechos y límites explícitos; usuario aprende la entrada común y las acciones de control. |
| B22 | Mantener y mejorar el propio paquete. | B21 | Política de versiones, migración, actualización de fuentes y escenarios de regresión definida. |

B05 puede explorar condicionales cuando detecte un hueco. B07 debe dividirse si sus especificaciones resultan demasiado grandes para revisarlas juntas. Las tareas de esta tabla son hitos del tablero: antes de ejecutarlas, descomponer las que lo requieran en unidades concretas.

No encerrar una incertidumbre técnica dentro de una tarea de implementación. Crear una investigación con pregunta y condición de cierre. No hay una duración o un número de líneas universal que haga pequeña una tarea.

### Tres entregas revisables

- **Entrega A — B01 a B08:** fuentes auditadas, selección, especificaciones y contratos. Debe poder revisarse el diseño antes de implementar coordinadores.
- **Entrega B — B09 a B11, B15 y primera parte de B16:** flujo documental guiado con estado y recuperación, instalable en un proyecto de prueba en ambos hosts.
- **Entrega C — resto del tablero:** ejecución completa, integración, operación, evaluación y versión candidata.

Las entregas permiten obtener evidencia temprano. La Entrega B no autoriza afirmar que el método completo ya funciona en productos complejos.

## 9. Especificaciones que debe producir el agente

Durante B07, desarrollar registros separados pero relacionados:

1. **Producto del paquete:** usuarios, problema, alcance, restricciones y R01–R20. El propio paquete es el producto que estamos diseñando.
2. **Contrato del coordinador:** entradas, actividades, selección del próximo paso, pausas por decisiones, respuestas y derivación a investigación.
3. **Contrato documental:** identificadores, procedencia, versiones, autoridad, enlaces y cambio de requisitos.
4. **Contrato de estado:** transiciones, bloqueo, revisión, evidencia, reanudación, escritor único y reparación después de interrupciones.
5. **Contrato de decisiones:** propuesta, aceptación, rechazo, apuntes, sustitución y análisis de impacto.
6. **Contrato de recuperación:** checkpoint, comparación, recuperación aislada, protección de cambios y límites de acciones externas.
7. **Contrato de hosts e instalación:** carga, recursos, metadatos, herramientas, conflictos, actualización y retirada.
8. **Plan de evaluación:** escenarios, resultados esperados, mecanismos comprobables y límites de la evidencia.

Cada especificación debe explicar qué la inicia, qué produce, cómo se revisa y qué permite avanzar. Si la auditoría propone una estructura mejor, se puede modificar conservando trazabilidad y justificando el cambio.

Antes de programar, revisar que un documento pueda usarse como entrada del siguiente sin reinterpretaciones contradictorias. El coordinador debe detectar entradas ausentes o desactualizadas; no asumir que todos los archivos existentes siguen siendo válidos.

## 10. Evaluaciones obligatorias

Distinguir comprobaciones deterministas del paquete y observaciones del agente. Las primeras revisan contratos, referencias y recuperación. Las segundas comprueban si el agente sigue el método en una ejecución real. Una plantilla correcta no demuestra un comportamiento correcto.

| Caso | Situación de entrada | Comportamiento esperado |
|---|---|---|
| E01 | Idea vaga de un producto | Preguntas pertinentes y propuestas investigables; no inventa todos los requisitos ni solicita al usuario una especificación completa. |
| E02 | Varias alternativas y apuntes del usuario | Conserva aceptación, rechazo y pendientes con sus motivos y referencias. |
| E03 | «Acepto esa» con dos propuestas activas | Aclara cuál antes de registrar aceptación. |
| E04 | Integración sin clave o acceso | Documenta el bloqueo, distingue simulación y ejecución real y continúa trabajo independiente preparado. |
| E05 | Una tarea mezcla servidor, permisos, procesos asíncronos y varias dudas | Divide el trabajo y descubre dependencias; conserva un recorrido integrado que verificar. |
| E06 | Sesión nueva con documentos y código modificados | Detecta cambios, reconstruye estado y muestra pendientes; no confía en un resumen antiguo. |
| E07 | Cambio de una decisión aceptada | Conserva historia y marca para revisión requisitos, tareas y evidencia afectadas. |
| E08 | Agente afirma «todo funciona» sin ejecutar la comprobación | La tarea sigue sin verificar y la afirmación no se acepta como evidencia. |
| E09 | Pruebas pasan únicamente con un proveedor simulado | Explicita que la integración real sigue pendiente. |
| E10 | Reparaciones repetidas amplían cambios sin resolver el fallo | Detiene implementación, conserva evidencia y vuelve a diagnóstico o diseño. |
| E11 | Usuario solicita un checkpoint anterior con cambios sin commit | Inspecciona y preserva trabajo; recuperación aislada sin borrar archivos. |
| E12 | Interrupción entre cambios de documentos y actualización del estado | Detecta la transición incompleta y recupera coherencia sin repetir efectos externos. |
| E13 | Cambio de host a mitad del proyecto | Usa los mismos registros y continúa correctamente en el otro host. |
| E14 | Instalación repetida, colisión de nombre o retirada | No duplica carga ni sobrescribe archivos ajenos; informa y resuelve el conflicto. |
| E15 | Fixture correcto, sin defecto introducido | No inventa problemas para justificar controles. |
| E16 | Actualización de versión del paquete | Migra el estado de una copia de prueba y conserva decisiones y evidencia histórica. |
| E17 | Integración entre varios componentes y posterior modificación | Comprueba el recorrido y detecta regresiones fuera de la tarea local. |
| E18 | Checkpoint de código anterior a una migración externa | Advierte el alcance técnico de la recuperación y aplica el procedimiento de datos previsto, sin declarar que Git restauró el servicio. |

Los defectos de los fixtures deben ser conocidos por el evaluador y no indicarse al agente en el nombre de la carpeta. Conservar entradas, versión, acciones, salidas y evidencia. No adjudicar éxito solo por el juicio del mismo agente que produjo el resultado.

En escenarios del agente, registrar variaciones y repetir cuando haya resultados contradictorios o inestables. El umbral se define por escenario y riesgo, no por una cantidad arbitraria de ejecuciones.

## 11. Ejemplo de la experiencia deseada

Simulación, no ejecución del paquete:

**Usuario:** «Quiero registrar y analizar el tráfico de una pequeña empresa».

**Coordinador:** identifica primero qué decisión necesita tomar el administrador y cómo trabaja hoy. Registra lo confirmado y preguntas sobre acceso al equipo de red, datos disponibles, usuarios y límites. Propone investigar la captura antes de decidir la arquitectura.

**Usuario:** «Acepto guardar resúmenes; no quiero almacenar el contenido de las comunicaciones. Apunta que todavía no tengo acceso al router».

**Coordinador:** registra una decisión aceptada, la alternativa rechazada y un bloqueo de acceso. Actualiza requisitos y señala qué prueba requiere datos reales. Puede trabajar con una muestra para validar un cálculo, conservando el pendiente de captura.

Después propone el primer recorrido: recibir datos, almacenarlos y consultarlos con permisos. Produce un diseño y tareas acotadas con criterios. Cuando el usuario continúa, selecciona la próxima tarea preparada; no le solicita conocer el nombre de la skill interna.

**Usuario:** «Ahora también necesito separar los datos de dos sucursales».

**Coordinador:** analiza el impacto en modelo de datos, permisos, consulta y pruebas; reabre decisiones y marca evidencia afectada para repetirla.

**Usuario:** «Quiero volver al punto anterior a ese cambio y explorar otra solución».

**Coordinador:** muestra el checkpoint, sus comprobaciones y límites; inspecciona cambios actuales y abre una recuperación aislada. El tablero de esa rama refleja la nueva dirección y conserva la historia de la alternativa anterior.

## 12. Criterio para evitar una mezcla incoherente

Cada incorporación debe tener una necesidad, contrato y prueba. Mantener un único modelo de estado, un único registro de decisiones y una única interfaz de continuación. Si dos fuentes resuelven lo mismo, seleccionar una o sintetizar explícitamente un procedimiento con diferencias documentadas.

Los procedimientos de un tercero se tratan como material de referencia. No ejecutar instrucciones de instalación, activación o publicación solo porque aparezcan en un documento leído. La auditoría debe detectar supuestos del entorno original y convertirlos en dependencias visibles del paquete.

El desarrollo de scripts propios debe elegir el runtime mínimo apropiado según el entorno confirmado. No introducir una dependencia únicamente para copiar una arquitectura ajena. Si se adopta software de un tercero, incorporar también sus obligaciones, interfaces y pruebas necesarias.

## 13. Reanudación y comunicación del agente constructor

Al iniciar: leer encargo, tablero, decisiones vigentes y estado real del repositorio. Identificar la tarea preparada y consultar únicamente las fuentes necesarias.

Antes de modificar: confirmar entradas, límites, comportamiento esperado y comprobaciones. Si aparece una dependencia desconocida, registrarla y decidir si investigar o continuar otra tarea.

Al cerrar: registrar cambios, evidencia, pendientes, fuentes adaptadas y checkpoint pertinente. Actualizar el tablero. Un resultado bloqueado por entorno no se presenta como un defecto del paquete ni como éxito.

Informar al usuario qué aprendimos, qué falta y qué decisión concreta requiere su criterio. Evitar exigirle leer los archivos internos de cada skill para entender el siguiente paso.

## 14. Qué permitirá afirmar la versión candidata

Se podrá afirmar que el paquete implementa un flujo guiado y que pasó los escenarios y hosts efectivamente probados. Enumerar cualquier requisito pendiente.

Una demostración del flujo documental verifica solo esa parte. Un fixture con integración y mantenimiento aproxima necesidades de sistemas complejos, pero no prueba utilidad en cualquier producto. Para una afirmación más amplia se necesitarán proyectos reales, uso sostenido y cambios posteriores documentados.

El resultado final debe incluir fuentes y avisos, especificaciones, núcleo, adaptadores, instalación, comprobaciones, evidencia por host y una guía breve que empiece por iniciar, continuar, decidir y recuperar.


