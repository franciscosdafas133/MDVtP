# Playbook — producto simple con el método

Para que **cualquier agente** (Cursor, Claude Code, Grok, otro) recorra un producto mínimo **usando el método**, no improvisando.

## Qué es esto

Un guion. El agente sigue los pasos. El veredicto **no** lo pone el mismo agente a ojo: lo ponen el script determinista y/o el usuario.

Hay dos modos:

| Modo | Quién | Comando / acción |
|---|---|---|
| Automático (sin juicio) | Script | `python3 scripts/product_flow.py recorrido-simple` |
| Con agente | Tú (Grok, etc.) | Sigue la sección «Pasos del agente» abajo |

## Producto de prueba

Idea: *Contador CLI que imprime `visitas: N` y guarda el número en un archivo.*

Carpeta de trabajo sugerida (el agente la crea):

`tests/fixtures/agente-recorrido/`  
(o la que indique quien lance la prueba; no pisar el repo del método sin `--fuerza` consciente).

## Pasos del agente

1. **Leer** `core/skills/product-flow/SKILL.md` y el procedure que toque.
2. **Iniciar** el workflow:

```bash
python3 <ruta-método>/scripts/product_flow.py iniciar \
  --proyecto <carpeta-trabajo> \
  --idea "Contador CLI: imprime visitas: N y guarda el número"
```

3. **Ciclo de código (obligatorio):** escanear → planificar → evaluar → reemplazar.  
   Escribir algo equivalente a `app/contador.py` + `app/comprobar.sh` (o tests).
4. **Correr la prueba de verdad** (`bash app/comprobar.sh` o equivalente). Si falla, no digas éxito.
5. **Evidenciar → presentar → verificar** con el script (`evidenciar`, `presentar`, `verificar`).
6. **Operar:** plan de entrega + pendientes reales honestos (`operar`).
7. **Validar:**

```bash
python3 <ruta-método>/scripts/validate_workflow.py <carpeta-trabajo>/workflow
```

8. **Entregar al evaluador** (usuario u otro agente): rutas de `workflow/`, salida de la prueba, y un JSON con el mismo espíritu que `ultimo-resultado.json` (entrada, acciones, evidencia). **No te autoapruebes.**

## Qué no hacer

- Marcar verificado sin evidencia vigente.
- Inventar que ya hubo despliegue o usuarios reales.
- Saltar el ciclo escanear → planificar → evaluar → reemplazar.
- Usar este playbook como si fuera GitHub Actions de producción: es una pista de prueba del método.

## Relación con el tablero

- Semilla de observación de agente → paso 18.  
- El script `recorrido-simple` es la comprobación **determinista** del cableado.  
- Cursor / Claude Code reales → paso 19. Grok u otro modelo: mismo playbook, registrar host y versión a mano.
