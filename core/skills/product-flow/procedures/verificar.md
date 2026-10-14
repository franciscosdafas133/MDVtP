# verificar (DEC-04 / X01)

El cambio de código ya debió seguir: **escanear → planificar → evaluar → reemplazar**.

Orden al cerrar:

1. Tarea/requisito claro  
2. Plan de pruebas (auto vs manual)  
3. **Puerta humana:** el usuario OK al plan  
4. Ejecutar pruebas ligadas a ese requisito  
5. Revisión manual si aplica  
6. Cerrar solo con evidencia **vigente**

```bash
# Registrar evidencia (comando, hash, etc.)
python3 <skill>/scripts/product_flow.py evidenciar \
  --proyecto . --tarea TASK-02 \
  --origen comando --valor "pytest -q tests/test_peluqueros.py" \
  --cubre "src/peluqueros.py"

# Pedir revisión (en_curso → en_revision)
python3 <skill>/scripts/product_flow.py presentar \
  --proyecto . --tarea TASK-02

# Cerrar (solo si hay EVID vigente o omitida justificada)
python3 <skill>/scripts/product_flow.py verificar \
  --proyecto . --tarea TASK-02

# Si falla la prueba
python3 <skill>/scripts/product_flow.py verificar \
  --proyecto . --tarea TASK-02 --fallo "expected 200 got 500"
```

**Prohibido:** decir “listo” si el test falló o no se corrió.
