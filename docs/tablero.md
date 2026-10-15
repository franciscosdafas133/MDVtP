# Tablero de construcción del paquete

Vista mantenible del progreso de construcción **del método** (no de una aplicación de usuario). Encargo: [PLAN_PAQUETE_FLUJO_IA.md](../PLAN_PAQUETE_FLUJO_IA.md) (se conserva en la raíz, sin copiarlo, para no crear dos autoridades). Objetivos: [objetivos.md](objetivos.md). Reglas: [reglas-hacer.md](reglas-hacer.md) y [reglas-no-hacer.md](reglas-no-hacer.md). Especificaciones: [especificaciones/](especificaciones/README.md). Decisiones: [decisiones.md](decisiones.md). Selección: [seleccion.md](seleccion.md).

Última actualización: 2026-10-14.

## Estados

`pendiente` → `preparada` → `en_curso` → `en_revision` → `verificada`; cualquier estado activo puede pasar a `bloqueada`.

- Solo pasa a `preparada` una tarea cuyas dependencias están `verificadas`.
- `verificada` exige evidencia pertinente y vigente registrada en esta tabla o enlazada.
- Descubrir una dependencia nueva cambia el tablero de forma explícita (anotar en «Cambios del tablero»).
- Los hitos B01–B22 se descomponen en unidades concretas antes de ejecutarse cuando lo requieran.

## Resumen

| Estado | Tareas |
|---|---|
| en_curso | — |
| en_revision | — |
| preparada | — |
| pendiente | — |
| bloqueada | — |
| verificada | B01–B22, I-01 |

**Siguiente actividad:** cerrar e2e v3 nivel 4 → luego sonda “producto complejo” (grafo de conceptos + recuperación; ver [OBJETIVO-PRODUCTO-COMPLEJO.md](especificaciones/OBJETIVO-PRODUCTO-COMPLEJO.md)). Mantener/publicar en GitHub al afinar.  
**Entrega B:** cerrada · **Entrega C:** cerrada (tablero completo).  
**Norte de producto (no es un hito B):** aprender con grafos de conceptos + recuperar conocimiento + LLM con fronteras honestas.

## Tareas

Responsable por defecto: agente constructor. Las decisiones de producto corresponden al usuario. La columna «Req.» es una asignación propuesta en B01; se revisará en B06.

