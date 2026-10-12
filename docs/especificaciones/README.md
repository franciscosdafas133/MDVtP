# Especificaciones del paquete

Índice de los ocho registros que pide el encargo (§9). **Estado de todos: borrador 0.1, previo a B07.** Recogen lo que el encargo ya fija y las preguntas abiertas. Se completarán en B07, cuando la auditoría de fuentes (B03–B05) y la selección (B06) estén verificadas. Si la auditoría propone otra estructura, puede cambiarse si se conserva la trazabilidad y se justifica el cambio.

| ID | Registro | Requisitos | Depende de | Estado |
|---|---|---|---|---|
| ESP-01 | [Producto del paquete](01-producto.md) | R01–R20 | — | borrador 0.1 |
| ESP-02 | [Contrato del coordinador](02-coordinador.md) | R02, R03, R08, R09, R17 | ESP-01, ESP-03, ESP-04 | borrador 0.1 |
| ESP-03 | [Contrato documental](03-documental.md) | R04, R06, R07, R11 | ESP-01 | borrador 0.1 |
| ESP-04 | [Contrato de estado](04-estado.md) | R08, R13, R14, R19 | ESP-03 | borrador 0.1 |
| ESP-05 | [Contrato de decisiones](05-decisiones.md) | R05, R06, R11 | ESP-03, ESP-04 | borrador 0.1 |
| ESP-06 | [Contrato de recuperación](06-recuperacion.md) | R12, R13, R18 | ESP-04 | borrador 0.1 |
| ESP-07 | [Contrato de hosts e instalación](07-hosts-instalacion.md) | R01, R16, R20 | ESP-02 | borrador 0.1 |
| ESP-08 | [Plan de evaluación](08-evaluacion.md) | R14, R15, R19 + E01–E18 | ESP-02 a ESP-07 | borrador 0.1 |

## Estructura común de cada especificación

1. **Qué la inicia:** el evento o la necesidad que la activa.
2. **Qué produce:** archivos, estados o resultados.
3. **Cómo se revisa:** quién la revisa y con qué comprobación.
4. **Qué permite avanzar:** la condición que habilita la actividad siguiente.
5. **Fijado por el encargo:** lo que no se reabre sin una decisión explícita.
6. **Abierto:** preguntas con la tarea que las resuelve.

## Regla de consistencia

Antes de programar (B08 → B09), comprobar que cada especificación sirve como entrada de la siguiente sin reinterpretaciones contradictorias: los nombres, estados e identificadores deben coincidir entre ESP-03, ESP-04 y ESP-05.
