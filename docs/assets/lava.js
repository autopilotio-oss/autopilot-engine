/* AUTOPILOT.OI lava, full page (Seb, Nov 4 2026: "the white, but the green lava more dynamic", "25% chrome like
   melted metal globs", "they can't mix", "smooth when we scroll", "over the full page ... fluid flow around the entire site").
   One fixed canvas behind the whole page, the size of the screen, so it costs the same at any page length.
   Globs drift on a smooth flow field like a lava lamp (rise, cool, sink), trail drips that pinch off and melt back,
   melt only into their own metal, push the other metal away, and flow around every word and button on screen.
   Scrolling drags them a little behind the page so they feel like liquid you are moving through.
   Reduced motion: one still frame. No WebGL: plain paper. */
(function () {
  var cv = document.querySelector('canvas[data-lava-page]');
  if (!cv) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // 0..2 chrome, 3 chrome drip, 4..11 lime, 12..16 lime drips, 17 pointer (mouse only)
  var N = 18, NC = 4;
  var gl = cv.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false, powerPreference: 'low-power' });
  if (!gl) return;
  var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var FS = [
    'precision highp float;',
    'uniform vec2 R;uniform vec3 B[' + N + '];uniform float T;',
    'const vec3 PAPER=vec3(.925,.925,.906);',
    'const vec3 LIME=vec3(.831,1.,.227);',
    'const vec3 DEEP=vec3(.56,.80,.02);',
    'float fL(vec2 p){float f=0.;for(int i=' + NC + ';i<' + N + ';i++){vec2 d=p-B[i].xy;float r=B[i].z;f+=r*r/(dot(d,d)+.00025);}return f;}',
    'float fC(vec2 p){float f=0.;for(int i=0;i<' + NC + ';i++){vec2 d=p-B[i].xy;float r=B[i].z;f+=r*r/(dot(d,d)+.00025);}return f;}',
    'float qL(vec2 p){return inversesqrt(fL(p)+1e-6);}float qC(vec2 p){return inversesqrt(fC(p)+1e-6);}',
    'float dL(vec2 p,float e){float q=qL(p);vec2 g=vec2(qL(p+vec2(e,0.))-qL(p-vec2(e,0.)),qL(p+vec2(0.,e))-qL(p-vec2(0.,e)))/(2.*e);return (1.-q)/max(length(g),1e-4);}',
    'float dC(vec2 p,float e){float q=qC(p);vec2 g=vec2(qC(p+vec2(e,0.))-qC(p-vec2(e,0.)),qC(p+vec2(0.,e))-qC(p-vec2(0.,e)))/(2.*e);return (1.-q)/max(length(g),1e-4);}',
    'float hL(vec2 p){return sqrt(clamp(1.-qL(p),0.,1.));}float hC(vec2 p){return sqrt(clamp(1.-qC(p),0.,1.));}',
    'vec3 nL(vec2 p,float e,float S){vec2 g=vec2(hL(p+vec2(e,0.))-hL(p-vec2(e,0.)),hL(p+vec2(0.,e))-hL(p-vec2(0.,e)))/(2.*e);return normalize(vec3(-g*S,1.));}',
    'vec3 nC(vec2 p,float e,float S){vec2 g=vec2(hC(p+vec2(e,0.))-hC(p-vec2(e,0.)),hC(p+vec2(0.,e))-hC(p-vec2(0.,e)))/(2.*e);return normalize(vec3(-g*S,1.));}',
    'vec3 lime(vec3 N3){vec3 L=normalize(vec3(-.45,.65,.9));float dif=clamp(dot(N3,L),0.,1.);',
    ' float spec=pow(clamp(dot(reflect(-L,N3),vec3(0.,0.,1.)),0.,1.),38.);float fres=pow(1.-clamp(N3.z,0.,1.),2.2);',
    ' return mix(DEEP,LIME,.35+.65*dif)+vec3(1.)*spec*.85+vec3(.95,1.,.75)*fres*.22;}',
    'vec3 chrome(vec3 N3,float t){vec3 r=reflect(vec3(0.,0.,-1.),N3);float y=r.y+.06*sin(r.x*2.5+t*.5);',
    ' vec3 c=mix(vec3(.86,.87,.88),vec3(1.),smoothstep(.15,.85,y));',
    ' if(y<-.05)c=mix(vec3(.50,.52,.53),vec3(.90,.91,.91),smoothstep(-.2,-.95,y));',
    ' c=mix(c,vec3(.13,.14,.15),exp(-pow((y+.03)/.10,2.))*.9);',
    ' c=mix(c,vec3(.55,.57,.58),exp(-pow((y-.5)/.12,2.))*.35);',
    ' float spec=pow(clamp(dot(reflect(-normalize(vec3(-.45,.65,.9)),N3),vec3(0.,0.,1.)),0.,1.),140.);',
    ' float rim=pow(1.-clamp(N3.z,0.,1.),2.5);',
    ' return c*(.82+.18*N3.z)-vec3(.22)*rim+vec3(1.)*spec*1.4;}',
    'float hash(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}',
    'void main(){',
    ' vec2 uv=gl_FragCoord.xy/R.y;float e=1.5/R.y,w=1.2/R.y;',
    ' float sl=dL(uv,e),sc=dC(uv,e);float iL=smoothstep(-w,w,sl),iC=smoothstep(-w,w,sc);',
    ' float sh=exp(-max(-sl,0.)*26.)*(1.-iL);',
    ' float dropL=smoothstep(.05,-.01,-dL(uv+vec2(.012,.02),e))*.10;',
    ' float dropC=smoothstep(.05,-.01,-dC(uv+vec2(.012,.024),e))*.16;',
    ' vec3 bg=PAPER-vec3(.10,.08,.12)*max(dropL,dropC)+LIME*sh*.10+(hash(gl_FragCoord.xy)-.5)*.022;',
    ' vec3 col=mix(bg,lime(nL(uv,e*1.5,.085)),iL);',
    ' col=mix(col,chrome(nC(uv,e*1.5,.06),T),iC);',
    ' gl_FragColor=vec4(col,1.);',
    '}'].join('\n');
  function sh(t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; }
  var pr = gl.createProgram();
  gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
  gl.useProgram(pr);
  var bf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  var lp = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
  var uR = gl.getUniformLocation(pr, 'R'), uB = gl.getUniformLocation(pr, 'B'), uT = gl.getUniformLocation(pr, 'T');

  function rnd(i, k) { var x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); }
  var aspect = 1, cssH = 1, cssW = 1;
  function mk(i, c) {
    return { c: c, x: .1 + .8 * rnd(i, 1), y: .1 + .8 * rnd(i, 2), vx: 0, vy: 0, ax: 0, ay: 0, cr: 0,
      r: c ? .068 + .016 * rnd(i, 3) : .07 + .05 * rnd(i, 3), ph: 6.28 * rnd(i, 4), pr: .5 + .6 * rnd(i, 5), pa: c ? .22 : .28 + .25 * rnd(i, 6),
      heat: 6.28 * rnd(i, 7), hs: .10 + .10 * rnd(i, 8),
      // each glob tours the whole screen on its own slow loop (20 to 45 s per lap), corner to corner
      wx: .14 + .16 * rnd(i, 14), wy: .11 + .15 * rnd(i, 15), wpx: 6.28 * rnd(i, 16), wpy: 6.28 * rnd(i, 17) };
  }
  var mains = [];
  for (var i = 0; i < 3; i++) mains.push(mk(i, true));
  for (i = 0; i < 8; i++) mains.push(mk(10 + i, false));
  function drip(P, k) { return { c: P.c, tail: 1, P: P, x: P.x, y: P.y - .05, vx: 0, vy: 0, ax: 0, ay: 0, cr: 0, ph: 6.28 * rnd(k, 21) }; }
  var orb = [mains[0], mains[1], mains[2], drip(mains[0], 1)];
  for (i = 3; i < 11; i++) orb.push(mains[i]);
  for (i = 0; i < 5; i++) orb.push(drip(mains[3 + i], 2 + i));
  var data = new Float32Array(N * 3);
  var ptr = { x: 9, y: .5, tx: .5, ty: .5, vx: 0, vy: 0, on: 0, act: 0 };

  // smooth flow field (sum of a few rotating waves): fluid, no sudden turns
  function flow(x, y, t, o) {
    var a = Math.sin(y * 3.1 + t * .23 + o) + Math.sin((x + y) * 2.3 - t * .17), b = Math.cos(x * 2.7 - t * .19 + o * 1.3) + Math.cos((x - y) * 1.9 + t * .21);
    return [a, b];
  }

  // words and buttons on screen, in canvas units; read once a frame
  var SEL = '[data-lava-avoid],.s5 .st5 b,.hx h1,.s5 h1,.hx h2,.s5 h2,.hx h3,.s5 h3,.hx p,.s5 p,.hx li,.s5 li,.hx .lab,.s5 .lab,.hx .b5,.s5 .b5,.hx .trust span,.s5 .trust span,.hx .ag-n,.s5 .ag-n,.hx .ag-pr,.s5 .ag-pr,.hx .ag-t,.s5 .ag-t,.hx .fd,.s5 .fd,.hx .pcap,.s5 .pcap,.hx summary,.s5 summary';
  var BIG = 'h1,h2,h3,.b5,[data-lava-avoid],.ag-pr,.lab,.st5 b,.ag-n';
  var els = [], big = [], rects = [], rectsBig = [];
  function collect() {
    els = Array.prototype.filter.call(document.querySelectorAll(SEL), function (el) { return !el.closest('.bd,.ph,.tb,.sm,.rc,.tg>div,.tk>div,.cp5'); });
    big = els.map(function (el) { return el.matches(BIG) || !!el.closest('[data-lava-avoid]'); });
  }
  function readRects() {
    rects.length = 0; rectsBig.length = 0;
    for (var q = 0; q < els.length; q++) {
      var r = els[q].getBoundingClientRect();
      if (r.bottom < -40 || r.top > cssH + 40 || !r.width) continue;
      var R = [r.left / cssH, r.right / cssH, 1 - r.bottom / cssH, 1 - r.top / cssH]; rects.push(R); if (big[q]) rectsBig.push(R);
    }
    // solid boxes (phone, cards) hide the globs behind them anyway; no need to avoid them
  }
  function resize() {
    cssW = window.innerWidth; cssH = Math.max(window.innerHeight, document.documentElement.clientHeight);
    var r = cv.getBoundingClientRect(); cssH = r.height || cssH; cssW = r.width || cssW;
    var s = Math.min(window.devicePixelRatio || 1, 2) * (cssW > 900 ? .5 : .45);
    var px = cssW * cssH * s * s; if (px > 420000) s *= Math.sqrt(420000 / px);
    var w = Math.max(2, Math.round(cssW * s)), h = Math.max(2, Math.round(cssH * s));
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; gl.viewport(0, 0, w, h); gl.uniform2f(uR, w, h); }
    aspect = cssW / cssH;
  }

  function repelRects(o, rad, list) {
    var m = rad * 1.6 + .025, hit = 0;
    for (var q = 0; q < list.length; q++) {
      var R = list[q];
      // distance from the glob centre to the box (negative inside); push along the shortest way out
      var cx = Math.max(R[0], Math.min(o.x, R[1])), cy = Math.max(R[2], Math.min(o.y, R[3]));
      var dx = o.x - cx, dy = o.y - cy, d = Math.sqrt(dx * dx + dy * dy), nx, ny, pen;
      if (d > 1e-5) { if (d > m) continue; nx = dx / d; ny = dy / d; pen = m - d; }
      else {
        var l = o.x - R[0], rr = R[1] - o.x, b = o.y - R[2], tp = R[3] - o.y, mn = Math.min(l, rr, b, tp);
        nx = mn === l ? -1 : mn === rr ? 1 : 0; ny = mn === b ? -1 : mn === tp ? 1 : 0; pen = m + mn;
      }
      var f = 320 * pen; o.ax += nx * f; o.ay += ny * f; hit = Math.max(hit, pen / m);
    }
    return hit;
  }

  var ph = 0, lastScroll = window.scrollY;
  function step(t, dt) {
    ph += dt;
    var rs = aspect < 1 ? Math.max(.5, aspect * 1.4) : 1;
    // scrolling: the liquid lags behind the page a little, then settles (eased, never a jump)
    var sy = window.scrollY, dsc = (sy - lastScroll) / cssH; lastScroll = sy;
    for (var i = 0; i < orb.length; i++) {
      var o = orb[i]; o.ax = 0; o.ay = 0;
      if (o.tail) continue;
      o.cr = rs * o.r * (1 + o.pa * Math.sin(ph * o.pr + o.ph));
      var fl = flow(o.x / Math.max(aspect, .6), o.y, ph, o.ph);
      var gxT = aspect * (.5 + .46 * Math.sin(ph * o.wx + o.wpx)), gyT = .5 + .46 * Math.sin(ph * o.wy + o.wpy);
      o.ax += (gxT - o.x) * .55; o.ay += (gyT - o.y) * .55;
      o.ax += fl[0] * .045; o.ay += fl[1] * .035;
      o.ay += Math.sin(ph * o.hs + o.heat) * .05;                  // lava lamp: warm globs rise, cool ones sink
      o.ay += dsc * 60 * (o.c ? .5 : .8);                        // scroll drag
      // soft walls: globs may peek past the edges but drift back in
      var pad = o.cr * .6;
      if (o.x < -pad) o.ax += (-pad - o.x) * 6; if (o.x > aspect + pad) o.ax += (aspect + pad - o.x) * 6;
      if (o.y < -pad) o.ay += (-pad - o.y) * 6; if (o.y > 1 + pad) o.ay += (1 + pad - o.y) * 6;
      o.ax -= o.vx * 1.4; o.ay -= o.vy * 1.4;
    }
    // the two big chrome globs like each other: they keep finding each other, melt, split
    var A0 = orb[0], A1 = orb[1], ddx = A1.x - A0.x, ddy = A1.y - A0.y, dd = Math.sqrt(ddx * ddx + ddy * ddy) + 1e-5, pull = Math.max(0, dd - .12) * .8;
    A0.ax += ddx / dd * pull; A0.ay += ddy / dd * pull; A1.ax -= ddx / dd * pull; A1.ay -= ddy / dd * pull;
    // drips trail their parent on a loose spring
    for (i = 0; i < orb.length; i++) {
      var q = orb[i]; if (!q.tail) continue; var P = q.P;
      var gx = P.x - P.vx * .22 + .012 * Math.sin(t * 1.1 + q.ph), gy = P.y - P.vy * .22 - P.cr * .55;
      q.cr = P.cr * (.48 + .10 * Math.sin(t * 1.7 + q.ph));
      q.ax = (gx - q.x) * 3.2 - q.vx * 1.7; q.ay = (gy - q.y) * 3.2 - q.vy * 1.7;
    }
    // mouse glob
    ptr.vx += ((ptr.tx * aspect - ptr.x) * 10 - ptr.vx * 4.2) * dt; ptr.vy += ((ptr.ty - ptr.y) * 10 - ptr.vy * 4.2) * dt;
    ptr.x += ptr.vx * dt; ptr.y += ptr.vy * dt; ptr.on += ((ptr.act ? 1 : 0) - ptr.on) * Math.min(1, dt * 4);
    var prr = rs * (.065 + .015 * Math.sin(t * 2.1)) * ptr.on;
    // chrome and lime never touch
    for (var a = 0; a < orb.length; a++) {
      var A = orb[a]; if (!A.c) continue;
      for (var b = 0; b <= orb.length; b++) {
        var Bx, By, Br, Bo = null;
        if (b === orb.length) { if (prr < .005) continue; Bx = ptr.x; By = ptr.y; Br = prr; } else { Bo = orb[b]; if (Bo.c) continue; Bx = Bo.x; By = Bo.y; Br = Bo.cr; }
        var dx = A.x - Bx, dy = A.y - By, d = Math.sqrt(dx * dx + dy * dy) + 1e-5, m = (A.cr + Br) * 1.8 + .04;
        if (d < m) { var f = (m - d) / m * 40, nx = dx / d, ny = dy / d; A.ax += nx * f * .5; A.ay += ny * f * .5; if (Bo) { Bo.ax -= nx * f; Bo.ay -= ny * f; } }
      }
    }
    // flow around every word and button on screen
    for (i = 0; i < orb.length; i++) {
      // chrome keeps clear of every word; lime may glide behind body text (black on lime reads fine) but never
      // behind headlines, buttons, prices or the lime highlights
      var oo = orb[i], hit = repelRects(oo, oo.cr, oo.c ? rects : rectsBig);
      // a glob trapped deep among words squeezes thin and slips through, then swells back in open space
      var deep = hit > .45;
      oo.sq = (oo.sq || 1) + ((deep ? .62 : 1) - (oo.sq || 1)) * Math.min(1, dt * (deep ? 4 : 1.2));
      if (deep) { oo.vx *= 1 - dt * 2; oo.vy *= 1 - dt * 2; }
    }
    for (i = 0; i < orb.length; i++) {
      var w = orb[i];
      w.vx += w.ax * dt; w.vy += w.ay * dt;
      var sp = Math.sqrt(w.vx * w.vx + w.vy * w.vy), mx = w.tail ? 1.2 : .5; if (sp > mx) { w.vx *= mx / sp; w.vy *= mx / sp; }
      w.x += w.vx * dt; w.y += w.vy * dt;
      data[i * 3] = w.x; data[i * 3 + 1] = w.y; data[i * 3 + 2] = w.cr * (w.sq || 1);
    }
    var j = (N - 1) * 3; data[j] = ptr.x; data[j + 1] = ptr.y; data[j + 2] = prr;
  }
  function draw(t) { gl.uniform1f(uT, t); gl.uniform3fv(uB, data); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); }

  window.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse') return;
    ptr.tx = e.clientX / cssW; ptr.ty = 1 - e.clientY / cssH;
    if (!ptr.act && ptr.on < .05) { ptr.x = ptr.tx * aspect; ptr.y = ptr.ty; ptr.vx = ptr.vy = 0; }
    ptr.act = 1;
  }, { passive: true });
  document.addEventListener('mouseleave', function () { ptr.act = 0; });

  var clock = 0, last = 0, raf = 0, acc = 0, H = 1 / 120, rc = 0;
  window.addEventListener('resize', function () { resize(); });
  collect(); resize(); readRects();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { collect(); readRects(); });
  for (var wi = 0; wi < 900; wi++) { clock += H; step(clock, H); } // settle off the words before the first frame
  draw(clock);
  cv.classList.add('on');
  if (reduce) return;
  function loop(now) {
    raf = 0;
    if (document.hidden) return;
    var dt = last ? Math.min(.05, (now - last) / 1000) : .016; last = now; clock += dt;
    if ((rc += dt) > 2) { rc = 0; collect(); }
    readRects();
    acc += dt; var n = 0;
    while (acc >= H && n < 8) { acc -= H; n++; step(clock - acc, H); }
    draw(clock); raf = requestAnimationFrame(loop);
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden && !raf) { last = 0; raf = requestAnimationFrame(loop); } });
  raf = requestAnimationFrame(loop);
})();
