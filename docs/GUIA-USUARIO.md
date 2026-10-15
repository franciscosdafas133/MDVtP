# Guía breve — el método (product-flow)

Versión candidata: ver [VERSION](../VERSION).  
Instalación: [INSTALL.md](../INSTALL.md).  
Límites: [LIMITES-CANDIDATA.md](LIMITES-CANDIDATA.md).  
Probar todo: [PROBAR-TODO.md](PROBAR-TODO.md).  
Mantener / publicar: [MANTENIMIENTO.md](MANTENIMIENTO.md) · [PUBLICAR-GITHUB.md](PUBLICAR-GITHUB.md).

## Para qué sirve

Te guía desde una idea vaga hasta un incremento con documentos, decisiones, pruebas honestas y un plan de entrega. **Tú** decides producto; el agente propone y el validador frena estados ilegales.

## Empezar (una vez)

```bash
# desde este repositorio
python3 scripts/install_metodo.py install --alcance global --hosts cursor,claude
```

En el chat: pide la skill **product-flow** (o `/product-flow`).

## Acciones que más usarás

| Quieres… | Comando |
|---|---|
| Empezar | `iniciar --proyecto . --idea "…" --modo rapido` |
| Retomar | `continuar` |
| Ver dónde estamos | `estado` |
| Apuntar una respuesta | `anotar --enlaza ASK-01 --texto "…" --resuelto` |
| Crear o editar un requisito | `requisito …` / `requisito --id REQ-01 …` |
| Decisión | `decidir --aceptar --aprobado-por …` |
| Tarea | `tarea --comprobacion "bash test.sh" …` |
| Partir una tarea | `dividir` (con criterio; opcional `\|REQ-xx` por hija) |
| Bloquear lo que no está | `bloquear --marca MANUAL_VERIFY_REQUIRED` |
| Probar de verdad | `evidenciar --origen comando --cubre app.py,test.sh --ejecutar` → `presentar` → `verificar` |
| Tras un cambio | `impactar --cambiado REQ-01 --motivo "…"` |
| Guardar partida | `checkpoint --commit` |
| Plan de entrega | `operar --uso "…" --pendientes "…"` |

## Ciclo de código

**Escanear → planificar → evaluar → reemplazar.**  
Luego evidenciar y verificar. No digas “ya está” si la prueba no corrió.

## Reglas cortas

- `--cubre` nombra el programa (y la prueba). Sin eso no hay evidencia de comando.
- Una integración real (`MANUAL_VERIFY_REQUIRED`) se queda pendiente: no se evidencia, no se desbloquea, no se verifica.
- El validador manda: `python3 …/validate_workflow.py workflow`.

## Comprobar el paquete

```bash
python3 scripts/run_regresion.py
```

Tiene que terminar en `7/7 → ok`.
