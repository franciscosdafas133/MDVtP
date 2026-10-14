# ESP-02 — Contrato del coordinador

Estado: borrador 0.3 · Fuente: encargo §4, §5, §13 · Decisiones: DEC-02, DEC-03, DEC-07 · Prototipo: B09 · Requisitos: R02, R03, R08, R09, R17

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
- **DEC-02:** al iniciar/continuar la skill, se asegura la ventana HTML en localhost (servidor local del paquete) enlazada al agente del host; el chat no es el único lugar para editar documentación.
- **DEC-03 / DEC-07:** el coordinador propone; el validador bloquea transiciones inválidas; las puertas de producto las responde el usuario.

## Actividades que enruta

Las doce de §2. Entrada/salida/avance (resumen B07):

| Actividad | Entrada mínima | Sale con | Si falta evidencia |
|---|---|---|---|
| Entender problema | Idea o producto.md | producto.md usable + puertas pendientes | Preguntas R03; no inventar requisitos |
| Descubrir | producto | descubrimiento + preguntas | Marcar área «falta / cómo averiguarlo» |
| Viabilidad | descubrimiento | hipótesis con estado | Bloqueo parcial (R10), no frenar todo |
| Diseñar sistema | requisitos aceptados | sistema.md (+ flujos) | No avanzar implementación |
| Base / plan | sistema + decisiones | plan y tareas | Dividir (R09) |
| Implementar | tarea preparada | código + eventos | Distinguir simulación vs real (E04) |
| Verificar | plan de pruebas OK (DEC-04) | evidencia o no cumple | MANUAL_VERIFY_REQUIRED |
| Diagnosticar | fallo | informe + test que falla | Parar a los 3 (DEC-05) |
| Entregar / operar | verificación | operación.md | Checklist pendiente explícito |
| Aprender | cierre incremento | apuntes / mejoras al método | No borrar historia |

**Selección del próximo paso:** tabla de rutas (inspiración X11) sobre **hechos del validador** (tareas preparadas, bloqueos, evidencia stale), no sobre la narración del modelo.

## Cómo se revisa

Escenarios E01, E03, E05 y E06, y el ejemplo de §11, ejecutados en ambos hosts (B19). Revisión de diseño: [REVISION-paso-7.md](REVISION-paso-7.md).

## Qué permite avanzar

Contrato aceptado con acciones ↔ transiciones ESP-04 → B09.

## Cerrado en B09 (prototipo)

| Pregunta | Resolución |
|---|---|
| Procedimientos internos | `core/skills/product-flow/procedures/` + script `scripts/product_flow.py` (iniciar/estado/continuar/demo) |
| Idea vaga → incremento | Crea `workflow/`, OBJ-01 hipótesis, ASK-01…09, TASK-01 en descubrimiento; validador OK |

## Cerrado en B14

| Pregunta | Resolución |
|---|---|
| ¿Cómo se entrega / opera? | `product_flow.py operar` rellena `operacion.md`: checklist contextual, pendientes reales obligatorios, recuperación prod ≠ git. |

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿Argumentos o conversación en cada host? | B15 (adaptadores ya existen; afinado en uso real) |
| Escenarios E17/E18 con despliegue real | B18–B20 |
