# Tablero de construcción del paquete

Vista mantenible del progreso de construcción **del método** (no de una aplicación de usuario). Encargo: [PLAN_PAQUETE_FLUJO_IA.md](../PLAN_PAQUETE_FLUJO_IA.md) (se conserva en la raíz, sin copiarlo, para no crear dos autoridades). Objetivos: [objetivos.md](objetivos.md). Reglas: [reglas-hacer.md](reglas-hacer.md) y [reglas-no-hacer.md](reglas-no-hacer.md). Especificaciones: [especificaciones/](especificaciones/README.md).

Última actualización: 2026-10-12.

## Estados

`pendiente` → `preparada` → `en_curso` → `en_revision` → `verificada`; cualquier estado activo puede pasar a `bloqueada`.

- Solo pasa a `preparada` una tarea cuyas dependencias están `verificadas`.
- `verificada` exige evidencia pertinente y vigente registrada en esta tabla o enlazada.
- Descubrir una dependencia nueva cambia el tablero de forma explícita (anotar en «Cambios del tablero»).
- Los hitos B01–B22 se descomponen en unidades concretas antes de ejecutarse cuando lo requieran.

## Resumen

| Estado | Tareas |
|---|---|
| en_curso | B02 |
| preparada | — |
| pendiente | B03–B22 |
| bloqueada | — |
| verificada | B01 |

**Siguiente actividad preparada:** B02 (en curso).

## Tareas

Responsable por defecto: agente constructor. Las decisiones de producto corresponden al usuario. La columna «Req.» es una asignación propuesta en B01; se revisará en B06.

| ID | Trabajo | Depende de | Estado | Req. | Entrega | Condición observable de terminación |
|---|---|---|---|---|---|---|
| B01 | Inspeccionar carpeta, herramientas y archivos existentes; conservar encargo y crear tablero. | — | verificada | — | A | Se conoce el entorno y existe un registro del estado inicial sin sobrescribir trabajo previo. |
| B02 | Obtener referencias principales y guardar versiones, rutas y licencias. | B01 | en_curso | R20 | A | El inventario reproduce los commits consultados y distingue fuentes originales de archivos propios. |
| B03 | Auditar cc-sdd, incluyendo sus dos hosts y dependencias de recursos. | B02 | pendiente | R01–R20 | A | Hay una ficha del recorrido real, sus paradas, estado, documentos, validaciones y huecos frente a R01–R20. |
| B04 | Comparar coordinación y recuperación de Spec Kit y GSD Core. | B02 | pendiente | R08, R12, R13, R19 | A | Matriz con mecanismos, dependencias, costes y límites; sin mezclar sus estados. |
| B05 | Auditar complementos de producto, investigación, pruebas y diagnóstico. | B02 | pendiente | R03, R05, R11, R14, R15, R18 | A | Cada pieza propuesta tiene ficha y requisito; redundancias y ausencias quedan visibles. |
| B06 | Elegir base y extracciones mínimas; producir mapa de cobertura. | B03, B04, B05 | pendiente | R01–R20 | A | Cada requisito tiene una solución prevista o un desarrollo propio explícito. Decisiones fundadas, no selección por popularidad. |
| B07 | Elaborar especificaciones del paquete y análisis de alternativas. | B06 | pendiente | R01–R20 | A | Se describen flujo, estado, decisiones, trazabilidad, recuperación, dos adaptadores, instalación y verificaciones. |
| B08 | Diseñar contratos y comprobaciones de integridad. | B07 | pendiente | R04, R05, R07, R11, R19 | A | Referencias y estados válidos definidos; cambios incompatibles o evidencia inválida producen un resultado verificable. |
| B09 | Construir prototipo de documentación guiada con una única entrada. | B08 | pendiente | R02, R03, R04, R05, R06, R17 | B | Una idea vaga llega a un incremento preparado con decisiones y preguntas registradas; no exige que el usuario elija skills. |
| B10 | Añadir continuidad, anotaciones e impacto de cambios. | B09 | pendiente | R06, R08, R11, R13 | B | Una sesión nueva retoma el punto correcto y un requisito modificado invalida las partes afectadas. |
| B11 | Añadir puntos de recuperación y recuperación aislada. | B10 | pendiente | R12 | B | Puede abrirse una rama/worktree desde un checkpoint y seguir allí, conservando el trabajo posterior. |
| B12 | Implementar división, asignación y control de tareas. | B09 | pendiente | R09, R10 | C | Una tarea sobredimensionada se divide; las dependencias sin resolver bloquean solo el trabajo pertinente. |
| B13 | Integrar implementación, revisión, verificación y diagnóstico. | B11, B12 | pendiente | R14, R15 | C | Un fallo y una reparación se gestionan con evidencia; el agente no marca éxito ante pruebas fallidas u omitidas. |
| B14 | Incorporar preparación de entrega, operación y mantenimiento. | B13 | pendiente | R18 | C | El flujo genera un plan contextual de entrega y recuperación; registra comprobaciones reales pendientes. |
| B15 | Implementar adaptadores Claude Code y Cursor. | B09 | pendiente | R01 | B | Ambos cargan el núcleo y sus recursos desde ubicaciones correctas; diferencias de herramientas registradas. |
| B16 | Implementar instalación, actualización y retirada. | B15 | pendiente | R16 | B (1.ª parte) / C | Instalación en carpeta de prueba, detección de conflictos, rutas válidas y retirada limitada a archivos propios. |
| B17 | Probar integridad, interrupciones y recuperación. | B10, B11, B16 | pendiente | R12, R13, R19 | C | Pruebas de referencias rotas, escritura interrumpida, estado inválido y cambios sin commit con resultados esperados. |
| B18 | Evaluar el comportamiento del agente sobre casos controlados. | B12, B13, B14, B17 | pendiente | R14 (E01–E18) | C | Casos sanos y casos con defectos; evidencia independiente de la autoevaluación del agente. |
| B19 | Ejecutar escenarios en Claude Code y Cursor reales. | B15–B18 | pendiente | R01 | C | Resultados por host y versión. Si falta un host o acceso, R01 permanece parcialmente pendiente. |
| B20 | Probar un incremento con componentes interactuando y un cambio posterior. | B19 | pendiente | R07, R11, R18 | C | Se verifica integración real en fixture/proyecto de prueba, se modifica un requisito y se comprueba la recuperación del flujo. |
| B21 | Preparar versión candidata y guía breve de usuario. | B20 | pendiente | R02, R17 | C | Paquete reproducible con requisitos satisfechos y límites explícitos; usuario aprende la entrada común y las acciones de control. |
| B22 | Mantener y mejorar el propio paquete. | B21 | pendiente | R20 | C | Política de versiones, migración, actualización de fuentes y escenarios de regresión definida. |

