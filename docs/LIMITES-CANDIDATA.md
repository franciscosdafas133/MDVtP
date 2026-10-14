# Límites de la versión candidata 0.1.0-rc1

## Se puede afirmar

- Hay una entrada única (`product-flow`) con scripts y validador.
- Instalación global/proyecto en Cursor y Claude Code (adaptadores).
- Flujo documental + estado + checkpoints + división + verificación con evidencia + operar.
- Baterías deterministas: integridad (B17), eval D (B18), integración+impacto (B20).
- Pasada de observación en Cursor y Claude Code firmada por el usuario (producto mínimo).

## No se puede afirmar (aún)

- Que el método “ya sirve” en productos grandes o de producción real sin más pruebas.
- Marketplace oficial de Cursor.
- Que la ventana HTML se abre sola al instalar (I-01: patrón existe; auto-arranque no).
- Migración automática entre versiones del paquete (eso es el paso 22).
- Que Git deshace pagos/APIs en producción (el método solo advierte el procedimiento).

## Cómo mejorar desde aquí

Usar el método en un producto real tuyo, anotar fricciones, y cerrar el paso 22 (política de versiones y regresiones).
