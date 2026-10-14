#!/usr/bin/env python3
"""Servidor local desechable I-01: HTML aparte (no dentro del chat).

Solo biblioteca estándar. Sirve el editor y una API JSON sobre producto.md.
La IA del host (agente de Cursor en el IDE) lee state/solicitud.json y escribe
state/propuesta.json; el HTML la muestra con aceptar/rechazar.
"""

from __future__ import annotations

import json
import mimetypes
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PRODUCTO = ROOT / "producto.md"
UI = ROOT / "ui" / "standalone.html"
STATE = ROOT / "state"
SOLICITUD = STATE / "solicitud.json"
PROPUESTA = STATE / "propuesta.json"
RECHAZOS = STATE / "rechazos.jsonl"
LOG = STATE / "standalone.jsonl"
HOST = "127.0.0.1"
PORT = 8765


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(kind: str, **payload: Any) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": now(), "kind": kind, **payload}, ensure_ascii=False) + "\n")


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def write_json(path: Path, data: dict[str, Any]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


class Handler(BaseHTTPRequestHandler):
    server_version = "I01Standalone/0.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        # Evitar ruido en stdout; va al registro del experimento.
        log("http", message=fmt % args)

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, data: Any) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _bytes(self, code: int, data: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in ("/", "/index.html", "/editor"):
            html = UI.read_text(encoding="utf-8").encode("utf-8")
            self._bytes(200, html, "text/html; charset=utf-8")
            return
        if path == "/api/documento":
            text = PRODUCTO.read_text(encoding="utf-8") if PRODUCTO.is_file() else ""
            self._json(200, {"path": str(PRODUCTO), "text": text})
            return
        if path == "/api/estado":
            self._json(
                200,
                {
                    "solicitud": read_json(SOLICITUD),
                    "propuesta": read_json(PROPUESTA),
                },
            )
            return
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if path == "/api/salud":
            self._json(200, {"ok": True, "service": "i01-standalone", "ts": now()})
            return
        if path.startswith("/ui/"):
            rel = path[len("/ui/") :]
            target = (ROOT / "ui" / rel).resolve()
            if not str(target).startswith(str((ROOT / "ui").resolve())) or not target.is_file():
                self._json(404, {"error": "no encontrado"})
                return
            data = target.read_bytes()
            ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
            self._bytes(200, data, ctype)
            return
        self._json(404, {"error": "ruta desconocida", "path": path})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json(400, {"error": "JSON inválido"})
            return

        if path == "/api/solicitar":
            text = payload.get("text")
            if not isinstance(text, str) or not text.strip():
                self._json(400, {"error": "falta text"})
                return
            # Nueva solicitud invalida propuesta previa.
            if PROPUESTA.is_file():
                PROPUESTA.unlink()
            data = {
                "ts": now(),
                "status": "pendiente",
                "text": text,
                "hint": (
                    "Agente del host: lee este archivo, propone corrección del documento "
                    "de producto (peluquería) y escribe state/propuesta.json con "
                    '{"reason":"...","proposal":"texto completo"}.'
                ),
            }
            write_json(SOLICITUD, data)
            log("solicitar", chars=len(text))
            self._json(200, {"ok": True, "solicitud": data})
            return

        if path == "/api/proponer":
            # Permite que el agente (u otra herramienta) deposite la propuesta por HTTP.
            reason = payload.get("reason") or ""
            proposal = payload.get("proposal")
            if not isinstance(proposal, str) or not proposal.strip():
                self._json(400, {"error": "falta proposal"})
                return
            data = {
                "ts": now(),
                "reason": reason,
                "proposal": proposal,
                "source": payload.get("source") or "host-agent",
            }
            write_json(PROPUESTA, data)
            sol = read_json(SOLICITUD) or {}
            sol["status"] = "propuesta_lista"
            write_json(SOLICITUD, sol)
            log("proponer", chars=len(proposal))
            self._json(200, {"ok": True, "propuesta": data})
            return

        if path == "/api/aceptar":
            text = payload.get("text")
            if not isinstance(text, str) or not text.strip():
                self._json(400, {"error": "falta text"})
                return
            PRODUCTO.write_text(text, encoding="utf-8")
            if PROPUESTA.is_file():
                PROPUESTA.unlink()
            if SOLICITUD.is_file():
                SOLICITUD.unlink()
            log("aceptar", chars=len(text), reason=payload.get("reason") or "")
            self._json(200, {"ok": True, "saved": True, "path": str(PRODUCTO)})
            return

        if path == "/api/rechazar":
            row = {
                "ts": now(),
                "reason": payload.get("reason") or "rechazado en HTML aparte",
                "proposal": payload.get("proposal") or "",
            }
            STATE.mkdir(parents=True, exist_ok=True)
            with RECHAZOS.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            if PROPUESTA.is_file():
                PROPUESTA.unlink()
            sol = read_json(SOLICITUD) or {}
            sol["status"] = "rechazada"
            write_json(SOLICITUD, sol)
            log("rechazar", reason=row["reason"])
            self._json(200, {"ok": True, "saved": False})
            return

        self._json(404, {"error": "ruta desconocida", "path": path})


def main() -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    if not UI.is_file():
        print(f"Falta {UI}", file=sys.stderr)
        sys.exit(1)
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}/"
    log("server_start", url=url)
    print(url, flush=True)
    print(f"Editor I-01 (HTML aparte) en {url}", file=sys.stderr)
    print("Ctrl+C para parar.", file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nParado.", file=sys.stderr)
    finally:
        httpd.server_close()
        log("server_stop")


if __name__ == "__main__":
    main()
