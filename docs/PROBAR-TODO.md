# Encargo: probar todas las funciones del método

Para Grok Bot, un amigo o tú. Una sola corrida. El resultado es el informe de fallos, no la app.

## Identidad (ajusta el Bot una vez)

```
Name: Probador del método
Title: Recorrido completo de product-flow
Description: Usas solo product-flow del repo franciscosdafas133/MDVtP. Simulas al dueño: decides tú. Construyes un producto mínimo que CORRE. El éxito es un informe de cada función (pasó / falló / no existe) con comando y salida. No push. No claves. No pagos reales.
```

## Reglas (Auto-review)

```
Ask first before git push, deleting outside the test folder, paid accounts, login/token/password.
Allow automatically: clone the public repo, folders under ~/mdvtp-pruebas/, python3/bash, reports, install the method into the test project.
```

## Tarea (pega esto en el chat)

```
Resultado
Una sola prueba de recorrido completo. Clona MDVtP (main), instala en la carpeta de prueba, y ejercita CADA función de la lista. Construye desde CERO un producto chico (tú eliges el oficio; no copies e2e viejos). Entrega INFORME.md con tabla función | pasó/falló | comando | nota.

CARPETA: ~/mdvtp-pruebas/recorrido-completo/

Fuentes
- https://github.com/franciscosdafas133/MDVtP — si vacío, PARA.
- Lee INSTALL.md, docs/GUIA-USUARIO.md, docs/LIMITES-CANDIDATA.md, skill product-flow.

Lista obligatoria (marca cada una)
1. install --alcance proyecto
2. iniciar --modo rapido (anota las ASK; si mezclan oficios que no aplican, anótalo)
3. anotar --resuelto en todas las ASK activas
4. continuar → debe pedir requisito, no repetir preguntas
5. requisito (crear) y requisito --id … (editar uno)
6. decidir --aceptar --aprobado-por
7. tarea con --comprobacion
8. dividir (con |REQ-xx por hija si aplica); no debe dejar dividir la tarea de descubrimiento
9. bloquear una pieza con MANUAL_VERIFY_REQUIRED
10. Construir el producto local hasta que corra
11. evidenciar --origen comando --ejecutar SIN --cubre → debe rechazar
12. evidenciar en rojo (sin código o prueba rota) → no vigente
13. evidenciar en verde CON --cubre programa,test → presentar → verificar
14. Cambiar el programa de --cubre; continuar o validador → la evidencia no sigue vigente a ciegas
15. Intentar desbloquear la integración real con frase + --aprobado-por + --sistema → debe rechazar
16. Intentar evidenciar comando en la tarea de integración real → debe rechazar
17. impactar una DEC o REQ y ver que la tarea afectada deja de estar verificada
18. reabrir una DEC y decidir --decision … (si aplica)
19. checkpoint --commit (sin dejar basura sin commit en el repo)
20. operar --uso … con pendientes honestos
21. validate_workflow → OK
22. run_regresion.py en el clone del método → 7/7

Prohibido
No edites JSON del workflow a mano. No copies apps de otras carpetas. No finjas integraciones reales. No push.

Cierre
INFORME.md en la carpeta con: nota 1–5 del método, tabla de la lista, fallos, mejoras.
No me pidas decidir. No me pidas la solución.
```
