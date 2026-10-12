# Decisiones de construcción del método

Registro de decisiones sobre **cómo construimos el paquete** (no de proyectos de usuario). Estados: `propuesta`, `aceptada`, `rechazada`, `aplazada`, `sustituida`. Una aceptación cubre solo la decisión aceptada (N-32). Un rechazo conserva su motivo.

Fuentes de los argumentos: [F01](auditoria/F01-cc-sdd.md) (hallazgos H*), [F02–F03](auditoria/F02-F03-coordinacion-recuperacion.md) (C*), [F04–F07](auditoria/F04-F07-complementos.md) (K*).

| ID | Decisión | Estado | Fecha |
|---|---|---|---|
| DEC-01 | Núcleo propio con extracciones; ninguna fuente como base instalada | propuesta | 2026-10-12 |
| DEC-02 | Coordinación conversacional dentro del host, sin motor externo | propuesta | 2026-10-12 |
| DEC-03 | Validador determinista propio, solo con biblioteca estándar | propuesta | 2026-10-12 |
| DEC-04 | Un protocolo de verificación (síntesis de cc-sdd y superpowers) | propuesta | 2026-10-12 |
| DEC-05 | Un protocolo de depuración (método de superpowers + informe de cc-sdd) | propuesta | 2026-10-12 |
| DEC-06 | Instalación local al proyecto con manifiesto SHA-256 | propuesta | 2026-10-12 |
| DEC-07 | Vocabulario y puertas: «checkpoint» = recuperación; decisiones de producto siempre con puerta humana | propuesta | 2026-10-12 |
| DEC-08 | Política de reutilización por licencia y marca | propuesta | 2026-10-12 |

---

## DEC-01 — Núcleo propio con extracciones

- **Contexto:** el encargo propone cc-sdd como candidato de base (§7, F01). B06 debe elegir la base sin dejarse llevar por la popularidad.
- **Alternativas:**
  - **A.** Bifurcar cc-sdd y adaptarlo.
  - **B.** Adoptar el motor de Spec Kit.
  - **C.** Adoptar el runtime de GSD Core.
  - **D.** Escribir un núcleo propio pequeño que incorpore piezas concretas de cada fuente.
- **Consecuencias:**
  - **A:** heredaríamos aprobaciones implícitas (H3), estado sin validación (H2), 17 skills duplicadas por host con deriva (H4), paradas entre fases (H1) y la ausencia de retirada. Habría que reescribir casi todo lo que más importa (R02, R05, R11–R13, R16, R19).
  - **B:** ver DEC-02.
  - **C:** Node ≥ 24 + npm + `claude-agent-sdk`, instalador de ~10 700 líneas, instalación global y ~300 archivos de instrucciones (C10, C11).
  - **D:** más trabajo propio en estado, decisiones y recuperación, que de todos modos no tiene ninguna fuente; a cambio, un único modelo de estado y contratos coherentes (§12 del encargo).
- **Propuesta:** **D**. cc-sdd pasa de «base» a fuente principal de piezas (revisión, verificación, división de tareas).
- **Estado:** propuesta.

## DEC-02 — Coordinación conversacional dentro del host

- **Contexto:** «decisión pendiente» del encargo (§7, F02): ¿adaptar los principios del motor de Spec Kit a un validador pequeño o adoptar parte del motor?
- **Alternativas:**
  - **A.** Motor externo que lanza al agente.
  - **B.** Skill coordinadora que el usuario usa en conversación, apoyada por un validador.
- **Consecuencias:**
  - **A:** el motor ejecuta al agente en modo no interactivo con permisos amplios (`cursor-agent -p --trust --approve-mcps --force`, C2) y las puertas se responden en un terminal. Se pierde la conversación con el coordinador (R02) y se amplía la superficie de riesgo.
  - **B:** el coordinador depende de que el modelo siga instrucciones. Por eso los controles obligatorios pasan al validador (DEC-03), como exige §6 del encargo.
- **Propuesta:** **B**. Del motor se toma el **contrato** (transiciones con lista permitida, escritura atómica, eventos después del estado, reanudación validada; C1), no el código.
- **Estado:** propuesta.

## DEC-03 — Validador determinista propio

- **Contexto:** R19 y §6 del encargo: las transiciones inválidas, las referencias rotas y la evidencia obsoleta deben detectarse mecánicamente.
- **Alternativas:**
  - **A.** Solo instrucciones.
  - **B.** Validador con dependencias (pydantic, npm…).
  - **C.** Validador solo con biblioteca estándar.
