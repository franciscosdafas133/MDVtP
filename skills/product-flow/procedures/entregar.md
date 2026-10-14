# entregar / operar (R18)

Cuando el incremento va a salir (o a staging):

1. Seguir el ciclo de código si aún hay cambios: escanear → planificar → evaluar → reemplazar.  
2. Generar/actualizar `workflow/operacion.md` con el plan contextual.  
3. Listar **comprobaciones reales pendientes** (no inventar que ya se probaron).  
4. Separar recuperación de **código** (checkpoint/worktree) vs **producción** (datos/APIs/pagos).

```bash
python3 <skill>/scripts/product_flow.py operar \
  --proyecto . \
  --resumen "Primera versión de reservas" \
  --pendientes "Pago real no probado; SMS del salón sin credenciales"
```
