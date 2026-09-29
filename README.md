# Grupo Tecnolog — sitio web

Landing estática (HTML + CSS + JS, sin build) para [grupotecnolog.com](https://grupotecnolog.com/), con el estilo definido en `DESIGN.md`.

## Ver en local

```bash
python3 serve.py 8765
```

Abrí <http://127.0.0.1:8765>. `serve.py` es un servidor estático con soporte de `Range`, necesario para que el video del hero cargue en Chrome y Safari (el `http.server` estándar no lo soporta y el video no reproduce).

## Idiomas y build

El sitio se genera en tres idiomas desde una plantilla:

```
src/template.html   plantilla HTML con marcadores {{clave}}
src/styles.css      CSS (se inlina en cada página)
i18n/es.json        textos en español (URL /)
i18n/en.json        textos en inglés (URL /en/)
i18n/pt.json        textos en portugués de Brasil (URL /pt/)
build.py            genera index.html, en/index.html, pt/index.html y sitemap.xml (CSS minificado inline)
tools/make_map.py   regenera assets/img/clients-map.svg (mapa de zonas atendidas) a partir de Natural Earth 10m
```

**Para cambiar cualquier texto o estilo: editar `src/` o `i18n/` y correr `python3 build.py`. Nunca editar los HTML generados.** Las tres páginas se enlazan con `hreflang` (es, en, pt-BR, x-default) y el sitemap lista las tres URLs.

## Estructura

- `index.html`, `en/index.html`, `pt/index.html` — páginas generadas (9 secciones: header, hero, nosotros, servicios, trabajos, números, clientes, contacto y footer).
- El CSS (`src/styles.css`) va inline en el `<style>` de cada página (tokens y componentes del design system brutalista con la paleta de GT). Se inlinó a propósito: elimina el único recurso que bloqueaba el render y da 100 en PageSpeed.
- `assets/fonts/` — Barlow Condensed, Inter (variable) y JetBrains Mono autoalojadas en woff2.
- `.htaccess` — compresión, caché de un año para estáticos y cabeceras de seguridad (Apache).
- `assets/js/main.js` — menú mobile, link activo, contadores, reveal y formulario → WhatsApp.
- `assets/img/`, `assets/logos/` — fotos y logos tomados del sitio actual, renombrados con keywords.
- `assets/video/gt-hero-loop.webm` — loop del hero (VP9, 1080×1350, 15 s). Falta la versión MP4 H.264 para Safari/iOS; mientras tanto se muestra el poster.
- `assets/img/decanter-gea-vino-video.webp` — miniatura de la "fachada" del video de YouTube "GEA Multi-Purpose Wine Decanter" (GEA Group, id `TZMTGBaIxv8`). El iframe de `youtube-nocookie.com` se inyecta recién al hacer clic, así no pesa en PageSpeed ni carga cookies de terceros. Para cambiar el video: reemplazar `data-yt` en `index.html` y regenerar la miniatura. El video que usa el sitio actual como fondo es `orU0nog5SSc` ("Decanter Centrifuge for Sludge Treatment", también de GEA).
- Mapa de contacto: iframe de Google Maps (ficha GRUPO TECNOLOG SA) con `loading="lazy"`.
- Mapa de clientes: `assets/img/clients-map.svg`, SVG estático con provincias (datos Natural Earth, dominio público) y pines ilustrativos. Para cambiar pines o etiquetas, editar `PINS`/`LABELS` en `tools/make_map.py` y correr `python3 tools/make_map.py <ne_10m_admin_1_states_provinces.geojson>` (descargar de github.com/nvkelso/natural-earth-vector).
- `robots.txt`, `sitemap.xml`, `site.webmanifest` — SEO técnico.

## SEO

Title y description orientados a "centrífugas y decanters para bodegas, venta y alquiler, Mendoza"; JSON-LD `LocalBusiness` + `OfferCatalog`; Open Graph/Twitter; `alt` descriptivos; un solo `h1`; imágenes con `loading="lazy"` y preload del hero.
