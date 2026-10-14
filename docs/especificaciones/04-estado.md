# ESP-04 — Contrato de estado

Estado: borrador 0.3 · Fuente: encargo §5, §6, §8 · Decisiones: DEC-02, DEC-03 · Contratos: B08 · Requisitos: R08, R13, R14, R19

## Qué la inicia

Cualquier transición de una tarea, decisión, comprobación o actividad, y cada reanudación de sesión.

## Qué produce

- `workflow/estado.json`: única autoridad sobre navegación y ejecución.
- `workflow/eventos.jsonl`: historial reconciliable de transiciones y decisiones.
- `workflow/tablero.md` regenerado a partir del estado y las referencias.

## Fijado por el encargo

- **Escritor único:** un solo responsable escribe el estado. Escrituras atómicas donde corresponda.
- **Soporta interrupciones:** al retomar, se contrastan estado, eventos, documentos y árbol de trabajo antes de ejecutar nuevas tareas. Una transición incompleta se detecta y se recupera sin repetir efectos externos (E12).
- **Reconstrucción sin chat (R13):** otra sesión reconstruye el estado desde archivos y código.
- **Progreso (R08):** al continuar se informa de qué está en curso, qué falta, qué bloquea y cuál es la siguiente actividad preparada.
- **Evidencia (R14):** una tarea solo pasa a verificada con evidencia pertinente y vigente. Las pruebas omitidas o bloqueadas se informan.
- **Bloqueos parciales (R10):** una dependencia sin resolver bloquea solo el trabajo que depende de ella.
- **Integridad (R19):** cambios de estado inválidos, referencias rotas y comprobaciones desactualizadas se detectan mecánicamente cuando sea posible.
- No se diseña copiando a la vez los modelos de estado de cc-sdd, Spec Kit y GSD Core (§7).

**Estados de tarea** (confirmados en B08, mismos nombres que el tablero de construcción): `pendiente`, `preparada`, `en_curso`, `bloqueada`, `en_revision`, `verificada`.

Transiciones permitidas (`core/contracts/transiciones.json`):

| Desde | Hacia | Condición |
|---|---|---|
| pendiente | preparada | Todas las dependencias verificadas. |
| preparada | en_curso | Entradas, límites y comprobaciones confirmados. |
| en_curso | en_revision | Cambios hechos y comprobaciones ejecutadas o declaradas omitidas. |
| en_revision | verificada | Evidencia pertinente y vigente registrada. |
| cualquiera activa | bloqueada | Dependencia o acceso ausente registrado. |
| bloqueada | estado anterior | Bloqueo resuelto con evidencia. |
| verificada | en_revision | Una decisión o requisito del que depende cambió (R11). |

## Cómo se revisa

Pruebas deterministas de B17: estado inválido, escritura interrumpida, referencia rota y cambios sin commit, cada una con su resultado esperado.

## Qué permite avanzar

Esquema de `estado.json`, formato de evento, transiciones y validador definidos → B09 y B10.

## Cerrado en B07

| Pregunta | Resolución |
|---|---|
| ¿Estado o eventos? | **Instantánea + registro:** `estado.json` es la autoridad de “dónde estamos”; `eventos.jsonl` audita y permite reparar. Si discrepan, el validador marca incoherencia y se reconcilia antes de avanzar (no event-sourcing puro). |
| ¿Motor Spec Kit? | DEC-02/03: solo **contrato** (transiciones, atómico, eventos después del estado); validador propio. |
| ¿Escritura atómica? | Archivo temporal + `rename` en el mismo directorio (Python stdlib); comprobar en B15/B17. |
| ¿Runtime del validador? | **Python 3** (biblioteca estándar), alineado con DEC-03 y el servidor de ventana I-01. |

## Cerrado en B08

| Pregunta | Resolución |
|---|---|
| Esquema de `estado.json` y eventos | `core/contracts/esquema-estado.json`, `esquema-evento.json`; fixture `tests/fixtures/workflow-ok/` |

## Abierto

Ninguno bloqueante para B09.
