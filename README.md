# SRS Cigarrería Alcalá con DevOps ("documentación como código")

El informe IEEE 830 vive en `docs/SRS.md`; los requisitos en `requisitos/requisitos.yml`; el esquema (Entrega 3) en `db/schema.sql`.
Cada `git push` ejecuta `.github/workflows/ci.yml`: valida el documento, prueba los criterios de aceptación,
genera la trazabilidad y construye el Word. Una etiqueta `v1.x` publica la versión.

Local (sin instalar nada más que PyYAML):
    pip install pyyaml
    python scripts/validar_srs.py
    python -m unittest discover -s tests -v
    python scripts/generar_trazabilidad.py
