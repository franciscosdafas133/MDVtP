# ESP-07 — Contrato de hosts e instalación

Estado: borrador 0.1 · Fuente: encargo §5, §6 · Requisitos: R01, R16, R20

## Qué la inicia

Instalar, actualizar o retirar el paquete en un proyecto, o cargarlo en un host.

## Qué produce

- Una única copia activa del núcleo por host, en la ubicación de skills de ese host.
- Un manifiesto de archivos instalados que permite detectar conflictos y retirar solo lo propio.
- El registro de versiones de host y de las superficies usadas (R01).

## Fijado por el encargo

**Organización del repositorio del paquete (§5):** `core/skills/product-flow/`, `core/templates/`, `core/contracts/`, `adapters/claude-code/`, `adapters/cursor/`, `scripts/`, `tests/fixtures/`, `tests/scenarios/`, `THIRD_PARTY_NOTICES.md`; `.reference-sources/` excluido del paquete distribuido. La forma interna exacta se resuelve en B07.

**Compatibilidad confirmada por la documentación oficial (§6):** ambos hosts admiten `SKILL.md` con recursos auxiliares. Claude Code: skills de proyecto en `.claude/skills/`. Cursor: `.cursor/skills/` y otras ubicaciones compatibles. Las funciones adicionales y la carga no son idénticas.

**Reglas:**

- Núcleo canónico con `name` y `description`; un instalador que materializa una sola copia activa por host. Evitar que Cursor descubra dos copias a la vez.
- Metadatos exclusivos, hooks, agentes secundarios e importación de archivos se resuelven en los adaptadores; no se suponen portables.
- Debe existir un modo secuencial funcional.
- El instalador instala solo archivos del paquete, detecta conflictos y permite retirar sus archivos sin eliminar los del usuario (R16). Una instalación repetida no duplica la carga (E14).
- Una instalación correcta no demuestra una ejecución correcta.
- Antes de publicar compatibilidad, probar los dos hosts reales y registrar sus versiones; si falta alguno, declararlo pendiente.
- Cada versión registra los cambios de contrato y cómo migrar proyectos de la anterior (R20, E16).

**Entorno conocido (B01):** Cursor 3.22.12 disponible por CLI. Claude Code en uso como extensión de VS Code, versión sin registrar.

## Cómo se revisa

B16 (instalación en una carpeta de prueba, conflictos y retirada), E13, E14, E16 y B19 en los hosts reales.

## Qué permite avanzar

Ubicaciones, manifiesto y diferencias de host comprobadas → B15 y B16.

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿Qué diferencias reales hay entre las variantes `claude-code-skills` y `cursor-skills` de cc-sdd? | B03 |
| ¿Qué ubicaciones de compatibilidad escanea Cursor? ¿Puede descubrir también `.claude/skills/`? | B03, B15 (comprobar en el host real) |
| ¿Cómo se implementa la entrada `/product-flow` en cada host: skill invocable, comando o regla? | B15 |
| ¿Formato del manifiesto y del registro de migraciones? | B07, B16 |
| ¿Runtime del instalador según el entorno confirmado? | B07 |
