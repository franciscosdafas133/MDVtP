# Revisión del paso 8 — Contratos y validador

Estado: **aceptada por el usuario** (`paso 8 ok`) · 2026-10-12  
Depende de: paso 7 aceptado · Siguiente: paso 9 (prototipo del coordinador)

Esto es el **candado**: reglas que una máquina puede comprobar, para que el agente no invente estados ni dé por bueno algo roto.

---

## En una frase

Definimos cómo deben verse los archivos del `workflow/` y un script Python que dice *OK* o *FALLA* con códigos claros.

---

## Qué hay ahora

| Pieza | Dónde |
|---|---|
| Vocabulario y transiciones | `core/contracts/` |
| Validador | `scripts/validate_workflow.py` |
| Ejemplos buenos y malos | `tests/fixtures/workflow-*` |

Probar en tu máquina:

```bash
python3 scripts/validate_workflow.py --self-test
```

Debe imprimir cinco `[OK]`.

---

## Reglas que fijamos (en cristiano)

1. **Ids con forma fija** — `REQ-01`, `TASK-02`, `DEC-01`… Nada de nombres libres para lo mecánico.
2. **Estados cerrados** — una tarea solo puede estar en: pendiente → preparada → en_curso → en_revision → verificada (o bloqueada). Una decisión: propuesta / aceptada / rechazada / aplazada / sustituida.
3. **Enlaces en un solo sitio** — `workflow/relaciones.json` es la lista oficial de “esto apunta a aquello”. Si algo apunta a un id que no existe → falla.
4. **Decisiones en JSON** — un archivo por decisión en `workflow/decisiones/`. Dos aceptadas sobre el mismo asunto → falla.
5. **Evidencia con caducidad** — si una prueba decía “ok” con un hash de archivo y el archivo cambió, el validador marca `evidencia_stale`. No puedes tener una tarea *verificada* solo con evidencias muertas.
6. **Eventos vs foto** — `estado.json` manda el “ahora”; `eventos.jsonl` es la historia. Si el último evento de una tarea no cuadra con el estado → incoherencia.

Los Markdown (producto, requisitos…) se rellenan en el paso 9; aquí el motor ya sabe qué ids y estados son legales.

---

## Qué demuestra el self-test

| Caso | Qué rompimos | Qué detecta |
|---|---|---|
| ok | nada | pasa |
| ref-rota | enlace a `REQ-99` | referencia rota |
| transición | de verificada a preparada | transición ilegal |
| evidencia-stale | hash distinto | evidencia caducada |
| decisión-conflicto | dos DEC aceptadas igual | conflicto |

---

## Checklist de tu revisión

- [ ] Te encaja que el “cerebro mecánico” sea JSON (`estado`, `relaciones`, `evidencias`, `decisiones`) y no solo Markdown
- [ ] Te encajan los estados de tarea y de decisión
- [ ] Te encaja que una referencia rota o una evidencia vieja **bloqueen** (no solo avisen en el chat)
- [ ] El comando `--self-test` te corre en verde

**Respuestas útiles:**  
`paso 8 ok` — cerramos y vamos al 9.  
`paso 8, cambiar: …` — ajustamos el contrato/validador.

---

## Qué no pide este paso

- El chat coordinador (`iniciar`, `continuar`…) — eso es el paso 9.  
- Instalar la skill en un proyecto real — más adelante.  
- Recuperación con worktree — paso de recuperación, no este.
