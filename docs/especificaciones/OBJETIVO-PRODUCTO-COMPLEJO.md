# Objetivo de producto complejo (norte del método)

No es una app a construir mañana. Es **hacia dónde** debe demostrar madurez el método: productos tangibles donde lo difícil es investigar, formular el flujo de datos/conocimiento y recién después construir.

## Producto-norte (ejemplo canónico)

**Aprender con relaciones (grafos de conceptos) + recuperar ese conocimiento + darle forma con un LLM.**

Ejemplos de uso:
- Página o agente donde construyes un grafo de conceptos (nodos = ideas, aristas = “necesita / es ejemplo de / contradice…”).
- Recuperas lo que ya sabes del grafo (no solo del chat).
- Un LLM explica, pregunta o genera ejercicios **atado** a ese grafo (no alucinando el modelo de conocimiento).

Lo importante no es “usar un LLM”. Es que el método obligue a formular:
- qué es un concepto y una relación;
- de dónde sale cada dato (usuario, ejercicio, modelo, fuente);
- qué se puede afirmar vs qué es hipótesis;
- qué queda simulado (API de modelo, embeddings, etc.) vs qué se prueba de verdad;
- cómo un cambio en el grafo invalida explicaciones o ejercicios ya “verificados”.

## Por qué importa para el método

Los niveles e2e 1–4 entrenan el esqueleto (formular llano, roles, cambio de regla, bloqueo real).  
Este norte exige además:
- investigación / descubrimiento denso;
- flujo de datos (raw → modelo → recuperación → respuesta);
- fronteras honestas con IA (simulación vs integración real).

## Camino (sin saltar)

1. Cerrar oleada e2e v3 nivel 4 (flujo + integración bloqueada).
2. **Sonda compleja-1 (rebanada):** motor de grafo de conceptos + CLI/API local + pruebas (sin LLM, o LLM marcado pendiente).
3. **Sonda compleja-2:** recuperación sobre el grafo + una explicación generada con frontera explícita (mock vs API real bloqueada).
4. Solo entonces: página/agente conversacional encima del motor.

Cada sonda: carpeta aparte, desde cero, notas formular/construir, sin copiar oleadas viejas.

## Criterio de éxito del norte

El método “sirve para complejo” cuando un dueño/agente puede llegar a un incremento que:
- tiene el **modelo de conocimiento** formulado (no solo pantallas);
- corre con evidencia;
- deja claro qué parte de IA/datos no está probada;
- al cambiar una relación del grafo, invalidar lo afectado.

Fecha de anclaje: 2026-10-14 (conversación con el usuario).
