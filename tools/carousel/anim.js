// Kinetic cover: window.ANIM(t) poses the cover (#s1) at time t seconds for the animated cover video.
// Everything enters in reading order (top to bottom), then holds in the exact typeset layout, so the still (01.jpg)
// and the last frames match. Per element extras, detected automatically:
//   big money/number lines ("$6.3B", "70%") count up; terminal lines type in; .stampL slams down;
//   the swipe line nudges right every 1.4s after the intro (points people to the next slide).
(function () {
  let els = null;
  const clamp = x => Math.max(0, Math.min(1, x));
  const out3 = x => 1 - Math.pow(1 - x, 3);
  const back = x => { const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  function init() {
    const S = document.getElementById('s1'); if (!S) return [];
    const fg = S.querySelector('.lavafg') || S;
    const list = [...fg.children].filter(e => !e.matches('.grain,.aplogo,.pg,iframe,svg'));
    const o = list.map(e => ({ e, top: e.getBoundingClientRect().top, tf: e.style.transform || '', fs: parseFloat(getComputedStyle(e).fontSize) }));
    o.sort((a, b) => a.top - b.top);
    o.forEach((x, i) => {
      x.delay = 0.12 + i * 0.17; x.dir = i % 2 ? 1 : -1;
      const txt = x.e.textContent.trim();
      const m = txt.match(/^(\$?)(\d+(?:\.\d+)?)([BMK%]?)(\s.*)?$/i);
      if (m && x.fs >= 120) x.count = { pre: m[1], n: +m[2], dec: (m[2].split('.')[1] || '').length, suf: m[3], rest: m[4] || '', orig: x.e.innerHTML };
      const pre = x.e.querySelector('pre');
      if (pre) { pre.innerHTML = pre.innerHTML.split('\n').map(l => `<span class="tl">${l}</span>`).join('\n'); x.lines = [...pre.querySelectorAll('.tl')]; }
      if (x.e.classList.contains('stampL')) { x.stamp = 1; x.delay += 0.5; }
      if (/swipe/i.test(txt)) x.swipe = 1;
    });
    return o;
  }
  window.ANIM = function (t) {
    if (!els) els = init();
    for (const x of els) {
      const e = x.e, p = clamp((t - x.delay) / 0.6);
      let tr = '';
      if (x.stamp) {
        const s = 1 + 1.6 * (1 - out3(p));
        e.style.opacity = p > 0 ? Math.min(1, p * 3) : 0;
        tr = `scale(${s})`;
      } else if (x.fs >= 100) {                       // headline lines slide in from alternating sides
        e.style.opacity = clamp(p * 2.2);
        tr = `translateX(${(1 - back(p)) * 120 * x.dir}px)`;
      } else {
        e.style.opacity = out3(p);
        tr = `translateY(${(1 - back(p)) * 50}px)`;
      }
      if (x.swipe && p >= 1) { const ph = ((t - x.delay - 0.6) % 1.4) / 1.4; tr += ` translateX(${Math.sin(Math.min(1, ph * 2.5) * Math.PI) * 16}px)`; }
      e.style.transform = (tr + ' ' + x.tf).trim();
      if (x.count) {
        const q = clamp((t - x.delay) / 1.3);
        if (q < 1) e.textContent = x.count.pre + (x.count.n * out3(q)).toFixed(x.count.dec) + x.count.suf + x.count.rest;
        else e.innerHTML = x.count.orig;
      }
      if (x.lines) x.lines.forEach((l, k) => { l.style.visibility = t > x.delay + 0.35 + k * 0.38 ? 'visible' : 'hidden'; });
    }
  };
})();
