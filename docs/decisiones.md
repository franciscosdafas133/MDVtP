# Decisiones de construcción del método

Registro de decisiones sobre **cómo construimos el paquete** (no de proyectos de usuario). Estados: `propuesta`, `aceptada`, `rechazada`, `aplazada`, `sustituida`. Una aceptación cubre solo la decisión aceptada (N-32). Un rechazo conserva su motivo.

Fuentes de los argumentos: [F01](auditoria/F01-cc-sdd.md) (hallazgos H*), [F02–F03](auditoria/F02-F03-coordinacion-recuperacion.md) (C*), [F04–F07](auditoria/F04-F07-complementos.md) (K*).

| ID | Decisión | Estado | Fecha |
|---|---|---|---|
| DEC-01 | Reutilizar y conectar las piezas buenas; construir solo lo que las une | **aceptada** | 2026-10-12 |
| DEC-02 | Coordinación en el host + ventana HTML (localhost) al usar la skill | **aceptada** | 2026-10-12 |
| DEC-03 | Validador propio: restricciones suficientes para documentar con orden; sin deps raras | **aceptada** | 2026-10-12 |
| DEC-04 | Verificación: plan con puerta humana; pruebas ligadas al requisito; fallo específico | **aceptada** | 2026-10-12 |
| DEC-05 | Depuración como experto: leer docs, reproducir, hipótesis, test, parar a los 3 | **aceptada** | 2026-10-12 |
| DEC-06 | Skill/paquete instalable en Cursor/proyecto, con manifiesto y retirada limpia | **aceptada** | 2026-10-12 |
| DEC-07 | Checkpoint = recuperar; puerta = decide el humano; aislamiento sin contaminar → B07/B11 | **aceptada** | 2026-10-12 |
| DEC-08 | Reutilizar lo que sirva; al lanzar, reconocer orígenes (licencia/marca) | **aceptada** | 2026-10-12 |

---

## DEC-01 — Reutilizar y conectar las piezas buenas; construir solo lo que las une

- **Contexto:** el encargo propone cc-sdd como candidato de base (§7, F01). Las auditorías B03–B05 encontraron piezas valiosas repartidas entre varias fuentes, pero cada fuente usa su propio sistema de estado y sus propias convenciones (`spec.json` en cc-sdd, `.planning/STATE.md` en GSD, runtime `_bmad/` en BMAD), que se contradirían si se instalaran juntas (§12 del encargo).
- **Alternativas consideradas:**
  - **A.** Bifurcar cc-sdd y parchearlo.
  - **B.** Adoptar el motor de Spec Kit.
  - **C.** Adoptar el runtime de GSD Core.
  - **D.** Reutilizar las piezas buenas de cada fuente y conectarlas.
- **Decisión:** **D**. No se reinventa lo que ya existe:
  - Se reutilizan las piezas seleccionadas (X01–X21 en [seleccion.md](seleccion.md)): copia adaptada cuando la licencia lo permite, idea cuando no.
  - Solo se construye lo que las une:
    1. **El coordinador**, la única entrada con la que habla el usuario, que elige qué pieza usar en cada momento.
    2. **Un registro común**, un solo lugar donde todas las piezas anotan decisiones, tareas y evidencia.
    3. **Los adaptadores**, que ajustan cada pieza a ese registro común y a cada host (Claude Code, Cursor).
- **Consecuencias:**
  - Un único modelo de estado y una única interfaz.
  - Cada pieza reutilizada se modifica para escribir en el registro común en lugar de en el suyo.
  - Los requisitos que ninguna fuente cubre (R18 y partes de R01, R06, R07, R20) siguen siendo desarrollo propio.
- **Rechazadas:**
  - **A**, por las aprobaciones implícitas, el estado sin validación y la deriva entre hosts (H1–H4).
  - **B**, ver DEC-02.
  - **C**, por el tamaño, las dependencias y la instalación global (C10, C11).
- **Apunte del usuario (2026-10-12):** «No es necesario construir la rueda si ya está hecha; lo ideal es sacar las partes buenas y conectarlas, crear esas conexiones de tal manera que este producto sea capaz de crear cualquier producto.»
- **Límite:** que sirva para «cualquier producto» es la meta, pero solo podrá afirmarse para los escenarios realmente probados (§14 del encargo).
- **Estado:** **aceptada** por el usuario el 2026-10-12, con esta redacción.

## DEC-02 — Coordinación conversacional dentro del host

- **Contexto:** «decisión pendiente» del encargo (§7, F02): ¿adaptar los principios del motor de Spec Kit a un validador pequeño o adoptar parte del motor?
- **Alternativas:**
  - **A.** Motor externo que lanza al agente.
  - **B.** Skill coordinadora que el usuario usa en conversación, apoyada por un validador.
