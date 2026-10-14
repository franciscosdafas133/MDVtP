# Revisión del paso 7 — Especificaciones del paquete

Estado: **aceptada por el usuario** · 2026-10-12  
Depende de: paso 6 cerrado (decisiones 1–8) · Siguiente: paso 8 (hecho, en revisión)  
Detalle técnico: ESP-01…08 (borrador 0.2)

Esto es el **panorama en español** de lo que el método será. Usuario: de acuerdo («construye»).

---

## 1. Qué producto es

| | |
|---|---|
| Producto | El **método** (skill/paquete), no la app de la peluquería |
| Para quién | Tú (o quien desarrolle) + el agente en Cursor/Claude |
| Problema | Otros kits cubren trozos; juntos se pelean. Nosotros **conectamos** piezas buenas |
| En ambos | Cursor y Claude Code, mismo núcleo |
| Ventana | Al usar la skill → **localhost** para docs (decisión 2) |

Detalle: [01-producto.md](01-producto.md)

---

## 2. Cómo interactúas (coordinador)

**Una sola entrada** (nombre de trabajo: `product-flow`). Acciones:

| Acción | Para qué |
|---|---|
| iniciar | Empezar un producto / flujo |
| continuar | Seguir desde donde quedó |
| estado | Qué hay, qué falta, qué bloquea |
| decidir | Aceptar / rechazar / aplazar (puerta) |
| anotar | Apuntar algo sin decidir aún |
| reabrir | Cambiar una decisión ya aceptada |
| recuperar | Volver a un checkpoint (aislado) |
| verificar | Plan de pruebas → tu OK → tests |

Al abrir/cerrar cada actividad, un informe fijo: objetivo, lo confirmado, lo propuesto, dudas, archivos, comprobaciones, checkpoint, siguiente paso.

**Próximo paso:** tabla de rutas sobre hechos del **validador** (no el feeling del modelo).  
**Profundidad:** más riesgo / más duda → más preguntas y más detalle (R17).

Detalle: [02-coordinador.md](02-coordinador.md)

---

## 3. Documentos del producto (los que aceptaste)

En el proyecto del usuario, carpeta `workflow/`:

| Documento | Contenido clave |
|---|---|
| producto | Problema, usuarios, alcance |
| descubrimiento | Hechos, hipótesis, preguntas |
| requisitos | Escenarios + **recorridos de usuario** |
| sistema | Componentes + **flujos de conexión y de datos** |
| decisiones/ | Una decisión por archivo |
| plan y tareas | Incremento actual |
| verificación | Cómo se prueba |
| operación | Entrega y recuperación en prod |
| estado.json / eventos / tablero / checkpoints | Motor de continuidad |

Orden de lectura: producto → descubrimiento → requisitos → sistema → plan → verificación → operación.  
Cada uno declara de quién depende.

Detalle: [03-documental.md](03-documental.md)

---

## 4. Estado (la “memoria” del flujo)

- **Autoridad:** `estado.json` (navegación/ejecución).  
- **Historia:** `eventos.jsonl`.  
- **Tablero** regenerable (no manda él).  
- Un solo escritor; escrituras atómicas.  
- Al retomar: contrastar estado + eventos + docs + git antes de actuar.  
- Tareas: pendiente → preparada → en_curso → en_revision → verificada (o bloqueada).

**Ante duda estado vs eventos:** gana el **estado** como foto actual; los eventos sirven para auditar y reparar. (Fijo en este paso 7.)

Detalle: [04-estado.md](04-estado.md)

---

## 5. Decisiones y puertas

Estados: propuesta / aceptada / rechazada / aplazada / sustituida.  
Aceptar solo cubre lo mostrado. Ambiguo → aclarar antes.  
Reabrir → se guarda la vieja, impacto, invalidar lo afectado.  
**Puerta humana** en todo lo de producto (decisión 7).  
Apuntes: van **dentro** del registro de la decisión/pregunta (enlace claro); lista de pendientes visible.

Detalle: [05-decisiones.md](05-decisiones.md)

