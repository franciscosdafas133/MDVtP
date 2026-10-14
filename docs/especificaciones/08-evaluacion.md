# ESP-08 — Plan de evaluación

Estado: borrador 0.2 · Fuente: encargo §10, §14 · Decisiones: DEC-04, DEC-05 · Requisitos: R14, R15, R19 y, de forma transversal, R01–R20

## Qué la inicia

Cerrar los contratos (B08) para las comprobaciones deterministas, y tener comportamiento implementado (B12–B14, B17) para las observaciones del agente.

## Qué produce

- Fixtures en `tests/fixtures/` y escenarios en `tests/scenarios/`.
- Resultados por escenario, host y versión, con entradas, acciones, salidas y evidencia conservadas.

## Fijado por el encargo

**Dos clases de comprobación:**

- **Deterministas del paquete:** contratos, referencias, transiciones y recuperación. Las ejecuta un script, sin juicio del agente.
- **Observaciones del agente:** si el agente sigue el método en una ejecución real. Una plantilla correcta no demuestra un comportamiento correcto.

**Escenarios obligatorios:** E01–E18 tal como aparecen en el encargo §10 (no se duplican aquí). Agrupación propuesta:

| Grupo | Escenarios | Clase principal |
|---|---|---|
| Descubrimiento y decisiones | E01, E02, E03 | Observación del agente |
| Dependencias y división | E04, E05, E09 | Observación + comprobación de estado |
| Continuidad e impacto | E06, E07, E12, E13 | Determinista + observación |
| Verificación honesta y diagnóstico | E08, E10, E15 | Observación con evaluador independiente |
| Recuperación | E11, E18 | Determinista + observación |
| Instalación y versiones | E14, E16 | Determinista |
| Integración | E17 | Determinista + observación |

**Reglas:**

- El defecto de un fixture lo conoce el evaluador y no se insinúa en el nombre de la carpeta.
- No se adjudica éxito por el juicio del mismo agente que produjo el resultado.
- Se registran las variaciones y se repite ante resultados contradictorios o inestables. El umbral se fija por escenario y riesgo, no con un número arbitrario de ejecuciones.
- Incluir fixtures sanos para comprobar que el agente no inventa problemas (E15).
- Si falta un host o un acceso, el resultado queda pendiente, no aprobado ni fallido (B19).

## Cómo se revisa

El usuario revisa en B18 y B19 el criterio de éxito de cada escenario antes de ejecutarlo, y después los resultados con su evidencia.

## Qué permite avanzar

Escenarios con resultado esperado y criterio de éxito definidos → B18 y B19. Resultados registrados → B21 enumera lo que puede afirmarse y lo pendiente.

## Cerrado en B07

| Pregunta | Resolución |
|---|---|
| ¿TEA? | Solo principios/formato (X20); no el arnés. Sus JSON demuestran procedencia, no eficacia (B05). |
| ¿Evaluador independiente? | (1) Scripts deterministas del paquete; (2) el **usuario** en puertas manuales y en revisión de B18; (3) opcional segunda sesión/modelo solo si hace falta desempate — nunca el mismo agente autojuzgándose. |
| ¿Formato de resultado? | JSON por escenario: host, versión, entrada, acciones, veredicto, evidencia, timestamp (inspiración X20). |

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| Umbral de estabilidad por escenario | B18 |
