/* AUTOPILOT.OI lava background (Seb, Nov 4 2026: "the white, but the green lava inside more dynamic", plus "25% chrome like melted metal globs").
   Glossy lime metaballs on paper white. Blobs drift on their own orbits, swell and shrink so they merge and split,
   one blob follows the pointer or finger, scrolling stirs them. Pauses off screen, one still frame for reduced motion.
   Usage: <canvas class="lava" data-lava></canvas> inside a position:relative parent. */
(function () {
  var cv = document.querySelector('canvas[data-lava]');
  if (!cv) return;
  var gl = cv.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false });
  if (!gl) { cv.classList.add('lava-off'); return; }
  var N = 12, NC = 3; // blobs 0..NC-1 are liquid chrome (about 25%), the rest lime; last blob follows the pointer. Chrome and lime never touch (they push each other away), each melts only into its own kind.
  var vs = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var fs = [
    'precision highp float;',
    'uniform vec2 R;uniform vec3 B[' + N + '];',
    'const vec3 PAPER=vec3(.925,.925,.906);',
    'const vec3 LIME=vec3(.831,1.,.227);',
    'const vec3 DEEP=vec3(.56,.80,.02);',
    'float fL(vec2 p){float f=0.;for(int i=' + NC + ';i<' + N + ';i++){vec2 d=p-B[i].xy;float r=B[i].z;f+=r*r/(dot(d,d)+.00025);}return f;}',
    'float fC(vec2 p){float f=0.;for(int i=0;i<' + NC + ';i++){vec2 d=p-B[i].xy;float r=B[i].z;f+=r*r/(dot(d,d)+.00025);}return f;}',
    'float qL(vec2 p){return inversesqrt(fL(p));}float qC(vec2 p){return inversesqrt(fC(p));}',
    // surface info: x=signed distance, yz=normal
    'vec3 surfL(vec2 uv,float e){float q=qL(uv);vec2 g=vec2(qL(uv+vec2(e,0.))-qL(uv-vec2(e,0.)),qL(uv+vec2(0.,e))-qL(uv-vec2(0.,e)))/(2.*e);float gn=max(length(g),1e-4);return vec3((1.-q)/gn,g/gn);}',
    'vec3 surfC(vec2 uv,float e){float q=qC(uv);vec2 g=vec2(qC(uv+vec2(e,0.))-qC(uv-vec2(e,0.)),qC(uv+vec2(0.,e))-qC(uv-vec2(0.,e)))/(2.*e);float gn=max(length(g),1e-4);return vec3((1.-q)/gn,g/gn);}',
    'float hL(vec2 p){return sqrt(clamp(1.-qL(p),0.,1.));}float hC(vec2 p){return sqrt(clamp(1.-qC(p),0.,1.));}',
    'vec3 nL(vec2 p,float e,float S){vec2 g=vec2(hL(p+vec2(e,0.))-hL(p-vec2(e,0.)),hL(p+vec2(0.,e))-hL(p-vec2(0.,e)))/(2.*e);return normalize(vec3(-g*S,1.));}',
    'vec3 nC(vec2 p,float e,float S){vec2 g=vec2(hC(p+vec2(e,0.))-hC(p-vec2(e,0.)),hC(p+vec2(0.,e))-hC(p-vec2(0.,e)))/(2.*e);return normalize(vec3(-g*S,1.));}',
    'vec3 lime(vec3 N3){vec3 L=normalize(vec3(-.45,.65,.9));float dif=clamp(dot(N3,L),0.,1.);',
    ' float spec=pow(clamp(dot(reflect(-L,N3),vec3(0.,0.,1.)),0.,1.),38.);float fres=pow(1.-clamp(N3.z,0.,1.),2.2);',
    ' return mix(DEEP,LIME,.35+.65*dif)+vec3(1.)*spec*.85+vec3(.95,1.,.75)*fres*.22;}',
    // liquid chrome: reflect a studio: bright sky, dark horizon band, warm floor, lime bounce from the glass around it
    'vec3 chrome(vec3 N3,float t){vec3 r=reflect(vec3(0.,0.,-1.),N3);float y=r.y+.06*sin(r.x*2.5+t*.5);',
    ' vec3 c=mix(vec3(.86,.87,.88),vec3(1.),smoothstep(.15,.85,y));',
    ' if(y<-.05)c=mix(vec3(.50,.52,.53),vec3(.90,.91,.91),smoothstep(-.2,-.95,y));',
    ' c=mix(c,vec3(.13,.14,.15),exp(-pow((y+.03)/.10,2.))*.9);',
    ' c=mix(c,vec3(.55,.57,.58),exp(-pow((y-.5)/.12,2.))*.35);',
    ' float spec=pow(clamp(dot(reflect(-normalize(vec3(-.45,.65,.9)),N3),vec3(0.,0.,1.)),0.,1.),140.);',
    ' float rim=pow(1.-clamp(N3.z,0.,1.),2.5);',
    ' return c*(.82+.18*N3.z)-vec3(.22)*rim+vec3(1.)*spec*1.4;}',
    'uniform float T;',
    'void main(){',
    ' vec2 uv=gl_FragCoord.xy/R.y;float e=1.5/R.y,w=1.2/R.y;',
    ' vec3 sl=surfL(uv,e),sc=surfC(uv,e);',
    ' float iL=smoothstep(-w,w,sl.x),iC=smoothstep(-w,w,sc.x);',
    ' float sh=exp(-max(-sl.x,0.)*26.)*(1.-iL);',
    ' float dropL=smoothstep(.05,-.01,-surfL(uv+vec2(.012,.02),e).x)*.10;',
    ' float dropC=smoothstep(.05,-.01,-surfC(uv+vec2(.012,.024),e).x)*.16;',
    ' vec3 bg=PAPER-vec3(.10,.08,.12)*max(dropL,dropC)+LIME*sh*.10;',
    ' vec3 col=mix(bg,lime(nL(uv,e*1.5,.05)),iL);',
    ' float front=smoothstep(-.006,.006,sc.x-sl.x+.004);', // chrome sits in front where it is deeper
    ' col=mix(col,chrome(nC(uv,e*1.5,.06),T),iC*max(front,1.-iL));',
    ' gl_FragColor=vec4(col,1.);',
    '}'].join('\n');
  function sh(t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; }
  var pr = gl.createProgram();
  gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) { cv.classList.add('lava-off'); return; }
  gl.useProgram(pr);
  var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  var lp = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
  var uR = gl.getUniformLocation(pr, 'R'), uB = gl.getUniformLocation(pr, 'B'), uT = gl.getUniformLocation(pr, 'T');

  // Motion: every blob chases a moving target on its own looping path (springy, so it overshoots and wobbles),
  // swells and shrinks so same material blobs melt together and split, and chrome and lime repel each other.
  function rnd(i, k) { var x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); }
  var orb = [];
  for (var i = 0; i < N - 1; i++) {
    var c = i < NC;
    orb.push({
      c: c,
      cx: c ? [.56, .56, .95][i] : .28 + .62 * rnd(i, 1), cy: c ? [.28, .28, .72][i] : .2 + .6 * rnd(i, 2),
      ax: c ? [.10, .10, .06][i] : .16 + .26 * rnd(i, 3), ay: c ? [.16, .16, .18][i] : .14 + .26 * rnd(i, 4),
      sx: (c ? .22 : .24 + .30 * rnd(i, 5)) * (rnd(i, 6) > .5 ? 1 : -1), sy: (c ? .18 : .20 + .28 * rnd(i, 7)),
      ph: 6.28 * rnd(i, 8) + (i === 1 ? 3.14 : 0),
      r: c ? .075 + .02 * rnd(i, 9) : .075 + .05 * rnd(i, 9),
      pr: .5 + .7 * rnd(i, 10), pa: c ? .28 : .30 + .30 * rnd(i, 11),
      x: 0, y: 0, vx: 0, vy: 0, cr: 0, init: 0
    });
  }
  var data = new Float32Array(N * 3);
  var W = 1, H = 1, aspect = 1, ptr = { x: 1.2, y: .55, tx: .78, ty: .55, on: 0, vx: 0, vy: 0 }, stir = 0, lastY = window.scrollY, prevT = 0;

  function resize() {
    var r = cv.getBoundingClientRect();
    var s = Math.min(window.devicePixelRatio || 1, 2) * (r.width > 900 ? .5 : .6);
    W = Math.max(2, Math.round(r.width * s)); H = Math.max(2, Math.round(r.height * s));
    cv.width = W; cv.height = H; aspect = W / H;
    gl.viewport(0, 0, W, H); gl.uniform2f(uR, W, H);
  }
  function frame(t, nodraw) {
    var dt = Math.min(.05, Math.max(.001, t - prevT || .016)); prevT = t;
    var k = 1 + stir * 2.2; stir *= .95;
    var rs = aspect < 1 ? Math.max(.42, aspect * 1.5) : 1;
    // targets, sizes
    for (var i = 0; i < orb.length; i++) {
      var o = orb[i], tt = t * k;
      var tx = o.cx * aspect + o.ax * aspect * .6 * Math.sin(tt * o.sx + o.ph) + .06 * Math.sin(tt * o.sx * 2.7 + i * 1.3);
      var ty = o.cy + o.ay * Math.cos(tt * o.sy + o.ph * 1.7) + .05 * Math.sin(tt * 1.3 + i * 2.1);
      if (o.c && i < 2) { tx += .10 * Math.cos(tt * .9 + o.ph) * (aspect < 1 ? 1 : .6); ty += .08 * Math.sin(tt * .9 + o.ph); } // the chrome pair circles, melts, splits
      o.cr = rs * o.r * (1 + o.pa * Math.sin(tt * o.pr * 1.4 + o.ph));
      if (!o.init) { o.x = tx; o.y = ty; o.init = 1; }
      o.ax2 = (tx - o.x) * 7 - o.vx * 3.4; o.ay2 = (ty - o.y) * 7 - o.vy * 3.4;
    }
    // pointer blob (lime)
    ptr.vx += ((ptr.tx * aspect - ptr.x) * 10 - ptr.vx * 4.2) * dt; ptr.vy += ((ptr.ty - ptr.y) * 10 - ptr.vy * 4.2) * dt;
    ptr.x += ptr.vx * dt; ptr.y += ptr.vy * dt;
    ptr.on += ((ptr.act ? 1 : .6) - ptr.on) * .05;
    var pr = rs * (.07 + .02 * Math.sin(t * 2.1)) * ptr.on;
    // chrome and lime never touch: push apart any chrome / lime pair that gets close
    for (var a2 = 0; a2 < orb.length; a2++) {
      var A = orb[a2]; if (!A.c) continue;
      for (var b2 = 0; b2 <= orb.length; b2++) {
        var Bx, By, Br, Bo = null;
        if (b2 === orb.length) { Bx = ptr.x; By = ptr.y; Br = pr; } else { Bo = orb[b2]; if (Bo.c) continue; Bx = Bo.x; By = Bo.y; Br = Bo.cr; }
        var dx = A.x - Bx, dy = A.y - By, d = Math.sqrt(dx * dx + dy * dy) + 1e-5, m = (A.cr + Br) * 1.55 + .035;
        if (d < m) {
          var f = (m - d) / m * 60, nx = dx / d, ny = dy / d;
          A.ax2 += nx * f * .45; A.ay2 += ny * f * .45;
          if (Bo) { Bo.ax2 -= nx * f; Bo.ay2 -= ny * f; }
        }
      }
    }
    for (var i2 = 0; i2 < orb.length; i2++) {
      var o3 = orb[i2];
      o3.vx += o3.ax2 * dt; o3.vy += o3.ay2 * dt; o3.x += o3.vx * dt; o3.y += o3.vy * dt;
      data[i2 * 3] = o3.x; data[i2 * 3 + 1] = o3.y; data[i2 * 3 + 2] = o3.cr;
    }
    var j = (N - 1) * 3;
    data[j] = ptr.x; data[j + 1] = ptr.y; data[j + 2] = pr;
    if (nodraw) return;
    gl.uniform1f(uT, t); gl.uniform3fv(uB, data); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  function setPtr(cx, cy) {
    var r = cv.getBoundingClientRect();
    if (cy < r.top || cy > r.bottom) { ptr.act = 0; return; }
    ptr.tx = (cx - r.left) / r.width; ptr.ty = 1 - (cy - r.top) / r.height; ptr.act = 1;
  }
  window.addEventListener('pointermove', function (e) { setPtr(e.clientX, e.clientY); }, { passive: true });
  window.addEventListener('touchmove', function (e) { var t = e.touches[0]; if (t) setPtr(t.clientX, t.clientY); }, { passive: true });
  window.addEventListener('scroll', function () { var y = window.scrollY; stir = Math.min(1, stir + Math.abs(y - lastY) / 300); lastY = y; }, { passive: true });
  window.addEventListener('resize', function () { resize(); frame(clock); });

  resize();
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var clock = 4, visible = true, last = 0, raf = 0;
  function loop(now) {
    raf = 0;
    if (!visible || document.hidden) return;
    var dt = last ? Math.min(.05, (now - last) / 1000) : .016; last = now; clock += dt;
    frame(clock); raf = requestAnimationFrame(loop);
  }
  for (var w = 0; w < 180; w++) { clock += 1 / 60; frame(clock, 1); } // settle so nothing starts overlapping
  frame(clock);
  cv.classList.add('lava-on');
  if (reduce) return;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible && !raf) { last = 0; raf = requestAnimationFrame(loop); } }).observe(cv);
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden && visible && !raf) { last = 0; raf = requestAnimationFrame(loop); } });
  raf = requestAnimationFrame(loop);
})();