| ID | Trabajo | Depende de | Estado | Req. | Entrega | Condición observable de terminación |
|---|---|---|---|---|---|---|
| B01 | Inspeccionar carpeta, herramientas y archivos existentes; conservar encargo y crear tablero. | — | verificada | — | A | Se conoce el entorno y existe un registro del estado inicial sin sobrescribir trabajo previo. |
| B02 | Obtener referencias principales y guardar versiones, rutas y licencias. | B01 | verificada | R20 | A | El inventario reproduce los commits consultados y distingue fuentes originales de archivos propios. |
| B03 | Auditar cc-sdd, incluyendo sus dos hosts y dependencias de recursos. | B02 | verificada | R01–R20 | A | Hay una ficha del recorrido real, sus paradas, estado, documentos, validaciones y huecos frente a R01–R20. |
| B04 | Comparar coordinación y recuperación de Spec Kit y GSD Core. | B02 | verificada | R08, R12, R13, R19 | A | Matriz con mecanismos, dependencias, costes y límites; sin mezclar sus estados. |
| B05 | Auditar complementos de producto, investigación, pruebas y diagnóstico. | B02 | verificada | R03, R05, R11, R14, R15, R18 | A | Cada pieza propuesta tiene ficha y requisito; redundancias y ausencias quedan visibles. |
| B06 | Elegir base y extracciones mínimas; producir mapa de cobertura. | B03, B04, B05 | verificada | R01–R20 | A | Cada requisito tiene una solución prevista o un desarrollo propio explícito. Decisiones fundadas, no selección por popularidad. |
| I-01 | Investigación: ¿puede una ventana editable usar la IA del host (Cursor / Claude Code) para corregir y proponer documentación en el momento? | B06 (DEC-01) | verificada | R01, R02, R05, R06 | A | Resultado registrado por host (funciona / en parte / no) con versión y evidencia, según la [ficha](investigaciones/I-01-ventana-interactiva.md). |
| B07 | Elaborar especificaciones del paquete y análisis de alternativas. | B06 | verificada | R01–R20 | A | Se describen flujo, estado, decisiones, trazabilidad, recuperación, dos adaptadores, instalación y verificaciones. |
| B08 | Diseñar contratos y comprobaciones de integridad. | B07 | verificada | R04, R05, R07, R11, R19 | A | Referencias y estados válidos definidos; cambios incompatibles o evidencia inválida producen un resultado verificable. |
| B09 | Construir prototipo de documentación guiada con una única entrada. | B08 | verificada | R02, R03, R04, R05, R06, R17 | B | Una idea vaga llega a un incremento preparado con decisiones y preguntas registradas; no exige que el usuario elija skills. |
| B10 | Añadir continuidad, anotaciones e impacto de cambios. | B09 | verificada | R06, R08, R11, R13 | B | Una sesión nueva retoma el punto correcto y un requisito modificado invalida las partes afectadas. |
| B11 | Añadir puntos de recuperación y recuperación aislada. | B10 | verificada | R12 | B | Puede abrirse una rama/worktree desde un checkpoint y seguir allí, conservando el trabajo posterior. |
| B12 | Implementar división, asignación y control de tareas. | B09 | verificada | R09, R10 | C | Una tarea sobredimensionada se divide; las dependencias sin resolver bloquean solo el trabajo pertinente. |
| B13 | Integrar implementación, revisión, verificación y diagnóstico. | B11, B12 | verificada | R14, R15 | C | Un fallo y una reparación se gestionan con evidencia; el agente no marca éxito ante pruebas fallidas u omitidas. |
| B14 | Incorporar preparación de entrega, operación y mantenimiento. | B13 | verificada | R18 | C | El flujo genera un plan contextual de entrega y recuperación; registra comprobaciones reales pendientes. |
| B15 | Implementar adaptadores Claude Code y Cursor. | B09 | verificada | R01 | B | Ambos cargan el núcleo y sus recursos desde ubicaciones correctas; diferencias de herramientas registradas. |
| B16 | Implementar instalación, actualización y retirada. | B15 | verificada | R16 | B (1.ª parte) / C | Instalación en carpeta de prueba, detección de conflictos, rutas válidas y retirada limitada a archivos propios. |
| B17 | Probar integridad, interrupciones y recuperación. | B10, B11, B16 | verificada | R12, R13, R19 | C | Pruebas de referencias rotas, escritura interrumpida, estado inválido y cambios sin commit con resultados esperados. |
| B18 | Evaluar el comportamiento del agente sobre casos controlados. | B12, B13, B14, B17 | verificada | R14 (E01–E18) | C | Casos sanos y casos con defectos; evidencia independiente de la autoevaluación del agente. Nota: parte O pendiente → B19. |
| B19 | Ejecutar escenarios en Claude Code y Cursor reales. | B15–B18 | verificada | R01 | C | Resultados por host y versión. Si falta un host o acceso, R01 permanece parcialmente pendiente. |
| B20 | Probar un incremento con componentes interactuando y un cambio posterior. | B19 | verificada | R07, R11, R18 | C | Se verifica integración real en fixture/proyecto de prueba, se modifica un requisito y se comprueba la recuperación del flujo. |
| B21 | Preparar versión candidata y guía breve de usuario. | B20 | verificada | R02, R17 | C | Paquete reproducible con requisitos satisfechos y límites explícitos; usuario aprende la entrada común y las acciones de control. |
| B22 | Mantener y mejorar el propio paquete. | B21 | verificada | R20 | C | Política de versiones, migración, actualización de fuentes y escenarios de regresión definida. |

