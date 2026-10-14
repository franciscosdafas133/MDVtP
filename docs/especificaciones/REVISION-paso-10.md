# Revisión del paso 10 — Continuidad, apuntes e impacto

Estado: **aceptada por el usuario** (`paso 10 ok`) · 2026-10-12  
Depende de: paso 9 aceptado · Siguiente: paso 11 (checkpoints / recuperación aislada)

---

## De qué trata (en cristiano)

El paso 9 abría el proyecto. El 10 hace tres cosas de “vida real”:

1. **Apuntar** algo sin decidir («todavía no tengo el router») y que no se pierda.  
2. Si **cambia un requisito**, lo que ya estaba “verificado” **deja de contar** solo: la tarea vuelve a revisión y la evidencia queda caducada (no se borra la historia).  
3. Si **cierras el chat y vuelves**, el método mira archivos + validador + apuntes + git sucio — no la memoria del modelo.

Como cuando cambias el plano de una casa: las fotos viejas de la obra siguen en el álbum, pero ya no demuestran que la casa actual está bien.

---

## Qué hay

| Acción | Comando |
|---|---|
| Anotar | `product_flow.py anotar --enlaza ASK-03 --texto "…"` |
| Impactar cambio | `product_flow.py impactar --cambiado REQ-01 --motivo "…"` |
| Retomar | `product_flow.py continuar` (ahora con contraste) |

Demo:

```bash
python3 scripts/product_flow.py demo-b10
```

Debe acabar con: `TASK-02=en_revision`, `EVID-01=stale`, un apunte, y `→ OK`.

---

## Checklist

- [ ] Te encaja poder **apuntar** sin convertir eso en decisión  
- [ ] Te encaja que al cambiar un requisito se **invalide** lo dependiente (no seguir como si nada)  
- [ ] Te encaja que al **continuar** mire validador / apuntes / git, no el chat  
- [ ] `demo-b10` te corre OK  

**Respuestas:** `paso 10 ok` · o · `paso 10, cambiar: …`

---

## Límites normales

- Recuperar en otra rama/worktree → paso 11.  
- `decidir` completo en script (propuesta → aceptada con alternativas) sigue apoyado sobre todo en la skill + JSON a mano/asistido.
