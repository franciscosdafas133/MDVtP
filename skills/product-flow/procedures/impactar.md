# impactar (cambio de requisito / decisión)

Cuando el usuario cambia un REQ, DEC u OBJ ya enlazado:

```bash
python3 <método>/scripts/product_flow.py impactar \
  --proyecto <proyecto> --cambiado REQ-01 \
  --motivo "ahora también elige servicios"
```

Efectos mecánicos:

- Tareas `verificada` que dependen → `en_revision`
- Sus evidencias `vigente` → `stale` (se conservan; ya no cuentan)
- Eventos en `eventos.jsonl`
- No toca el código automáticamente

Luego `continuar` para ver el siguiente paso.
