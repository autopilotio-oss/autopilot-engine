/* AUTOPILOT.OI site helper: analytics (GoatCounter), UTMs on checkout links, opt-in events,
   and a guard that greys out buy buttons for products not live on Gumroad (docs/live.json, written by the Gumroad sync). */
(function () {
  var page = (location.pathname.replace(/^\/|\/$/g, '') || 'home').replace(/\//g, '-');
  // Attribution (Revenue Engine 2.0): keep the inbound UTM set for the visit (session) and the first known touch (local).
  // Missing values stay empty, so orders without a source are reported as "unknown", never guessed.
  var q = new URLSearchParams(location.search), K = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'], cur = {}, first = null;
  try {
    if (q.get('utm_source')) { K.forEach(function (k) { if (q.get(k)) sessionStorage.setItem('ap_' + k, q.get(k)); }); }
    K.forEach(function (k) { var v = sessionStorage.getItem('ap_' + k); if (v) cur[k] = v; });
    first = JSON.parse(localStorage.getItem('ap_first') || 'null');
    if (!first && cur.utm_source) { first = { s: cur.utm_source, c: cur.utm_campaign || '', t: new Date().toISOString().slice(0, 10) }; localStorage.setItem('ap_first', JSON.stringify(first)); }
  } catch (e) {}
  var src = cur.utm_source || null, camp = cur.utm_campaign || null;
  // Lead attribution: every Kit opt-in on the site posts a FormData to app.kit.com. Add the visit's UTM set and first touch
  // as Kit custom fields (utm_source, utm_campaign, utm_content, first_touch). Empty values are simply not sent.
  try {
    var _f = window.fetch;
    window.fetch = function (url, opt) {
      try {
        if (typeof url === 'string' && url.indexOf('app.kit.com/forms/') > -1 && opt && opt.body instanceof FormData) {
          ['utm_source', 'utm_campaign', 'utm_content'].forEach(function (k) { if (cur[k] && !opt.body.has('fields[' + k + ']')) opt.body.append('fields[' + k + ']', cur[k]); });
          if (first && first.s) opt.body.append('fields[first_touch]', first.s + (first.c ? ':' + first.c : '') + '@' + first.t);
        }
      } catch (e) {}
      return _f.apply(this, arguments);
    };
  } catch (e) {}
  // GoatCounter (no cookies). Page views are automatic.
  var gc = document.createElement('script'); gc.async = true; gc.src = 'https://gc.zgo.at/count.js';
  gc.setAttribute('data-goatcounter', 'https://autopilotoi.goatcounter.com/count'); document.head.appendChild(gc);
  function ev(name) { try { if (window.goatcounter && goatcounter.count) goatcounter.count({ path: name, title: name, event: true }); } catch (e) {} }
  var LAUNCH = { code: 'LAUNCH30', until: Date.parse('2026-11-11T03:00:00Z'), slugs: ['subs-agent', 'refund-agent', 'bill-agent', 'all-money-agents', 'raise-agent', 'debt-agent', 'shop-agent', 'video-agent', 'sell-agent', 'deposit-agent', 'workspace', 'tiktok-agents'] };
  LAUNCH.on = Date.now() < LAUNCH.until;
  function banner() {
    if (!LAUNCH.on || !document.querySelector('a[href*="gumroad.com/l/"]') || document.getElementById('ap-launch')) return;
    var b = document.createElement('div'); b.id = 'ap-launch';
    b.style.cssText = 'position:sticky;top:0;z-index:50;background:#D4FF3A;color:#050505;text-align:center;font:600 13px/1.3 "Chakra Petch",system-ui,sans-serif;padding:9px 12px;letter-spacing:.02em';
    b.textContent = 'Launch week: 30% off every agent with code LAUNCH30, applied at checkout. Ends Nov 10.';
    document.body.insertBefore(b, document.body.firstChild);
    Array.prototype.forEach.call(document.querySelectorAll('.ap-launch-price'), function (el) { el.style.display = 'block'; });
  }
  function slugOf(a) { var m = (a.getAttribute('href') || '').match(/gumroad\.com\/l\/([a-z0-9-]+)/i); return m ? m[1] : null; }
  function wire() {
    var links = Array.prototype.slice.call(document.querySelectorAll('a[href*="gumroad.com/l/"]'));
    links.forEach(function (a) {
      var slug = slugOf(a); if (!slug || a.dataset.apWired) return; a.dataset.apWired = '1';
      try {
        var u = new URL(a.href);
        // FIRST SALES MODE launch code (Seb approved, list prices unchanged): Gumroad applies /l/<slug>/<CODE> at checkout.
        if (LAUNCH.on && LAUNCH.slugs.indexOf(slug) > -1 && u.pathname.split('/').filter(Boolean).length === 2) u.pathname = u.pathname.replace(/\/$/, '') + '/' + LAUNCH.code;
        // Gumroad keeps these on the sale (url_params), which is how orders get joined to content.
        u.searchParams.set('utm_source', src || 'site'); u.searchParams.set('utm_medium', cur.utm_medium || (src ? 'organic_social' : 'site'));
        u.searchParams.set('utm_campaign', camp || page); u.searchParams.set('utm_content', cur.utm_content || ('site_' + page.replace(/[^a-z0-9]+/gi, '_').toLowerCase()));
        if (first && first.s) u.searchParams.set('ft', first.s + (first.c ? ':' + first.c : ''));
        a.href = u.toString();
      } catch (e) {}
      a.addEventListener('click', function () { ev('checkout-click/' + slug.replace(/-/g, '_') + '/' + page + '/' + (src || 'direct')); });
    });
    // Hide buy buttons for products that are not live yet. Fails open: if live.json can't load, links stay as they are.
    fetch('/live.json', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.live || !d.live.length) return;
      links.forEach(function (a) {
        var slug = slugOf(a); if (!slug || d.live.indexOf(slug) > -1) return;
        a.removeAttribute('href'); a.setAttribute('aria-disabled', 'true'); a.title = 'Coming soon';
        a.style.opacity = '.45'; a.style.pointerEvents = 'none';
        if (!a.children.length) a.textContent = 'Coming soon';
      });
    }).catch(function () {});
    // Email opt-ins (every Kit form on the site uses id kf).
  }
  function init() {
    banner(); wire();
    var f = document.getElementById('kf'); if (f) f.addEventListener('submit', function () { ev('optin/' + page + '/' + (src || 'direct')); });
    // Quiz: results are drawn after the last answer, so wire their links then and count the completion.
    var out = document.getElementById('out');
    if (out && window.MutationObserver) new MutationObserver(function () { if (!out.classList.contains('hide')) { ev('quiz-complete'); wire(); } }).observe(out, { attributes: true, attributeFilter: ['class'] });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
