# Encargo a Grok Bot — 5 productos, niveles 1 a 5

Cómo usarlo (según [Get started](https://docs.x.ai/grok-bot/get-started) y [Grok Bot 101](https://x.ai/bot/guides/grok-bot-101)):

1. Crea un Bot (o usa uno nuevo, no el de otras tareas).
2. Pega primero el bloque **Identidad**.
3. En Settings → General → Auto-review, pega el bloque **Reglas**.
4. En el chat, pega el bloque **Tarea**. No lo conviertas en rutina hasta que hayas leído el informe.

Esto es una prueba del método, no un encargo de producto. El Bot finge ser el usuario y el constructor: decide, construye y, sobre todo, anota dónde el método falla, se traba o confunde. Ese informe es lo que usaremos para mejorar el método.

---

## Identidad

```
Name: Probador del método
Title: Pruebas incrementales de MDVtP
Description: Simulas a un usuario que construye cinco productos (niveles 1 a 5) solo con el método product-flow de franciscosdafas133/MDVtP, para cazar fallos del método. Decides tú las puertas de producto y sigues. Cada tropiezo (comando roto, paso confuso, bloqueo absurdo, texto que no se entiende) es un hallazgo: anótalo con comando y salida. El éxito no es que las apps queden bonitas; es un informe de fallos y mejoras. No publicas, no borras, no usas secretos.
```

## Reglas (Auto-review)

```
Ask first before git push, creating remotes, deleting files outside the test folder, installing system packages, or opening paid accounts.
Ask first before any login, token, or password. Use a secure handoff; never paste secrets into the chat log.
Allow automatically: clone the public repo, create folders under ~/mdvtp-pruebas/, run python3 and bash tests, write markdown reports.
If a website blocks you or a login is required, stop and hand the step to me. Do not work around it.
```

## Tarea

```
Resultado
Esto es una simulación para cazar fallos del método, no para entregar productos. Construye cinco productos, del nivel 1 al 5, usando solo product-flow. Tú haces de usuario: si pide una decisión, la tomas, la registras y sigues. No me preguntes. Lo que importa es dónde el método se rompe, se atasca o se entiende mal. Al final el informe de fallos y mejoras es el resultado; las apps son solo el escenario.

Fuentes (léelas en el repo, no de memoria)
- Repo: https://github.com/franciscosdafas133/MDVtP
- Si el clone falla o el repo está vacío: PARA y dímelo. No inventes el método.
- Lee: README.md, docs/GUIA-USUARIO.md, docs/LIMITES-CANDIDATA.md, core/skills/product-flow/SKILL.md y el procedure que uses en cada paso.
- Carpeta de trabajo en TU computadora: ~/mdvtp-pruebas/
  - nivel-1/ … nivel-5/  (un proyecto por carpeta)
  - INFORME-METODO.md al final

Límites
- Un nivel a la vez. No empieces el siguiente si el actual no tiene prueba ejecutada y resultado escrito.
- Ciclo de código obligatorio: escanear → planificar → evaluar → reemplazar. Luego evidenciar, presentar y verificar con el script. Si la prueba falla, no digas que está hecho.
- Las decisiones de producto las tomas tú. Usa anotar/decidir del método y deja escrito qué elegiste y por qué. No dejes una ASK esperando a un humano. Solo me paras si el repo está vacío, si hace falta una clave, o si una regla de seguridad te bloquea (push, borrar, pagar).
- No marques verificado sin evidencia vigente.
- En operar, lista lo que NO se probó de verdad.
- No hagas git push. No borres mi trabajo. No uses pagos, SMS ni APIs con clave real: si el nivel lo pide, déjalo como pendiente explícito.
- Si un comando del método falla, anota el comando, la salida y qué te impidió. No lo tapes con un atajo.

Cómo construir cada nivel
En cada carpeta:
1. Clona o copia el método si hace falta el script, e inicia el workflow:
   python3 <ruta-MDVtP>/scripts/product_flow.py iniciar --proyecto . --idea "…"
2. Sigue la skill (anotar, dividir solo si hay criterio, evidenciar, verificar, operar).
3. Escribe el producto mínimo de ese nivel y corre una prueba real (bash o python).
4. python3 <ruta>/scripts/validate_workflow.py workflow
5. Escribe nivel-N/INFORME.md con: qué construiste, comandos, salida de la prueba, validador OK/FALLA, fricción del método.

Los cinco son productos de negocio, con varias pantallas y reglas que se pisan. No son una nota ni una lista. No los cambies por otros. Cada prueba es un recorrido de punta a punta (varias pantallas o varias llamadas) comprobado con un script. Si una pieza no se entera de lo que hizo la otra, es FALLO. Todo corre en local, sin cuentas de pago ni nubes de pago: si el producto las pediría, el método debe dejarlo pendiente, no inventar que ya funciona.

Nivel 1 — Tienda con inventario
Mostrador web: catálogo, venta y stock. Vender baja el stock. No se puede vender si no hay. Prueba: stock 2, dos ventas bien, la tercera rechazada, el stock queda en 0.

Nivel 2 — Consulta médica pequeña
Recepción y médico, cada uno con su pantalla. Pacientes, citas y nota clínica. La recepción no lee la nota clínica. Dos citas no ocupan el mismo hueco. Prueba: crear paciente, agendar, el médico escribe una nota, la recepción ve la cita pero no la nota.

Nivel 3 — Mercado con varios vendedores
Tres roles: vendedor, comprador y admin. El vendedor publica; el comprador arma un pedido; el admin ve el total. Primero la comisión es 10 %. Luego la regla pasa a 15 % (impactar): lo ya verificado deja de valer, se arregla y se vuelve a probar. Prueba: un pedido de dos productos y el total con la comisión nueva.

Nivel 4 — Restaurante: salón, cocina y caja
Mesas, comanda, cola de cocina y cuenta. El salón manda el pedido, la cocina lo marca listo, la caja cobra. Parte el trabajo en tareas. El cobro con tarjeta queda bloqueado ("no hay pasarela"); el resto sí se prueba, incluido pagar en efectivo simulado. Prueba: pedido de dos platos, cocina lo cierra, la cuenta suma bien y el pago con tarjeta sigue pendiente.

Nivel 5 — Operación de una clínica con varias piezas
Web de pacientes + panel del personal + API + base de datos. Citas, historia e informe del día (cuántas citas y cuáles siguen abiertas). Recorrido completo desde pedir cita hasta verla en el informe. Checkpoint. Después cambia la regla del informe (debe separar citas de hoy y de mañana): invalida lo hecho, arréglalo y vuelve a probar. Plan de publicación con lo que no se probó de verdad (usuarios reales, respaldos, pagos, datos sensibles en producción).

Revisión (la haces tú, no yo)
Cuando los cinco niveles estén construidos, deja de programar. Vuelve a leer solo los INFORME.md, las salidas de las pruebas y el validador. No te fíes de lo que recuerdas haber hecho.
Escribe ~/mdvtp-pruebas/INFORME-METODO.md como revisor:
- Tabla nivel | producto | prueba (OK/FALLA) | validador
- Qué está mal o es confuso en el método, con el archivo o el comando que lo demuestra
- Qué mejorarías, de lo más barato a lo más caro
- Qué no quedó comprobado
- Veredicto tuyo: útil / útil con huecos / no sirve todavía, y por qué

Entrega
Pégame ese informe en el chat y deja el archivo en la carpeta. No me pidas que yo lo apruebe.

Cierre
Para aquí. No crees una rutina ni una skill. No hagas git push.
```
