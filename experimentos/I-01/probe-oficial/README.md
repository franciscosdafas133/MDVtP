# Probe oficial MCP Apps (I-01)

Copia adaptada del repro del [foro Cursor](https://forum.cursor.com/t/mcp-apps-client-stopped-issuing-resources-read-ui-widgets-dont-mount-regression-in-3-9-16/165222): un panel verde mínimo.

- Registrado en `~/.cursor/mcp.json` como `mcpAppsProbe` (alcance User/global).
- Node/npm de usuario: `~/.local/node-v24.21.0/` (sin `sudo`).
- Log: `global.log` (método `resources/read` = el host pidió el HTML).

Herramienta: `probe_show_widget`.
