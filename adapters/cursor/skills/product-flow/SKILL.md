---
name: product-flow
description: >-
  Única entrada del método para Cursor. El instalador materializa la copia en
  .cursor/skills/product-flow/ y el núcleo en .metodo/.
---

# product-flow (adaptador Cursor)

Tras `python3 scripts/install_metodo.py install --proyecto <dir> --hosts cursor`:

- Skill activa: `.cursor/skills/product-flow/`
- Núcleo: `.metodo/` (scripts, contracts, templates, procedures)

Evita tener otra carpeta `product-flow` que Cursor descubra a la vez.

Comandos típicos desde el proyecto instalado:

```bash
python3 .metodo/scripts/product_flow.py iniciar --proyecto . --idea "…"
python3 .metodo/scripts/validate_workflow.py workflow
```
