# depurar (DEC-05 / X02 + ciclo usuario)

Mismo ciclo que implementar, aplicado al fallo:

1. **Escanear** código/docs y el error  
2. Reproducir  
3. **Planificar** una sola hipótesis  
4. **Evaluar** (¿tiene sentido? ¿hay test que la demuestre?)  
5. **Reemplazar** con el arreglo mínimo  
6. Volver a verificar  

Tope: **3 intentos**. Al tercero → parar y preguntar al usuario.

Tope: **3 intentos**. Al tercero → parar y preguntar al usuario.

```bash
python3 <skill>/scripts/product_flow.py depurar \
  --proyecto . --tarea TASK-02 \
  --hipotesis "El handler no lee el query param" \
  --resultado fallo

# Tras el 3er fallo el script bloquea la tarea y exige puerta humana.
```
