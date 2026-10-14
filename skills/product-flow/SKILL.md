---
name: product-flow
description: >-
  Única entrada del método: inicia o continúa el flujo de producto (documentación,
  decisiones, estado). Usar cuando el usuario quiera empezar un producto, seguir,
  ver estado, decidir, anotar, verificar, recuperar o impactar. No pedir que elija
  otras skills. Aplicable a cualquier proyecto donde exista o se cree workflow/.
---

# product-flow

Coordinador del método. El usuario no elige skills auxiliares: tú enrutas.

## Dónde está instalado (este proyecto)

Skill self-contained (esta carpeta, o la copia instalada en el host) (o `.claude/skills/…`).

```bash
python3 .cursor/skills/product-flow/scripts/product_flow.py iniciar --proyecto . --idea "…"
python3 .cursor/skills/product-flow/scripts/product_flow.py continuar --proyecto .
python3 .cursor/skills/product-flow/scripts/validate_workflow.py workflow
```

(Si instalaste en Claude: cambia `.cursor` por `.claude`.)


## Reglas

- Escribe en `workflow/` del **proyecto abierto** (cwd / raíz del workspace).
- Antes de marcar verificado: corre el validador de esta skill.
- Puertas de producto las responde el usuario.
- Procedimientos: `procedures/` junto a este SKILL.md.
- Detalle canónico también en `SKILL.md` del núcleo si existe copia en el repo del método.
