# Contratos del método (paso 8)

Reglas **comprobables a máquina** sobre el `workflow/` de un proyecto de usuario.  
Inspiración: contrato de estado Spec Kit (X10) y evidencia `stale` de GSD (X12); implementación propia en Python stdlib.

| Archivo | Para qué |
|---|---|
| [vocabulario.json](vocabulario.json) | Prefijos, estados, tipos de relación/evento |
| [transiciones.json](transiciones.json) | Transiciones permitidas |
| [esquema-estado.json](esquema-estado.json) | Forma de `estado.json` |
| [esquema-evento.json](esquema-evento.json) | Forma de cada línea de `eventos.jsonl` |
| [esquema-decision.json](esquema-decision.json) | Una decisión por archivo JSON |
| [esquema-relacion.json](esquema-relacion.json) | Nodos y aristas (`relaciones.json`) |
| [esquema-evidencia.json](esquema-evidencia.json) | Evidencias y `stale` |
| [esquema-apuntes.json](esquema-apuntes.json) | Apuntes NOTE enlazados (paso 10) |
| [esquema-checkpoint.json](esquema-checkpoint.json) | Metadatos de checkpoint (paso 11) |
| [reglas-division.json](reglas-division.json) | Cuándo/cómo dividir tareas (paso 12) |
| [reglas-verificacion-debug.json](reglas-verificacion-debug.json) | Verificar y depurar (paso 13) |
| [reglas-operacion.json](reglas-operacion.json) | Entrega / operación (paso 14, R18) |

**Validador:** `scripts/validate_workflow.py`  
**Revisión humana:** [docs/especificaciones/REVISION-paso-8.md](../../docs/especificaciones/REVISION-paso-8.md)

Metadatos de docs Markdown (producto, requisitos…): en el paso 9 las plantillas alinean front matter mínimo; la autoridad de ids/enlaces es `relaciones.json`.
