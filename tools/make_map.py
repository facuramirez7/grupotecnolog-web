#!/usr/bin/env python3
"""Genera src/clients-map.svg: norte y centro de Argentina con provincias (Natural Earth 10m, dominio público)
y pines ilustrativos de las zonas atendidas. Uso: python3 tools/make_map.py ruta/ne_10m_admin_1_states_provinces.geojson"""
import json, math, sys, os

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img', 'clients-map.svg')
LON0, LON1, LAT0, LAT1 = -72.4, -59.0, -41.6, -22.0   # recorte: oeste y norte argentino, de Mendoza a Jujuy
W = 620.0
HIGHLIGHT = {'Mendoza': 'a', 'San Juan': 'b', 'La Rioja': 'b', 'Catamarca': 'c', 'Salta': 'c', 'Neuquén': 'c', 'Río Negro': 'c'}
LABELS = {'Mendoza': (-70.3, -35.7), 'San Juan': (-70.0, -30.3), 'La Rioja': (-65.9, -29.9), 'Catamarca': (-65.9, -27.7), 'Salta': (-64.3, -25.2), 'Neuquén': (-70.6, -38.9), 'Río Negro': (-66.3, -40.3)}
# (lon, lat, tamaño) — pines ilustrativos
PINS = [
    (-68.87, -33.03, 9), (-68.79, -32.98, 7), (-68.84, -32.89, 7), (-68.59, -32.72, 6), (-68.47, -33.08, 6), (-68.47, -33.19, 6),
    (-69.15, -33.37, 7), (-69.02, -33.58, 7), (-69.04, -33.77, 6), (-68.33, -34.62, 7), (-67.69, -34.98, 6),
    (-68.53, -31.54, 7), (-68.28, -31.65, 6), (-68.58, -31.68, 6), (-67.49, -29.16, 6),
    (-67.56, -28.06, 6), (-65.98, -26.07, 7),
    (-68.30, -38.62, 6), (-67.58, -39.03, 6),
]

def merc(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
MY0, MY1 = merc(LAT0), merc(LAT1)
SCALE = W / (LON1 - LON0)
H = (MY1 - MY0) * SCALE
def proj(lon, lat): return ((lon - LON0) * SCALE, (MY1 - merc(lat)) * SCALE)

M = 1.0  # margen en grados fuera del recorte
def ring_path(ring, tol=2.2):
    pts, last = [], None
    for lon, lat in ring:
        if not (LON0 - M <= lon <= LON1 + M and LAT0 - M <= lat <= LAT1 + M): continue
        x, y = proj(lon, lat)
        if last is None or abs(x - last[0]) + abs(y - last[1]) >= tol:
            pts.append((x, y)); last = (x, y)
    if len(pts) < 4: return ''
    return 'M' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts) + 'z'

def area(ring):
    s = 0
    for i in range(len(ring)):
        x1, y1 = ring[i]; x2, y2 = ring[(i + 1) % len(ring)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2

d = json.load(open(SRC, encoding='utf-8'))
feats = [f for f in d['features'] if f['properties'].get('adm0_a3') == 'ARG']
paths = []
for f in sorted(feats, key=lambda f: f['properties']['name']):
    name = f['properties']['name']
    geom = f['geometry']
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    dd = ''
    for poly in polys:
        outer = poly[0]
        if area(outer) < 0.02: continue   # islas mínimas
        lons = [q[0] for q in outer]; lats = [q[1] for q in outer]
        if max(lons) < LON0 - M or min(lons) > LON1 + M or max(lats) < LAT0 - M or min(lats) > LAT1 + M: continue
        dd += ring_path(outer)
    if not dd: continue
    cls = 'prov' + (' hl-' + HIGHLIGHT[name] if name in HIGHLIGHT else '')
    paths.append(f'<path class="{cls}" d="{dd}"><title>{name}</title></path>')

labels = ''.join(f'<text class="lbl" x="{proj(lo, la)[0]:.1f}" y="{proj(lo, la)[1]:.1f}">{n}</text>' for n, (lo, la) in LABELS.items())
pins = ''.join(f'<circle class="pin-halo" cx="{proj(lo, la)[0]:.1f}" cy="{proj(lo, la)[1]:.1f}" r="{r * 2.2:.0f}"/><circle class="pin" cx="{proj(lo, la)[0]:.1f}" cy="{proj(lo, la)[1]:.1f}" r="{r}"/>' for lo, la, r in PINS)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">
<title id="ar-map-title">Zonas donde Grupo Tecnolog atiende bodegas e industrias: Mendoza, San Juan, La Rioja, Catamarca, Salta, Neuquén y Río Negro</title>
<style>.prov{{fill:#f3f3f3;stroke:#c6c6c6;stroke-width:.8}}.hl-a{{fill:#cdeaf6}}.hl-b{{fill:#e0f2f9}}.hl-c{{fill:#edf7fb}}.lbl{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;fill:#444;text-anchor:middle}}.pin{{fill:#006690;stroke:#fff;stroke-width:2}}.pin-halo{{fill:#0098cb;opacity:.16}}</style>
<defs><clipPath id="ar-clip"><rect x="0" y="0" width="{W:.0f}" height="{H:.0f}"/></clipPath><linearGradient id="ar-fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0.86" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient></defs>
<g clip-path="url(#ar-clip)">{''.join(paths)}</g>
{labels}
{pins}
<rect class="fade" x="0" y="0" width="{W:.0f}" height="{H:.0f}" fill="url(#ar-fade)"/>
</svg>'''
open(OUT, 'w', encoding='utf-8').write(svg)
print(f'svg {len(svg)//1024} KB, {len(paths)} provincias, viewBox {W:.0f}x{H:.0f}')
