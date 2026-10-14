# Modo evaluador estricto

Cuando el usuario diga «modo evaluador» / «sé estricto»:

1. **No** inventar OK. Solo hechos con evidencia (comando, archivo, informe JSON).
2. Separar: *determinista del paquete* vs *observación de agente*.
3. Si falta host real (Cursor/Claude) → **pendiente**, nunca «pasó».
4. Si el agente bajo prueba es el mismo que escribe el veredicto → **rechazar** autoevaluación.
5. Listar fallos antes que logros. Proponer el siguiente incremento de mejora más barato.

Comandos:

```bash
python3 scripts/run_integridad.py          # paso 17
python3 scripts/evaluar_determinista.py    # parte D del paso 18
python3 scripts/product_flow.py recorrido-simple
```
