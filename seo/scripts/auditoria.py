#!/usr/bin/env python3
"""Auditoría SEO técnica de dulcesmarisol.es.

Recorre todas las URLs del sitemap de Rank Math y revisa cada página:
título, metadescripción, H1, canonical, robots, imágenes sin alt,
nº de palabras, datos estructurados y tiempo de respuesta.
Después busca duplicados (títulos, descripciones y descripciones de
productos de WooCommerce).

Uso:
    python3 seo/scripts/auditoria.py [--salida seo/datos/auditoria-YYYY-MM-DD.json]

Las credenciales de WordPress las inyecta el proxy del entorno; el script
no necesita ninguna clave.
"""
import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import requests

SITIO = "https://dulcesmarisol.es"
UA = "DulcesMarisol-SEO-Audit/1.0"
S = requests.Session()
S.headers["User-Agent"] = UA


def get(url, **kw):
    for intento in range(3):
        try:
            t0 = time.time()
            r = S.get(url, timeout=30, **kw)
            r.elapsed_s = round(time.time() - t0, 2)
            return r
        except requests.RequestException:
            if intento == 2:
                raise
            time.sleep(2 * (intento + 1))


def urls_sitemap():
    urls = []
    idx = get(f"{SITIO}/sitemap_index.xml").text
    for sm in re.findall(r"<loc>(.*?)</loc>", idx):
        urls += re.findall(r"<loc>(.*?)</loc>", get(sm).text)
    # quitar URLs de imágenes que algunos sitemaps incluyen
    return sorted({u for u in urls if not re.search(r"\.(jpe?g|png|webp|gif)$", u, re.I)})


def texto(fragmento):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragmento))).strip()


def uno(patron, s):
    m = re.search(patron, s, re.I | re.S)
    return html.unescape(m.group(1).strip()) if m else None


def analizar(url):
    d = {"url": url}
    try:
        r = get(url)
    except Exception as e:  # noqa: BLE001
        d["error"] = str(e)
        return d
    s = r.text
    d["estado"] = r.status_code
    d["tiempo_s"] = r.elapsed_s
    d["bytes"] = len(r.content)
    d["titulo"] = uno(r"<title[^>]*>(.*?)</title>", s)
    d["descripcion"] = uno(r'<meta\s+name="description"\s+content="(.*?)"', s)
    d["robots"] = uno(r'<meta\s+name="robots"\s+content="(.*?)"', s)
    d["canonical"] = uno(r'<link\s+rel="canonical"\s+href="(.*?)"', s)
    d["h1"] = [texto(h) for h in re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)]
    d["n_h2"] = len(re.findall(r"<h2[\s>]", s))
    imgs = re.findall(r"<img\b[^>]*>", s)
    d["n_imgs"] = len(imgs)
    d["imgs_sin_alt"] = [
        # alt="" es correcto en imágenes decorativas; solo cuenta si falta el atributo
        uno(r'src="(.*?)"', i) for i in imgs if not re.search(r'\balt=', i)
    ][:20]
    cuerpo = re.sub(r"<(script|style|header|footer|nav)\b.*?</\1>", " ", s, flags=re.S | re.I)
    m = re.search(r"<main\b.*?</main>", cuerpo, re.S | re.I)
    d["palabras"] = len(texto(m.group(0) if m else cuerpo).split())
    d["schema"] = sorted(set(re.findall(r'"@type"\s*:\s*"(\w+)"', s)))
    d["og_imagen"] = bool(re.search(r'property="og:image"', s))
    d["enlaces_internos"] = len(set(re.findall(rf'href="({re.escape(SITIO)}[^"#?]*)', s)))
    return d