Notas del encargo: B05 puede explorar fuentes condicionales (F08–F10) si detecta un hueco. B07 debe dividirse si sus especificaciones son demasiado grandes para revisarlas juntas. Una incertidumbre técnica no se esconde dentro de una tarea de implementación: se crea una investigación con pregunta y condición de cierre.

## Entregas revisables

- **Entrega A — B01 a B08:** fuentes auditadas, selección, especificaciones y contratos. Se revisa el diseño antes de implementar coordinadores.
- **Entrega B — B09 a B11, B15 y primera parte de B16:** flujo documental guiado con estado y recuperación, instalable en un proyecto de prueba en ambos hosts. No autoriza afirmar que el método completo funciona en productos complejos.
- **Entrega C — resto del tablero:** ejecución completa, integración, operación, evaluación y versión candidata.

## Detalle de la tarea activa

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
| P-03 | `npm` no aparece en el PATH aunque Node está instalado. | Solo relevante si un instalador o validador elige Node; el runtime mínimo se decide en B07 (regla del §12). | B07, B16 | Agente (investigar cuando aplique) |

## Cambios del tablero

| Fecha | Cambio | Motivo |
|---|---|---|
| 2026-10-12 | Creación del tablero con B01–B22 del encargo; asignación propuesta de requisitos por tarea. | B01. |
| 2026-10-12 | B01 verificada; git inicializado (P-01 resuelta); B02 pasa a en_curso. | Aprobación del usuario. |
| 2026-10-12 | Encargo conservado en la raíz como `PLAN_PAQUETE_FLUJO_IA.md` en lugar de copiarlo a `docs/encargo.md`. | Evitar dos copias con autoridad sobre el mismo contenido. Revisable. |
