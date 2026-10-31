/* AUTOPILOT.OI site helper: analytics (GoatCounter), UTMs on checkout links, opt-in events,
   and a guard that greys out buy buttons for products not live on Gumroad (docs/live.json, written by the Gumroad sync). */
(function () {
  var page = (location.pathname.replace(/^\/|\/$/g, '') || 'home').replace(/\//g, '-');
  // Keep the visitor's first traffic source for the whole visit.
  var q = new URLSearchParams(location.search), src = null;
  try { src = q.get('utm_source') || sessionStorage.getItem('ap_src'); if (q.get('utm_source')) sessionStorage.setItem('ap_src', q.get('utm_source')); } catch (e) {}
  var camp = null; try { camp = q.get('utm_campaign') || sessionStorage.getItem('ap_camp'); if (q.get('utm_campaign')) sessionStorage.setItem('ap_camp', q.get('utm_campaign')); } catch (e) {}
  // GoatCounter (no cookies). Page views are automatic.
  var gc = document.createElement('script'); gc.async = true; gc.src = 'https://gc.zgo.at/count.js';
  gc.setAttribute('data-goatcounter', 'https://autopilotoi.goatcounter.com/count'); document.head.appendChild(gc);
  function ev(name) { try { if (window.goatcounter && goatcounter.count) goatcounter.count({ path: name, title: name, event: true }); } catch (e) {} }
  function slugOf(a) { var m = (a.getAttribute('href') || '').match(/gumroad\.com\/l\/([a-z0-9-]+)/i); return m ? m[1] : null; }
  function wire() {
    var links = Array.prototype.slice.call(document.querySelectorAll('a[href*="gumroad.com/l/"]'));
    links.forEach(function (a) {
      var slug = slugOf(a); if (!slug || a.dataset.apWired) return; a.dataset.apWired = '1';
      try {
        var u = new URL(a.href);
        u.searchParams.set('utm_source', src || 'site'); u.searchParams.set('utm_medium', 'site');
        u.searchParams.set('utm_campaign', camp || page); u.searchParams.set('utm_content', slug);
        a.href = u.toString();
      } catch (e) {}
      a.addEventListener('click', function () { ev('checkout-click/' + slug + '/' + page); });
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
    wire();
    var f = document.getElementById('kf'); if (f) f.addEventListener('submit', function () { ev('optin/' + page); });
    // Quiz: results are drawn after the last answer, so wire their links then and count the completion.
    var out = document.getElementById('out');
    if (out && window.MutationObserver) new MutationObserver(function () { if (!out.classList.contains('hide')) { ev('quiz-complete'); wire(); } }).observe(out, { attributes: true, attributeFilter: ['class'] });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
