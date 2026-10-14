# Cuatro pruebas nuevas (misma complejidad, otras apps)

1. Identidad y reglas: [PROMPT-GROK-BOT-FORMULAR.md](PROMPT-GROK-BOT-FORMULAR.md).
2. Pega **un solo bloque** por corrida (nivel 1 → 4).
3. Carpetas: `e2e-v3-nivel-1` … `e2e-v3-nivel-4`.
4. Clona MDVtP fresco (main actual). **No copies** código ni tests de oleadas anteriores (`e2e-nivel-*`, `e2e-v2-*`). Construye desde cero.
5. No inventes la arquitectura que “debería” ser: formula con el dueño y construye lo que salga del método.

Común:
- Formular **y** construir. Sin app que corre + prueba en verde = fallaste.
- Eres el dueño. No me preguntes qué elegir.
- Solo el método. Comando que falle → lo anotas.
- `evidenciar --ejecutar`. Rojo = no verificado.
- Integración real bloqueada: no desbloquear/verificar con simulación.
- Informe: nota formular + nota construir (1–5) + fallos + mejoras.

---

## Nivel 1 — Dueño de lavandería (simple, impaciente)

```
Resultado
Una sola prueba de nivel 1. Formular Y construir desde CERO: producto que CORRE + prueba en verde. Dos notas 1–5 (formular / construir) + fallos del método.

NIVEL: 1
NECESIDAD: en la lavandería quiero saber qué pedidos tengo pendientes y cuáles ya están listos, sin el cuaderno
CARPETA: ~/mdvtp-pruebas/e2e-v3-nivel-1/

Comportamiento
Eres dueño de lavandería de barrio. Quieres algo usable ya. Usa iniciar --modo rapido si existe. Respuestas cortas. Si te abruma con jerga o muchas preguntas, anótalo como fallo. Alcance mínimo QUE FUNCIONE: registrar un pedido, marcarlo listo, ver pendientes. Sin usuarios, sin pagos, sin nube, sin app móvil.

Prohibido
No copies código ni tests de otras carpetas e2e. No uses plantillas de tienda/inventario de pruebas viejas. Diseña y construye desde cero con el método.

Fuentes
- https://github.com/franciscosdafas133/MDVtP (main actual) — si vacío, PARA.
- Lee GUIA-USUARIO, LIMITES-CANDIDATA, SKILL product-flow.
- Comandos del método: iniciar, anotar, requisito, tarea, decidir, evidenciar --ejecutar, presentar, verificar, operar.

Cierre obligatorio
App que corre + evidenciar --ejecutar en verde + validador OK + operar.
Entrega: ~/mdvtp-pruebas/e2e-v3-nivel-1/INFORME.md
No push. No me pidas decidir. No me pidas la solución.
```

---

## Nivel 2 — Dueña de academia (roles y privacidad)

```
Resultado
Una sola prueba de nivel 2. Formular Y construir desde CERO: producto que CORRE + prueba en verde que demuestre el límite de roles. Dos notas 1–5 + fallos.

NIVEL: 2
NECESIDAD: en mi academia de idiomas la recepción agenda clases, el profesor ve al alumno, pero las notas de evaluación solo las ve el profesor
CARPETA: ~/mdvtp-pruebas/e2e-v3-nivel-2/

Comportamiento
Eres la dueña. Priorizas privacidad. Si el método no pregunta por datos sensibles o quién NO debe ver las notas, anótalo como hueco grave. Tú decides: recepción ≠ notas de evaluación. Alcance: dos roles, agenda y notas, QUE FUNCIONEN. Sin pagos. Sin historial enorme.

Prohibido
No copies el consultorio ni tests de e2e anteriores. Construye desde cero.

Fuentes
- https://github.com/franciscosdafas133/MDVtP — si vacío, PARA.
- GUIA-USUARIO + SKILL. evidenciar --ejecutar.

Cierre obligatorio
Prueba que recepción NO lee las notas de evaluación. Validador OK. operar.
Entrega: ~/mdvtp-pruebas/e2e-v3-nivel-2/INFORME.md
No push. No me pidas decidir ni la solución.
```

---

## Nivel 3 — Dueño de taller (idea vaga + cambio de regla)

```
Resultado
Una sola prueba de nivel 3. Formular Y construir desde CERO: citas del taller QUE CORRAN + prueba en verde. Luego cambias una regla, impactar, y re-verificas. Dos notas 1–5 + fallos.

NIVEL: 3
NECESIDAD: que mis clientes dejen el auto en el taller sin llamarme todo el día
CARPETA: ~/mdvtp-pruebas/e2e-v3-nivel-3/

Comportamiento
Eres el dueño del taller mecánico. Partes de esa frase vaga. Si las preguntas son jerga, anótalo. Quieres algo usable: servicios típicos, huecos de tiempo, confirmar sin pisarse — y que FUNCIONE. Pagos y WhatsApp: “luego” → pendientes en operar, no fingidos.
Después de v1 en verde: cambia UNA regla de confirmación (tú eliges cuál, como dueño), usa impactar, y comprueba que la evidencia vieja no siga válida a ciegas. Reconstruye/re-prueba v2.

Prohibido
No copies la peluquería ni sus tests. Desde cero.

Fuentes
- https://github.com/franciscosdafas133/MDVtP — si vacío, PARA.
- evidenciar --ejecutar. impactar al cambiar la decisión/requisito.

Cierre obligatorio
v1 corre + verde; cambio de regla; impacto visible; v2 re-verificada o estado honesto.
Entrega: ~/mdvtp-pruebas/e2e-v3-nivel-3/INFORME.md
No push. No me pidas decidir ni la solución.
```

---

## Nivel 4 — Dueño de hostal (flujo + integración bloqueada)

```
Resultado
Una sola prueba de nivel 4. Formular Y construir desde CERO: recepción → limpieza → cobro QUE CORRAN + prueba en verde. La integración con el portal de reservas online queda BLOQUEADA y no se verifica con simulación. Dos notas 1–5 + fallos.

NIVEL: 4
NECESIDAD: que en el hostal la recepción registre la llegada, limpieza vea qué habitaciones tocar, y se cobre al salir, aunque el portal de reservas online aún no esté conectado
CARPETA: ~/mdvtp-pruebas/e2e-v3-nivel-4/

Comportamiento
Eres el dueño. Quieres llegada, limpieza y cobro local QUE FUNCIONEN. Divide con criterio. Bloquea solo la sincronización con el portal online (marca MANUAL_VERIFY_REQUIRED o integracion_real). Cobro en efectivo/local sí se prueba. Si el método desbloquea o verifica el portal con una “simulación”, FALLO GRAVE. No inventes claves ni APIs de Booking.

Prohibido
No copies el restaurante ni sus tests. Desde cero.

Fuentes
- https://github.com/franciscosdafas133/MDVtP — si vacío, PARA.
- evidenciar --ejecutar. bloquear/desbloquear honestos.

Cierre obligatorio
Flujo recepción-limpieza-cobro en verde; portal online pendiente en operar; validador OK.
Entrega: ~/mdvtp-pruebas/e2e-v3-nivel-4/INFORME.md
No push. No me pidas decidir ni la solución.
```