- **Consecuencias:**
  - **A:** el motor ejecuta al agente en modo no interactivo con permisos amplios (`cursor-agent -p --trust --approve-mcps --force`, C2) y las puertas se responden en un terminal. Se pierde la conversación con el coordinador (R02) y se amplía la superficie de riesgo.
  - **B:** el coordinador depende de que el modelo siga instrucciones. Por eso los controles obligatorios pasan al validador (DEC-03), como exige §6 del encargo.
- **Propuesta:** **B**. Del motor se toma el **contrato** (transiciones con lista permitida, escritura atómica, eventos después del estado, reanudación validada; C1), no el código.
- **Apunte del usuario (2026-10-12):** el chat se queda corto para documentar; quiere «algo interactivo como una ventana» para armar desde un producto hasta el propio flujo, con gráficos e interacción, y pide buscar MCP para graficar e interactuar.
- **Requisitos del usuario para la ventana (2026-10-12):** «interactivo, poder editarlo y que use algún modelo de mi mismo IDE con el que está Claude o de Cursor para que me corrija en ese momento y proponga en tiempo real toda la documentación; que sea visible, manejable y controlable». Es decir:
  1. La documentación se ve y se edita en una ventana, no solo en el chat.
  2. La IA es la del propio host (la suscripción de Claude Code o la de Cursor); no hay una clave ni un modelo aparte.
  3. Mientras se edita, la IA corrige y propone en el momento.
  4. El usuario controla qué se acepta.
- **Caminos técnicos:**
  - ~~Cursor: MCP App dentro del chat~~ — **probado, no pinta** en este Cursor (I-01).
  - **Cursor: HTML aparte** (navegador + servidor local) enlazado al agente del IDE por archivos/API local — **en prueba** (I-01 reabierta a pedido del usuario).
  - Claude Code: ventana local + *channel* — sin probar.
- **Apunte del usuario (2026-10-12, tras el fallo MCP App):** «tal vez no deba ser dentro del chat sino un html aparte».
- **Decisión:** **B** + ventana **HTML en localhost** (no MCP App en el chat). Al aplicar/ejecutar la skill del método en el host, debe abrirse esa ventana ya enlazada al agente del IDE (misma suscripción; el usuario acepta/rechaza). Sin motor externo. Detalle de la prueba: [I-01](investigaciones/I-01-ventana-interactiva.md).
- **Apunte del usuario al aceptar (2026-10-12):** «una vez apliques la skill debería abrirse así» (localhost conectado).
- **Límite (I-01):** en Cursor 3.22.12 la MCP App en chat no pinta; el camino viable probado es HTML aparte. Corrección “en el momento” y pizarra quedan para especificar/implementar después (B07+). Claude Code sin probar (P-02).
- **Estado:** **aceptada** por el usuario el 2026-10-12.

## DEC-03 — Validador determinista propio

- **Contexto:** R19 y §6 del encargo: las transiciones inválidas, las referencias rotas y la evidencia obsoleta deben detectarse mecánicamente.
- **Alternativas:**
  - **A.** Solo instrucciones.
  - **B.** Validador con dependencias (pydantic, npm…).
  - **C.** Validador solo con biblioteca estándar.
- **Consecuencias:** **A** incumple R19. **B** obliga a instalar paquetes en el proyecto del usuario (`npm` no está ni en este entorno; `pip` sin comprobar). **C** limita las herramientas, pero el contrato es pequeño (JSON, hashes, git).
- **Propuesta:** **C**. Calcula los hechos (tareas preparadas, bloqueos, evidencia `stale`; C3, C4) y rechaza escrituras inválidas. El coordinador aplica la tabla de rutas sobre esos hechos.
- **Apunte del usuario (2026-10-12):** no un «freno simple» débil: **las restricciones suficientes** para crear la documentación de forma ordenada y con sentido (paso a paso, bien guiado). «Simple» solo describe la implementación (biblioteca estándar, sin deps raras), no la pobreza de las reglas.
- **Decisión:** **C**, con ese matiz. El validador exige el orden y la coherencia del flujo documental; no sustituye al juicio de producto del usuario (puertas humanas, DEC-07).
- **Pendiente para B07:** runtime (Node 24 o Python 3.13; ambos presentes aquí), catálogo concreto de restricciones, y si se invoca solo desde el coordinador o también desde hooks del host (depende de B15).
- **Estado:** **aceptada** por el usuario el 2026-10-12.

## DEC-04 — Un protocolo de verificación

- **Alternativas:**
  - **A.** `kiro-verify-completion` (F01).
  - **B.** `verification-before-completion` (F07).
  - **C.** Síntesis de ambos.
