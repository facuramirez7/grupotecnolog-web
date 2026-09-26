# Grupo Tecnolog — sitio web

Landing estática (HTML + CSS + JS, sin build) para [grupotecnolog.com](https://grupotecnolog.com/), con el estilo definido en `DESIGN.md`.

## Ver en local

```bash
python3 serve.py 8765
```

Abrí <http://127.0.0.1:8765>. `serve.py` es un servidor estático con soporte de `Range`, necesario para que el video del hero cargue en Chrome y Safari (el `http.server` estándar no lo soporta y el video no reproduce).

## Estructura

- `index.html` — página única con 9 secciones: header, hero, nosotros, servicios, proyectos, números, clientes, contacto y footer.
- El CSS va inline en el `<style>` de `index.html` (tokens y componentes del design system brutalista con la paleta de GT). Se inlinó a propósito: elimina el único recurso que bloqueaba el render y da 100 en PageSpeed.
- `assets/fonts/` — Barlow Condensed, Inter (variable) y JetBrains Mono autoalojadas en woff2.
- `.htaccess` — compresión, caché de un año para estáticos y cabeceras de seguridad (Apache).
- `assets/js/main.js` — menú mobile, link activo, contadores, reveal y formulario → WhatsApp.
- `assets/img/`, `assets/logos/` — fotos y logos tomados del sitio actual, renombrados con keywords.
- `assets/video/gt-hero-loop.webm` — loop del hero (VP9, 1080×1350, 15 s). Falta la versión MP4 H.264 para Safari/iOS; mientras tanto se muestra el poster.
- `assets/img/decanter-gea-vino-video.webp` — miniatura de la "fachada" del video de YouTube "GEA Multi-Purpose Wine Decanter" (GEA Group, id `TZMTGBaIxv8`). El iframe de `youtube-nocookie.com` se inyecta recién al hacer clic, así no pesa en PageSpeed ni carga cookies de terceros. Para cambiar el video: reemplazar `data-yt` en `index.html` y regenerar la miniatura. El video que usa el sitio actual como fondo es `orU0nog5SSc` ("Decanter Centrifuge for Sludge Treatment", también de GEA).
- Mapa: iframe de Google Maps (ficha GRUPO TECNOLOG SA) con `loading="lazy"` en la sección Contacto.
- `robots.txt`, `sitemap.xml`, `site.webmanifest` — SEO técnico.

## SEO

Title y description orientados a "centrífugas y decanters para bodegas, venta y alquiler, Mendoza"; JSON-LD `LocalBusiness` + `OfferCatalog`; Open Graph/Twitter; `alt` descriptivos; un solo `h1`; imágenes con `loading="lazy"` y preload del hero.
