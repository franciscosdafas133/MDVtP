# I-01 — Prueba de la ventana interactiva

Estado: verificada · Creada: 2026-10-12 · Decide: [DEC-02](../decisiones.md) (aceptada) · Requisitos: R01, R02, R05, R06 · Documentos: [ESP-03](../especificaciones/03-documental.md)

Investigación con pregunta y condición de cierre (regla del encargo: una incertidumbre técnica no se esconde dentro de una tarea de implementación). Es una **prueba de concepto desechable**: responde a una pregunta, no construye el producto.

## Pregunta

¿Puede una ventana mostrar un documento del método, dejar que el usuario lo edite y hacer que **la IA del propio host** (Cursor o Claude Code, sin otra clave ni otro modelo) corrija y proponga en el momento, con el usuario aceptando o rechazando cada propuesta?

## Por qué importa

El usuario quiere trabajar la documentación de sus productos en algo más que un chat. Sus palabras (2026-10-12): «interactivo, poder editarlo y que use algún modelo de mi mismo IDE […] para que me corrija en ese momento y proponga en tiempo real toda la documentación; que sea visible, manejable y controlable». Si la ventana no puede usar la IA del host, la decisión 2 cambia.

## Contexto que no hay que volver a discutir

- **DEC-01 aceptada:** se reutilizan piezas existentes y solo se construye lo que las une.
- **DEC-02, propuesta en revisión:** el agente trabaja dentro de la conversación del host. Ningún motor externo lo lanza en segundo plano con permisos amplios. La ventana se añade a esa conversación y no la sustituye.
- **Documentos del producto acordados:** producto, descubrimiento, requisitos (con recorridos del usuario), sistema (con flujos de conexión y de datos), decisiones, plan y tareas, verificación y operación. Cada documento declara de cuáles depende y cuáles dependen de él (mapa de lectura en ESP-03).
- **Pizarra prevista:** draw.io MCP como principal y Excalidraw MCP como extra en Cursor. **No forma parte de esta prueba.**

## Caminos técnicos a comprobar

| Host | Camino | Qué se sabe (sin probar) |
|---|---|---|
| Cursor (≥ 2.6) | **MCP App**: un servidor MCP local con una herramienta que declara un recurso `ui://`. Cursor lo muestra dentro del chat en un iframe aislado. | La especificación permite que la app pida llamadas a herramientas, envíe mensajes y actualice el contexto del modelo. Cursor 2.6 anunció soporte. |
| Claude Code (extensión de VS Code) | **Ventana local + channel**: una página local envía las ediciones a un servidor MCP con la capacidad `claude/channel`, que las empuja a la sesión abierta. | Vista previa de investigación; requiere v2.1.80 o superior y la opción `--channels`. No consta que la extensión de VS Code admita channels ni que muestre MCP Apps. |

Se empieza por **Cursor**. Claude Code va después y depende de saber la versión de la extensión (pregunta P-02 del tablero).

## Escenario de la prueba

Documento de ejemplo: un `producto.md` corto de una app de reservas para una peluquería, con una frase vaga a propósito (p. ej. «la app es para todo el mundo»).

1. Se abre la ventana con el documento visible.
2. El usuario edita una frase en la ventana.
3. Sin que el usuario escriba en el chat, la IA del host recibe el cambio y propone una corrección o pregunta (p. ej. «"todo el mundo" es demasiado amplio: ¿clientes, peluqueros o ambos?»).
4. La propuesta aparece en la ventana con **aceptar** y **rechazar**.
5. El archivo en disco solo cambia si el usuario acepta. El rechazo queda anotado.

## Condición de cierre

Por cada host probado se registra:

- **resultado:** funciona / funciona en parte / no funciona;
- versión del host y del sistema;
- qué pasos del escenario se cumplieron y cuáles no, con evidencia: captura, registro o diff del archivo;
- límites encontrados (latencia, permisos que pide el host, dependencias que hubo que instalar).

