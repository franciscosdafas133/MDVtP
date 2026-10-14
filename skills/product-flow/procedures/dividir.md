# dividir (R09) — no se parte por capricho

Inspirado en cc-sdd `tasks-generation` + `tasks-parallel-analysis` (sin horas).

## ¿Cuándo SÍ dividir?

Debes poder marcar **un** `--porque`:

| Criterio | Significa |
|---|---|
| `varios_resultados_verificables` | Hay ≥2 finales que se comprueban aparte |
| `varias_fronteras` | API / UI / datos distintos (salvo integración explícita) |
| `duda_determinante` | Una duda cambia el diseño del resto |
| `una_evidencia_no_basta` | Una sola prueba no cerraría la tarea |

Si no encaja ninguno → **no dividas**.

## ¿Cuándo NO?

- Un solo resultado y una frontera.
- Tarea de integración que une piezas ya hechas.
- Trozos ridículos (bookkeeping).

## Cada hija

- Condición **observable**: qué será verdad al acabar (API, UI, BD, test…).
- **Prohibido** tamaño en horas.
- Evita vaguedades (“implementar soporte”) sin resultado concreto.
- Modo:
  - `cadena` (default): espera a lo anterior.
  - `paralelo`: misma oleada; solo si no se pisan datos/archivos y se puede probar sola.

## Comando

```bash
python3 <skill>/scripts/product_flow.py dividir \
  --proyecto . \
  --padre TASK-99 \
  --porque varios_resultados_verificables \
  --motivo "Mezcla listado, UI y confirmación" \
  --hijas "Listar peluqueros|GET /peluqueros 200|paralelo;Página horarios|Existe /horarios|paralelo;Confirmar reserva|Registro en BD|cadena"
```

Reglas detalladas: `core/contracts/reglas-division.json` (o copia en la skill instalada).
