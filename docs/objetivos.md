# Objetivos del paquete

Fuente: [PLAN_PAQUETE_FLUJO_IA.md](../PLAN_PAQUETE_FLUJO_IA.md) §1–§3, §10 y §14. Estado: propuesta para revisión (B01). Los identificadores `OBJ-xx` son los que inician la cadena de trazabilidad `OBJ → REQ → DEC → TASK → CHECK → EVID`.

## Objetivo general

Construir un paquete instalable, en español, que guíe el desarrollo de productos de software mediante un flujo conectado de skills, documentos, decisiones y verificaciones. El usuario conversa con un único coordinador y entiende en todo momento qué está aceptando, rechazando, dejando pendiente o cambiando. El paquete funciona en Claude Code y en Cursor a partir de un núcleo común.

El producto que diseñamos es **el propio método**. Ahora no se desarrolla una aplicación de negocio.

## Objetivos específicos

| ID | Objetivo | Requisitos | Cómo sabremos que se cumple |
|---|---|---|---|
| OBJ-01 | **Una sola entrada guiada.** El usuario inicia, continúa, consulta el estado y cambia de dirección con el mismo coordinador, sin conocer las skills internas. Ante una idea vaga, el coordinador descubre qué preguntar y por qué. | R02, R03, R08 | E01, E03, E06 |
| OBJ-02 | **Registro honesto del conocimiento.** Hechos e hipótesis conservan su estado y procedencia; cada decisión tiene alternativas, consecuencias y estado; los apuntes del usuario quedan asociados a lo que comentan. | R04, R05, R06 | E02, E03 |
| OBJ-03 | **Trazabilidad e impacto.** Un resultado de producto puede seguirse hasta requisitos, decisiones, tareas, comprobaciones y evidencia. Reabrir una decisión invalida lo afectado. Las incoherencias se detectan mecánicamente cuando es posible. | R07, R11, R19 | E07, E12, E17 |
| OBJ-04 | **Continuidad y recuperación.** Otra sesión reconstruye el estado desde archivos y código. Se puede volver a un checkpoint en una rama aislada sin perder trabajo posterior. | R12, R13 | E06, E11, E13, E18 |
| OBJ-05 | **Ejecución controlada.** El trabajo amplio se divide; las dependencias reales se registran y se distingue simulación de integración real; nada se declara verificado sin evidencia; la depuración se detiene si no converge. | R09, R10, R14, R15 | E04, E05, E08, E09, E10, E15 |
| OBJ-06 | **Ciclo completo y profundidad proporcional.** El flujo cubre descubrimiento, construcción, integración, entrega, operación y aprendizaje, y ajusta el detalle al riesgo e incertidumbre del proyecto. | R17, R18 | E17, E18 |
| OBJ-07 | **Portabilidad e instalación limpia.** El mismo escenario se completa en Claude Code y Cursor. El instalador solo toca archivos propios, detecta conflictos y permite retirarlos. | R01, R16 | E13, E14 |
| OBJ-08 | **Método mantenible y evaluado.** Cada versión registra cambios de contrato y migración; el comportamiento del agente se evalúa con casos controlados y evidencia independiente de su autoevaluación. | R20 (y R14) | E15, E16, B18 |

Cobertura: R01–R20 quedan asignados a al menos un objetivo.

## Objetivos por entrega

- **Entrega A (B01–B08):** diseño revisable antes de programar. Fuentes auditadas, selección justificada, especificaciones y contratos con comprobaciones de integridad.
- **Entrega B (B09–B11, B15, 1.ª parte de B16):** flujo documental guiado con estado y recuperación, instalable en un proyecto de prueba en ambos hosts.
- **Entrega C (resto):** ejecución completa, integración, operación, evaluación y versión candidata con guía breve (iniciar, continuar, decidir, recuperar).

## Fuera de alcance (no objetivos)

- Construir ahora una aplicación de negocio.
- Instalar o activar todos los proyectos de referencia, o combinar sus sistemas de estado.
- Maximizar el número de skills: el número de skills no es una meta.
- Exigir al usuario una especificación completa por adelantado o rellenar documentos por cumplir casillas.
- Afirmar utilidad en cualquier producto: la versión candidata solo permite afirmar lo que pasó en los escenarios y hosts efectivamente probados.

## Qué permitirá afirmar la versión candidata

Que el paquete implementa un flujo guiado y pasó los escenarios y hosts realmente probados, con la lista de requisitos pendientes. Una afirmación más amplia necesita proyectos reales, uso sostenido y cambios posteriores documentados.
