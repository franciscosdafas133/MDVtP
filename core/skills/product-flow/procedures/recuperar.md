# recuperar

Abrir una copia aislada desde un checkpoint **sin pisar** el trabajo actual.

```bash
python3 <método>/scripts/product_flow.py recuperar \
  --proyecto <proyecto> --checkpoint CP-01
```

- Por defecto: `git worktree` en una carpeta hermana.
- Si no hay worktree: `--rama` crea la rama y no cambia tu checkout.
- Sin git: solo restaura el snapshot de documentos (aviso de límite).
- Nunca borra cambios sin commit del proyecto actual.