Notas del encargo: B05 puede explorar fuentes condicionales (F08–F10) si detecta un hueco. B07 debe dividirse si sus especificaciones son demasiado grandes para revisarlas juntas. Una incertidumbre técnica no se esconde dentro de una tarea de implementación: se crea una investigación con pregunta y condición de cierre.

## Entregas revisables

- **Entrega A — B01 a B08:** fuentes auditadas, selección, especificaciones y contratos. Se revisa el diseño antes de implementar coordinadores.
- **Entrega B — B09 a B11, B15 y primera parte de B16:** **cerrada 2026-10-14.** Flujo documental guiado con estado, recuperación e instalación global/proyecto. No autoriza afirmar que el método completo funciona en productos complejos.
- **Entrega C — resto del tablero:** ejecución completa, integración, operación, evaluación y versión candidata.

## Detalle de la tarea activa

### I-01 — verificada

- **Resultado Cursor:** funciona en parte (HTML aparte). MCP App en chat: no.
- **DEC-02:** aceptada — al aplicar la skill debe abrirse localhost enlazado al IDE.

### B22 — verificada

- Usuario: `paso 22 ok`. Repo: https://github.com/franciscosdafas133/MDVtP

### B21 — verificada

- Usuario: okey / sigamos al 22. `0.1.0-rc1` + guía.

### B20 — verificada

- Usuario: `paso 20 ok`.

### B19 — verificada

- Cursor + Claude Code aprobados por el usuario.

### B18 — verificada (parcial D)

- Usuario: `paso 18 parcial ok`. Observación agente → B19.

### B17 — verificada

- Usuario: `paso 17 ok`. `run_integridad.py` 8/8.

### B14 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia:** `operar` + `demo-b14`. Usuario: `paso 14 ok`.
- **Siguiente actividad:** B17 (+ recorrido producto simple).

### B13 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia:** evidenciar/verificar/depurar + ciclo **escanear→planificar→evaluar→reemplazar** (apunte usuario). `demo-b13` OK. Usuario: `paso 13 ok`.
- **Siguiente actividad:** B14.

### B12 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia:** dividir con criterios + paralelo/cadena; `demo-b12` OK. Usuario: `paso 12 ok`.
- **Siguiente actividad:** B13.

### B15 / B16 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia:** instalador global/proyecto; skill self-contained; [INSTALL.md](../INSTALL.md). Usuario: `entrega B ok` (2026-10-14).
- **Siguiente actividad:** B12 (entrega C).

### B11 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia (2026-10-12):** checkpoint/recuperar + demo-b11. Usuario de acuerdo con el orden (cierra 11 e instalación).
- **Siguiente actividad:** B15/B16.

### B10 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia (2026-10-12):** anotar/impactar/continuar; `demo-b10` OK. Usuario: `paso 10 ok`.
- **Siguiente actividad:** B11.

### B09 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia (2026-10-12):** skill `product-flow`, plantillas, `product_flow.py demo` OK. Usuario: `paso 9 ok`.
- **Siguiente actividad:** B10.

### B08 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia (2026-10-12):** `core/contracts/`; `scripts/validate_workflow.py`; fixtures; [REVISION-paso-8.md](especificaciones/REVISION-paso-8.md). Self-test OK. Usuario: `paso 8 ok`.
- **Siguiente actividad:** B09.

### B07 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia (2026-10-12):** ESP-01…08 borrador 0.2; [REVISION-paso-7.md](especificaciones/REVISION-paso-7.md). Usuario: de acuerdo («construye»).
- **Siguiente actividad:** B08.

