#!/usr/bin/env python3
"""Servidor MCP desechable para I-01: ventana editable + IA del host.

Solo biblioteca estándar. Habla JSON-RPC 2.0 por stdin/stdout.
"""

from __future__ import annotations

import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PRODUCTO = ROOT / "producto.md"
UI_HTML = ROOT / "ui" / "editor.html"
STATE_DIR = ROOT / "state"
LOG_PATH = STATE_DIR / "prueba.jsonl"
REJECTED_PATH = STATE_DIR / "rechazos.jsonl"
RESOURCE_URI = "ui://i01/editor"
MIME = "text/html;profile=mcp-app"
SERVER_NAME = "i01-ventana"
SERVER_VERSION = "0.1.0"

# Protocolo MCP reciente; Cursor anuncia el suyo en initialize.
PROTOCOL_VERSION = "2024-11-05"


def log_event(kind: str, **payload: Any) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": kind,
        **payload,
    }
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_producto() -> str:
    return PRODUCTO.read_text(encoding="utf-8")


def write_producto(text: str) -> None:
    PRODUCTO.write_text(text, encoding="utf-8")


def load_ui() -> str:
    return UI_HTML.read_text(encoding="utf-8")


def ok_text(
    text: str,
    structured: dict[str, Any] | None = None,
    *,
    ui_resource: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "content": [{"type": "text", "text": text}],
    }
    if structured is not None:
        result["structuredContent"] = structured
    if ui_resource:
        # Algunos hosts miran _meta en el resultado, no solo en tools/list.
        result["_meta"] = {
            "ui": {"resourceUri": ui_resource},
            "ui/resourceUri": ui_resource,
        }
    return result


def tool_abrir_documento(_args: dict[str, Any]) -> dict[str, Any]:
    text = read_producto()
    log_event("abrir_documento", chars=len(text))
    result = ok_text(
        "Ventana de producto abierta. Edita el documento y pide corrección a la IA.",
        {"path": str(PRODUCTO), "text": text},
        ui_resource=RESOURCE_URI,
    )
    # Algunos hosts montan si el HTML va embebido en el resultado.
    result["content"].append(
        {
            "type": "resource",
            "resource": {
                "uri": RESOURCE_URI,
                "mimeType": MIME,
                "text": load_ui(),
            },
        }
    )
    return result


def tool_leer_documento(_args: dict[str, Any]) -> dict[str, Any]:
    text = read_producto()
    return ok_text(text, {"path": str(PRODUCTO), "text": text})


def tool_aceptar_propuesta(args: dict[str, Any]) -> dict[str, Any]:
    new_text = args.get("text")
    if not isinstance(new_text, str) or not new_text.strip():
        return {
            "isError": True,
            "content": [{"type": "text", "text": "Falta el texto aceptado."}],
        }
    reason = args.get("reason") or ""
    write_producto(new_text)
    log_event("aceptar", reason=reason, chars=len(new_text))
    return ok_text(
        f"Guardado en {PRODUCTO.name}.",
        {"path": str(PRODUCTO), "saved": True},
    )


def tool_rechazar_propuesta(args: dict[str, Any]) -> dict[str, Any]:
    reason = args.get("reason") or "sin motivo"
    proposal = args.get("proposal") or ""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
        "proposal": proposal,
    }
    with REJECTED_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    log_event("rechazar", reason=reason)
    return ok_text("Rechazo anotado. El archivo no cambió.", {"saved": False})


TOOLS: dict[str, dict[str, Any]] = {
    "abrir_documento": {
        "name": "abrir_documento",
        "title": "Abrir editor de producto",
        "description": (
            "Abre la ventana interactiva con producto.md (app de reservas de "
            "peluquería). Úsala cuando el usuario pida la ventana de producto, "
            "I-01 o editar la documentación en la ventana."
        ),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        # Formato nuevo + legacy (registerAppTool del SDK hace lo mismo).
        "_meta": {
            "ui": {"resourceUri": RESOURCE_URI, "visibility": ["model", "app"]},
            "ui/resourceUri": RESOURCE_URI,
        },
    },
    "leer_documento": {
        "name": "leer_documento",
        "description": "Lee el contenido actual de producto.md del experimento I-01.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "_meta": {"ui": {"visibility": ["model", "app"]}},
    },
    "aceptar_propuesta": {
        "name": "aceptar_propuesta",
        "description": (
            "Escribe en disco el texto aceptado por el usuario en la ventana. "
            "Solo la ventana (o el usuario vía agente) debe llamarla tras Aceptar."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Texto completo a guardar"},
                "reason": {"type": "string", "description": "Resumen de la corrección"},
            },
            "required": ["text"],
            "additionalProperties": False,
        },
        "_meta": {"ui": {"visibility": ["app", "model"]}},
    },
    "rechazar_propuesta": {
        "name": "rechazar_propuesta",
        "description": "Anota un rechazo sin modificar el archivo en disco.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "proposal": {"type": "string"},
                "reason": {"type": "string"},
            },
            "additionalProperties": False,
        },
        "_meta": {"ui": {"visibility": ["app", "model"]}},
    },
}

