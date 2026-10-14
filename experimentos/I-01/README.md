# I-01 — Prueba desechable de ventana interactiva

**Desechable.** No forma parte del paquete. Responde a la pregunta de [docs/investigaciones/I-01-ventana-interactiva.md](../../docs/investigaciones/I-01-ventana-interactiva.md).

## Qué hay aquí

| Archivo | Rol |
|---|---|
| `server.py` | Servidor MCP (stdio, solo biblioteca estándar de Python). |
| `ui/editor.html` | Ventana MCP App: edita el documento y pide corrección a la IA del host. |
| `producto.md` | Documento de ejemplo (app de reservas de peluquería). |
| `state/` | Propuestas aceptadas/rechazadas y registro de la prueba. |

Sin `npm`, sin SDK. El protocolo `postMessage` de MCP Apps está implementado a mano en el HTML.

## Cómo probarlo (camino actual: HTML aparte)

La MCP App dentro del chat **no pinta** en este Cursor. El camino vigente es el navegador:

```bash
python3 experimentos/I-01/standalone_server.py
# abre http://127.0.0.1:8765/
```

1. Edita el texto en el navegador.
2. Pulsa **Pedir corrección a la IA del IDE**.
3. En Cursor, el agente lee `state/solicitud.json` y deja `state/propuesta.json` (o `POST /api/proponer`).
4. En el HTML: **Aceptar** o **Rechazar**.

### Camino abandonado aquí (MCP App)

Queda en `server.py` / `probe-oficial/` como evidencia de que Cursor no montó el widget.

## Qué se mide

- ¿Se abre la ventana con el documento?
- ¿Se puede editar?
- ¿`sampling/createMessage` usa el modelo de Cursor (sin otra clave)?
- Si no, ¿funciona el plan B (`ui/message` al chat)?
- ¿El archivo en disco solo cambia al aceptar?
