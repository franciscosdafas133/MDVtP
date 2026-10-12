# ESP-06 — Contrato de recuperación

Estado: borrador 0.1 · Fuente: encargo §5 · Requisitos: R12, R13, R18

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

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿Rama o worktree por defecto? ¿Qué toma de `using-git-worktrees` (F07) y de `undo` de GSD Core (F03)? | B04, B05 |
| ¿Cómo se relacionan commits con tareas para analizar dependencias al revertir? | B04 (F03 relaciona commits y dependencias) |
| ¿Qué hacer en proyectos sin git? Hoy la propia carpeta de construcción no lo es (P-01 del tablero). | B07 |
| ¿Cómo se describe el procedimiento de datos de `operacion.md` para que el checkpoint lo referencie? | B14 |