HANDLERS = {
    "abrir_documento": tool_abrir_documento,
    "leer_documento": tool_leer_documento,
    "aceptar_propuesta": tool_aceptar_propuesta,
    "rechazar_propuesta": tool_rechazar_propuesta,
}


def handle_initialize(params: dict[str, Any]) -> dict[str, Any]:
    client_caps = params.get("capabilities") or {}
    log_event("initialize", client=params.get("clientInfo"), capabilities=client_caps)
    return {
        "protocolVersion": params.get("protocolVersion") or PROTOCOL_VERSION,
        "capabilities": {
            "tools": {"listChanged": False},
            "resources": {"listChanged": False},
            "extensions": {
                "io.modelcontextprotocol/ui": {
                    "mimeTypes": [MIME],
                }
            },
        },
        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
    }


def handle_tools_list(_params: dict[str, Any]) -> dict[str, Any]:
    tools = list(TOOLS.values())
    # Comprobar que _meta.ui.resourceUri sigue en la respuesta (Cursor lo necesita).
    log_event(
        "tools/list",
        count=len(tools),
        abrir_meta=TOOLS["abrir_documento"].get("_meta"),
    )
    return {"tools": tools}


def handle_tools_call(params: dict[str, Any]) -> dict[str, Any]:
    name = params.get("name")
    args = params.get("arguments") or {}
    if name not in HANDLERS:
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"Herramienta desconocida: {name}"}],
        }
    log_event("tools/call", name=name)
    return HANDLERS[name](args)


def handle_resources_list(_params: dict[str, Any]) -> dict[str, Any]:
    return {
        "resources": [
            {
                "uri": RESOURCE_URI,
                "name": "Editor de producto (I-01)",
                "description": "Ventana editable de producto.md",
                "mimeType": MIME,
                "_meta": {"ui": {"csp": {}}},
            }
        ]
    }


def handle_resources_read(params: dict[str, Any]) -> dict[str, Any]:
    uri = params.get("uri")
    if uri != RESOURCE_URI:
        raise ValueError(f"Recurso desconocido: {uri}")
    log_event("resources/read", uri=uri)
    return {
        "contents": [
            {
                "uri": RESOURCE_URI,
                "mimeType": MIME,
                "text": load_ui(),
                "_meta": {"ui": {"csp": {}}},
            }
        ]
    }


def handle_ping(_params: dict[str, Any]) -> dict[str, Any]:
    return {}


METHODS = {
    "initialize": handle_initialize,
    "ping": handle_ping,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
    "resources/list": handle_resources_list,
    "resources/read": handle_resources_read,
}


def respond(msg_id: Any, result: Any) -> None:
    out = {"jsonrpc": "2.0", "id": msg_id, "result": result}
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def respond_error(msg_id: Any, code: int, message: str) -> None:
    out = {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": code, "message": message},
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def notify(method: str, params: dict[str, Any] | None = None) -> None:
    out: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        out["params"] = params
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def process(message: dict[str, Any]) -> None:
    method = message.get("method")
    msg_id = message.get("id")
    params = message.get("params") or {}

    # Notificaciones del cliente (sin id): ignorar salvo logging.
    if msg_id is None:
        if method == "notifications/initialized":
            log_event("client_initialized")
        return

    if method == "notifications/initialized":
        respond(msg_id, {})
        return

    handler = METHODS.get(method) if isinstance(method, str) else None
    if handler is None:
        respond_error(msg_id, -32601, f"Método no soportado: {method}")
        return

    try:
        result = handler(params)
        respond(msg_id, result)
        if method == "initialize":
            # Algunos hosts esperan esta notificación del servidor; no hace daño.
            pass
    except Exception as exc:  # noqa: BLE001 — POC: registrar y devolver error
        log_event("error", method=method, error=str(exc), trace=traceback.format_exc())
        respond_error(msg_id, -32000, str(exc))


def main() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    log_event("server_start", root=str(ROOT))
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            log_event("bad_json", line=line[:200])
            continue
        process(message)


if __name__ == "__main__":
    main()
