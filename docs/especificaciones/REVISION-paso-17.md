# Revisión del paso 17 — Integridad e interrupciones

Estado: **aceptada** (`paso 17 ok`) · 2026-10-14  

## Evidencia

```bash
python3 scripts/run_integridad.py   # 8/8 ok
```

Informe: `tests/scenarios/integridad/ultimo-informe.json`

Casos: fixtures validador, estado inválido, JSON truncado, dirty bloquea checkpoint, recuperación aislada (demo-b11), escritura atómica, install smoke, recorrido-simple.
