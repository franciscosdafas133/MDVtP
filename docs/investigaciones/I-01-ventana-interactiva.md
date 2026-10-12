# I-01 — Prueba de la ventana interactiva

Estado: preparada · Creada: 2026-10-12 · Decide: [DEC-02](../decisiones.md) · Requisitos: R01, R02, R05, R06 · Documentos: [ESP-03](../especificaciones/03-documental.md)

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

_Pendiente._

## Fuentes

- [MCP Apps — visión general](https://modelcontextprotocol.io/extensions/apps/overview) y [especificación 2026-01-26](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx)
- [Cursor 2.6: MCP Apps](https://forum.cursor.com/t/cursor-2-6-mcp-apps/153482)
- [Claude Code — referencia de channels](https://code.claude.com/docs/en/channels-reference)
- [Is MCP good yet? (soporte por cliente)](https://ismcpgoodyet.com/)
- Pizarras: [draw.io MCP](https://github.com/lgazo/drawio-mcp-server), [Excalidraw MCP](https://glama.ai/mcp/servers/dkrcam97vn)