- **Propuesta:** **C**, con el orden y el rigor acordados con el usuario.
- **Orden (no se salta a automático):** (1) requisito claro → (2) plan de pruebas (auto vs manual) → (3) puerta humana sobre el plan → (4) solo entonces pruebas auto → (5) revisión manual → (6) cierre con evidencia fresca. Veredictos: cumple / no cumple / míralo tú.
- **Rigor de las pruebas (apunte del usuario, 2026-10-12):**
  - Cada prueba debe **apuntar directamente** a la funcionalidad/requisito que dice comprobar (no “humo” genérico).
  - Si no cumple, el informe debe ser **específico**: qué se esperaba, qué ocurrió, qué comando/paso falló.
  - Fuentes: síntesis cc-sdd + superpowers (X01); guía de testing y traza requisito→prueba inspirada en TEA/HumanLayer (ideas, no runtime TEA). Evidencia vigente vía DEC-03.
- **Estado:** **aceptada** por el usuario el 2026-10-12.

## DEC-05 — Un protocolo de depuración

- **Alternativas:**
  - **A.** `kiro-debug` (F01).
  - **B.** `systematic-debugging` (F07).
  - **C.** Síntesis.
- **Propuesta:** **C**. Método de superpowers + informe de cc-sdd (`ROOT_CAUSE`, `CATEGORY`, `NEXT_ACTION: RETRY / BLOCK / STOP_FOR_HUMAN`).
- **Apunte del usuario (2026-10-12):** alineado con cómo solucionan fallos los expertos: **leer documentación** (del proyecto, del error, del método) antes de parchear; reproducir; una hipótesis; test que falla y luego arreglo; a la tercera sin avance, parar y preguntar al humano.
- **Estado:** **aceptada** por el usuario el 2026-10-12.

## DEC-06 — Instalación local con manifiesto SHA-256

- **Alternativas:**
  - **A.** Copia simple (cc-sdd: sin retirada; puede sobrescribir `CLAUDE.md`/`AGENTS.md`).
  - **B.** Global en el home (GSD).
  - **C.** Local con manifiesto de huellas (Spec Kit).
- **Propuesta:** **C**. Se instala en el proyecto una sola copia activa por host. El manifiesto registra la SHA-256 de cada archivo; la retirada borra solo lo no modificado y lista lo conservado; el instalador nunca sobrescribe archivos del usuario (C9, C10, R16, E14).
- **Apunte del usuario (2026-10-12):** la documentación es lo que genera/guía su producto; quiere el método como **skill instalable** (en el proyecto), no como lío global ni copia a ciegas.
- **Apunte del usuario (2026-10-12, matiz):** que se pueda **descargar/instalar directamente en Cursor** y **iniciar ahí** (experiencia de skill/paquete en el IDE), sin un ritual raro aparte. Sigue siendo instalación local al proyecto (o al mecanismo nativo de Cursor para skills del proyecto), con manifiesto y retirada limpia; el detalle de marketplace vs carpeta del proyecto se fija en B07/B16.
- **Estado:** **aceptada** por el usuario el 2026-10-12.

## DEC-07 — Vocabulario y puertas humanas

- **Contexto:** «checkpoint» significa cosas distintas en GSD y en el encargo (C8). El modo automático puede decidir por el usuario (C5).
- **Propuesta:**
  - «Checkpoint» = punto de recuperación / “guardar partida” (encargo §5); no es el menú general de versiones.
  - «Puerta» = parada para una persona (aceptar / rechazar / pendiente).
  - Toda decisión de producto, y toda acción irreversible o externa, lleva una puerta que **nunca** se aprueba en automático (equivalente a `blocking-human` de GSD).
  - Las puertas técnicas pueden avanzar solas dentro del alcance autorizado (§4 del encargo).
- **Apunte del usuario (2026-10-12):** checkpoint ≈ mantener lo anterior para poder volver. Las **copias del paquete** son DEC-06. El **trabajo aislado sin contaminar** lo actual (rama/worktree) no se inventa aquí: se especifica en B07 e implementa en B11 (R12, X14/X15).
- **Estado:** **aceptada** por el usuario el 2026-10-12.

## DEC-08 — Política de reutilización

- **Contexto:** licencias y marca (K1, K2; §7 del encargo).
- **Propuesta:**

| Fuente | Copia adaptada de texto | Condición |
|---|---|---|
| F01 cc-sdd, F07 superpowers (MIT) | Permitida | Aviso MIT en `THIRD_PARTY_NOTICES.md` y declaración de cambios |
| F02 Spec Kit, F03 GSD Core (MIT) | Permitida, pero en principio solo se toman ideas y contratos | Ídem si se copia texto o código |
| F04 HumanLayer (Apache-2.0) | Solo inspiración salvo necesidad | Si se copia: conservar el aviso de licencia y marcar los cambios |
| F05 BMAD, F06 TEA (MIT + marca) | Solo inspiración | Ningún nombre ni identificador con «bmad»; «inspirado en BMad Method» en avisos |

- **Apunte del usuario (2026-10-12):** se reutiliza el método/piezas que sirvan para integrarlas al producto nuevo; al lanzar, se **reconoce** de dónde salió (avisos, terceros, sin apropiarse de marcas ajenas).
- **Estado:** **aceptada** por el usuario el 2026-10-12.
