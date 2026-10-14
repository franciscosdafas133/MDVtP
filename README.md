# MDVtP — el método (product-flow)

Paquete para **Cursor** y **Claude Code** que guía el desarrollo de un producto: idea → docs → decisiones → tareas → pruebas honestas → plan de entrega.

Versión: ver [VERSION](VERSION) (`0.1.0-rc1`).

## Instalar

```bash
git clone https://github.com/franciscosdafas133/MDVtP.git
cd MDVtP
python3 scripts/install_metodo.py install --alcance global --hosts cursor,claude
```

Detalle: [INSTALL.md](INSTALL.md).  
Uso diario: [docs/GUIA-USUARIO.md](docs/GUIA-USUARIO.md).  
Límites de esta candidata: [docs/LIMITES-CANDIDATA.md](docs/LIMITES-CANDIDATA.md).

## En el chat

Pide la skill **product-flow** (o `/product-flow`) e indica una idea de producto.

## Comprobar

```bash
python3 scripts/run_regresion.py
```

## Licencias

Avisos de terceros: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