### B06 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia (2026-10-12):** [seleccion.md](seleccion.md); [decisiones.md](decisiones.md) con DEC-01…08 **aceptadas**; I-01 verificada (HTML aparte, funciona en parte).
- **Checkpoint:** `CP-06` = commit de selección + este cierre de decisiones (pendiente de commit si el usuario lo pide).
- **Siguiente actividad:** B07.


### B05 — verificada

- **Responsable:** agente constructor.
- **Evidencia (2026-10-12):** F04–F07 obtenidas por sparse checkout, con los commits verificados y las licencias registradas. Informe en [auditoria/F04-F07-complementos.md](auditoria/F04-F07-complementos.md): fichas por pieza, comparación de protocolos de verificación y depuración (uno por función), dependencias de entorno, 8 hallazgos y cobertura R01–R20 tras B03–B05, con las ausencias visibles.
- **Ausencia principal:** R18 (entrega, operación y mantenimiento) no la cubre ninguna fuente; desarrollo propio en B14.
- **Restricciones de redistribución:** la marca BMad no está cubierta por MIT (renombrar las piezas de F05 y F06); F04 es Apache-2.0 (conservar el aviso y declarar los cambios).
- **Condicionales F08–F10:** no obtenidas; motivos registrados en la ficha (§6).
- **Límites:** no se ejecutó nada; los resultados de TEA prueban la procedencia de sus ejecuciones, no su eficacia.
- **Checkpoint:** `CP-05` = commits `706bb0d` (fuentes y ficha) + este (tablero).
- **Siguiente actividad:** B06.


### B04 — verificada

- **Responsable:** agente constructor.
- **Evidencia (2026-10-12):** [auditoria/F02-F03-coordinacion-recuperacion.md](auditoria/F02-F03-coordinacion-recuperacion.md), con una matriz de 15 mecanismos (coordinación, estado, transiciones, atomicidad, eventos, reanudación, siguiente paso, evidencia obsoleta, puertas, avance automático, deshacer, instalación, hosts, dependencias, tamaño) y 11 hallazgos. Los estados de ambas fuentes se describen por separado.
- **Conclusiones propuestas para B06:** no adoptar el motor de Spec Kit, porque exige lanzar al agente en modo no interactivo con permisos amplios y rompe R02; no adoptar el runtime de GSD (tamaño y dependencias). En su lugar, un validador propio que copia el contrato de estado de Spec Kit, la tabla de rutas y la evidencia `stale` de GSD, y el manifiesto con SHA-256 de Spec Kit para R16. R12 (recuperación aislada) requiere desarrollo propio.
- **Límites:** no se ejecutó nada; no se leyó el código de `gsd-tools.cjs` ni la mayor parte de `engine.py`.
- **Checkpoint:** `CP-04` = commit «B04: comparación de Spec Kit y GSD Core».
- **Siguiente actividad:** B05.


### B03 — verificada

- **Responsable:** agente constructor.
- **Evidencia (2026-10-12):** [auditoria/F01-cc-sdd.md](auditoria/F01-cc-sdd.md) con recorrido real y paradas, estado y documentos, controles, instalación, diferencias entre hosts, 11 hallazgos, fichas por pieza y huecos frente a R01–R20. La sección 1 declara qué se leyó entero, qué por búsqueda dirigida y qué no se leyó.
- **Ampliación de fuente:** sparse checkout de F01 ampliado con `tools/cc-sdd/src` y `tools/cc-sdd/test` para seguir el instalador (procedimiento §7, paso 2); lock actualizado.
- **Hallazgos principales:** las fases se detienen y exigen conocer la skill siguiente (H1); el estado no tiene validación (H2); hay aprobaciones implícitas al generar la fase siguiente (H3); las variantes por host están duplicadas y con deriva (H4); no hay retirada del instalador; no hay checkpoints, invalidación ni operación.
- **Límites:** no se ejecutó nada; las afirmaciones sobre Cursor (`openai.yaml`, `disable-model-invocation`, `$1`) quedan sin comprobar hasta B15.
- **Checkpoint:** `CP-03` = commit «B03: auditoría de cc-sdd».
- **Siguiente actividad:** B04.


