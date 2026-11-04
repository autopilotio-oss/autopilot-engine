/* AUTOPILOT.OI lava (Seb, Nov 4 2026: "the white, but the green lava inside more dynamic", "25% chrome like melted
   metal globs", "they can't mix different elements", "make it flawless").
   Glossy lime and liquid chrome metaballs on paper white. Each material melts only into itself; chrome and lime push
   each other apart. Globs flow around text and buttons (anything marked data-lava-avoid). One lime glob follows the
   pointer, scrolling stirs them, and in the hero one chrome glob drifts in front of the phone's edge.
   Markup: <div data-lava-scene="hero|strip"><canvas class="lava" data-lava="back"></canvas>
           [<canvas class="lava lava-front" data-lava="front"></canvas>] ...content... </div>
   Each scene pauses off screen; reduced motion gets one still frame; no WebGL keeps the CSS fallback. */
(function () {
  var N = 12, NC = 3;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var FS = [
    'precision highp float;',
    'uniform vec2 R;uniform vec3 B[' + N + '];uniform float T,FRONT;',
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
    'void main(){',
    ' vec2 uv=gl_FragCoord.xy/R.y;float e=1.5/R.y,w=1.2/R.y;',
    ' float sc=dC(uv,e);float iC=smoothstep(-w,w,sc);',
    ' if(FRONT>.5){gl_FragColor=vec4(chrome(nC(uv,e*1.5,.06),T)*iC,iC);return;}',
    ' float sl=dL(uv,e);float iL=smoothstep(-w,w,sl);',
    ' float sh=exp(-max(-sl,0.)*26.)*(1.-iL);',
    ' float dropL=smoothstep(.05,-.01,-dL(uv+vec2(.012,.02),e))*.10;',
    ' float dropC=smoothstep(.05,-.01,-dC(uv+vec2(.012,.024),e))*.16;',
    ' vec3 bg=PAPER-vec3(.10,.08,.12)*max(dropL,dropC)+LIME*sh*.10;',
    ' vec3 col=mix(bg,lime(nL(uv,e*1.5,.05)),iL);',
    ' col=mix(col,chrome(nC(uv,e*1.5,.06),T),iC);',
    ' gl_FragColor=vec4(col,1.);',
    '}'].join('\n');

  function makeGL(cv, front) {
    var gl = cv.getContext('webgl', { antialias: false, alpha: !!front, premultipliedAlpha: true });
    if (!gl) return null;
    function sh(t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; }
    var pr = gl.createProgram();
    gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return null;
    gl.useProgram(pr);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var lp = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
    var U = function (n) { return gl.getUniformLocation(pr, n); };
    gl.uniform1f(U('FRONT'), front ? 1 : 0);
    if (front) gl.clearColor(0, 0, 0, 0);
    return { gl: gl, cv: cv, uR: U('R'), uB: U('B'), uT: U('T') };
  }

  function rnd(i, k) { var x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); }
  var count = 0;

  function Scene(root) {
    var hero = (root.getAttribute('data-lava-scene') || 'hero') === 'hero';
    var back = root.querySelector('canvas[data-lava="back"]'), frontCv = root.querySelector('canvas[data-lava="front"]');
    if (!back) return;
    var B = makeGL(back, false);
    if (!B) { back.classList.add('lava-off'); return; }
    var F = frontCv && !reduce ? makeGL(frontCv, true) : null;
    var seed = hero ? 0 : 7 + (++count) * 13;
    var orb = [];
    for (var i = 0; i < N - 1; i++) {
      var c = i < NC, s = i + seed;
      orb.push({
        c: c, front: !!F && i === 2,
        cx: hero && c ? [.56, .56, .93][i] : (hero ? .28 + .62 * rnd(s, 1) : .04 + .92 * rnd(s, 1)),
        cy: hero && c ? [.24, .24, .70][i] : (hero ? .2 + .6 * rnd(s, 2) : .15 + .7 * rnd(s, 2)), cyM: hero ? (c ? [.16, .16, .30][i] : .04 + .30 * rnd(s, 2)) : (c ? .10 : .05 + .14 * rnd(s, 2)),
        ax: hero && c ? [.10, .10, .05][i] : .16 + .26 * rnd(s, 3), ay: hero && c ? [.14, .14, .16][i] : .14 + .26 * rnd(s, 4),
        sx: (c ? .22 : .24 + .30 * rnd(s, 5)) * (rnd(s, 6) > .5 ? 1 : -1), sy: (c ? .18 : .20 + .28 * rnd(s, 7)),
        ph: 6.28 * rnd(s, 8) + (i === 1 ? 3.14 : 0),
        r: (!hero && (i === 2 || i > NC + 4)) ? 0 : (c ? .075 + .02 * rnd(s, 9) : (hero ? .075 + .05 * rnd(s, 9) : .06 + .05 * rnd(s, 9))),
        pr: .5 + .7 * rnd(s, 10), pa: c ? .28 : .30 + .30 * rnd(s, 11),
        x: 0, y: 0, vx: 0, vy: 0, cr: 0, init: 0, ax2: 0, ay2: 0
      });
    }
    var data = new Float32Array(N * 3), fdata = new Float32Array(N * 3);
    var aspect = 1, ptr = { x: 9, y: .5, tx: .8, ty: .5, on: 0, vx: 0, vy: 0, act: 0 }, stir = 0, prevT = 0;
    var avoid = [], avoidFront = [];

    function rectsOf(sel) {
      var out = [], cr = back.getBoundingClientRect();
      if (!cr.height) return out;
      Array.prototype.forEach.call(root.querySelectorAll(sel), function (el) {
        var r = el.getBoundingClientRect(); if (!r.width) return;
        out.push([(r.left - cr.left) / cr.height, (r.right - cr.left) / cr.height, 1 - (r.bottom - cr.top) / cr.height, 1 - (r.top - cr.top) / cr.height]);
      });
      return out;
    }
    var freeX = 0;
    function measure() {
      avoid = rectsOf('[data-lava-avoid]'); avoidFront = rectsOf('[data-lava-avoid-front]');
      freeX = 0; avoid.forEach(function (R) { freeX = Math.max(freeX, R[1]); });
    }
    function size(G) {
      var r = G.cv.getBoundingClientRect();
      var s = Math.min(window.devicePixelRatio || 1, 2) * (r.width > 900 ? .5 : .6);
      var w = Math.max(2, Math.round(r.width * s)), h = Math.max(2, Math.round(r.height * s));
      G.cv.width = w; G.cv.height = h; G.gl.viewport(0, 0, w, h); G.gl.uniform2f(G.uR, w, h);
      return w / h;
    }
    function resize() { aspect = size(B); if (F) size(F); measure(); }

    function pushOut(o, rects, rad) {
      for (var q = 0; q < rects.length; q++) {
        var R = rects[q], m = rad * 1.45 + .025;
        var x0 = R[0] - m, x1 = R[1] + m, y0 = R[2] - m, y1 = R[3] + m;
        if (o.x > x0 && o.x < x1 && o.y > y0 && o.y < y1) {
          // escape through the nearest side that keeps the glob on the canvas
          var opts = [[o.x - x0, -1, 0, x0 > 0], [x1 - o.x, 1, 0, x1 < aspect], [o.y - y0, 0, -1, y0 > 0], [y1 - o.y, 0, 1, y1 < 1]];
          opts.sort(function (a, b) { return (a[3] === b[3]) ? a[0] - b[0] : (a[3] ? -1 : 1); });
          var e = opts[0], f = 260 * (e[0] + .02);
          o.ax2 += e[1] * f; o.ay2 += e[2] * f; o.vx *= .9; o.vy *= .9;
        }
      }
    }
    function step(t) {
      var dt = Math.min(.05, Math.max(.001, t - prevT || .016)); prevT = t;
      var k = 1 + stir * 2.2; stir *= .95;
      var rs = aspect < 1 ? Math.max(.42, aspect * 1.5) : (hero ? 1 : 1.55);
      for (var i = 0; i < orb.length; i++) {
        var o = orb[i], tt = t * k;
        var side = !hero && aspect - freeX > .5; // wide strip: globs live in the open space right of the words
        var fx = freeX + .08, fw = aspect - fx;
        var tx = side ? fx + fw * (.15 + .7 * (o.cx - .04) / .92) + Math.min(o.ax * aspect * .6, fw * .3) * Math.sin(tt * o.sx + o.ph)
                      : o.cx * aspect + o.ax * aspect * .6 * Math.sin(tt * o.sx + o.ph) + .06 * Math.sin(tt * o.sx * 2.7 + i * 1.3);
        var narrow = hero ? aspect < .8 : aspect < 1.2;
        var ty = (narrow ? o.cyM : o.cy) + (narrow ? (hero ? .10 : .05) : o.ay) * Math.cos(tt * o.sy + o.ph * 1.7) + .05 * Math.sin(tt * 1.3 + i * 2.1);
        if (o.c && i < 2) { tx += .10 * Math.cos(tt * .9 + o.ph) * (aspect < 1 ? 1 : .6); ty += .08 * Math.sin(tt * .9 + o.ph); }
        o.cr = rs * o.r * (1 + o.pa * Math.sin(tt * o.pr * 1.4 + o.ph));
        if (!o.init) { o.x = tx; o.y = ty; o.init = 1; }
        o.ax2 = (tx - o.x) * 7 - o.vx * 3.4; o.ay2 = (ty - o.y) * 7 - o.vy * 3.4;
      }
      ptr.vx += ((ptr.tx * aspect - ptr.x) * 10 - ptr.vx * 4.2) * dt; ptr.vy += ((ptr.ty - ptr.y) * 10 - ptr.vy * 4.2) * dt;
      ptr.x += ptr.vx * dt; ptr.y += ptr.vy * dt;
      ptr.on += ((ptr.act ? 1 : 0) - ptr.on) * .06;
      var pr = rs * (.07 + .02 * Math.sin(t * 2.1)) * ptr.on;
      // chrome and lime never touch
      for (var a = 0; a < orb.length; a++) {
        var A = orb[a]; if (!A.c) continue;
        for (var b = 0; b <= orb.length; b++) {
          var Bx, By, Br, Bo = null;
          if (b === orb.length) { if (pr < .005) continue; Bx = ptr.x; By = ptr.y; Br = pr; } else { Bo = orb[b]; if (Bo.c) continue; Bx = Bo.x; By = Bo.y; Br = Bo.cr; }
          var dx = A.x - Bx, dy = A.y - By, d = Math.sqrt(dx * dx + dy * dy) + 1e-5, m = (A.cr + Br) * 1.8 + .04;
          if (A.cr > 0 && Br > 0 && d < m) { var f = (m - d) / m * 130, nx = dx / d, ny = dy / d; A.ax2 += nx * f * .45; A.ay2 += ny * f * .45; if (Bo) { Bo.ax2 -= nx * f; Bo.ay2 -= ny * f; } }
        }
      }
      // flow around the words and buttons; the front glob also stays off the phone screen
      for (var z = 0; z < orb.length; z++) { var oz = orb[z]; pushOut(oz, avoid, oz.cr); if (oz.front) pushOut(oz, avoidFront, oz.cr * .55); }
      for (var u = 0; u < orb.length; u++) {
        var w = orb[u];
        w.vx += w.ax2 * dt; w.vy += w.ay2 * dt; w.x += w.vx * dt; w.y += w.vy * dt;
        data[u * 3] = w.x; data[u * 3 + 1] = w.y; data[u * 3 + 2] = w.cr;
        fdata[u * 3] = w.x; fdata[u * 3 + 1] = w.y; fdata[u * 3 + 2] = w.front ? w.cr : 0;
      }
      var j = (N - 1) * 3; data[j] = ptr.x; data[j + 1] = ptr.y; data[j + 2] = pr; fdata[j + 2] = 0;
    }
    function draw(t) {
      var g = B.gl; g.uniform1f(B.uT, t); g.uniform3fv(B.uB, data); g.drawArrays(g.TRIANGLE_STRIP, 0, 4);
      if (F) { var h = F.gl; h.clear(h.COLOR_BUFFER_BIT); h.uniform1f(F.uT, t); h.uniform3fv(F.uB, fdata); h.drawArrays(h.TRIANGLE_STRIP, 0, 4); }
    }
    function setPtr(cx, cy) {
      var r = back.getBoundingClientRect();
      if (cy < r.top || cy > r.bottom || cx < r.left || cx > r.right) { ptr.act = 0; return; }
      ptr.tx = (cx - r.left) / r.width; ptr.ty = 1 - (cy - r.top) / r.height;
      if (!ptr.act && ptr.on < .05) { ptr.x = ptr.tx * aspect; ptr.y = ptr.ty; ptr.vx = ptr.vy = 0; }
      ptr.act = 1;
    }
    window.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') setPtr(e.clientX, e.clientY); }, { passive: true });
    window.addEventListener('touchmove', function (e) { var t = e.touches[0]; if (t) setPtr(t.clientX, t.clientY); }, { passive: true });
    window.addEventListener('touchend', function () { ptr.act = 0; }, { passive: true });
    var lastY = window.scrollY;
    window.addEventListener('scroll', function () { var y = window.scrollY; stir = Math.min(1, stir + Math.abs(y - lastY) / 300); lastY = y; }, { passive: true });

    var clock = 4, visible = true, last = 0, raf = 0, mt = 0;
    window.addEventListener('resize', function () { resize(); step(clock); draw(clock); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    resize();
    for (var wi = 0; wi < 240; wi++) { clock += 1 / 60; step(clock); } // settle: nothing starts on top of words or the other metal
    draw(clock);
    back.classList.add('lava-on');
    if (reduce) return;
    function loop(now) {
      raf = 0;
      if (!visible || document.hidden) return;
      var dt = last ? Math.min(.05, (now - last) / 1000) : .016; last = now; clock += dt;
      if ((mt += dt) > 1) { mt = 0; measure(); }
      step(clock); draw(clock); raf = requestAnimationFrame(loop);
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible && !raf) { last = 0; raf = requestAnimationFrame(loop); } }, { rootMargin: '80px' }).observe(root);
    }
    document.addEventListener('visibilitychange', function () { if (!document.hidden && visible && !raf) { last = 0; raf = requestAnimationFrame(loop); } });
    raf = requestAnimationFrame(loop);
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-lava-scene]'), Scene);
})();
