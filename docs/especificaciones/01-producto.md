# ESP-01 — Producto del paquete

Estado: borrador 0.1 · Fuente: encargo §1–§3, §11, §14 · Objetivos: [objetivos.md](../objetivos.md)

## Qué la inicia

El encargo. Se revisa al terminar B06 (selección de base) y cada vez que cambie un requisito.

## Qué produce

La definición del producto: usuarios, problema, alcance, restricciones y requisitos R01–R20 con sus criterios de aceptación. Es la entrada de todas las demás especificaciones.

## Usuarios

- **Usuario principal:** una persona que desarrolla un producto de software con un agente de IA (Claude Code o Cursor) y quiere avanzar sin estudiar el funcionamiento interno de las skills. Revisa decisiones y evidencia en español.
- **Agente:** el modelo que ejecuta el método dentro del host. Necesita contratos claros y validadores, no solo instrucciones.
- **Mantenedor del paquete:** quien actualiza fuentes, contratos y migraciones (R20).

## Problema

Los métodos existentes (F01–F11) cubren partes del ciclo con estados, comandos y supuestos distintos. Ninguno ofrece en ambos hosts, a la vez, una entrada única, decisiones visibles, trazabilidad con invalidación, recuperación aislada y verificación honesta. Combinarlos sin criterio produce varios modelos de estado y autoridades en conflicto (§12).

## Alcance

- **Dentro:** descubrimiento, requisitos, diseño, planificación por incrementos, implementación, verificación, diagnóstico, entrega, operación, mantenimiento y aprendizaje (§2), con profundidad proporcional al riesgo (R17).
- **Fuera:** desarrollar ahora una aplicación de negocio, o ejecutar o instalar las fuentes de referencia.

## Restricciones

- Experiencia en español; identificadores técnicos estables y breves (§3).
- Un núcleo común y dos adaptadores (Claude Code y Cursor) (§6).
- Un único modelo de estado, un único registro de decisiones y una única interfaz de continuación (§12).
- Las instrucciones orientan al modelo; los controles obligatorios necesitan validadores (§6).
- Runtime mínimo según el entorno confirmado (§12). Entorno de B01: Node 24, Python 3.13, git 2.53, jq 1.8; sin `npm` en el PATH.

## Requisitos

R01–R20 tal como aparecen en el encargo §3 (no se duplican aquí para no crear una segunda autoridad). Mapa requisito → objetivo en [objetivos.md](../objetivos.md); requisito → tarea en el [tablero](../tablero.md).

## Cómo se revisa

El usuario la revisa en la Entrega A. Cada requisito debe tener una solución prevista o un desarrollo propio explícito en el mapa de cobertura de B06.

## Qué permite avanzar

ESP-01 aceptada y el mapa de cobertura de B06 sin requisitos huérfanos → se pueden cerrar ESP-02 a ESP-08.

## Abierto

| Pregunta | Se resuelve en |
|---|---|
| ¿Qué fuente sirve de base (cc-sdd como candidata) y qué se desarrolla por cuenta propia? | B06 |
| ¿Qué nivel de profundidad corresponde a cada tipo de proyecto (criterios de R17)? | B07 |
| ¿Qué afirmaciones exactas permitirá la versión candidata? | B21 (§14) |