def problemas_pagina(d):
    p = []
    if "error" in d:
        return [f"error de red: {d['error']}"]
    if d["estado"] != 200:
        p.append(f"estado HTTP {d['estado']}")
    t = d["titulo"] or ""
    if not t:
        p.append("sin <title>")
    elif len(t) > 60:
        p.append(f"título largo ({len(t)} car.)")
    elif len(t) < 30:
        p.append(f"título corto ({len(t)} car.)")
    ds = d["descripcion"] or ""
    if not ds:
        p.append("sin metadescripción")
    elif len(ds) > 160:
        p.append(f"metadescripción larga ({len(ds)} car.)")
    elif len(ds) < 70:
        p.append(f"metadescripción corta ({len(ds)} car.)")
    if len(d["h1"]) != 1:
        p.append(f"{len(d['h1'])} H1")
    if d["canonical"] and d["canonical"].rstrip("/") != d["url"].rstrip("/"):
        p.append(f"canonical apunta a otra URL: {d['canonical']}")
    if d["robots"] and "noindex" in d["robots"]:
        p.append("noindex en una URL del sitemap")
    if d["imgs_sin_alt"]:
        p.append(f"{len(d['imgs_sin_alt'])} imágenes sin alt")
    if d["palabras"] < 250:
        p.append(f"poco texto ({d['palabras']} palabras)")
    if d["tiempo_s"] > 2.5:
        p.append(f"respuesta lenta ({d['tiempo_s']} s)")
    if not d["og_imagen"]:
        p.append("sin og:image")
    return p


def productos_woo():
    """Descripciones de productos vía API de WooCommerce (requiere credencial)."""
    prods, pagina = [], 1
    while True:
        r = get(f"{SITIO}/wp-json/wc/v3/products",
                params={"per_page": 100, "page": pagina, "status": "publish"})
        if r.status_code != 200:
            return None, f"API WooCommerce respondió {r.status_code}"
        lote = r.json()
        prods += lote
        if len(lote) < 100:
            return prods, None
        pagina += 1


def duplicados(valores):
    grupos = defaultdict(list)
    for clave, url in valores:
        if clave:
            grupos[clave].append(url)
    return [{"valor": k[:120], "urls": v} for k, v in grupos.items() if len(v) > 1]


def main():
    ap = argparse.ArgumentParser()
    hoy = dt.date.today().isoformat()
    ap.add_argument("--salida", default=f"seo/datos/auditoria-{hoy}.json")
    a = ap.parse_args()

    urls = urls_sitemap()
    with ThreadPoolExecutor(max_workers=4) as ex:
        paginas = list(ex.map(analizar, urls))
    for d in paginas:
        d["problemas"] = problemas_pagina(d)

    res = {
        "fecha": hoy,
        "n_urls": len(urls),
        "paginas": paginas,
        "titulos_duplicados": duplicados([(d.get("titulo"), d["url"]) for d in paginas]),
        "descripciones_duplicadas": duplicados([(d.get("descripcion"), d["url"]) for d in paginas]),
    }

    prods, err = productos_woo()
    if prods is None:
        res["productos_error"] = err
    else:
        res["productos"] = [{
            "id": p["id"], "nombre": p["name"], "url": p["permalink"],
            "palabras_desc": len(texto(p["description"]).split()),
            "palabras_desc_corta": len(texto(p["short_description"]).split()),
            "imgs_sin_alt": sum(1 for i in p.get("images", []) if not i.get("alt")),
            "rank_math": {m["key"]: m["value"] for m in p.get("meta_data", [])
                          if m["key"] in ("rank_math_title", "rank_math_description",
                                          "rank_math_focus_keyword")},
        } for p in prods]
        res["descripciones_producto_duplicadas"] = duplicados([
            (hashlib.md5(texto(p["description"]).encode()).hexdigest()
             if len(texto(p["description"])) > 100 else None, p["permalink"])
            for p in prods])

    import os
    os.makedirs(os.path.dirname(a.salida), exist_ok=True)
    with open(a.salida, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)

    # resumen legible por stdout
    con_prob = [d for d in paginas if d["problemas"]]
    print(f"Auditoría {hoy}: {len(urls)} URLs, {len(con_prob)} con problemas")
    cuenta = defaultdict(int)
    for d in paginas:
        for p in d["problemas"]:
            cuenta[re.sub(r"\(.*?\)|\d+", "", p).strip()] += 1
    for k, v in sorted(cuenta.items(), key=lambda x: -x[1]):
        print(f"  {v:4d} × {k}")
    print(f"  títulos duplicados: {len(res['titulos_duplicados'])}")
    print(f"  metadescripciones duplicadas: {len(res['descripciones_duplicadas'])}")
    if "productos" in res:
        print(f"  productos: {len(res['productos'])}, descripciones duplicadas: "
              f"{len(res['descripciones_producto_duplicadas'])} grupos")
    else:
        print(f"  productos: {res['productos_error']}")
    print(f"Detalle: {a.salida}")


if __name__ == "__main__":
    sys.exit(main())
