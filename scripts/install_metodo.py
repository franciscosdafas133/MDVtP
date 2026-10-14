#!/usr/bin/env python3
"""Instala el método para usarlo en cualquier proyecto (B15–B16).

Modos:
  --alcance global   → ~/.cursor/skills/product-flow (vale para todos tus proyectos)
  --alcance proyecto → <proyecto>/.cursor/skills/product-flow (solo ese repo)

La skill va self-contained: SKILL.md + procedures + scripts + contracts + templates.
Manifiesto SHA-256 para actualizar/retirar sin borrar lo ajeno.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _paquete_version() -> str:
    vfile = ROOT / "VERSION"
    if vfile.is_file():
        return vfile.read_text(encoding="utf-8").strip() or "0.1.0-rc1"
    return "0.1.0-rc1"


PAQUETE_VERSION = _paquete_version()
SKILL_NAME = "product-flow"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files(src: Path) -> list[Path]:
    if src.is_file():
        return [src]
    return sorted(p for p in src.rglob("*") if p.is_file())


def home_skill_dir(host: str) -> Path:
    home = Path.home()
    if host == "cursor":
        return home / ".cursor" / "skills" / SKILL_NAME
    if host == "claude":
        return home / ".claude" / "skills" / SKILL_NAME
    raise ValueError(host)


def project_skill_dir(proyecto: Path, host: str) -> Path:
    if host == "cursor":
        return proyecto / ".cursor" / "skills" / SKILL_NAME
    if host == "claude":
        return proyecto / ".claude" / "skills" / SKILL_NAME
    raise ValueError(host)


def skill_body(alcance: str, skill_root_hint: str) -> str:
    if alcance == "global":
        rutas = f"""## Dónde está instalado (global)

Skill self-contained en:
`{skill_root_hint}`

En **cualquier** proyecto que abras:
1. El workflow del producto va en `workflow/` de ese proyecto.
2. Usa los scripts de la skill (ruta de arriba).

```bash
python3 {skill_root_hint}/scripts/product_flow.py iniciar --proyecto . --idea "…"
python3 {skill_root_hint}/scripts/product_flow.py continuar --proyecto .
python3 {skill_root_hint}/scripts/validate_workflow.py workflow
```
"""
    else:
        rutas = """## Dónde está instalado (este proyecto)

Skill self-contained en `.cursor/skills/product-flow/` (o `.claude/skills/…`).

```bash
python3 .cursor/skills/product-flow/scripts/product_flow.py iniciar --proyecto . --idea "…"
python3 .cursor/skills/product-flow/scripts/product_flow.py continuar --proyecto .
python3 .cursor/skills/product-flow/scripts/validate_workflow.py workflow
```

(Si instalaste en Claude: cambia `.cursor` por `.claude`.)
"""
    return f"""---
name: product-flow
description: >-
  Única entrada del método: inicia o continúa el flujo de producto (documentación,
  decisiones, estado). Usar cuando el usuario quiera empezar un producto, seguir,
  ver estado, decidir, anotar, verificar, recuperar o impactar. No pedir que elija
  otras skills. Aplicable a cualquier proyecto donde exista o se cree workflow/.
---

# product-flow

Coordinador del método. El usuario no elige skills auxiliares: tú enrutas.

{rutas}

## Reglas

