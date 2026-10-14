# Revisión de la entrega B — Flujo usable e instalable

Estado: **aceptada por el usuario** (`entrega B ok`) · 2026-10-14  
Incluye: pasos 9, 10, 11, 15 y 1.ª parte del 16  
Siguiente: entrega C (paso 12 — partir tareas)

---

## De qué va esta entrega (en cristiano)

Con la B deberías poder:

1. Empezar un producto con **una sola puerta** (`product-flow`), sin elegir mil skills.  
2. Que el sistema **recuerde** (estado, apuntes) y **invalide** lo viejo si cambia un requisito.  
3. **Guardar partida** y recuperarla en un sitio aparte.  
4. **Instalar** el método **en global** (cualquier proyecto) o en un repo concreto, y **quitarlo** limpio. Ver [INSTALL.md](../../INSTALL.md).

No afirma: “el método ya sirve para productos complejos de punta a punta”. Eso es la C.

---

## Checklist de la B

### Paso 9 — Coordinador

- [ ] Una sola entrada te encaja (`iniciar` / `continuar` / `estado`…)  
- [ ] Idea vaga → docs + preguntas, no código a lo loco  
- [ ] Demo: `python3 scripts/product_flow.py demo`

### Paso 10 — Continuidad

- [ ] Puedes apuntar sin decidir  
- [ ] Si cambia un requisito, lo verificado deja de contar solo  
- [ ] Al continuar mira archivos/validador/git, no la memoria del chat  
- [ ] Demo: `python3 scripts/product_flow.py demo-b10`

### Paso 11 — Checkpoint / recuperar

- [ ] Guardar partida con alcance honesto  
- [ ] Recuperar en mesa aparte sin ensuciar lo actual  
- [ ] Demo: `python3 scripts/product_flow.py demo-b11`

### Pasos 15–16 — Instalación (cualquier proyecto)

- [ ] Install **global** → sirve en todos tus proyectos  
- [ ] Install **por proyecto** si quieres compartirlo en un repo  
- [ ] Manifiesto con huellas; retirada limpia  
- [ ] Camino a GitHub: `build-dist` + `.cursor-plugin/` + INSTALL.md  
- [ ] Demo: `python3 scripts/install_metodo.py demo`

Detalle solo de instalación: [REVISION-paso-15-16.md](REVISION-paso-15-16.md)

---

## Límites que aceptas al cerrar la B

- Claude Code en host real: versión aún por registrar.  
- Ventana localhost: existe el patrón; no arranca sola al cargar la skill.  
- Partir tareas grandes, implementar con evidencia, operación en prod → **entrega C**.

---

## Cómo responder

- `entrega B ok` o `pasos 15-16 ok` — cerramos B y vamos al paso 12.  
- `entrega B, cambiar: …` — ajustamos solo eso.