La investigación se cierra cuando Cursor tiene un resultado registrado. Claude Code puede quedar `pendiente` si falta la versión o el acceso, y se dice así.

## Reglas de la prueba

- Todo vive en `experimentos/I-01/` y se marca como desechable. No se mezcla con el paquete.
- Mínimas dependencias. `npm` no está en el PATH (P-03): antes de instalar nada se pregunta al usuario. La especificación de MCP Apps permite implementar el protocolo `postMessage` a mano sin el SDK.
- Nada se instala de forma global. No se toca `.reference-sources/`.
- La ventana nunca escribe el archivo sin la aceptación del usuario.
- Comunicación con el usuario: ver [AGENTS.md](../../AGENTS.md).

## Después de la prueba

1. Anotar los resultados en la sección siguiente.
2. Actualizar DEC-02 en [decisiones.md](../decisiones.md) con lo aprendido y proponerla de nuevo al usuario.
3. Actualizar el [tablero](../tablero.md): I-01 verificada y la siguiente actividad.

## Resultados

### Cursor — **no funciona** (ventana interactiva; 2026-10-12)

| Campo | Valor |
|---|---|
| Resultado | **no funciona** (para el escenario de la ventana) |
| Versión host | Cursor 3.22.12 (`cursor-vscode` 1.0.0 en el handshake MCP) |
| Sistema | Linux 6.19.14 (Kali); Node v24.21.0; Python 3.13; sin `npm` en PATH |
| Experimento | `experimentos/I-01/` (Python stdlib + HTML; sin SDK) |

**Pasos del escenario**

| Paso | ¿Cumplido? | Evidencia |
|---|---|---|
| 1. Abrir ventana con el documento | No | El usuario no vio cajita editable en el chat; solo texto de la herramienta |
| 2. Editar en la ventana | No | No hubo UI |
| 3. IA del host corrige sin escribir en el chat | No probado | Depende del paso 1 |
| 4. Aceptar / rechazar en la ventana | No probado | Depende del paso 1 |
| 5. Archivo solo cambia al aceptar | No probado en UI | La herramienta `aceptar_propuesta` sí escribe en disco (smoke test) |

**Qué sí funcionó**

- MCP `i01-ventana` conecta en verde.
- Cursor anuncia Apps: `extensions.io.modelcontextprotocol/ui` con `text/html;profile=mcp-app`.
- `abrir_documento` se ejecuta y devuelve texto + `structuredContent`.
- Smoke test fuera de Cursor: `initialize`, `tools/list`, `resources/read`, `aceptar_propuesta` OK.

**Hallazgo clave**

En el registro `experimentos/I-01/state/prueba.jsonl`, tras varias llamadas a `abrir_documento` desde Cursor, **nunca** aparece `resources/read` del `ui://i01/editor`. El host no pidió el HTML; por eso no puede pintar la ventana. Se reintentó con `_meta.ui.resourceUri` y el formato legacy `ui/resourceUri` en la herramienta y en el resultado: mismo comportamiento.

**Límites**

- No se instaló el SDK oficial (`@modelcontextprotocol/ext-apps`); la ficha permitía el protocolo a mano y prohibía instalar sin preguntar (`npm` ausente).
- No se probó otra superficie (p. ej. Agents Window a pantalla completa) como variable controlada; el usuario miró el chat donde escribe y no apareció nada.
- No se pudo medir latencia ni `sampling/createMessage` porque no hubo UI.

### Cursor — reabierta: bug de alcance proyecto vs global (2026-10-12)

Causa probable (foro Cursor, mismo síntoma: herramienta OK, **0** `resources/read`, sin widget):

- Los MCP Apps en servidores del **proyecto** (`.cursor/mcp.json` → id `project-0-…`) no montan el HTML.
- El mismo servidor en **`~/.cursor/mcp.json`** (id `user-…`) sí dispara `resources/read` y pinta el widget.

