# ESP-06 — Contrato de recuperación

Estado: borrador 0.3 · Fuente: encargo §5 · Decisiones: DEC-07 · Prototipo: B11 · Requisitos: R12, R13, R18

## Qué la inicia

Crear un checkpoint al cerrar una actividad comprobada, o una petición del usuario como «quiero volver al punto anterior a ese cambio».

## Qué produce

- Metadatos en `workflow/checkpoints/`.
- Una rama o worktree aislado creado desde el commit del checkpoint, con su propio tablero que refleja la nueva dirección y conserva la historia de la alternativa anterior.

## Fijado por el encargo

**Metadatos de un checkpoint:** nombre comprensible, commit, versión del paquete, documentos asociados, comprobaciones ejecutadas, aspectos pendientes y dependencias externas. Solo se etiqueta como «comprobado» para el alcance realmente verificado. Los datos simulados y la falta de credenciales aparecen de forma explícita. Nada de copias indiscriminadas de datos o secretos.

**Tres tipos de recuperación, que no se confunden:**

1. **Reabrir una decisión:** conservar la anterior, proponer un reemplazo y revisar el impacto (ESP-05). No toca el código automáticamente.
2. **Recuperar código y documentos:** identificar un commit comprobado, revisar los cambios actuales y crear una rama o worktree desde ese punto. Continuar allí sin perder el trabajo posterior. Si se pide revertir en la rama activa, analizar dependencias y proteger los cambios propios y del usuario; nunca borrados masivos.
3. **Recuperar un sistema desplegado:** procedimiento específico para datos, infraestructura e integraciones. Git no deshace una migración externa, un pago ni una acción ejecutada por una API (E18).

**Protección:** el agente nunca descarta en silencio cambios sin commit (E11).

## Cómo se revisa

Escenarios E11 y E18 y pruebas de B17 (cambios sin commit, recuperación aislada).

## Qué permite avanzar

Formato de checkpoint y procedimiento de recuperación aislada aceptados → B11.

## Cerrado en B07

| Pregunta | Resolución |
|---|---|
| ¿Rama o worktree? | **Worktree por defecto** si `git worktree` está disponible (X14); si no, rama. Salvaguardas de undo (X15): no borrar sin confirmar. |
| ¿Commits ↔ tareas? | El metadato del checkpoint guarda ids de tareas/docs; al revertir se lista impacto por esas relaciones (ESP-03). |
| ¿Sin git? | Checkpoints documentales (copia versionada bajo `workflow/checkpoints/`) + aviso: no hay recuperación de código aislada. El propio repo del método ya usa git (P-01 resuelta). |

## Cerrado en B11

| Pregunta | Resolución |
|---|---|
| Comandos | `product_flow.py checkpoint` / `recuperar`; esquema `core/contracts/esquema-checkpoint.json` |
| Demo | `product_flow.py demo-b11` (worktree aislado; trabajo posterior conservado) |

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| Procedimiento de datos en `operacion.md` referenciado por checkpoint | B14 |
