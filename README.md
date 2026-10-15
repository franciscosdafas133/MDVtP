# MDVtP — product-flow (el método)

Skill / plugin para **Cursor** y **Claude Code**: idea → preguntas → requisitos → tareas → pruebas honestas → entrega.

Versión: [VERSION](VERSION) (`0.1.0-rc1`).

## Qué descargas

| Ruta | Para qué |
|---|---|
| `skills/product-flow/` | La skill (copiar a `~/.cursor/skills/` o `~/.claude/skills/`) |
| `.cursor-plugin/plugin.json` | Declaración del plugin (apunta a `skills/`) |

Instalación: [INSTALL.md](INSTALL.md).  
Uso: [docs/GUIA-USUARIO.md](docs/GUIA-USUARIO.md).  
Límites: [docs/LIMITES-CANDIDATA.md](docs/LIMITES-CANDIDATA.md).  
Probar todas las funciones: [docs/PROBAR-TODO.md](docs/PROBAR-TODO.md).

```bash
git clone https://github.com/franciscosdafas133/MDVtP.git
cp -R MDVtP/skills/product-flow ~/.cursor/skills/product-flow
```

## Comprobar

```bash
cd MDVtP && python3 scripts/run_regresion.py
```

## Licencias

[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
