# Revisión del paso 11 — Checkpoints y recuperación aislada

Estado: **aceptada por el usuario** · 2026-10-12  
Depende de: paso 10 aceptado · Siguiente: pasos 15–16 (instalación en proyecto)

---

## De qué trata (en cristiano)

Aquí está el “guardar partida” y el “abrir esa partida en otra mesa”.

- **Checkpoint:** marcas un punto (con qué se comprobó de verdad y qué quedó pendiente).  
- **Recuperar:** abres ese punto en un **sitio aparte** (worktree/rama). Lo que hiciste después en el proyecto original **sigue ahí**; no se mezcla.

No es lo mismo que una **puerta** (tú decides producto). Tampoco deshace un pago en producción: eso es otro tipo de recuperación (más adelante en operación).

---

## Qué hay

```bash
python3 scripts/product_flow.py checkpoint --proyecto … --nombre "…" --alcance "…" --commit
python3 scripts/product_flow.py recuperar --proyecto … --checkpoint CP-01
python3 scripts/product_flow.py demo-b11
```

La demo crea un repo de prueba, guarda CP-01, hace un cambio después, abre un worktree: el cambio posterior **no** aparece en el aislado y **sí** en el original.

---

## Checklist

- [ ] Te encaja guardar un punto con alcance explícito (qué sí / qué no se comprobó)  
- [ ] Te encaja recuperar en un sitio **aparte** sin ensuciar lo actual  
- [ ] Te encaja el límite sin git (solo docs)  
- [ ] `demo-b11` te da OK  

**Respuestas:** `paso 11 ok` · o · `paso 11, cambiar: …`
