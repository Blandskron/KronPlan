# Provenance & Security Audit — `ui-ux-pro-max`

- **Upstream Repository:** `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`
- **Pinned Commit SHA:** `8db36338810d`
- **License:** MIT (ver [`LICENSE`](./LICENSE))
- **Antigravity Compatibility:** Instalada en `.agents/skills/ui-ux-pro-max/SKILL.md` siguiendo la especificación de workspace skills (`agy-customizations`).

## Auditoría de Seguridad y Alcance

Antes de incorporar esta skill al repositorio se revisaron los seis scripts Python (`core.py`, `design_system.py`, `preview.py`, `reasoning_contract.py`, `search.py`, `validate_data.py`):

1. **Solo biblioteca estándar de Python:** cero dependencias externas (`csv`, `json`, `re`, `math`, `difflib`, `collections`, `itertools`, `pathlib`, `argparse`, `os`, `sys`, `io`, `tempfile`, `unicodedata`, `datetime`, `html.escape`, `hashlib`, `statistics`).
2. **Ejecución 100 % offline:** lee exclusivamente los catálogos CSV/JSON locales en `data/` sin realizar llamadas de red ni telemetría.
3. **Sin ejecución dinámica ni shell:** cero usos de `subprocess`, `os.system`, `eval`, `exec`, `__import__` o `importlib`.
4. **Alcance acotado:** se excluyeron las suites de tests internos del upstream (`scripts/tests/`), manteniendo íntegro el catálogo `data/` (incluidos los 22 archivos en `data/stacks/`) para que `scripts/validate_data.py` valide el contrato completo sin errores.
