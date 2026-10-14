# Mantenimiento del método (paso 22)

## Versiones

| Campo | Dónde | Regla |
|---|---|---|
| Versión del paquete | [VERSION](../VERSION) | Semver: `MAYOR.MENOR.PARCHE` + opcional `-rcN` / `-dev` |
| Plugin Cursor | [.cursor-plugin/plugin.json](../.cursor-plugin/plugin.json) | Misma versión que `VERSION` al publicar |
| `contrato_version` en workflows | `core/contracts/` + `estado.json` | Subir **menor** si hay campos nuevos compatibles; **mayor** si rompe workflows viejos |
| Skill instalada | `manifest.json` al instalar | `install` vuelve a copiar; no borra archivos ajenos |

**Al soltar una versión:**

1. Actualizar `VERSION` y `plugin.json`.
2. `python3 scripts/install_metodo.py build-dist`
3. `python3 scripts/run_regresion.py` (debe ser ok).
4. Anotar en el tablero / commit qué cambió y qué límites siguen (ver [LIMITES-CANDIDATA.md](LIMITES-CANDIDATA.md)).

## Migración de un proyecto de usuario

Hoy (0.1.0-rc1):

- Si solo actualizas la skill (`install` de nuevo), el `workflow/` del usuario **se conserva**.
- Si cambia `contrato_version` de forma incompatible: documentar el mapeo aquí y, si hace falta, un script `migrate_workflow.py` (aún no existe — crear cuando haya el primer breaking change).
- Nunca reescribir decisiones/evidencia históricas en silencio.

## Actualizar fuentes de referencia

1. Autoridad de commits: [sources.lock.json](../sources.lock.json).
2. Procedimiento: sparse checkout en `.reference-sources/` (no versionar esa carpeta).
3. Tras actualizar una fuente: ficha en `docs/auditoria/` o nota en [fuentes.md](fuentes.md); revisar [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
4. No copiar código de terceros al núcleo sin licencia y aviso.

## Regresión (mínimo antes de publicar)

```bash
python3 scripts/run_regresion.py
```

Incluye: integridad B17, eval determinista B18, integración B20, `build-dist`, validador `--self-test`.

## Mejora continua

- Fricciones de uso real → apuntes / issues → siguiente `VERSION`.
- Escenarios E01–E18 de observación: repetir en hosts cuando cambie el comportamiento del agente o del host.
