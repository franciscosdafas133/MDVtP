# ESP-02 — Contrato del coordinador

Estado: borrador 0.1 · Fuente: encargo §4, §5, §13 · Requisitos: R02, R03, R08, R09, R17

## Qué la inicia

Cualquier mensaje del usuario dirigido al paquete: iniciar, continuar, consultar el estado, decidir, anotar, reabrir, recuperar o verificar.

## Qué produce

- La selección de la actividad siguiente y su justificación.
- Actualizaciones de documentos y del estado a través del escritor único (ESP-04).
- El informe de apertura y cierre de cada actividad.

## Fijado por el encargo

**Interfaz propuesta:** `/product-flow` con las acciones `iniciar`, `continuar`, `estado`, `decidir`, `anotar`, `reabrir`, `recuperar` y `verificar`. El adaptador puede exponerlas como argumentos o como conversación, según lo que el host permita de verdad (§4).

**Informe al iniciar y al cerrar cada actividad (§4):**

```text
Objetivo actual:
Actividad en curso:
Lo confirmado:
Lo propuesto:
Lo rechazado o aplazado:
Dudas y bloqueos:
Archivos actualizados:
Comprobaciones y pendientes:
Punto de recuperación disponible:
Siguiente paso y por qué:
```

**Comportamiento:**

- Entiende lenguaje natural («acepto esa alternativa», «apunta esto», «eso no lo quiero», «qué falta», «continúa», «quiero volver al diseño anterior»).
- Ante una referencia ambigua, aclara antes de cambiar estados (E03).
- Continúa automáticamente los pasos técnicos preparados dentro del alcance autorizado. Pide información solo cuando la respuesta corresponde al usuario o a un tercero, y mientras tanto avanza en trabajo independiente.
- Ante una idea vaga, propone preguntas relevantes, explica por qué importan y cómo responderlas (R03). Recorre las áreas de descubrimiento de §2: usuarios y permisos, datos y recuperación, integraciones y credenciales, procesos asíncronos, concurrencia, experiencia de uso, calidad, entornos, costes y operación. En cada área registra si aplica, qué se conoce, qué falta y cómo averiguarlo.
- Divide una tarea con varios objetivos o dudas determinantes antes de ejecutarla (R09).
- Cuando un paso necesita una investigación, la crea con su pregunta y su condición de cierre.
- Al retomar, contrasta estado, eventos, documentos y árbol de trabajo antes de actuar; detecta entradas ausentes o desactualizadas (§9).
- Una skill coordinadora carga procedimientos según la actividad; las skills auxiliares, si existen, solo se usan a través del coordinador (§5).

## Actividades que enruta

Las doce de §2: entender el problema, descubrir necesidades, investigar viabilidad, diseñar el sistema, preparar una base, planificar incrementos, implementar e integrar, verificar, diagnosticar, entregar, operar y mantener, y aprender. Para cada una se definirá en B07 su entrada, su salida, su condición de avance y qué hacer si falta evidencia (columna «Si falta evidencia» de §2).

## Cómo se revisa

Escenarios E01, E03, E05 y E06, y el ejemplo de §11, ejecutados en ambos hosts (B19).

## Qué permite avanzar

Contrato aceptado con todas las acciones asignadas a una transición de ESP-04 → B09 puede construir el prototipo.

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿Cómo se selecciona el próximo paso? ¿Tabla de enrutamiento por estado (estilo `progress` de GSD Core) u otra? | B04, B07 |
| ¿Argumentos o conversación en cada host? | B15 (según capacidades comprobadas) |
| ¿Qué procedimientos internos existen y cómo se cargan sin saturar el contexto? | B03, B07 (Agent OS como referencia condicional) |
| ¿Cómo se gradúa la profundidad (R17): criterios y señales de riesgo? | B07 |
