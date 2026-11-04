/* AUTOPILOT.OI lava background (Seb, Nov 4 2026: "the white, but the green lava inside more dynamic").
   Glossy lime metaballs on paper white. Blobs drift on their own orbits, swell and shrink so they merge and split,
   one blob follows the pointer or finger, scrolling stirs them. Pauses off screen, one still frame for reduced motion.
   Usage: <canvas class="lava" data-lava></canvas> inside a position:relative parent. */
(function () {
  var cv = document.querySelector('canvas[data-lava]');
  if (!cv) return;
  var gl = cv.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false });
  if (!gl) { cv.classList.add('lava-off'); return; }
  var N = 10;
  var vs = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var fs = [
    'precision highp float;',
    'uniform vec2 R;uniform vec3 B[' + N + '];',
    'const vec3 PAPER=vec3(.925,.925,.906);',
    'const vec3 LIME=vec3(.831,1.,.227);',
    'const vec3 DEEP=vec3(.56,.80,.02);',
    'float field(vec2 p){float f=0.;for(int i=0;i<' + N + ';i++){vec2 d=p-B[i].xy;float r=B[i].z;f+=r*r/(dot(d,d)+.00025);}return f;}',
    'float qf(vec2 p){return inversesqrt(field(p));}',
    'void main(){',
    ' vec2 uv=gl_FragCoord.xy/R.y;',
    ' float q=qf(uv);float e=1.5/R.y;',
    ' vec2 g=vec2(qf(uv+vec2(e,0.))-qf(uv-vec2(e,0.)),qf(uv+vec2(0.,e))-qf(uv-vec2(0.,e)))/(2.*e);',
    ' float gn=max(length(g),1e-4);float dist=(1.-q)/gn;vec2 n=g/gn;',
    ' float inside=smoothstep(-1.2/R.y,1.2/R.y,dist);',
    ' float depth=clamp(dist*9.,0.,1.);',
    ' vec3 N3=normalize(vec3(-n*(1.-depth),depth*1.2+.25));',
    ' vec3 L=normalize(vec3(-.45,.65,.9));',
    ' float dif=clamp(dot(N3,L),0.,1.);',
    ' float spec=pow(clamp(dot(reflect(-L,N3),vec3(0.,0.,1.)),0.,1.),38.);',
    ' float fres=pow(1.-clamp(N3.z,0.,1.),2.2);',
    ' vec3 body=mix(DEEP,LIME,.35+.65*dif);',
    ' body+=vec3(1.)*spec*.85+vec3(.95,1.,.75)*fres*.22;',
    ' float sh=exp(-max(-dist,0.)*26.)*(1.-inside);',
    ' vec2 so=uv+vec2(.012,.02);float qs=qf(so);float ds=(1.-qs)/max(gn,1e-4);',
    ' float drop=smoothstep(.05,-.01,-ds)*.10*(1.-inside);',
    ' vec3 bg=PAPER-vec3(.10,.08,.12)*drop+LIME*sh*.10;',
    ' gl_FragColor=vec4(mix(bg,body,inside),1.);',
    '}'].join('\n');
  function sh(t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; }
  var pr = gl.createProgram();
  gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) { cv.classList.add('lava-off'); return; }
  gl.useProgram(pr);
  var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  var lp = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
  var uR = gl.getUniformLocation(pr, 'R'), uB = gl.getUniformLocation(pr, 'B');

  // blob orbits: center, radius of orbit, speeds, phase, base size, pulse
  function rnd(i, k) { var x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); }
  var orb = [];
  for (var i = 0; i < N - 1; i++) {
    orb.push({
      cx: .15 + .85 * rnd(i, 1), cy: .1 + .8 * rnd(i, 2),
      ax: .18 + .32 * rnd(i, 3), ay: .14 + .3 * rnd(i, 4),
      sx: (.10 + .22 * rnd(i, 5)) * (rnd(i, 6) > .5 ? 1 : -1), sy: .08 + .2 * rnd(i, 7),
      ph: 6.28 * rnd(i, 8), r: .055 + .06 * rnd(i, 9), pr: .3 + .5 * rnd(i, 10), pa: .25 + .35 * rnd(i, 11)
    });
  }
  var data = new Float32Array(N * 3);
  var W = 1, H = 1, aspect = 1, ptr = { x: .78, y: .55, tx: .78, ty: .55, on: 0 }, stir = 0, lastY = window.scrollY;

  function resize() {
    var r = cv.getBoundingClientRect();
    var s = Math.min(window.devicePixelRatio || 1, 2) * (r.width > 900 ? .5 : .6);
    W = Math.max(2, Math.round(r.width * s)); H = Math.max(2, Math.round(r.height * s));
    cv.width = W; cv.height = H; aspect = W / H;
    gl.viewport(0, 0, W, H); gl.uniform2f(uR, W, H);
  }
  function frame(t) {
    var k = 1 + stir * 2.5; stir *= .94; var rs = aspect < 1 ? Math.max(.42, aspect * 1.5) : 1;
    for (var i = 0; i < orb.length; i++) {
      var o = orb[i], tt = t * k;
      var x = o.cx * aspect + o.ax * aspect * .55 * Math.sin(tt * o.sx + o.ph) + .05 * Math.sin(tt * o.sx * 2.3 + i);
      var y = o.cy + o.ay * Math.cos(tt * o.sy + o.ph * 1.7) + .04 * Math.sin(tt * .9 + i * 2.1);
      var r = rs * o.r * (1 + o.pa * Math.sin(tt * o.pr + o.ph));
      data[i * 3] = x; data[i * 3 + 1] = y; data[i * 3 + 2] = r;
    }
    ptr.x += (ptr.tx - ptr.x) * .07; ptr.y += (ptr.ty - ptr.y) * .07;
    ptr.on += ((ptr.act ? 1 : .55) - ptr.on) * .05;
    var j = (N - 1) * 3;
    data[j] = ptr.x * aspect; data[j + 1] = ptr.y; data[j + 2] = rs * (.075 + .02 * Math.sin(t * 1.7)) * ptr.on;
    gl.uniform3fv(uB, data); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
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
  frame(clock);
  cv.classList.add('lava-on');
  if (reduce) return;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible && !raf) { last = 0; raf = requestAnimationFrame(loop); } }).observe(cv);
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden && visible && !raf) { last = 0; raf = requestAnimationFrame(loop); } });
  raf = requestAnimationFrame(loop);
})();
