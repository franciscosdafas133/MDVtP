# Cómo instalar el método (en cualquier proyecto)

Versión candidata: ver [VERSION](VERSION).  
Guía de uso: [docs/GUIA-USUARIO.md](docs/GUIA-USUARIO.md).  
Límites: [docs/LIMITES-CANDIDATA.md](docs/LIMITES-CANDIDATA.md).

## Lo que quieres

Abrir **cualquier** carpeta de proyecto en Cursor y poder usar `product-flow`
(empezar idea → docs → decisiones → checkpoints), sin copiar el repo del método
a mano cada vez.

## Opción recomendada: instalación global (una vez)

Desde este repositorio (clonado):

```bash
python3 scripts/install_metodo.py install --alcance global --hosts cursor
# o también Claude Code:
python3 scripts/install_metodo.py install --alcance global --hosts cursor,claude
```

Eso deja la skill en:

- `~/.cursor/skills/product-flow/`
- y/o `~/.claude/skills/product-flow/`

Luego, en **cualquier** proyecto:

```bash
python3 ~/.cursor/skills/product-flow/scripts/product_flow.py iniciar --proyecto . --idea "Mi app…"
```

En el chat de Cursor: pide usar la skill **product-flow** (o `/product-flow` si tu host lo lista así).

Comprobar / quitar:

```bash
python3 scripts/install_metodo.py status --alcance global
python3 scripts/install_metodo.py uninstall --alcance global
```

## Opción: solo un proyecto (para el equipo que clona ese repo)

```bash
python3 scripts/install_metodo.py install --alcance proyecto --proyecto /ruta/al/proyecto --hosts cursor
```

Queda en `/ruta/al/proyecto/.cursor/skills/product-flow/`.

## Publicar en GitHub para que otros instalen

1. Genera el bundle publicable:

```bash
python3 scripts/install_metodo.py build-dist
```

Eso escribe `skills/product-flow/` (self-contained) y el repo ya tiene
`.cursor-plugin/plugin.json`.

2. Sube el repo a GitHub (sin `.reference-sources/`).

3. Quien lo use puede:

   - **A.** Clonar y correr `install --alcance global`, o  
   - **B.** En Cursor: Customize → importar plugin **From GitHub Repository**
     (cuando el marketplace/plugin del host lo permita), o  
   - **C.** Copiar `skills/product-flow/` a `~/.cursor/skills/product-flow/`.

## Qué NO hace todavía

- No está en el Marketplace oficial de Cursor (hace falta revisión de Cursor).
- La ventana HTML localhost no se arranca sola al instalar (sí existe el patrón I-01).

## Demo local

```bash
python3 scripts/install_metodo.py demo
```
