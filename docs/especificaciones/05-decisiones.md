# ESP-05 — Contrato de decisiones

Estado: borrador 0.1 · Fuente: encargo §4, §5 · Requisitos: R05, R06, R11

## Qué la inicia

Una alternativa que el coordinador propone, una respuesta del usuario («acepto», «no lo quiero», «apunta esto», «aplázalo») o una petición de reabrir.

## Qué produce

Un registro por decisión significativa en `workflow/decisiones/`, eventos en `eventos.jsonl` y, si se reabre, un análisis de impacto con los artefactos marcados para revisión.

## Fijado por el encargo

**Contenido mínimo de una decisión:** identificador, contexto, alternativas, consecuencias de cada una, estado, motivo, apuntes asociados y relaciones con requisitos, tareas y evidencia.

**Estados:** `propuesta`, `aceptada`, `rechazada`, `aplazada`, `sustituida`.

**Reglas:**

- Una aceptación cubre solo la propuesta mostrada. Aceptar una sección no aprueba decisiones nuevas ni documentos posteriores.
- Si hay varias propuestas activas y la referencia del usuario es ambigua, se aclara antes de registrar nada (E03).
- Un rechazo conserva su motivo. La alternativa rechazada no vuelve a aparecer como elegida sin evidencia nueva.
- Los apuntes del usuario se vinculan a la decisión, pregunta o requisito que comentan (R06).
- **Reabrir (R11):** se conserva la decisión anterior (pasa a `sustituida` cuando se acepta la nueva), se propone un reemplazo, se analiza el impacto en documentos y tareas y se invalidan las aprobaciones y evidencias afectadas. El código no se modifica automáticamente para imitar un estado pasado.

**Ejemplo del encargo (§11):** «Acepto guardar resúmenes; no quiero almacenar el contenido de las comunicaciones. Apunta que todavía no tengo acceso al router» → una decisión aceptada, una alternativa rechazada con su motivo y un bloqueo de acceso registrado.

## Cómo se revisa

Escenarios E02, E03 y E07. Validador: transiciones de estado válidas y sin decisiones aceptadas en conflicto sobre el mismo asunto.

## Qué permite avanzar

Formato de registro y transiciones aceptados → el coordinador (ESP-02) implementa las acciones `decidir`, `anotar` y `reabrir`.

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿Qué umbral convierte una elección en «decisión significativa» con registro propio? | B07 (proporcional, R17) |
| ¿Qué toma de `bmad-correct-course` para el análisis de impacto y qué de `bmad-advanced-elicitation` para revisar propuestas? | B05 |
| ¿Los apuntes viven dentro de la decisión o en un registro de apuntes enlazado? | B07 |