- Escribe en `workflow/` del **proyecto abierto** (cwd / raíz del workspace).
- Antes de marcar verificado: corre el validador de esta skill.
- Puertas de producto las responde el usuario.
- Procedimientos: `procedures/` junto a este SKILL.md.
- Detalle canónico también en `SKILL.md` del núcleo si existe copia en el repo del método.
"""


def build_bundle(dest: Path, alcance: str) -> None:
    """Materializa skill self-contained en dest/."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    # procedures + skill base
    src_skill = ROOT / "core" / "skills" / "product-flow"
    for name in ("procedures",):
        shutil.copytree(src_skill / name, dest / name)
    # scripts
    (dest / "scripts").mkdir()
    for name in ("product_flow.py", "validate_workflow.py"):
        shutil.copy2(ROOT / "scripts" / name, dest / "scripts" / name)
    # contracts & templates
    shutil.copytree(ROOT / "core" / "contracts", dest / "contracts")
    shutil.copytree(ROOT / "core" / "templates", dest / "templates")
    # notices
    notices = ROOT / "THIRD_PARTY_NOTICES.md"
    if notices.is_file():
        shutil.copy2(notices, dest / "THIRD_PARTY_NOTICES.md")
    else:
        (dest / "THIRD_PARTY_NOTICES.md").write_text(
            "# Avisos de terceros\n\nVer DEC-08 / docs/seleccion.md\n",
            encoding="utf-8",
        )

    hint = str(dest)
    (dest / "SKILL.md").write_text(skill_body(alcance, hint), encoding="utf-8")


