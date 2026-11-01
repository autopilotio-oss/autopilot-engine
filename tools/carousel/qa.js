// Typesetting + QA pass for carousel slides. Runs in the page after fonts load, before screenshots.
// 1. data-fit="W"     : scale a one line element so its INK (not its box) is exactly W px wide.
// 2. data-stack="g"   : stack a group top to bottom with equal ink gaps (data-gap on the first, default 22).
//    data-after="g"   : put this element data-gap px (default 40) under the bottom of stack g.
// 3. optical align    : one line .fx elements whose left is within 20px of each other get their ink left edges
//                       snapped to the same x (fixes Anton side bearings: big type looks indented otherwise).
// 4. QA               : every text element must sit inside the safe area, not collide with other text, the logo
//                       or the page number, and aligned edges must match within 2px. Results -> window.QA.
(function () {
  const CV = document.createElement('canvas').getContext('2d');
  const SAFE = { x0: 40, x1: 1040, y0: 36, y1: 1316 };
  const transparent = c => c === 'transparent' || /rgba\(.*,\s*0\)$/.test(c);
  const px = v => parseFloat(v) || 0;
  function lineH(cs, m) { return cs.lineHeight === 'normal' ? m.fontBoundingBoxAscent + m.fontBoundingBoxDescent : px(cs.lineHeight); }
  function measure(el) {
    const cs = getComputedStyle(el);
    let t = el.innerText.replace(/\s+/g, ' ').trim();
    if (cs.textTransform === 'uppercase') t = t.toUpperCase();
    CV.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    CV.letterSpacing = cs.letterSpacing === 'normal' ? '0px' : cs.letterSpacing;
    return { cs, m: CV.measureText(t), t };
  }
  function oneLine(el) {
    const { cs, m } = measure(el);
    const h = el.getBoundingClientRect().height - px(cs.paddingTop) - px(cs.paddingBottom);
    return h <= lineH(cs, m) * 1.45 && !el.querySelector('br,div,pre,img');
  }
  // ink box in slide coordinates
  function ink(el) {
    const s = el.closest('.s').getBoundingClientRect(), r = el.getBoundingClientRect();
    const { cs, m } = measure(el);
    if (!transparent(cs.backgroundColor) || cs.transform !== 'none')
      return { x0: r.left - s.left, x1: r.right - s.left, y0: r.top - s.top, y1: r.bottom - s.top, box: 1 };
    if (!oneLine(el)) return inkMulti(el, s);
    const left = r.left - s.left + px(cs.paddingLeft) + px(cs.borderLeftWidth);
    const fh = m.fontBoundingBoxAscent + m.fontBoundingBoxDescent;
    const base = r.top - s.top + px(cs.paddingTop) + (lineH(cs, m) - fh) / 2 + m.fontBoundingBoxAscent;
    return { x0: left - m.actualBoundingBoxLeft, x1: left + m.actualBoundingBoxRight, y0: base - m.actualBoundingBoxAscent, y1: base + m.actualBoundingBoxDescent };
  }
  // multi line text: per line rects shrunk from font box to real ink, plus any highlight boxes inside
  function inkMulti(el, s) {
    const B = { x0: 1e9, x1: -1e9, y0: 1e9, y1: -1e9 };
    const add = (x0, x1, y0, y1) => { B.x0 = Math.min(B.x0, x0 - s.left); B.x1 = Math.max(B.x1, x1 - s.left); B.y0 = Math.min(B.y0, y0 - s.top); B.y1 = Math.max(B.y1, y1 - s.top); };
    for (const e of el.querySelectorAll('*')) { const c = getComputedStyle(e); if (!transparent(c.backgroundColor)) { const r = e.getBoundingClientRect(); add(r.left, r.right, r.top, r.bottom); } }
    const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let tn;
    while ((tn = w.nextNode())) {
      if (!tn.textContent.trim()) continue;
      const pe = tn.parentElement, c = getComputedStyle(pe);
      let t = tn.textContent; if (c.textTransform === 'uppercase') t = t.toUpperCase();
      CV.font = `${c.fontStyle} ${c.fontWeight} ${c.fontSize} ${c.fontFamily}`; const m = CV.measureText(t);
      const rg = document.createRange(); rg.selectNodeContents(tn);
      for (const r of rg.getClientRects()) {
        const fh = m.fontBoundingBoxAscent + m.fontBoundingBoxDescent, pad = (r.height - fh) / 2;
        add(r.left, r.right, r.top + pad + m.fontBoundingBoxAscent - m.actualBoundingBoxAscent, r.top + pad + m.fontBoundingBoxAscent + m.actualBoundingBoxDescent);
      }
    }
    return B.x0 > 1e8 ? (() => { const r = el.getBoundingClientRect(); return { x0: r.left - s.left, x1: r.right - s.left, y0: r.top - s.top, y1: r.bottom - s.top }; })() : B;
  }
  function fit(slide) {
    for (const el of slide.querySelectorAll('[data-fit]')) {
      const W = +el.dataset.fit;
      for (let k = 0; k < 3; k++) { const b = ink(el); el.style.fontSize = (px(getComputedStyle(el).fontSize) * W / (b.x1 - b.x0)) + 'px'; }
    }
  }
  function stack(slide) {
    const groups = {};
    slide.querySelectorAll('[data-stack]').forEach(el => (groups[el.dataset.stack] ||= []).push(el));
    const bottoms = {};
    for (const [g, els] of Object.entries(groups)) {
      els.sort((a, b) => px(a.style.top) - px(b.style.top));
      const gap = +(els[0].dataset.gap || 22);
      let y = ink(els[0]).y1;
      for (const el of els.slice(1)) { const b = ink(el); el.style.top = (px(el.style.top) + (y + gap - b.y0)) + 'px'; y = ink(el).y1; }
      bottoms[g] = y;
    }
    for (const el of slide.querySelectorAll('[data-after]')) {
      const y = bottoms[el.dataset.after]; if (y == null) continue;
      const b = ink(el); el.style.top = (px(el.style.top) + (y + +(el.dataset.gap || 40) - b.y0)) + 'px';
    }
  }
  function align(slide) {
    const els = [...slide.querySelectorAll('.fx')].filter(e => e.innerText.trim() && e.style.left && getComputedStyle(e).transform === 'none' && !e.dataset.free);
    const used = new Set();
    for (const a of els) {
      if (used.has(a)) continue;
      const grp = els.filter(e => !used.has(e) && Math.abs(px(e.style.left) - px(a.style.left)) <= 20);
      if (grp.length < 2) continue;
      const target = Math.min(...grp.map(e => px(e.style.left)));
      for (const e of grp) { used.add(e); const b = ink(e); e.style.left = (px(e.style.left) + target - b.x0) + 'px'; e.dataset.alignedTo = target; }
    }
  }
  function texts(slide) {
    const sel = '.fx,.ln,.chip,.band .h,.band .d,.band .n,.t,.b,.ph-sub,.ph-swipe,.ph-kick,.src,.why,.handle,.tagbox';
    return [...slide.querySelectorAll(sel)].filter(e => e.innerText.trim() && !e.parentElement.closest(sel.replace(/,/g, ',') ) || e.matches('.ln'))
      .filter(e => e.innerText.trim() && getComputedStyle(e).visibility !== 'hidden' && getComputedStyle(e).opacity !== '0');
  }
  function rgba(c) { const m = c.match(/[\d.]+/g) || [0, 0, 0, 0]; return m.length === 3 ? [+m[0], +m[1], +m[2], 1] : m.map(Number); }
  function lum([r, g, b]) { const f = v => (v /= 255) <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); }
  function bgOf(el) {
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (!transparent(cs.backgroundColor)) return rgba(cs.backgroundColor);
      const g = cs.backgroundImage.match(/rgba?\([^)]+\)|#[0-9a-f]{3,8}/i);
      if (g && cs.backgroundImage.includes('gradient')) return rgba(g[0]);
    }
    return [12, 12, 12, 1];
  }
  function contrast(el) {
    const c = rgba(getComputedStyle(el).color), bg = bgOf(el), a = c[3] ?? 1;
    const fg = [0, 1, 2].map(i => c[i] * a + bg[i] * (1 - a));
    const L1 = lum(fg), L2 = lum(bg); return (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
  }
  function qa(slide, n) {
    const out = [], els = texts(slide), boxes = els.map(e => [e, ink(e)]);
    const s = slide.getBoundingClientRect();
    const no = [...slide.querySelectorAll('.aplogo,.pg,.ph-div img')].map(e => { const r = e.getBoundingClientRect(); return [e.className, { x0: r.left - s.left, x1: r.right - s.left, y0: r.top - s.top, y1: r.bottom - s.top }]; });
    const name = e => (e.innerText.trim().slice(0, 28) || e.className).replace(/\s+/g, ' ');
    for (const [e, b] of boxes) {
      if (!e.matches('.tagbox') && (b.x0 < SAFE.x0 - .5 || b.x1 > SAFE.x1 + .5 || b.y0 < SAFE.y0 || b.y1 > SAFE.y1))
        out.push({ slide: n, level: 'error', msg: `"${name(e)}" outside safe area (${b.x0.toFixed(0)},${b.y0.toFixed(0)} to ${b.x1.toFixed(0)},${b.y1.toFixed(0)})` });
      for (const [cls, r] of no) if (b.x0 < r.x1 && b.x1 > r.x0 && b.y0 < r.y1 && b.y1 > r.y0)
        out.push({ slide: n, level: 'error', msg: `"${name(e)}" hits ${cls}` });
      const big = px(getComputedStyle(e).fontSize) >= 40, cr = contrast(e);
      if (cr < (big ? 3 : 4.5) && !e.dataset.lowcontrast)
        out.push({ slide: n, level: 'error', msg: `"${name(e)}" hard to read: contrast ${cr.toFixed(1)}:1` });
      if (e.dataset.alignedTo && Math.abs(b.x0 - +e.dataset.alignedTo) > 2)
        out.push({ slide: n, level: 'error', msg: `"${name(e)}" ink edge off by ${(b.x0 - e.dataset.alignedTo).toFixed(1)}px` });
      if (e.dataset.fit && Math.abs(b.x1 - b.x0 - +e.dataset.fit) > 3)
        out.push({ slide: n, level: 'error', msg: `"${name(e)}" width ${(b.x1 - b.x0).toFixed(0)} not ${e.dataset.fit}` });
    }
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
      const [a, A] = boxes[i], [c, C] = boxes[j];
      if (a.contains(c) || c.contains(a) || a.dataset.overlap || c.dataset.overlap) continue;
      if (getComputedStyle(a).transform !== 'none' || getComputedStyle(c).transform !== 'none') continue;
      const ox = Math.min(A.x1, C.x1) - Math.max(A.x0, C.x0), oy = Math.min(A.y1, C.y1) - Math.max(A.y0, C.y0);
      if (ox > 2 && oy > 2) out.push({ slide: n, level: 'error', msg: `"${name(a)}" collides with "${name(c)}" (${ox.toFixed(0)}x${oy.toFixed(0)}px)` });
    }
    return out;
  }
  window.TYPESET = function () {
    const res = [];
    document.querySelectorAll('.s').forEach((sl, i) => { fit(sl); stack(sl); align(sl); });
    document.querySelectorAll('.s').forEach((sl, i) => res.push(...qa(sl, i + 1)));
    window.QA = res; return res;
  };
})();
