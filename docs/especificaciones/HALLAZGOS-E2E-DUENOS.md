# Hallazgos e2e (mejorar, no reinventar)

## Oleada A — dueños formular (b0d336d)

Notas formular: 2 / 2 / 2 / 3. Apps OK; método flojo al formular.  
Fallo grave: desbloquear/verificar tarjeta con simulación.

## Oleada B — CLI niveles 1–5 + INFORME-METODO (b0d336d)

Veredicto del probador: útil con huecos. Documental bien; promesa de pruebas honestas rota (evidencia texto libre; `siguiente_preparada`; `recuperar` worktree; `impactar` TASK/DEC).

## Oleada D — e2e-v3-nivel-1 lavandería (a8885a3)

Formular **4/5**, construir **4/5**. Modo rápido, continuar→requisito, `--ejecutar`, huellas, impactar DEC: OK.  
Huecos: `python3 -c pass` aún verificaba; stale solo avisaba; sin pistas lavandería; operar sin «cómo se usa».

**Tras el informe (local):** comando debe alinear con `--comprobacion`; `python -c pass` rechazado; `continuar` marca stale; pistas lavandería/academia/hostal; `operar --uso`.

## Oleada C — e2e-v2-nivel-1 (95f38ae en GitHub)

Comparado con b0d336d:

| Antes | En 95f38ae |
|---|---|
| Sin `requisito` / `tarea` / `decidir` | Arreglado (0 JSON a mano) |
| Sin `--ejecutar` | Arreglado (rojo no cierra) |
| `siguiente_preparada` en FALLA | No apareció en nivel 1 |
| Formular 2/5 | Sigue 2/5 (9 ASK + jerga; sin `--modo rapido` en ese commit) |
| Construir | 4/5; aún: `true` / manual cierran |

**Importante:** las mejoras de formular (modo rápido, pistas, anti-simulación, `continuar` tras ASK, `impactar` DEC) están en el **árbol de trabajo local**, no en el commit `95f38ae` que clonó el Bot. Hay que publicarlas para la siguiente oleada.

## Prioridad tras oleada C

| # | Hallazgo | Estado |
|---|---|---|
| 1 | Publicar modo rápido + pistas + anti-sim + impactar DEC | Local OK → falta commit/push |
| 2 | Rechazar `evidenciar true` y manual si hay comprobación | Hecho en local (esta oleada) |
| 3 | Guardar hashes de `--cubre` y que el validador los recalcule | Hecho en local |
| 4 | Orden de campos en `decidir` | Hecho en local |
| 5 | `continuar` tras ASK → requisito | Local OK → falta publicar |
| 6 | Proponer REQ desde respuestas (agente/skill) | Pendiente |
| 7 | Sección «Cómo se usa» en operar | Pendiente barato |

## Qué no tocar

Entrada única, puertas, evidencia, validador, operar honesto. Afinar, no otro método.
