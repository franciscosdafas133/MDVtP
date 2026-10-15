# Límites de la versión candidata 0.1.0-rc1

## Se puede afirmar

- Hay una entrada única (`product-flow`) con scripts y validador.
- Instalación en un proyecto o global, en Cursor y Claude Code.
- De una idea a preguntas en lenguaje llano (`--modo rapido`), requisitos, decisiones y tareas, sin editar JSON a mano.
- Evidencia: `evidenciar --ejecutar` corre la prueba; hay que nombrar el programa con `--cubre`; en rojo no se verifica.
- Un cambio en un archivo de `--cubre` deja la evidencia obsoleta y reabre la tarea.
- Se puede actualizar un requisito con `requisito --id REQ-01 …` (luego `impactar` si ya había tareas verificadas).
- Dividir, bloquear una pieza y seguir con el resto. El padre de una división se cierra con transiciones legales cuando las hijas están verificadas.
- Integración real (`MANUAL_VERIFY_REQUIRED`): no se evidencia, no se desbloquea ni se verifica. Queda pendiente.
- Regresión: `python3 scripts/run_regresion.py`.

## No se puede afirmar (aún)

- Que varias personas ajenas lo hayan corroborado en sus máquinas.
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
