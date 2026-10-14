# Especificaciones del paquete

Índice de los ocho registros del encargo (§9). Alineados con [decisiones.md](../decisiones.md) y [seleccion.md](../seleccion.md). Contratos máquina: [`core/contracts/`](../../core/contracts/).

**Revisión actual:** [REVISION-paso-8.md](REVISION-paso-8.md). Paso 7 cerrado: [REVISION-paso-7.md](REVISION-paso-7.md).

| ID | Registro | Requisitos | Depende de | Estado |
|---|---|---|---|---|
| ESP-01 | [Producto del paquete](01-producto.md) | R01–R20 | — | borrador 0.2 |
| ESP-02 | [Contrato del coordinador](02-coordinador.md) | R02, R03, R08, R09, R17 | ESP-01, ESP-03, ESP-04 | borrador 0.2 |
| ESP-03 | [Contrato documental](03-documental.md) | R04, R06, R07, R11 | ESP-01 | borrador 0.3 |
| ESP-04 | [Contrato de estado](04-estado.md) | R08, R13, R14, R19 | ESP-03 | borrador 0.3 |
| ESP-05 | [Contrato de decisiones](05-decisiones.md) | R05, R06, R11 | ESP-03, ESP-04 | borrador 0.3 |
| ESP-06 | [Contrato de recuperación](06-recuperacion.md) | R12, R13, R18 | ESP-04 | borrador 0.2 |
| ESP-07 | [Contrato de hosts e instalación](07-hosts-instalacion.md) | R01, R16, R20 | ESP-02 | borrador 0.2 |
| ESP-08 | [Plan de evaluación](08-evaluacion.md) | R14, R15, R19 + E01–E18 | ESP-02 a ESP-07 | borrador 0.2 |

## Estructura común

1. Qué la inicia  
2. Qué produce  
3. Cómo se revisa  
4. Qué permite avanzar  
5. Fijado (encargo + decisiones aceptadas)  
6. Abierto (solo lo que queda para B08/B15/…)

## Regla de consistencia

Antes de programar (B08 → B09): nombres, estados e identificadores alineados entre ESP-03, ESP-04 y ESP-05.
