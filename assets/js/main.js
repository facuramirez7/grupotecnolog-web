(function () {
  'use strict';

  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('menu');

  // Sombra del header al hacer scroll
  var onScroll = function () {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Menú mobile
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? toggle.getAttribute('data-open') : toggle.getAttribute('data-close'));
      menu.classList.toggle('is-open', !open);
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        menu.classList.remove('is-open');
      }
    });
  }

  // Link activo según sección visible
  var links = Array.prototype.slice.call(document.querySelectorAll('.menu a[href^="#"]'));
  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    var active = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) {
          a.classList.toggle('is-active', a.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(function (s) { active.observe(s); });
  }

  // Contadores de la sección Números
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var statsEl = document.querySelector('.stats');
  var locale = (statsEl && statsEl.getAttribute('data-locale')) || document.documentElement.lang || 'es-AR';
  var fmt = function (n) { return n.toLocaleString(locale); };
  var animate = function (el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var start = null, dur = 1400;
    var step = function (ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  var counters = document.querySelectorAll('.count');
  if (!reduce && 'IntersectionObserver' in window && counters.length) {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { animate(entry.target); obs.unobserve(entry.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { io.observe(c); });
  }

  // Reveal de tarjetas
  var revealTargets = document.querySelectorAll('.step-card, .project-card, .logo-grid li');
  if (!reduce && 'IntersectionObserver' in window) {
    var ro = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry, i) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px -5% 0px' });
    revealTargets.forEach(function (el, i) {
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 4) * 60 + 'ms';
      ro.observe(el);
    });
  }

  // Formulario → WhatsApp con mensaje prellenado
  var form = document.getElementById('form-contacto');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var v = function (id) { return (document.getElementById(id).value || '').trim(); };
      var l = function (name) { return form.getAttribute('data-l-' + name) || name; };
      var lines = [
        form.getAttribute('data-wa-intro') || '',
        l('name') + ': ' + v('f-nombre'),
        v('f-bodega') ? l('company') + ': ' + v('f-bodega') : '',
        l('email') + ': ' + v('f-email'),
        v('f-tel') ? l('phone') + ': ' + v('f-tel') : '',
        l('interest') + ': ' + v('f-interes'),
        v('f-msg') ? l('message') + ': ' + v('f-msg') : ''
      ].filter(Boolean);
      var url = 'https://wa.me/5492612770017?text=' + encodeURIComponent(lines.join('\n'));
      window.open(url, '_blank', 'noopener');
    });
  }

  // Video del hero: no reproducir si el usuario pide menos movimiento
  var heroVideo = document.querySelector('.hero-video');
  if (heroVideo && !reduce) {
    var startVideo = function () {
      heroVideo.play().catch(function () { /* el poster queda visible */ });
    };
    if (document.readyState === 'complete') startVideo();
    else window.addEventListener('load', startVideo, { once: true });
    // Si la pestaña estaba en segundo plano, el navegador bloquea el autoplay: reintentar al volver
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'visible' && heroVideo.paused) startVideo();
    });
  }

  // Fachada de YouTube: el iframe (y las cookies de YouTube) se cargan recién al hacer clic
  Array.prototype.forEach.call(document.querySelectorAll('.video-facade'), function (btn) {
    btn.addEventListener('click', function () {
      if (btn.classList.contains('is-playing')) return;
      var id = btn.getAttribute('data-yt');
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&modestbranding=1&hl=es';
      iframe.title = btn.getAttribute('aria-label').replace('Reproducir video: ', '');
      iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
      iframe.setAttribute('allowfullscreen', '');
      iframe.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
      btn.classList.add('is-playing');
      btn.appendChild(iframe);
    }, { once: true });
  });

  // Año del footer
  var y = document.getElementById('anio');
  if (y) y.textContent = String(new Date().getFullYear());
})();