def write_manifest(dest_skill: Path, alcance: str, hosts: list[str]) -> dict:
    archivos = {}
    for f in iter_files(dest_skill):
        if f.name == "manifest.json":
            continue
        rel = str(f.relative_to(dest_skill))
        archivos[rel] = {"sha256": sha256_file(f)}
    manifest = {
        "paquete": "product-flow-metodo",
        "version": PAQUETE_VERSION,
        "alcance": alcance,
        "hosts": hosts,
        "instalado": now_iso(),
        "archivos": archivos,
    }
    (dest_skill / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def load_manifest(dest_skill: Path) -> dict | None:
    p = dest_skill / "manifest.json"
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def conflicts_for(dest_skill: Path, fuerza: bool) -> list[str]:
    if not dest_skill.exists():
        return []
    prev = load_manifest(dest_skill)
    out = []
    if prev is None:
        # hay algo pero no es nuestro manifiesto
        if any(dest_skill.iterdir()):
            out.append(str(dest_skill))
        return out
    for f in iter_files(dest_skill):
        if f.name == "manifest.json":
            continue
        rel = str(f.relative_to(dest_skill))
        rec = (prev.get("archivos") or {}).get(rel, {}).get("sha256")
        if rec and sha256_file(f) != rec:
            out.append(f"{dest_skill.name}/{rel} (modificado)")
    return out


def cmd_install(
    alcance: str,
    proyecto: Path | None,
    hosts: list[str],
    fuerza: bool,
) -> int:
    targets: list[Path] = []
    if alcance == "global":
        for h in hosts:
            targets.append(home_skill_dir(h))
    else:
        if proyecto is None:
            print("--proyecto es obligatorio con --alcance proyecto", file=sys.stderr)
            return 2
        proyecto = proyecto.resolve()
        if not proyecto.is_dir():
            print(f"No es directorio: {proyecto}", file=sys.stderr)
            return 2
        for h in hosts:
            targets.append(project_skill_dir(proyecto, h))

    all_conflicts: list[str] = []
    for t in targets:
        all_conflicts.extend(conflicts_for(t, fuerza))
    if all_conflicts and not fuerza:
        print("Conflictos (revisa o usa --fuerza):", file=sys.stderr)
        for c in all_conflicts:
            print(f"  · {c}", file=sys.stderr)
        return 1

    for t in targets:
        build_bundle(t, alcance)
        write_manifest(t, alcance, hosts)

    print(f"Instalado (alcance={alcance}, versión={PAQUETE_VERSION})")
    for t in targets:
        print(f"  → {t}")
    if alcance == "global":
        print("  Ya puedes abrir cualquier proyecto y usar /product-flow")
        print(
            f"  Ejemplo:\n    python3 {targets[0]}/scripts/product_flow.py "
            'iniciar --proyecto . --idea "…"'
        )
    else:
        print("  En este proyecto: usa la skill product-flow o los scripts bajo .cursor/skills/…")
    return 0


def cmd_status(alcance: str, proyecto: Path | None, hosts: list[str]) -> int:
    ok_all = True
    for h in hosts:
        if alcance == "global":
            dest = home_skill_dir(h)
        else:
            if proyecto is None:
                print("Falta --proyecto", file=sys.stderr)
                return 2
            dest = project_skill_dir(proyecto.resolve(), h)
        m = load_manifest(dest)
        print(f"[{h}] {dest}")
        if not m:
            print("  (no instalado)")
            ok_all = False
            continue
        print(f"  versión={m.get('version')} instalado={m.get('instalado')}")
        broken = []
        for rel, meta in (m.get("archivos") or {}).items():
            path = dest / rel
            if not path.is_file():
                broken.append(f"faltante {rel}")
            elif sha256_file(path) != meta.get("sha256"):
                broken.append(f"modificado {rel}")
        if broken:
            ok_all = False
            for b in broken:
                print(f"  · {b}")
        else:
            print(f"  integridad OK ({len(m.get('archivos') or {})} archivos)")
    return 0 if ok_all else 1


def cmd_uninstall(
    alcance: str,
    proyecto: Path | None,
    hosts: list[str],
    forzar_modificados: bool,
) -> int:
    removed = 0
    skipped = 0
    for h in hosts:
        if alcance == "global":
            dest = home_skill_dir(h)
        else:
            if proyecto is None:
                print("Falta --proyecto", file=sys.stderr)
                return 2
            dest = project_skill_dir(proyecto.resolve(), h)
        m = load_manifest(dest)
        if not m:
            print(f"Nada en {dest}")
            continue
        for rel, meta in list((m.get("archivos") or {}).items()):
            path = dest / rel
            if not path.is_file():
                continue
            if sha256_file(path) != meta.get("sha256") and not forzar_modificados:
                print(f"Conservado (modificado): {path}")
                skipped += 1
                continue
            path.unlink()
            removed += 1
        man = dest / "manifest.json"
        if man.is_file():
            man.unlink()
            removed += 1
        # si no quedan archivos nuestros, borrar árbol
        if dest.is_dir():
            leftovers = list(iter_files(dest))
            if not leftovers or forzar_modificados:
                shutil.rmtree(dest, ignore_errors=True)
            else:
                # podar vacíos
                for p in sorted(dest.rglob("*"), reverse=True):
                    if p.is_dir() and not any(p.iterdir()):
                        p.rmdir()
        print(f"Retirado: {dest}")
    print(f"Archivos retirados≈{removed}; conservados modificados={skipped}")
    return 0


def cmd_build_dist() -> int:
    """Genera skills/product-flow/ en el repo (para GitHub / plugin Cursor)."""
    dest = ROOT / "skills" / SKILL_NAME
    build_bundle(dest, alcance="proyecto")
    # SKILL genérico para distribución (sin ruta home)
    (dest / "SKILL.md").write_text(
        skill_body(
            "proyecto",
            ".cursor/skills/product-flow",
        ).replace(
            "Skill self-contained en `.cursor/skills/product-flow/`",
            "Skill self-contained (esta carpeta, o la copia instalada en el host)",
        ),
        encoding="utf-8",
    )
    write_manifest(dest, "dist", ["cursor", "claude"])
    print(f"Bundle de distribución: {dest}")
    return 0


def cmd_demo() -> int:
    demo = ROOT / "tests" / "fixtures" / "demo-instalacion"
    if demo.exists():
        shutil.rmtree(demo)
    demo.mkdir(parents=True)

    print("=== DEMO install proyecto ===\n")
    if cmd_install("proyecto", demo, ["cursor", "claude"], fuerza=False) != 0:
        return 1
    print("\n=== DEMO status proyecto ===\n")
    if cmd_status("proyecto", demo, ["cursor", "claude"]) != 0:
        return 1

    # smoke: iniciar workflow en el proyecto demo usando la skill instalada
    script = demo / ".cursor" / "skills" / "product-flow" / "scripts" / "product_flow.py"
    import subprocess

    r = subprocess.run(
        [
            sys.executable,
            str(script),
            "iniciar",
            "--proyecto",
            str(demo),
            "--idea",
            "demo install cualquier proyecto",
        ],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(r.stdout, r.stderr, file=sys.stderr)
        return 1
    print("iniciar vía skill instalada: OK")

    skill = demo / ".cursor" / "skills" / "product-flow" / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\n# editado\n", encoding="utf-8")
    print("\n=== DEMO conflicto ===\n")
    if cmd_install("proyecto", demo, ["cursor"], fuerza=False) == 0:
        print("ERROR: debía fallar", file=sys.stderr)
        return 1
    print("(conflicto OK)")

    print("\n=== DEMO uninstall ===\n")
    if cmd_install("proyecto", demo, ["cursor", "claude"], fuerza=True) != 0:
        return 1
    if cmd_uninstall("proyecto", demo, ["cursor", "claude"], False) != 0:
        return 1
    left = (demo / ".cursor" / "skills" / "product-flow").exists()
    print(f"\n=== Demo proyecto limpio={not left} → {'OK' if not left else 'FALLA'} ===")

    # demo global en carpeta temporal (no tocar el home real del usuario)
    print("\n=== DEMO global (HOME temporal) ===\n")
    fake_home = ROOT / "tests" / "fixtures" / "demo-home-global"
    if fake_home.exists():
        shutil.rmtree(fake_home)
    fake_home.mkdir(parents=True)
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(fake_home)
    try:
        if cmd_install("global", None, ["cursor"], fuerza=True) != 0:
            return 1
        gdir = fake_home / ".cursor" / "skills" / "product-flow"
        ok = (gdir / "scripts" / "product_flow.py").is_file()
        print(f"global en fake HOME: {'OK' if ok else 'FALLA'}")
        cmd_uninstall("global", None, ["cursor"], True)
    finally:
        if old_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = old_home

    return 0 if not left and ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Instalar product-flow para cualquier proyecto (global) o uno concreto"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_i = sub.add_parser("install", help="Instalar o actualizar")
    p_i.add_argument(
        "--alcance",
        choices=("global", "proyecto"),
        default="global",
        help="global = todos tus proyectos; proyecto = solo un repo (default: global)",
    )
    p_i.add_argument(
        "--proyecto",
        type=Path,
        default=None,
        help="Obligatorio si --alcance proyecto",
    )
    p_i.add_argument("--hosts", default="cursor", help="cursor,claude")
    p_i.add_argument("--fuerza", action="store_true")

    p_s = sub.add_parser("status", help="Integridad de la instalación")
    p_s.add_argument("--alcance", choices=("global", "proyecto"), default="global")
    p_s.add_argument("--proyecto", type=Path, default=None)
    p_s.add_argument("--hosts", default="cursor")

    p_u = sub.add_parser("uninstall", help="Retirar instalación")
    p_u.add_argument("--alcance", choices=("global", "proyecto"), default="global")
    p_u.add_argument("--proyecto", type=Path, default=None)
    p_u.add_argument("--hosts", default="cursor")
    p_u.add_argument("--fuerza-modificados", action="store_true")

    sub.add_parser("build-dist", help="Genera skills/product-flow/ para publicar en GitHub")
    sub.add_parser("demo", help="Prueba install proyecto + global (HOME fake)")

    args = p.parse_args(argv)
    hosts = [h.strip() for h in getattr(args, "hosts", "cursor").split(",") if h.strip()]

    if args.cmd == "install":
        return cmd_install(args.alcance, args.proyecto, hosts, args.fuerza)
    if args.cmd == "status":
        return cmd_status(args.alcance, args.proyecto, hosts)
    if args.cmd == "uninstall":
        return cmd_uninstall(
            args.alcance, args.proyecto, hosts, args.fuerza_modificados
        )
    if args.cmd == "build-dist":
        return cmd_build_dist()
    if args.cmd == "demo":
        return cmd_demo()
    return 2


if __name__ == "__main__":
    sys.exit(main())
