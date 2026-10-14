# Cuatro pruebas: formular + construir hasta app que corre

1. En el Bot, deja Identidad y Reglas de [PROMPT-GROK-BOT-FORMULAR.md](PROMPT-GROK-BOT-FORMULAR.md).
2. En cada corrida pega **solo un bloque** de abajo (nivel 1 → 4, uno por uno).
3. Carpetas nuevas: `e2e-v2-nivel-1` … `e2e-v2-nivel-4` (no reuses la oleada anterior).
4. Termina el INFORME de ese nivel antes de pegar el siguiente.

Comportamiento común:
- El método es **formular y construir**. Sin app que corre + prueba en verde = fallaste.
- Eres el dueño. No me preguntes qué elegir.
- Solo MDVtP. Comando que falle → lo anotas; no inventas que pasó.
- `evidenciar --ejecutar`. Rojo = no verificado.
- Tarjeta/pasarela: bloqueada; simulación no desbloquea ni verifica.
- Al final: nota formular + nota construir (1–5) + fallos + mejoras.

**Importante:** el clone debe traer la versión con `--modo rapido`, `requisito`/`tarea`/`decidir` y anti-simulación. Si GitHub está desactualizado respecto a tu repo local, actualiza el remoto **antes** de lanzar al Bot, o indícale una ruta local del método.

---

## Nivel 1 — Dueño de tienda (impaciente)

```
Resultado
Una sola prueba de nivel 1. Formular Y construir: inventario que CORRE + prueba en verde. Dos notas 1–5 (formular / construir) + fallos del método.

NIVEL: 1
NECESIDAD: quiero saber qué productos me quedan en la tienda sin apuntarlo en un cuaderno
CARPETA: ~/mdvtp-pruebas/e2e-v2-nivel-1/

Comportamiento
Eres dueño de tienda de barrio. Quieres algo usable ya. Usa iniciar --modo rapido si existe. Respuestas cortas. Si te abruma con jerga (staging, colas) o 9 preguntas, anótalo como fallo. Alcance: stock + venta que baja stock, QUE FUNCIONE. Sin usuarios, sin pagos, sin nube.

Fuentes
- https://github.com/franciscosdafas133/MDVtP — si el repo está vacío, PARA.
- Lee GUIA-USUARIO, LIMITES-CANDIDATA, core/skills/product-flow/SKILL.md
- Comandos: iniciar, anotar, requisito, tarea, decidir, evidenciar --ejecutar, presentar, verificar, operar, validate_workflow. No edites JSON a mano si el comando existe.

Cierre obligatorio
App que corre + evidenciar --ejecutar en verde + validador OK + operar.
Entrega: ~/mdvtp-pruebas/e2e-v2-nivel-1/INFORME.md
(producto formulado, qué construiste, cómo se prueba, validador, nota formular, nota construir, fallos, mejoras, qué no comprobaste)
No push. No me pidas decidir.
```

---

## Nivel 2 — Dueña de consultorio (privacidad)

```
Resultado
Una sola prueba de nivel 2. Formular Y construir: citas + nota clínica QUE CORREN + prueba en verde. Dos notas 1–5 + fallos del método.

NIVEL: 2
NECESIDAD: quiero que recepción agende citas y el médico vea al paciente, pero la nota clínica solo la ve el médico
CARPETA: ~/mdvtp-pruebas/e2e-v2-nivel-2/

Comportamiento
Eres la dueña. Priorizas privacidad. Si el método no pregunta por datos sensibles / quién NO debe ver la nota, anótalo como hueco grave. No aceptes “no aplica” en roles: tú decides recepción ≠ nota clínica. Alcance: dos roles, citas y nota, QUE FUNCIONEN. Sin historial enorme. Sin pagos.

Fuentes
- https://github.com/franciscosdafas133/MDVtP — si vacío, PARA.
- GUIA-USUARIO + SKILL. requisito/tarea/decidir por comando. evidenciar --ejecutar.

Cierre obligatorio
Prueba que demuestre que recepción NO lee la nota. Validador OK. operar.
Entrega: ~/mdvtp-pruebas/e2e-v2-nivel-2/INFORME.md
No push. No me pidas decidir.
```

---

## Nivel 3 — Dueño de peluquería (idea vaga + cambio de regla)

```
Resultado
Una sola prueba de nivel 3. Formular Y construir: reservas QUE CORREN + prueba en verde. Luego cambias una regla de confirmación, impactar, y vuelves a verificar. Dos notas 1–5 + fallos.

NIVEL: 3
NECESIDAD: que mis clientes reserven en la peluquería sin llamarme
CARPETA: ~/mdvtp-pruebas/e2e-v2-nivel-3/

Comportamiento
Eres el dueño. Partes de esa frase vaga. Si las preguntas son jerga que no entiendes, anótalo. Quieres duración de servicios, horario, reservar sin pisar huecos — y que FUNCIONE. Pago y SMS: “luego” → pendientes en operar, no fingidos. Después de v1 en verde: cambia la regla de confirmación (decidir/reabrir + impactar) y comprueba que la evidencia vieja no siga como verificada a ciegas.

Fuentes
- https://github.com/franciscosdafas133/MDVtP — si vacío, PARA.
- GUIA-USUARIO + SKILL. evidenciar --ejecutar. impactar al cambiar la decisión.

Cierre obligatorio
v1 corre + verde; cambio de regla; impacto visible; v2 re-verificada o en_revision honesta.
Entrega: ~/mdvtp-pruebas/e2e-v2-nivel-3/INFORME.md
No push. No me pidas decidir.
```

---

## Nivel 4 — Dueño de restaurante (tarjeta bloqueada)

```
Resultado
Una sola prueba de nivel 4. Formular Y construir: salón → cocina → caja QUE CORREN + prueba en verde. Tarjeta bloqueada y NO verificada con simulación. Dos notas 1–5 + fallos.

NIVEL: 4
NECESIDAD: que el salón mande la comanda a cocina y la caja cobre, aunque la tarjeta aún no esté lista
CARPETA: ~/mdvtp-pruebas/e2e-v2-nivel-4/

Comportamiento
Eres el dueño. Mesas, comanda, cocina, cuenta QUE FUNCIONEN. Divide con criterio. Bloquea solo tarjeta (marca MANUAL_VERIFY_REQUIRED o equivalente). Efectivo simulado sí se prueba. Si el método desbloquea o verifica tarjeta con una nota de “simulación”, FALLO GRAVE. No inventes Stripe ni claves.

Fuentes
- https://github.com/franciscosdafas133/MDVtP — si vacío, PARA.
- GUIA-USUARIO + SKILL. evidenciar --ejecutar. bloquear/desbloquear honestos.

Cierre obligatorio
Flujo salón-cocina-caja en verde; tarjeta pendiente en operar; validador OK.
Entrega: ~/mdvtp-pruebas/e2e-v2-nivel-4/INFORME.md
No push. No me pidas decidir.
```
