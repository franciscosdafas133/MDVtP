import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerAppResource, registerAppTool } from "@modelcontextprotocol/ext-apps/server";
import { z } from "zod";

const LABEL = process.env.PROBE_LABEL ?? "unlabeled";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const LOG = path.join(HERE, `${LABEL}.log`);
const RESOURCE_URI = "ui://probe/widget.html";

const record = (event, extra = {}) =>
  fs.appendFileSync(
    LOG,
    JSON.stringify({ t: new Date().toISOString(), label: LABEL, event, ...extra }) + "\n",
  );

record("server_start", { pid: process.pid });

const server = new McpServer(
  { name: `mcp-apps-probe-${LABEL}`, version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } },
);

registerAppTool(
  server,
  "probe_show_widget",
  {
    title: "Probe Show Widget",
    description:
      "Muestra un panel verde mínimo de MCP App. Prueba I-01: ¿Cursor pide resources/read?",
    annotations: { readOnlyHint: true, openWorldHint: false },
    inputSchema: {
      nonce: z.string().optional().describe("Valor arbitrario para evitar dedupe."),
    },
    _meta: { ui: { resourceUri: RESOURCE_URI } },
  },
  async ({ nonce }) => {
    record("tool_call", { tool: "probe_show_widget", nonce: nonce ?? null });
    return {
      content: [
        {
          type: "text",
          text:
            `probe widget (scope=${LABEL}, nonce=${nonce ?? "none"}). ` +
            `Si no ves un recuadro verde arriba, el host no hizo resources/read.`,
        },
      ],
      structuredContent: { scope: LABEL, nonce: nonce ?? null },
    };
  },
);

registerAppResource(
  server,
  "Probe Widget",
  RESOURCE_URI,
  { description: "Widget HTML mínimo para probar MCP Apps." },
  async () => {
    record("resource_read", { uri: RESOURCE_URI });
    return {
      contents: [
        {
          uri: RESOURCE_URI,
          mimeType: "text/html;profile=mcp-app",
          text:
            "<!DOCTYPE html><html><body style=\"margin:0;padding:16px;font:14px system-ui;background:#14532d;color:#ecfdf5\">" +
            `<strong>MCP App montada</strong> — alcance: ${LABEL}` +
            "<p style=\"margin:8px 0 0\">Si ves este fondo verde, la ventana interactiva funciona en Cursor.</p>" +
            "</body></html>",
        },
      ],
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);

const downstream = transport.onmessage;
transport.onmessage = (msg, extra) => {
  if (msg && typeof msg === "object" && "method" in msg) {
    record("jsonrpc_recv", { method: msg.method });
  }
  downstream?.(msg, extra);
};

record("connected");
