# bloquear / desbloquear (R10)

Bloqueo **parcial**: solo esa tarea (y avisas quién puede seguir).

```bash
python3 <skill>/scripts/product_flow.py bloquear \
  --proyecto . --tarea TASK-03 \
  --motivo "Sin acceso a la BD de staging" \
  --marca MANUAL_VERIFY_REQUIRED
```

Marcas útiles: `simulacion` | `integracion_real` | `MANUAL_VERIFY_REQUIRED`.

Desbloquear cuando haya evidencia real:

```bash
python3 <skill>/scripts/product_flow.py desbloquear \
  --proyecto . --tarea TASK-03 \
  --evidencia "Credenciales staging recibidas 2026-10-14"
```

No uses desbloquear en una tarea que fue **dividida** — trabaja las hijas.
