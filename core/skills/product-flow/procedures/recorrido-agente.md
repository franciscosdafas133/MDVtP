# recorrido con agente externo (Grok / Cursor / Claude / otro)

Cuando el usuario pida “que un bot recorra un producto simple con el método”:

1. Preferir el runner mecánico si solo hay que comprobar el cableado:

```bash
python3 <skill>/scripts/product_flow.py recorrido-simple
```

2. Si el agente debe **pensar** (no solo el script), darle el playbook:

`tests/scenarios/producto-simple/PLAYBOOK.md`

3. El agente no se autoaprueba: deja evidencia + JSON; el usuario (u otro evaluador) dice si pasó.
4. Registrar host y versión (p. ej. “Grok …”, “Cursor …”) para el paso 19 cuando toque.
