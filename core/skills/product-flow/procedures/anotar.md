# anotar

1. Identificar a qué apunta el apunte (ASK / DEC / REQ / OBJ / TASK). Si es ambiguo, aclarar.
2. Ejecutar:

```bash
python3 <método>/scripts/product_flow.py anotar \
  --proyecto <proyecto> --enlaza ASK-03 \
  --texto "Todavía no tengo acceso al router"
```

3. Queda en `workflow/apuntes.json` + nodo NOTE en `relaciones.json`.
4. Los pendientes aparecen en `estado` / `continuar`.
5. No convierte el apunte en decisión. Si hay que decidir, usa `decidir`.
