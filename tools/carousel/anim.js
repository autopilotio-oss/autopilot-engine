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
      x.delay = 0.05 + i * 0.12; x.dir = i % 2 ? 1 : -1;
      const txt = x.e.textContent.trim();
      const m = txt.match(/^(\$?)(\d+(?:\.\d+)?)([BMK%]?)(\s.*)?$/i);
      if (m && x.fs >= 120) x.count = { pre: m[1], n: +m[2], dec: (m[2].split('.')[1] || '').length, suf: m[3], rest: m[4] || '', orig: x.e.innerHTML };
      const pre = x.e.querySelector('pre');
      if (pre) { pre.innerHTML = pre.innerHTML.split('\n').map(l => `<span class="tl">${l}</span>`).join('\n'); x.lines = [...pre.querySelectorAll('.tl')]; }
      if (x.e.classList.contains('stampL')) { x.stamp = 1; x.delay += 0.5; }
      if (/swipe/i.test(txt)) x.swipe = 1;
      if (x.e.dataset.stagger !== undefined) { x.kids = [...x.e.children]; x.stag = 1; }
      else { const sg = x.e.querySelector('[data-stagger]'); if (sg) { x.kids = [...sg.children]; x.stag = 1; } }
    });
    return o;
  }
  // NEVER BLANK (Seb, Nov 4: covers must not look empty at the start; the grid and the feed autoplay show early frames).
  // Every element is fully visible in every frame. Motion is a settle (small push and scale), pops and pulses, then a
  // gentle loop: tabs wave, the stamp re-slams and the swipe cue nudges, while the lava keeps moving underneath.
  let movers = null;
  window.ANIM = function (t) {
    if (!els) els = init();
    if (!movers) { const S = document.getElementById('s1'); movers = S ? [...S.querySelectorAll('[data-spin],[data-scroll],[data-float],[data-dash],[data-push]')] : []; movers.forEach(m => m.dataset.tf0 = m.style.transform || ''); }
    for (const m of movers) {                           // spinning badges and scrolling tickers (grid v2)
      if (m.dataset.push) { m.style.transform = `scale(${1.02 + Math.min(t, 16) * 0.004})`; continue; }
      if (m.dataset.dash) { m.style.strokeDashoffset = -(t * 260) % +m.dataset.dash; continue; }
      if (m.dataset.float) { m.style.transform = `translateY(${Math.sin(t * 1.3) * 12}px) rotate(${Math.sin(t * .9) * 1.2}deg) ` + m.dataset.tf0; continue; }
      if (m.dataset.spin) m.style.transform = `rotate(${(t * +m.dataset.spin) % 360}deg)`;
      else { const v = +m.dataset.scroll, w = m.scrollWidth / 2 || 1000; let x = (t * v) % w; if (v > 0) x -= w; m.style.transform = `translateX(${x}px)`; }
    }
    const loop = t > 3.2 ? ((t - 3.2) % 4) / 4 : -1;
    for (const x of els) {
      const e = x.e, p = clamp((t - x.delay) / 0.7);
      let tr = '';
      e.style.opacity = 1;
      if (x.e.matches('[data-scroll],[data-spin],[data-float]')) continue;
      if (x.stag) {                                     // tabs/chips: small pop in sequence, then a soft wave
        x.kids.forEach((c, k) => { const q = clamp((t - x.delay - k * 0.12) / 0.5);
          const w = loop >= 0 ? Math.max(0, Math.sin(clamp(loop * 3 - k * 0.12) * Math.PI)) * -10 : 0;
          c.style.opacity = 1; c.style.transform = `translateY(${(1 - back(q)) * 16 + w}px) scale(${0.9 + 0.1 * back(q)})`; });
      } else if (x.stamp) {                             // slam pulse at its turn and again each loop
        const q1 = clamp((t - x.delay - 0.6) / 0.45), q2 = loop >= 0 ? clamp(loop * 4) : 1;
        const s = 1 + 0.35 * Math.sin(q1 * Math.PI) * (q1 < 1) + 0.12 * Math.sin(q2 * Math.PI) * (q2 < 1);
        tr = `scale(${s})`;
      } else if (x.fs >= 100) {                         // headline lines settle into place
        tr = `scale(${1 + (1 - out3(p)) * 0.045})`; e.style.transformOrigin = '50% 50%';
      } else {
        tr = `translateY(${(1 - back(p)) * 14}px)`;
      }
      if (x.swipe && p >= 1) { const ph = ((t - x.delay - 0.7) % 1.4) / 1.4; tr += ` translateX(${Math.sin(Math.min(1, ph * 2.5) * Math.PI) * 16}px)`; }
      e.style.transform = (tr + ' ' + x.tf).trim();
      if (x.count) {                                    // count up from 60%, never from zero
        const q = clamp((t - x.delay) / 1.2);
        if (q < 1) { const v = (x.count.n * (0.6 + 0.4 * out3(q))).toFixed(x.count.dec); e.innerHTML = x.count.orig.replace(/(^|>)([^<\d]*)\d+(?:\.\d+)?/, `$1$2${v}`); }
        else e.innerHTML = x.count.orig;
      }
      if (x.lines) x.lines.forEach((l, k) => { l.style.visibility = 'visible'; l.style.opacity = t > x.delay + 0.35 + k * 0.38 ? 1 : 0.35; });
    }
  };
})();
