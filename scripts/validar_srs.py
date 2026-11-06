#!/usr/bin/env python3
"""Validador del SRS: revisa docs/SRS.md y requisitos/requisitos.yml.
Errores (ERROR) hacen fallar el pipeline. Pendientes del documento (AVISO) se reportan y,
con --estricto, también hacen fallar. Salida compatible con anotaciones de GitHub Actions."""
import re, sys, collections, pathlib, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SRS = (RAIZ / "docs" / "SRS.md").read_text(encoding="utf-8")
REQ = yaml.safe_load((RAIZ / "requisitos" / "requisitos.yml").read_text(encoding="utf-8"))
TESTS = (RAIZ / "tests" / "test_esquema.py").read_text(encoding="utf-8")

errores, avisos = [], []

# ---------- 1. Requisitos como código ----------
ids = [r["id"] for r in REQ["funcionales"] + REQ["no_funcionales"]]
for i, n in collections.Counter(ids).items():
    if n > 1:
        errores.append(f"ID de requisito duplicado: {i}")
for r in REQ["funcionales"]:
    if not r.get("criterios"):
        errores.append(f"{r['id']} no tiene criterios de aceptación")
    if r["prioridad"] not in ("Alta", "Media", "Baja"):
        errores.append(f"{r['id']} tiene prioridad inválida")
    if r["verificacion"] == "automatica":
        if not r.get("prueba") or f"def {r['prueba']}(" not in TESTS:
            errores.append(f"{r['id']}: la prueba '{r.get('prueba')}' no existe en tests/test_esquema.py")
    if r["prioridad"] == "Alta" and r["verificacion"] == "revision":
        avisos.append(f"{r['id']} es de prioridad Alta y aún se verifica solo a mano")
for r in REQ["no_funcionales"]:
    if not re.search(r"\d", r["meta"]):
        errores.append(f"{r['id']} no es medible (la meta no tiene un número): {r['meta']}")

# ---------- 2. Consistencia SRS <-> requisitos.yml ----------
rf_en_srs = set(re.findall(r"\|\s*RF\s?(\d{2})\s*\|", SRS))
rf_en_yml = {r["id"].split("-")[1] for r in REQ["funcionales"]}
for x in sorted(rf_en_yml - rf_en_srs):
    errores.append(f"RF-{x} está en requisitos.yml pero no aparece en el SRS")
for x in sorted(rf_en_srs - rf_en_yml):
    errores.append(f"RF {x} está en el SRS pero no en requisitos.yml")

# ---------- 3. Calidad del documento (pendientes) ----------
for pat, msg in [
    (r"\[Inserte aquí el texto\]", "marcador sin completar '[Inserte aquí el texto]'"),
    (r"\[Insertar imagen[^\]]*\]", "imagen pendiente '[Insertar imagen]'"),
    (r"\[(Nombre|Fecha|Firma o sello)\]", "dato de la ficha sin completar"),
    (r"Requisito funcional (\d|n)\b", "encabezado genérico 'Requisito funcional N' sin reemplazar"),
    (r"Alta/Esencial \| Media/Deseado \| Baja/ Opcional", "prioridad del requisito sin elegir (quedaron las tres opciones)"),
]:
    n = len(re.findall(pat, SRS))
    if n:
        avisos.append(f"{n} × {msg}")

# Duplicados dentro de la misma sección (lo repetido entre secciones puede ser intencional)
for bloque in re.split(r"(?m)^#{1,4} ", SRS):
    lineas = [l.strip() for l in bloque.splitlines() if len(l.strip()) > 40 and not l.strip().startswith("|")]
    for l, n in collections.Counter(lineas).items():
        if n > 1:
            avisos.append(f"línea repetida {n} veces en la misma sección: «{l[:70]}…»")

# RNF del SRS: cada viñeta de la sección debe tener un número
m = re.search(r"## Requisitos no funcionales(.*?)## Otros requisitos", SRS, re.S)
if m:
    for l in m.group(1).splitlines():
        l = l.strip(" \t-")
        if l.startswith("El ") and not re.search(r"\d", l):
            avisos.append(f"RNF del SRS sin cifra medible: «{l[:80]}…»")

# ---------- Salida ----------
for e in errores: print(f"::error::{e}")
for a in avisos:  print(f"::warning::{a}")
print(f"\nResumen: {len(errores)} errores, {len(avisos)} pendientes en el documento.")
estricto = "--estricto" in sys.argv
sys.exit(1 if errores or (estricto and avisos) else 0)
