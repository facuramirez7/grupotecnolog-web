#!/usr/bin/env python3
"""Genera index.html (es), en/index.html y pt/index.html desde src/template.html + i18n/*.json.
Uso: python3 build.py
Se edita src/ e i18n/, nunca los HTML generados."""
import json, re, html, sys, os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://grupotecnolog.com'
LANGS = {
    'es': dict(out='index.html', url=SITE + '/', code='es-AR', og='es_AR', hl='es', locale='es-AR', in_language='es', gea_url='https://www.gea.com/es/'),
    'en': dict(out='en/index.html', url=SITE + '/en/', code='en', og='en_US', hl='en', locale='en-US', in_language='en', gea_url='https://www.gea.com/en/'),
    'pt': dict(out='pt/index.html', url=SITE + '/pt/', code='pt-BR', og='pt_BR', hl='pt-BR', locale='pt-BR', in_language='pt-BR', gea_url='https://www.gea.com/pt/'),
}
CONST = {
    'maps_place': 'https://www.google.com/maps/place/GRUPO+TECNOLOG+SA/@-33.023988,-68.8743844,19.23z/data=!4m15!1m8!3m7!1s0x967e75311cd957b7:0x4645e2080e4f8c36!2sSan+Mart%C3%ADn+1652,+M5507+Luj%C3%A1n+de+Cuyo,+Mendoza!3b1!8m2!3d-33.0242921!4d-68.8743844!16s%2Fg%2F11j6g3mzhf!3m5!1s0x967e75311c9c780f:0x1a8981648589e1e2!8m2!3d-33.0241911!4d-68.8743517!16s%2Fg%2F11gbv4yhb6?entry=ttu&g_ep=EgoyMDI2MDkyMy4wIKXMDSoASAFQAw%3D%3D',
}
FILTERS = {
    'url': lambda v: quote(v, safe=''),
    'attr': lambda v: html.escape(v, quote=True),
    'json': lambda v: json.dumps(v, ensure_ascii=False)[1:-1],
    'jsonlist': lambda v: ', '.join(json.dumps(x, ensure_ascii=False) for x in v),
}

def flatten(d, prefix=''):
    out = {}
    for k, v in d.items():
        key = f'{prefix}{k}'
        if isinstance(v, dict): out.update(flatten(v, key + '.'))
        else: out[key] = v
    return out

def render(template, values):
    missing = []
    def sub(m):
        key, flt = m.group(1), m.group(2)
        if key not in values:
            missing.append(key); return m.group(0)
        v = values[key]
        return FILTERS[flt](v) if flt else v
    out = re.sub(r'\{\{([a-z_.0-9]+)(?:\|([a-z]+))?\}\}', sub, template)
    return out, missing

def main():
    tpl = open(os.path.join(ROOT, 'src/template.html'), encoding='utf-8').read()
    css = open(os.path.join(ROOT, 'src/styles.css'), encoding='utf-8').read()
    keys_by_lang = {}
    for lang, cfg in LANGS.items():
        data = json.load(open(os.path.join(ROOT, f'i18n/{lang}.json'), encoding='utf-8'))
        values = flatten(data)
        keys_by_lang[lang] = set(values)
        values['css'] = css
        for k, v in cfg.items(): values[f'lang.{k}'] = v
        for k, v in CONST.items(): values[f'const.{k}'] = v
        for l in LANGS: values[f'switch.{l}'] = 'is-active' if l == lang else ''
        out, missing = render(tpl, values)
        if missing:
            sys.exit(f'[{lang}] claves faltantes: {sorted(set(missing))}')
        if '{{' in out:
            sys.exit(f'[{lang}] quedaron marcadores sin reemplazar')
        path = os.path.join(ROOT, cfg['out'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').write(out)
        print(f'{cfg["out"]:16} {len(out)//1024} KB')
    # claves iguales en los tres idiomas
    base = keys_by_lang['es']
    for lang, ks in keys_by_lang.items():
        if ks != base:
            sys.exit(f'[{lang}] claves distintas a es: faltan {sorted(base-ks)} / sobran {sorted(ks-base)}')
    # sitemap con hreflang
    alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>' for h, u in
                   [('es', LANGS['es']['url']), ('en', LANGS['en']['url']), ('pt-BR', LANGS['pt']['url']), ('x-default', LANGS['es']['url'])])
    imgs = ''.join(f'''
    <image:image>
      <image:loc>{SITE}/assets/img/{f}</image:loc>
    </image:image>''' for f in ['centrifuga-gea-bodega.jpg', 'centrifuga-separadora-vino-1200.webp', 'caneria-acero-inoxidable-bodega-1200.webp', 'intercambiador-frio-calor-acero-inoxidable-1200.webp'])
    from datetime import date
    today = date.today().isoformat()
    urls = ''.join(f'''
  <url>
    <loc>{cfg['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{'1.0' if lang == 'es' else '0.9'}</priority>{alts}{imgs}
  </url>''' for lang, cfg in LANGS.items())
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{urls}
</urlset>
'''
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sitemap)
    print('sitemap.xml      3 urls con hreflang')

if __name__ == '__main__':
    main()
