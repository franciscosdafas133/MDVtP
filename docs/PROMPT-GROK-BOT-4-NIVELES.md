# Cuatro pruebas: formular + construir (una por nivel)

Usa el mismo Bot **Formulador del método** (identidad y reglas de [PROMPT-GROK-BOT-FORMULAR.md](PROMPT-GROK-BOT-FORMULAR.md)).

En cada prueba pega **solo un bloque de Tarea**. Termina y guarda el informe antes de pasar al siguiente nivel. Carpetas distintas: `e2e-nivel-1` … `e2e-nivel-4`.

Comportamiento común (siempre):
- El método no es solo formular: es **formular y construir** (docs → decisiones → código → prueba real → operar). Si te quedas en papeles sin producto que corra, fallaste la prueba.
- Eres el dueño del producto. No me preguntes qué elegir.
- Usas solo el método (repo MDVtP). Si el comando falla, anotas fallo; no inventas que pasó.
- `evidenciar --ejecutar`. Prueba en rojo = no verificado.
- Al final: **dos notas 1–5** (formular / construir) + fallos y mejoras del método.

---

## Nivel 1 — Dueño de tienda de barrio (simple, poco paciente)

**Comportamiento que asumes:** Dueño de una tienda pequeña. Quieres algo ya. No lees manuales largos. Si el método te pide 9 preguntas, contestas corto o “no aplica”, y te molestas si no te deja avanzar. No inventas un ERP.

```
Resultado
Una sola prueba de nivel 1. El método es formular Y construir: sales con producto que corre y prueba en verde, no solo docs. Al final dos notas 1–5 (formular / construir) + fallos del método.

NIVEL: 1
NECESIDAD: quiero saber qué productos me quedan en la tienda sin apuntarlo en un cuaderno
CARPETA: ~/mdvtp-pruebas/e2e-nivel-1/

Comportamiento
Eres el dueño de una tienda de barrio. Quieres algo usable ya. Respuestas cortas a las ASK. Si el método se pone pesado, lo anotas como fallo. Alcance: una pantalla o flujo mínimo de inventario (stock, venta baja stock) QUE FUNCIONE. Sin usuarios, sin pagos, sin nube.

Fuentes: https://github.com/franciscosdafas133/MDVtP — si el repo está vacío, PARA.
Lee GUIA-USUARIO y SKILL. Construye, evidenciar --ejecutar, presentar, verificar, operar.

Entrega: ~/mdvtp-pruebas/e2e-nivel-1/INFORME.md
(producto formulado, qué construiste, prueba/validador, nota formular, nota construir, fallos, mejoras)
No push. No me pidas decidir.
```

---

## Nivel 2 — Dueña de consulta (cuidadosa con privacidad)

**Comportamiento que asumes:** Dueña de un consultorio. Te importa quién ve qué. No aceptas que recepción lea la nota clínica. Prefieres preguntar bien antes de construir de más.

```
Resultado
Una sola prueba de nivel 2. El método es formular Y construir: producto que corre + prueba en verde. Dos notas 1–5 (formular / construir) + fallos del método.

NIVEL: 2
NECESIDAD: quiero que recepción agende citas y el médico vea al paciente, pero la nota clínica solo la ve el médico
CARPETA: ~/mdvtp-pruebas/e2e-nivel-2/

Comportamiento
Eres la dueña del consultorio. Priorizas privacidad. Si el método no te fuerza a decidir roles y datos sensibles, anótalo como hueco. Alcance: dos roles, citas y nota clínica QUE FUNCIONEN. Sin historial enorme. Sin pagos.

Fuentes: https://github.com/franciscosdafas133/MDVtP — si el repo está vacío, PARA.
Lee GUIA-USUARIO y SKILL. Construye, evidenciar --ejecutar, presentar, verificar, operar.

Entrega: ~/mdvtp-pruebas/e2e-nivel-2/INFORME.md
No push. No me pidas decidir.
```

---

## Nivel 3 — Dueño de peluquería (la idea vaga clásica)

**Comportamiento que asumes:** Dueño de peluquería. Empezaste con una frase vaga. No eres técnico. Aceptas un piloto local. Si te piden tarjeta o SMS, dices “luego” y el método debe dejarlo pendiente, no fingirlo.

```
Resultado
Una sola prueba de nivel 3. El método es formular Y construir: reservas que corren + prueba en verde. Dos notas 1–5 (formular / construir) + fallos del método.

NIVEL: 3
NECESIDAD: que mis clientes reserven en la peluquería sin llamarme
CARPETA: ~/mdvtp-pruebas/e2e-nivel-3/

Comportamiento
Eres el dueño de la peluquería. Partes de esa frase vaga. Respondes las ASK como dueño. Quieres servicios, hora, confirmar, sin pisar huecos — y que eso FUNCIONE. Pago y SMS: “luego” → pendientes en operar. Si cambias una regla de confirmación, impactar y volver a verificar.

Fuentes: https://github.com/franciscosdafas133/MDVtP — si el repo está vacío, PARA.
Lee GUIA-USUARIO y SKILL. Construye, evidenciar --ejecutar, presentar, verificar, operar.

Entrega: ~/mdvtp-pruebas/e2e-nivel-3/INFORME.md
No push. No me pidas decidir.
```

---

## Nivel 4 — Dueño de restaurante (operación con hueco real)

**Comportamiento que asumes:** Dueño de restaurante. Quieres salón → cocina → cuenta. Sabes que la tarjeta no está lista: no dejas que el método diga “cobrado con tarjeta”. Exiges bloqueo parcial: el resto sigue.

```
Resultado
Una sola prueba de nivel 4. El método es formular Y construir: salón/cocina/caja que corren + prueba en verde. Dos notas 1–5 (formular / construir) + fallos del método.

NIVEL: 4
NECESIDAD: que el salón mande la comanda a cocina y la caja cobre, aunque la tarjeta aún no esté lista
CARPETA: ~/mdvtp-pruebas/e2e-nivel-4/

Comportamiento
Eres el dueño del restaurante. Quieres mesas, comanda, cocina y cuenta QUE FUNCIONEN. Divide con criterio. Bloquea solo tarjeta. Efectivo simulado sí se prueba. Si el método no distingue simulación vs real, fallo grave. No inventes Stripe.

Fuentes: https://github.com/franciscosdafas133/MDVtP — si el repo está vacío, PARA.
Lee GUIA-USUARIO y SKILL. Construye, evidenciar --ejecutar, presentar, verificar, operar (tarjeta pendiente).

Entrega: ~/mdvtp-pruebas/e2e-nivel-4/INFORME.md
No push. No me pidas decidir.
```
