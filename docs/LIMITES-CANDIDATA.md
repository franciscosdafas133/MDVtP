# Límites de la versión candidata 0.1.0-rc1

## Se puede afirmar

- Hay una entrada única (`product-flow`) con scripts y validador.
- Instalación en un proyecto o global, en Cursor y Claude Code.
- De una idea a preguntas en lenguaje llano (`--modo rapido`), requisitos, decisiones y tareas, sin editar JSON a mano.
- Evidencia: `evidenciar --ejecutar` corre la prueba; en rojo no se verifica.
- Un cambio de código deja la evidencia obsoleta y reabre la tarea.
- Dividir, bloquear una pieza y seguir con el resto. El padre de una división se cierra con transiciones legales cuando las hijas están verificadas.
- Integración real (`MANUAL_VERIFY_REQUIRED`): un script local, aunque salga 0, no la desbloquea ni la verifica. Hace falta declarar quién probó el sistema real (`--aprobado-por` y `--sistema`).
- Regresión: `python3 scripts/run_regresion.py`.

## No se puede afirmar (aún)

- Que ya sirva, sin más pruebas, para un producto grande (agente educativo, grafos de conocimiento, LLM).
- Que un extraño haya repetido el nivel 4 después del cierre del mock local (el informe e2e-v3-nivel-4 es de `1c46568`, anterior a ese cierre).
- Marketplace oficial de Cursor.
- Que la ventana HTML se abre sola al instalar.
- Que Git deshace pagos o APIs ya ejecutadas.

## Cómo comprobarlo en otra máquina

```bash
git clone https://github.com/franciscosdafas133/MDVtP.git
cd MDVtP
python3 scripts/run_regresion.py
```

Tiene que terminar en `7/7 → ok`. Uso diario: [GUIA-USUARIO.md](GUIA-USUARIO.md) e [INSTALL.md](../INSTALL.md).
