# bloquear / desbloquear (R10)

Bloqueo **parcial**: solo esa tarea (y avisas quién puede seguir).

```bash
python3 <skill>/scripts/product_flow.py bloquear \
  --proyecto . --tarea TASK-03 \
  --motivo "Sin pasarela de tarjeta" \
  --marca MANUAL_VERIFY_REQUIRED
```

Marcas útiles: `simulacion` | `integracion_real` | `MANUAL_VERIFY_REQUIRED`.

Si el motivo habla de tarjeta/pasarela y omites `--marca`, el método pone `MANUAL_VERIFY_REQUIRED` solo.

Desbloquear integración real **solo** con un id `EVID-…` de `evidenciar --origen comando --ejecutar` en verde. Una nota de simulación no vale:

```bash
python3 <skill>/scripts/product_flow.py desbloquear \
  --proyecto . --tarea TASK-03 \
  --evidencia EVID-01
```

No uses desbloquear en una tarea que fue **dividida** — trabaja las hijas.