---

## 6. Recuperación

| Tipo | Qué hace |
|---|---|
| Reabrir decisión | Impacto en docs; no toca código solo |
| Checkpoint | Guardar partida (commit + metadatos) |
| Recuperar aislado | Rama/worktree desde el checkpoint; **no contamina** lo actual |
| Sistema desplegado | Procedimiento aparte (git no deshace un pago) |

**Por defecto:** worktree si el entorno lo permite; si no, rama.  
**Sin git:** checkpoints solo de documentos + aviso de límite (no recuperación de código aislada).

Detalle: [06-recuperacion.md](06-recuperacion.md)

---

## 7. Hosts e instalación (skill en Cursor)

| | |
|---|---|
| Forma | Skill/paquete instalable en el **proyecto**, usable desde Cursor (y Claude) |
| Al iniciar | Abre/usa ventana **localhost** enlazada al agente |
| Manifiesto | Huellas SHA-256; retirada limpia; no pisa tus archivos |
| Layout del repo del método | `core/`, `adapters/claude-code/`, `adapters/cursor/`, `scripts/`, tests, avisos |
| Runtime | **Python 3** (validador + servidor de ventana + instalador); Node no obligatorio |

Detalle: [07-hosts-instalacion.md](07-hosts-instalacion.md)

---

## 8. Verificación y depuración (cómo se prueba / se arregla)

**Verificar (decisión 4):**  
requisito claro → plan (auto vs manual) → **tu OK al plan** → tests pegados al requisito → tu revisión manual → cierre.  
Si falla: qué se esperaba, qué pasó, qué comando.

**Depurar (decisión 5):**  
leer docs → reproducir → una hipótesis → test que falle → arreglar → a la 3ª, parar y preguntarte.

**Evaluación del método:** escenarios E01–E18 del encargo; pruebas a máquina + observación del agente (sin autoaprobarse).

Detalle: [08-evaluacion.md](08-evaluacion.md)

---

## 9. Análisis de alternativas (por qué no otra cosa)

| Tema | Elegido | Descartado / por qué |
|---|---|---|
| Base | Conectar piezas (decisión 1) | Bifurcar cc-sdd entero; motor Spec Kit; runtime GSD |
| Coordinación | Conversación + validador + HTML localhost | Motor externo que lanza el agente |
| Ventana | HTML aparte | MCP App en chat (no pinta en este Cursor) |
| Validador | Python stdlib, restricciones fuertes | Solo prompts; deps npm/pip gordas |
| Instalación | En el proyecto + manifiesto | Global en el home; copia a ciegas |
| Verificación | Plan + puerta + tests específicos | “El agente dice que sí” |
| Depuración | Método experto (leer, reproducir…) | Parches a ciegas |
| Licencias | Reutilizar + reconocer; sin marca BMad | Copiar nombres ajenos |

Selección detallada: [seleccion.md](../seleccion.md)

---

## 10. Checklist de tu revisión

Marca mentalmente sí/no:

- [ ] Te encaja la **única entrada** y las acciones de la tabla §2  
- [ ] Te encaja la lista de **documentos** y el orden de lectura  
- [ ] Te encaja **estado + eventos** (foto vs historia)  
- [ ] Te encajan **puertas** y cómo se reabre una decisión  
- [ ] Te encaja **checkpoint / recuperación aislada** (y el límite sin git)  
- [ ] Te encaja **skill en Cursor** + localhost + Python  
- [ ] Te encaja **verificar/depurar** como quedó en las decisiones 4 y 5  
- [ ] Te encaja el **análisis de alternativas** (§9)

**Respuestas útiles:**  
`paso 7 ok` — cerramos revisión y vamos al 8.  
`paso 7, cambiar: …` — ajustamos solo eso.

---

## Qué no pide este paso

- Programar ya el coordinador (eso es entrega B, paso 9+).  
- Contratos JSON/esquemas finales del validador (paso 8).  
- Probar Claude Code a fondo (sigue pendiente la versión, pregunta del tablero).
