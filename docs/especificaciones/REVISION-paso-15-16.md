# Revisión de los pasos 15–16 — Instalable en cualquier proyecto

Estado: **lista para revisión del usuario** · 2026-10-14  
Meta: que puedas aplicar el método a **cualquier** proyecto, no solo a este repo.

---

## En cristiano

Quieres: abrir la carpeta de la peluquería (o la que sea) y usar el método ahí.

Eso ya se puede así:

1. **Una vez** (instalación global):

```bash
python3 scripts/install_metodo.py install --alcance global --hosts cursor
```

2. **En cualquier proyecto**:

```bash
python3 ~/.cursor/skills/product-flow/scripts/product_flow.py iniciar --proyecto . --idea "…"
```

Y en el chat: skill **product-flow**.

Guía completa: [INSTALL.md](../../INSTALL.md)

---

## Qué hay debajo

| Pieza | Para qué |
|---|---|
| Skill self-contained | `SKILL.md` + scripts + contratos + plantillas en una sola carpeta |
| `--alcance global` | `~/.cursor/skills/product-flow/` → todos tus proyectos |
| `--alcance proyecto` | Solo un repo (útil para equipos) |
| `build-dist` | Genera `skills/product-flow/` para publicar en GitHub |
| `.cursor-plugin/plugin.json` | Empaque para importar el repo como plugin en Cursor |
| Manifiesto SHA-256 | Actualizar/quitar sin borrar lo tuyo |

Demo: `python3 scripts/install_metodo.py demo` (proyecto + global en HOME falso).

---

## Checklist

- [ ] Te encaja instalar **una vez en global** y usarlo en cualquier proyecto  
- [ ] Te encaja también poder instalarlo **solo en un repo**  
- [ ] Te encaja el camino a GitHub (`build-dist` + plugin + INSTALL.md)  
- [ ] Sabes que el Marketplace oficial de Cursor es un paso aparte (revisión de Cursor)

**Respuestas:** `pasos 15-16 ok` / `entrega B ok` · o · `cambiar: …`

---

## Límites honestos

- Publicar en el Marketplace oficial ≠ subir a GitHub; GitHub ya permite clonar/instalar/importar plugin.  
- Ventana localhost no se auto-arranca al instalar.  
- Falta registrar versión de Claude Code en host real (P-02).