### B02 — verificada

- **Responsable:** agente constructor.
- **Alcance:** fuentes principales F01–F03. Los complementos F04–F07 se obtienen en B05, cuando se audite cada pieza; las condicionales F08–F10 solo si aparece un hueco; F11 no se obtiene.
- **Evidencia (2026-10-12):**
  - Sparse checkout en `.reference-sources/{cc-sdd,spec-kit,gsd-core}`; `git rev-parse HEAD` coincide con los commits del encargo en las tres copias.
  - Licencias raíz MIT leídas; huellas SHA-256 en [sources.lock.json](../sources.lock.json), comprobadas con `sha256sum -c`.
  - Existen todas las rutas que cita el encargo, incluidas las diez skills `kiro-*` en ambas variantes de host.
  - Inventario y separación entre fuentes y archivos propios en [fuentes.md](fuentes.md). `.reference-sources/` está excluido de git.
  - No se ejecutó ningún instalador, script ni suite de las fuentes.
- **Hallazgo:** las copias contienen `CLAUDE.md`/`AGENTS.md` que un host podría cargar como instrucciones (riesgo R-01 en [fuentes.md](fuentes.md)).
- **Checkpoint:** `CP-02` = commit «B02: inventario y lock de fuentes principales».
- **Siguiente actividad:** B03.


### B01 — verificada

- **Responsable:** agente constructor. Revisión: usuario.
- **Evidencia (2026-10-12):**
  - Carpeta `creación_método/` contenía solo `PLAN_PAQUETE_FLUJO_IA.md` (43 620 bytes, 423 líneas). No se sobrescribió ni movió.
  - La carpeta **no es un repositorio git** (`git rev-parse` → «not a git repository»), tampoco sus carpetas padre.
  - Herramientas detectadas: git 2.53.0, Node v24.21.0, Python 3.13.12, jq 1.8.1, Cursor 3.22.12 (CLI `cursor`). `npm` no está en el PATH. La CLI `claude` no está en el PATH; Claude Code se usa como extensión de VS Code (versión sin registrar).
  - Sistema: Linux 6.19.14 (Kali), shell zsh.
  - Archivos creados: `docs/tablero.md`, `docs/objetivos.md`, `docs/reglas-hacer.md`, `docs/reglas-no-hacer.md`, `docs/especificaciones/` (borradores 0.1).
- **Repositorio:** git inicializado en `main` (2026-10-12) con identidad local del usuario; `.gitignore` excluye `.reference-sources/`.
- **Revisión:** aceptada por el usuario el 2026-10-12.
- **Checkpoint:** `CP-01` = commit «B01: estado inicial, tablero, objetivos, reglas y especificaciones 0.1». Comprobado solo para: existencia y contenido de los documentos de B01; no hay código ni pruebas.
- **Siguiente actividad:** B02 (obtener F01–F03 con sparse checkout en `.reference-sources/`, sin ejecutar instaladores).

## Preguntas y bloqueos abiertos

| ID | Pregunta | Por qué importa | Afecta a | Quién responde |
|---|---|---|---|---|
| ~~P-01~~ | ~~¿Inicializar un repositorio git en `creación_método/`?~~ **Resuelta 2026-10-12: sí.** | Sin git no hay commits ni checkpoints para la propia construcción (R12) y B02 colocará clones dentro de la carpeta; conviene excluir `.reference-sources/` con `.gitignore`. | B01, B02, B11 | Usuario |
| P-02 | ¿Qué versión de Claude Code (extensión) se usará para las pruebas reales? | R01 exige registrar versiones de host. | B15, B19 | Usuario / se puede consultar más adelante |
| R-01 | Instrucciones de terceros (`CLAUDE.md`, `AGENTS.md`) dentro de `.reference-sources/` podrían cargarse como contexto activo. | Podrían desviar al agente constructor (N-06, N-07). | B03–B05, B15 | Agente: tratarlos como datos; comprobar en B15 |
| ~~P-03~~ | ~~`npm` / Node~~ **Resuelta en B07/B08: runtime = Python 3 stdlib** (validador, ventana, instalador). Node no obligatorio. | — | B16 | — |

