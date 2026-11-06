#!/usr/bin/env python3
"""Genera docs/trazabilidad.md: requisito -> criterio -> prueba -> estado de verificación."""
import pathlib, yaml
RAIZ = pathlib.Path(__file__).resolve().parent.parent
REQ = yaml.safe_load((RAIZ / "requisitos" / "requisitos.yml").read_text(encoding="utf-8"))
out = ["# Matriz de trazabilidad\n", "| Requisito | Prioridad | Criterios de aceptación | Prueba | Verificación |", "|---|---|---|---|---|"]
for r in REQ["funcionales"]:
    out.append(f"| {r['id']} {r['nombre']} | {r['prioridad']} | {'; '.join(r['criterios'])} | {r.get('prueba') or '—'} | {r['verificacion']} |")
out += ["", "# Requisitos no funcionales medibles\n", "| ID | Requisito | Meta | Cómo se verifica |", "|---|---|---|---|"]
for r in REQ["no_funcionales"]:
    out.append(f"| {r['id']} | {r['nombre']} | {r['meta']} | {r['verificacion']} |")
(RAIZ / "docs" / "trazabilidad.md").write_text("\n".join(out) + "\n", encoding="utf-8")
auto = sum(1 for r in REQ["funcionales"] if r["verificacion"] == "automatica")
print(f"trazabilidad.md generada: {auto}/{len(REQ['funcionales'])} RF verificados automáticamente")
