# Revisión del paso 9 — Prototipo del coordinador

Estado: **aceptada por el usuario** (`paso 9 ok`) · 2026-10-12  
Depende de: paso 8 aceptado · Siguiente: paso 10 (continuidad e impacto)

---

## De qué trata (en cristiano)

Aquí aparece por fin el **compañero de una sola puerta**: `product-flow`.

Le das una idea vaga (ej. la peluquería) y el método:

1. Crea la carpeta `workflow/` con los documentos  
2. Deja la idea como hipótesis (`OBJ-01`)  
3. Te suelta preguntas de descubrimiento (sin inventar requisitos)  
4. Te dice el siguiente paso según el **validador**, no según el feeling del chat  
5. Tú no tienes que elegir entre mil skills

Todavía no es el producto completo (faltan continuidad fina, recuperación, instalación pulida). Es el **prototipo** que demuestra la entrada única.

---

## Qué hay

| Pieza | Dónde |
|---|---|
| Skill | `core/skills/product-flow/` (+ adaptador Cursor) |
| Plantillas | `core/templates/` |
| Script | `scripts/product_flow.py` (`iniciar` / `estado` / `continuar` / `demo`) |

Probar:

```bash
python3 scripts/product_flow.py demo
```

Debe crear `tests/fixtures/demo-iniciar/workflow/`, pasar el validador e imprimir el informe (objetivo, dudas, siguiente paso…).

---

## Checklist

- [ ] Te encaja **una sola entrada** (`product-flow`) sin menú de skills  
- [ ] Te encaja que una idea vaga produzca docs + preguntas, no código a lo loco  
- [ ] Te encaja el informe fijo (objetivo, confirmado, propuesto, dudas, siguiente…)  
- [ ] El comando `demo` te corre bien  

**Respuestas:** `paso 9 ok` · o · `paso 9, cambiar: …`

---

## Límites de este paso (normales)

- `decidir` / `anotar` / ventana localhost: el agente los hace con la skill; el script aún automatiza sobre todo iniciar/estado/continuar.  
- Recuperación con worktree → paso 11.  
- Instalador que copie la skill a cualquier proyecto → paso 16.
