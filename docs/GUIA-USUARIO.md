# Guía breve — el método (product-flow)

Versión candidata: ver [VERSION](../VERSION).  
Instalación: [INSTALL.md](../INSTALL.md).  
Límites: [LIMITES-CANDIDATA.md](LIMITES-CANDIDATA.md).  
Mantener / publicar: [MANTENIMIENTO.md](MANTENIMIENTO.md) · [PUBLICAR-GITHUB.md](PUBLICAR-GITHUB.md).

## Para qué sirve

Te guía desde una idea vaga hasta un incremento con documentos, decisiones, pruebas honestas y un plan de entrega. **Tú** decides producto; el agente propone y el validador frena estados ilegales.

## Empezar (una vez)

```bash
# desde el repo del método
python3 scripts/install_metodo.py install --alcance global --hosts cursor,claude
```

En el chat: pide la skill **product-flow** (o `/product-flow`).

## Acciones que más usarás

| Quieres… | Di / comando |
|---|---|
| Empezar un producto | «iniciar» / `product_flow.py iniciar --proyecto . --idea "…"` |
| Retomar | «continuar» |
| Ver dónde estamos | «estado» |
| Aceptar o rechazar una propuesta | «decidir» (puerta humana) |
| Apuntar sin decidir | «anotar» |
| Guardar partida | «checkpoint» |
| Volver a un punto (sitio aparte) | «recuperar» |
| Partir una tarea gorda | «dividir» (con criterio, no por horas) |
| Cerrar con prueba de verdad | evidenciar → presentar → verificar |
| Plan de publicación | «operar» |

## Ciclo de código (siempre)

**Escanear → planificar → evaluar → reemplazar.**  
Luego evidenciar y verificar. No digas “ya está” si la prueba no corrió.

## Comprobar que el workflow no está roto

```bash
python3 <ruta-skill>/scripts/validate_workflow.py <proyecto>/workflow
```

## Demos rápidas (en el repo del método)

```bash
python3 scripts/run_integridad.py
python3 scripts/product_flow.py recorrido-simple
python3 scripts/run_integracion_b20.py
```
