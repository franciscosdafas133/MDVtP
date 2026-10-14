# ESP-07 — Contrato de hosts e instalación

Estado: borrador 0.3 · Fuente: encargo §5, §6 · Decisiones: DEC-02, DEC-06, DEC-08 · Prototipo: B15/B16 · Requisitos: R01, R16, R20

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

## Cerrado en B07

| Pregunta | Resolución |
|---|---|
| ¿Forma de entrega? | DEC-06: **skill/paquete instalable** en el proyecto; experiencia “descargar e iniciar en Cursor”. |
| ¿Ventana? | DEC-02: al iniciar la skill, levantar/usar servidor local HTML (patrón I-01). |
| ¿Runtime instalador + ventana + validador? | **Python 3** stdlib. |
| ¿Manifiesto? | JSON con ruta relativa + SHA-256 + versión del paquete; retirada según DEC-06. |
| ¿Avisos? | `THIRD_PARTY_NOTICES.md` (DEC-08). |
| ¿Deriva cc-sdd entre hosts? | Un solo núcleo; adaptadores solo metadatos/rutas (hallazgo H4). |

## Cerrado en B15/B16 (1.ª parte)

| Pregunta | Resolución |
|---|---|
| Instalador | `scripts/install_metodo.py` (`--alcance global\|proyecto`, status, uninstall, build-dist, demo) |
| Dónde | Skill **self-contained** en `~/.cursor/skills/product-flow` (global) o `.cursor/skills/` (proyecto); igual Claude |
| Publicación | `skills/product-flow/` + `.cursor-plugin/plugin.json` + [INSTALL.md](../../INSTALL.md) |
| Manifiesto | SHA-256; conflictos sin `--fuerza`; retirada solo de lo propio |
| Adaptadores | `adapters/cursor/`, `adapters/claude-code/` |
| Demo | `install_metodo.py demo` OK (proyecto + HOME fake) |

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿Cursor carga también `.claude/skills/`? | Probar en host real (B19); por eso una sola skill activa por host que uses |
| Arranque automático de ventana localhost al usar la skill | Enlace fino post-instalación / uso |
| Migraciones entre versiones del paquete | R20 / B22 |
| Versión Claude Code registrada | P-02 / B19 |
