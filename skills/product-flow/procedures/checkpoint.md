# checkpoint

Guardar partida (no es una puerta humana).

```bash
python3 <método>/scripts/product_flow.py checkpoint \
  --proyecto <proyecto> \
  --nombre "Después del descubrimiento" \
  --alcance "Qué se comprobó de verdad" \
  --pendientes "ASK abiertas; sin tests de producto" \
  --commit
```

- `--commit` solo si el árbol está limpio (no mezcla basura sin commit).
- Sin git o sin `--commit`: queda snapshot documental en `workflow/checkpoints/CP-NN/`.
- El alcance no puede ser más amplio que lo realmente verificado.