**Cambio aplicado:** servidor registrado en `~/.cursor/mcp.json`; el de proyecto pasó a `.cursor/mcp.json.proyecto-desactivado`.

**Reintento global (2026-10-12):** servidor aparece como `i01-ventana` **User**, namespace `user-i01-ventana`. Tras `abrir_documento`, el registro sigue **sin** `resources/read`. El workaround del foro **no bastó** en Cursor 3.22.12 de este entorno (posible flag de cuenta, o nuestro servidor Python no deja `_meta` en la caché interna de Cursor).

**Intento oficial (2026-10-12): también falla.**

- Probe: `experimentos/I-01/probe-oficial/` (SDK `@modelcontextprotocol/ext-apps` + `@modelcontextprotocol/sdk`).
- Node/npm usuario: `~/.local/node-v24.21.0/`.
- Registro global: `mcpAppsProbe` → namespace `user-mcpAppsProbe`.
- Smoke fuera de Cursor: `_meta.ui.resourceUri` + `resources/read` OK.
- En Cursor: `initialize` → `tools/list` → `resources/list` → `tools/call` **sin** `resources/read` (`probe-oficial/global.log`). El usuario no vio el panel verde.
- Conclusión: el fallo **no** es el servidor Python casero; en esta sesión/cuenta de Cursor 3.22.12 el montaje inline de MCP Apps no está activo (mismo patrón que el foro: el host declara la capacidad y no lee el HTML). No hay workaround fiable del lado del proyecto.

### Conclusión parcial Cursor (MCP App)

**no funciona** la MCP App *dentro del chat*. No se abandona la idea de ventana: el usuario pidió corregir el enfoque.

### Cursor — camino B: HTML aparte (en curso, 2026-10-12)

Tras el fallo del chat, el usuario indicó: la ventana «tal vez no deba ser dentro del chat sino un html aparte».

| Pieza | Ruta |
|---|---|
| Servidor local | `experimentos/I-01/standalone_server.py` (`http://127.0.0.1:8765/`) |
| Editor | `experimentos/I-01/ui/standalone.html` |
| Puente con la IA del IDE | `state/solicitud.json` ← usuario; `state/propuesta.json` ← agente del host; aceptar/rechazar en el HTML |

Escenario: el navegador muestra y edita; «Pedir corrección» deja la solicitud; el agente de Cursor (misma suscripción del IDE, sin otra clave) escribe la propuesta; el HTML la muestra con aceptar/rechazar; disco solo cambia al aceptar.

**Resultado Cursor (HTML aparte): funciona en parte** (2026-10-12).

| Paso del escenario | ¿Cumplido? |
|---|---|
| Ventana con documento visible | Sí (`http://127.0.0.1:8765/`) |
| Editar | Sí |
| IA del host propone (sin otra clave) | Sí (agente Cursor vía puente local) |
| En el momento / sin fricción | Parcial (hay que pedir corrección; el servidor debe estar vivo) |
| Aceptar / rechazar en la ventana | Sí (UI lista; el usuario puede aceptar cuando quiera) |
| MCP App en el chat | No |

**Cierre:** DEC-02 aceptada con la condición de producto: al aplicar la skill, abrir localhost así. Claude Code pendiente (P-02).

### Claude Code

_Pendiente (falta versión de la extensión, P-02)._

## Fuentes

- [MCP Apps — visión general](https://modelcontextprotocol.io/extensions/apps/overview) y [especificación 2026-01-26](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx)
- [Cursor 2.6: MCP Apps](https://forum.cursor.com/t/cursor-2-6-mcp-apps/153482)
- [Claude Code — referencia de channels](https://code.claude.com/docs/en/channels-reference)
- [Is MCP good yet? (soporte por cliente)](https://ismcpgoodyet.com/)
- Pizarras: [draw.io MCP](https://github.com/lgazo/drawio-mcp-server), [Excalidraw MCP](https://glama.ai/mcp/servers/dkrcam97vn)
