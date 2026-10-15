# Cómo instalar el método

Versión: ver [VERSION](VERSION).  
Uso: [docs/GUIA-USUARIO.md](docs/GUIA-USUARIO.md).  
Límites: [docs/LIMITES-CANDIDATA.md](docs/LIMITES-CANDIDATA.md).

Lo que se descarga para usar es la skill en `skills/product-flow/` (y el plugin en `.cursor-plugin/`).

## Opción A — Skill (la más directa)

```bash
git clone https://github.com/franciscosdafas133/MDVtP.git
cp -R MDVtP/skills/product-flow ~/.cursor/skills/product-flow
# Claude Code:
# cp -R MDVtP/skills/product-flow ~/.claude/skills/product-flow
```

En el chat: pide **product-flow**.

```bash
python3 ~/.cursor/skills/product-flow/scripts/product_flow.py iniciar --proyecto . --idea "Mi app…"
```

## Opción B — Plugin en Cursor

1. Clona o abre este repo.
2. En Cursor: Customize → importar plugin **From GitHub Repository**  
   `https://github.com/franciscosdafas133/MDVtP`  
   (o “from folder” si tu Cursor lo permite sobre este clone).
3. Debe cargar la skill desde `skills/` (ver `.cursor-plugin/plugin.json`).

Aún no está en el Marketplace oficial.

## Opción C — Instalador del repo

```bash
cd MDVtP
python3 scripts/install_metodo.py install --alcance global --hosts cursor,claude
python3 scripts/install_metodo.py status --alcance global
```

Solo un proyecto:

```bash
python3 scripts/install_metodo.py install --alcance proyecto --proyecto /ruta/al/proyecto --hosts cursor
```

## Comprobar el paquete

```bash
cd MDVtP
python3 scripts/run_regresion.py
```

Tiene que terminar en `7/7 → ok`.
