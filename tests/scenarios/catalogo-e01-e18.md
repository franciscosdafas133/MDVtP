# Catálogo E01–E18 (evaluación)

Clases:

- **D** = determinista (script / fixture; no juicio del agente)
- **O** = observación de agente (Cursor / Claude Code / otro); evaluador ≠ mismo agente
- **M** = mixto

| ID | Clase | Cubierto ahora | Cómo se comprueba |
|---|---|---|---|
| E01 | O | parcial (runner inicia con idea vaga) | Agente: preguntas, no inventar REQ; playbook producto-simple |
| E02 | O | no | Sesión agente + apuntes/decisiones |
| E03 | O | no | Dos propuestas; aclara cuál |
| E04 | O+D | parcial | `bloquear` + marca simulación; agente debe documentar |
| E05 | O+D | parcial D | `dividir` / demo-b12 |
| E06 | O+D | parcial D | `continuar` contrasta git/apuntes |
| E07 | O+D | parcial D | `impactar` invalida dependientes |
| E08 | O+D | parcial D | verificar sin EVID falla (demo-b13) |
| E09 | O | no | Agente declara integración real pendiente |
| E10 | O+D | parcial D | depurar tope 3 (demo-b13) |
| E11 | D | sí | dirty + checkpoint; demo-b11; batería B17 |
| E12 | D | sí | JSON truncado / `.tmp` → validador falla (B17) |
| E13 | O | no | Mismo workflow en otro host (B19) |
| E14 | D | sí | `install_metodo.py demo` |
| E15 | O+D | parcial D | fixture workflow-ok no inventa fallos |
| E16 | D/O | no | Migración de versión (pendiente política B22) |
| E17 | O+D | parcial | recorrido-simple; integración real → B20 |
| E18 | O | no | Advertencia migración externa ≠ git (operar texto; falta caso agente) |

**Regla:** el agente bajo prueba no escribe el veredicto final. Scripts + usuario/evaluador externo.