- **Consecuencias:** **A** incumple R19. **B** obliga a instalar paquetes en el proyecto del usuario (`npm` no está ni en este entorno; `pip` sin comprobar). **C** limita las herramientas, pero el contrato es pequeño (JSON, hashes, git).
- **Propuesta:** **C**. Calcula los hechos (tareas preparadas, bloqueos, evidencia `stale`; C3, C4) y rechaza escrituras inválidas. El coordinador aplica la tabla de rutas sobre esos hechos.
- **Pendiente para B07:** runtime (Node 24 o Python 3.13; ambos presentes aquí) y si se invoca solo desde el coordinador o también desde hooks del host (depende de B15).
- **Estado:** propuesta.

## DEC-04 — Un protocolo de verificación

- **Alternativas:**
  - **A.** `kiro-verify-completion` (F01).
  - **B.** `verification-before-completion` (F07).
  - **C.** Síntesis de ambos.
- **Propuesta:** **C**. Se toman de cc-sdd los tipos de afirmación y la salida `VERIFIED / NOT_VERIFIED / MANUAL_VERIFY_REQUIRED`, necesaria para E04, E09 y N-45. De superpowers, las señales de alarma y el ciclo rojo-verde de regresión. La regla de evidencia vigente se apoya en DEC-03 (C4). Detalle en F04–F07 §3.1.
- **Estado:** propuesta.

## DEC-05 — Un protocolo de depuración

- **Alternativas:**
  - **A.** `kiro-debug` (F01).
  - **B.** `systematic-debugging` (F07).
  - **C.** Síntesis.
- **Propuesta:** **C**. El método es el de superpowers: reproducir, analizar el patrón, una sola hipótesis, test que falla antes de reparar y parar al tercer intento fallido para cuestionar el diseño (E10). El informe estructurado y las categorías vienen de cc-sdd (`ROOT_CAUSE`, `CATEGORY`, `NEXT_ACTION: RETRY / BLOCK / STOP_FOR_HUMAN`). Detalle en F04–F07 §3.2.
- **Estado:** propuesta.

## DEC-06 — Instalación local con manifiesto SHA-256

- **Alternativas:**
  - **A.** Copia simple (cc-sdd: sin retirada; puede sobrescribir `CLAUDE.md`/`AGENTS.md`).
  - **B.** Global en el home (GSD).
  - **C.** Local con manifiesto de huellas (Spec Kit).
- **Propuesta:** **C**. Se instala en el proyecto una sola copia activa por host. El manifiesto registra la SHA-256 de cada archivo; la retirada borra solo lo no modificado y lista lo conservado; el instalador nunca sobrescribe archivos del usuario (C9, C10, R16, E14).
- **Estado:** propuesta.

## DEC-07 — Vocabulario y puertas humanas

- **Contexto:** «checkpoint» significa cosas distintas en GSD y en el encargo (C8). El modo automático puede decidir por el usuario (C5).
- **Propuesta:**
  - «Checkpoint» = punto de recuperación (encargo §5).
  - «Puerta» = parada para una persona.
  - Toda decisión de producto, y toda acción irreversible o externa, lleva una puerta que **nunca** se aprueba en automático (equivalente a `blocking-human` de GSD).
  - Las puertas técnicas pueden avanzar solas dentro del alcance autorizado (§4 del encargo).
- **Estado:** propuesta.

## DEC-08 — Política de reutilización

- **Contexto:** licencias y marca (K1, K2; §7 del encargo).
- **Propuesta:**

| Fuente | Copia adaptada de texto | Condición |
|---|---|---|
| F01 cc-sdd, F07 superpowers (MIT) | Permitida | Aviso MIT en `THIRD_PARTY_NOTICES.md` y declaración de cambios |
| F02 Spec Kit, F03 GSD Core (MIT) | Permitida, pero en principio solo se toman ideas y contratos | Ídem si se copia texto o código |
| F04 HumanLayer (Apache-2.0) | Solo inspiración salvo necesidad | Si se copia: conservar el aviso de licencia y marcar los cambios |
| F05 BMAD, F06 TEA (MIT + marca) | Solo inspiración | Ningún nombre ni identificador con «bmad»; «inspirado en BMad Method» en avisos |

- **Estado:** propuesta.
