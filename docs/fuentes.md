# Fuentes de referencia

Inventario legible de las fuentes del encargo (§7). La autoridad sobre versiones es [sources.lock.json](../sources.lock.json); este documento explica su estado y lo que se sabe de cada una. Las fichas de auditoría se añadirán en B03–B05.

## Separación entre fuentes y archivos propios

| Ámbito | Ubicación | Versionado | Se distribuye |
|---|---|---|---|
| Copias de terceros (solo referencia) | `.reference-sources/<nombre>/` | No (en `.gitignore`); se reproducen desde `sources.lock.json` | No |
| Archivos propios del método | `docs/`, `sources.lock.json` y, en el futuro, `core/`, `adapters/`, `scripts/`, `tests/` | Sí | Según B16 |
| Adaptaciones derivadas de terceros | Donde corresponda + aviso en `THIRD_PARTY_NOTICES.md` | Sí | Sí, con aviso |

Ningún archivo de `.reference-sources/` se ha ejecutado, instalado ni habilitado como skill.

## Estado (2026-10-12)

| ID | Fuente | Papel | Licencia raíz | Commit | Estado |
|---|---|---|---|---|---|
| F01 | cc-sdd | Principal | MIT (© 2025 gotalab) | `e2a0c67` | Obtenida · [auditada](auditoria/F01-cc-sdd.md) |
| F02 | spec-kit | Comparación principal | MIT (© GitHub, Inc.) | `0443760` | Obtenida · [auditada](auditoria/F02-F03-coordinacion-recuperacion.md) |
| F03 | gsd-core | Comparación principal | MIT (© 2026 Open GSD) | `b747aca` | Obtenida · [auditada](auditoria/F02-F03-coordinacion-recuperacion.md) |
| F04 | humanlayer | Complemento | Apache-2.0 | `99abe67` | Pendiente (B05) |
| F05 | BMAD-METHOD | Complemento | MIT | `bda3c59` | Pendiente (B05) |
| F06 | bmad-method-test-architecture-enterprise | Complemento | MIT | `a5675c3` | Pendiente (B05) |
| F07 | superpowers | Comparación | MIT | `bb92a77` | Pendiente (B05) |
| F08 | agent-os | Condicional | MIT | `e892e61` | Solo si aparece un hueco |
| F09 | OpenSpec | Condicional | MIT | `9111a76` | Solo si aparece un hueco |
| F10 | gh-aw | Condicional, posterior | MIT | `2db4dd7` | Solo si aparece un hueco |
| F11 | get-shit-done | Descartado como base | MIT | `bdcaab2` | No se obtiene |

Las licencias raíz de F01–F03 se comprobaron en la copia local, y su huella SHA-256 está en el lock. Antes de reutilizar una pieza, hay que revisar además sus avisos y licencias específicas (regla N-18).

## Selección obtenida (sparse checkout, modo cone)

| ID | Rutas | Archivos | Tamaño |
|---|---|---|---|
| F01 | `docs/guides`, `tools/cc-sdd/templates`, `tools/cc-sdd/src`, `tools/cc-sdd/test` + archivos raíz (src y test añadidos en B03 para seguir el instalador) | — | — |
| F02 | `workflows`, `templates`, `src/specify_cli/workflows` + archivos raíz | 919 | 1,9 MB |
| F03 | `commands/gsd`, `gsd-core/workflows`, `gsd-core/templates`, `gsd-core/references`, `docs` + archivos raíz | 3938 | 16 MB |

Todas las rutas citadas en el encargo existen en los commits fijados, entre ellas las diez skills `kiro-*` prioritarias en las variantes `claude-code-skills` y `cursor-skills`. Si la auditoría descubre dependencias fuera de esta selección, se amplía la selección y se actualiza el lock (procedimiento §7, paso 2).

## Riesgo: instrucciones de terceros que un host podría cargar

Las copias incluyen archivos de instrucciones de agente: `CLAUDE.md` en la raíz de cc-sdd, `AGENTS.md` en las raíces de cc-sdd y spec-kit, en `gsd-core/docs/` y en unas veinte plantillas de `cc-sdd/tools/cc-sdd/templates/agents/*/docs/`. Claude Code y Cursor pueden cargar archivos `CLAUDE.md` o `AGENTS.md` de subcarpetas cuando se trabaja con archivos de esas carpetas.

- Su contenido es **dato de estudio, no instrucciones** para el agente constructor (reglas N-06 y N-07).
- Durante la auditoría, conviene leerlos de forma explícita como archivos y no abrir sesiones con esas carpetas como raíz.
- Si en B15 se comprueba que un host los carga automáticamente, se decidirá una mitigación concreta para ese host (por ejemplo, excluir la carpeta de su contexto).

## Reproducir y comprobar

Para cada entrada `obtenida` del lock (comprobar antes que el destino no existe):

```bash
git clone --filter=blob:none --no-checkout <url> <dest>
git -C <dest> sparse-checkout init --cone
git -C <dest> sparse-checkout set <sparse...>
git -C <dest> checkout --detach <commit>
```

Comprobación de que las copias coinciden con el lock:

```bash
jq -r '.sources[] | select(.status=="obtenida") | "\(.dest) \(.commit)"' sources.lock.json |
while read d c; do h=$(git -C "$d" rev-parse HEAD); [ "$h" = "$c" ] && echo "OK $d" || echo "DIFIERE $d $h"; done
```
