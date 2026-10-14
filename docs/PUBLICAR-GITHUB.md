# Publicar el método en GitHub (después del paso 22)

Sí: el siguiente paso natural es **subirlo a GitHub como producto instalable**, no como basurero de experimentos.

## Checklist

1. `python3 scripts/run_regresion.py` → ok  
2. `python3 scripts/install_metodo.py build-dist` (ya lo incluye la regresión)  
3. Commit limpio (sin `.reference-sources/`, sin secretos, demos de fixtures ignoradas)  
4. Crear repo en GitHub (público o privado)  
5. `git remote add origin …` y `git push -u origin HEAD`  
6. En el README del repo (o este doc): enlace a [INSTALL.md](../INSTALL.md) y [GUIA-USUARIO.md](GUIA-USUARIO.md)  
7. Quien lo use: clonar + `install --alcance global`, o copiar `skills/product-flow/`

## Qué no subir

- `.reference-sources/` (ya en `.gitignore`)  
- Homes/demos con `.git` de prueba  
- Credenciales, `.env`, claves de API  

## Opcional después

- Tag `v0.1.0-rc1`  
- Importar plugin en Cursor “From GitHub Repository” cuando el host lo permita  