## Cambios del tablero

| Fecha | Cambio | Motivo |
|---|---|---|
| 2026-10-14 | Norte explícito: producto complejo (grafos de conceptos + recuperación + LLM con fronteras). Camino: cerrar e2e-4 → sondas complejas. | Usuario: apuntar a ese tipo de producto, no hacerlo de golpe. |
| 2026-10-14 | Oleada C (e2e-v2-1 @ 95f38ae): construir 4/5; formular 2/5. Local: modo rápido, anti-true/manual, huellas cubre, decidir. Falta publicar. | Usuario pegó INFORME-METODO + e2e-v2. |
| 2026-10-14 | Oleada e2e dueños: anti-simulación, modo rápido, pistas de negocio, impactar DEC, regresión OK. | Usuario: analizar pruebas para mejorar, no reinventar. |
| 2026-10-14 | B22 verificada; publicación a GitHub MDVtP. | Usuario: paso 22 ok + URL del repo. |
| 2026-10-14 | B21 verificada; B22 en_revision (mantenimiento + regresión + checklist GitHub). | Usuario: okey, sigamos al 22; luego GitHub. |
| 2026-10-14 | B20 verificada; B21 en_revision (0.1.0-rc1 + guía). | Usuario: paso 20 ok. |
| 2026-10-14 | B19 verificada (claude ok); B20 en_revision (integración + impactar). | Usuario: claude ok, continuemos. |
| 2026-10-14 | B19 Cursor aprobado por usuario; Claude pendiente. | Usuario: aprobado. |
| 2026-10-14 | B17 verificada; B18 parcial ok; B19 en_curso. | Usuario: sí. |
| 2026-10-14 | B17/B18 en_revision: batería integridad + eval determinista; obs. agente pendiente. | Usuario: haz los pasos; luego modo evaluador. |
| 2026-10-14 | B14 verificada; B17 en_curso; añadido recorrido-simple (semilla B18). | Usuario: paso 14 ok; pidió agente que recorra producto simple. |
| 2026-10-14 | B14 en_revision: operar + demo-b14. | Plan de entrega y pendientes reales (R18). |
| 2026-10-14 | B13 verificada (ciclo escanear→planificar→evaluar→reemplazar); B14 en_curso. | Usuario: paso 13 ok con ese ciclo. |
| 2026-10-14 | B13 en_revision: evidenciar/verificar/depurar + demo-b13. | Verificación honesta DEC-04/05. |
| 2026-10-14 | B12 verificada; B13 en_curso. | Usuario: `paso 12 ok`. |
| 2026-10-14 | B12 en_revision: dividir/bloquear + demo-b12. | Inicio entrega C. |
| 2026-10-14 | Entrega B cerrada (B15/B16 verificadas); B12 en_curso. | Usuario: `entrega B ok`. |
| 2026-10-12 | B15/B16 en_revision: instalador + adaptadores. | 1.ª parte entrega B instalable. |
| 2026-10-12 | B11 verificada; B15/B16 en_curso (instalación). | Usuario: de acuerdo con el orden 11→15/16→12. |
| 2026-10-12 | B11 en_revision: checkpoint/recuperar + demo-b11. | Recuperación aislada R12. |
| 2026-10-12 | B10 verificada; B11 en_curso. | Usuario: `paso 10 ok`. |
| 2026-10-12 | B10 en_revision: anotar/impactar/continuar + demo-b10. | Continuidad e impacto R11. |
| 2026-10-12 | B09 verificada; B10 en_curso. | Usuario: `paso 9 ok`. |
| 2026-10-12 | B09 en_revision: skill product-flow + demo. | Prototipo de entrada única. |
| 2026-10-12 | B08 verificada; B09 en_curso. | Usuario: `paso 8 ok`. |
| 2026-10-12 | B07 verificada; B08 en_revision (contratos + validador + fixtures). | Usuario aceptó paso 7 («construye»). |
| 2026-10-12 | B07 en_revision: ESP 0.2 + REVISION-paso-7.md para el usuario. | Paso 7 listo para revisión. |
| 2026-10-12 | B06 verificada: DEC-01…08 aceptadas; B07 preparada. | Usuario cerró el panorama del paso 6 (DEC-08: reutilizar y reconocer). |
| 2026-10-12 | DEC-02 aceptada; I-01 verificada (HTML aparte, funciona en parte). | Usuario: al aplicar la skill debe abrirse localhost así. |
| 2026-10-12 | I-01 reabierta: camino HTML aparte (`:8765`); DEC-02 actualizada. | Usuario: la ventana no debe depender del chat; MCP App descartada aquí. |
| 2026-10-12 | I-01 verificada de nuevo: probe oficial global tampoco monta; DEC-02 actualizada. | `user-mcpAppsProbe` sin `resources/read`; fallo del host/sesión, no del servidor. |
| 2026-10-12 | I-01 reabierta: MCP pasado a `~/.cursor/mcp.json` (workaround bug proyecto vs global). | Foro Cursor: Apps de proyecto no llaman `resources/read`; las globales sí. |
| 2026-10-12 | I-01 verificada en Cursor: ventana MCP App no se pinta; DEC-02 actualizada con el hallazgo. | Prueba con el usuario: servidor verde, sin UI en el chat; host no llama `resources/read`. |
| 2026-10-12 | I-01 pasa a en_curso; experimento en `experimentos/I-01/` y servidor `i01-ventana` en `.cursor/mcp.json`. | Prueba de la ventana interactiva en Cursor. |
| 2026-10-12 | Nueva investigación I-01 (ventana interactiva), preparada; ESP-03 pasa a 0.2; se crea `AGENTS.md` para continuar en Cursor. | El usuario pidió una ventana interactiva; hay incertidumbre técnica sobre si la IA del host puede usarse desde ella. |
| 2026-10-12 | Creación del tablero con B01–B22 del encargo; asignación propuesta de requisitos por tarea. | B01. |
| 2026-10-12 | B01 verificada; git inicializado (P-01 resuelta); B02 pasa a en_curso. | Aprobación del usuario. |
| 2026-10-12 | DEC-01 reescrita y aceptada por el usuario: «reutilizar y conectar las piezas buenas; construir solo lo que las une». | Apunte del usuario. |
| 2026-10-12 | B06 pasa a en_revision; se crea [decisiones.md](decisiones.md) con DEC-01 a DEC-08 propuestas. | Selección de base. |
| 2026-10-12 | B05 verificada; B06 pasa a preparada. El commit `706bb0d` salió sin el tablero por un fallo del script de actualización; se corrige en el commit siguiente. | Auditoría F04–F07. |
| 2026-10-12 | B04 verificada. Vocabulario: «checkpoint» = punto de recuperación; las paradas humanas se llamarán «puertas» (C8). | Comparación F02/F03. |
| 2026-10-12 | B03 verificada. Corrección: cc-sdd instala 17 skills por host (no 20, como se dijo en conversación). | Auditoría F01. |
| 2026-10-12 | B02 verificada; B03, B04 y B05 pasan a preparada. Complementos F04–F07 se obtienen dentro de B05. | Evidencia de B02. |
| 2026-10-12 | Encargo conservado en la raíz como `PLAN_PAQUETE_FLUJO_IA.md` en lugar de copiarlo a `docs/encargo.md`. | Evitar dos copias con autoridad sobre el mismo contenido. Revisable. |
