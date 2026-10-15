---
name: product-flow
description: >-
  Única entrada del método: inicia o continúa el flujo de producto (documentación,
  decisiones, estado). Usar cuando el usuario quiera empezar un producto, seguir,
  ver estado, decidir, anotar, verificar o recuperar. No pedir que elija otras skills.
---

# product-flow

Eres el coordinador del método. El usuario **no** elige skills auxiliares: tú enrutas.

## Acciones

| Acción | Cuándo |
|---|---|
| iniciar | Idea nueva o proyecto sin `workflow/` |
| continuar | Retomar desde archivos |
| estado | Qué hay / qué falta / qué bloquea |
| decidir | Registrar aceptación (`--aceptar --aprobado-por`) |
| anotar | Apunte enlazado (no es decisión) |
| reabrir | Sustituir una decisión aceptada |
| requisito / tarea | Crear REQ o TASK sin editar JSON a mano |
| impactar | Tras cambiar REQ/DEC/TASK: invalidar dependientes |
| checkpoint | Guardar partida (metadatos + snapshot / commit) |
| recuperar | Worktree/rama aislada desde un CP |
| dividir | Partir tarea gorda (con criterio; cadena/paralelo) |
| bloquear / desbloquear | Bloqueo parcial; el resto puede seguir |
| evidenciar / presentar / verificar | Cerrar solo si la prueba se ejecutó y salió 0 (`evidenciar --ejecutar --cubre programa,test`) |
| requisito | Crear REQ; actualizar con `--id REQ-01` |
| depurar | Intentos acotados; a la 3.ª pregunta al usuario |
| operar / entregar | Plan de entrega + pendientes reales (R18) |
| recorrido-simple | Demo automática de un producto mínimo (playbook para otros agentes) |

**Ciclo de cambio de código (obligatorio):** escanear → planificar → evaluar → reemplazar/aplicar. Luego evidenciar y verificar.

## Mecánica (obligatoria)

1. Escribe/lee en `workflow/` del **proyecto del usuario** (no en el repo del método salvo demos).
2. Los scripts viven en `scripts/` del repo del método. Si la skill está instalada, están en la carpeta `scripts/` junto a este archivo. Antes de avanzar tareas o marcar verificado, ejecuta:

```bash
python3 <ruta-del-método>/scripts/validate_workflow.py <proyecto>/workflow
```

Si falla, repara o pregunta; no ignores el validador.
3. Para crear el esqueleto desde una idea:

```bash
python3 <ruta-del-método>/scripts/product_flow.py iniciar --proyecto <proyecto> --idea "…"
python3 <ruta-del-método>/scripts/product_flow.py iniciar --proyecto <proyecto> --idea "…" --modo rapido
```

Preguntas en lenguaje llano; `--modo rapido` deja 3 ASK. Añade pistas según el tipo de negocio (citas, consultorio, restaurante, tienda). Cuando las ASK activas ya tienen apunte, `continuar` pide pasar a `requisito`, no repetir preguntas.

4. Estado / continuar (continuar contrasta validador + apuntes + git):

```bash
python3 <ruta-del-método>/scripts/product_flow.py estado --proyecto <proyecto>
python3 <ruta-del-método>/scripts/product_flow.py continuar --proyecto <proyecto>
```

5. Anotar, impactar, checkpoint, recuperar:

```bash
python3 <ruta-del-método>/scripts/product_flow.py anotar --proyecto <proyecto> --enlaza ASK-03 --texto "…"
python3 <ruta-del-método>/scripts/product_flow.py impactar --proyecto <proyecto> --cambiado REQ-01 --motivo "…"
python3 <ruta-del-método>/scripts/product_flow.py checkpoint --proyecto <proyecto> --nombre "…" --alcance "…" --commit
python3 <ruta-del-método>/scripts/product_flow.py recuperar --proyecto <proyecto> --checkpoint CP-01
```

6. **Ventana de docs (DEC-02):** si el servidor standalone del método está disponible, ábrelo/apúntalo (`http://127.0.0.1:8765/`). El chat no es el único sitio para editar docs.
7. Cada apertura/cierre de actividad usa el informe fijo (ver `procedures/informe.md`).
8. Idea vaga → preguntas por áreas. Registra ASK; no inventes requisitos confirmados.
9. Tú propones; el **usuario** acepta puertas de producto. El validador bloquea estados ilegales.
10. Si cambia un requisito o decisión ya enlazada → `impactar` antes de seguir como si nada.
11. Al entregar / operar:

```bash
python3 <ruta-del-método>/scripts/product_flow.py operar \
  --proyecto <proyecto> \
  --resumen "…" \
  --pendientes "…; …"
```

## Procedimientos

Lee solo el procedimiento de la acción en curso bajo `procedures/`.
