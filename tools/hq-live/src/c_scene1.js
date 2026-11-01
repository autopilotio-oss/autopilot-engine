// ---------------------------------------------------------------------------
// Procedural textures
// ---------------------------------------------------------------------------
const rnd = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
function canvasTex(w, h, draw, repeat) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); }
  return t;
}
function brick(g, w, h, base) {
  g.fillStyle = '#2a201b'; g.fillRect(0, 0, w, h);
  const bh = 8, bw = 22;
  for (let y = 0, r = 0; y < h; y += bh, r++) for (let x = -(r % 2) * bw / 2; x < w; x += bw) {
    const k = 0.75 + rnd() * 0.4; const c = base.map((v) => Math.min(255, v * k | 0));
    g.fillStyle = `rgb(${c})`; g.fillRect(x + 1, y + 1, bw - 2, bh - 2);
  }
  g.fillStyle = 'rgba(0,0,0,.18)'; for (let i = 0; i < 40; i++) g.fillRect(rnd() * w, rnd() * h, 2 + rnd() * 30, 1 + rnd() * 3);
}
const brickTex = (base, rx, ry) => canvasTex(256, 256, (g, w, h) => brick(g, w, h, base), [rx, ry]);
// building facade with windows; emissive map lights random windows at night
function facade(cols, rows, base, storefront) {
  const W = 512, H = 512; const lit = [];
  const color = canvasTex(W, H, (g) => {
    brick(g, W, H, base);
    const mw = W / cols, mh = H / rows;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      if (storefront && r === rows - 1) continue;
      const x = c * mw + mw * 0.22, y = r * mh + mh * 0.2, ww = mw * 0.56, hh = mh * 0.58;
      g.fillStyle = '#d8d2c4'; g.fillRect(x - 3, y + hh, ww + 6, 4);
      g.fillStyle = '#10161c'; g.fillRect(x, y, ww, hh);
      g.fillStyle = 'rgba(160,180,200,.18)'; g.fillRect(x + 2, y + 2, ww / 2 - 3, hh - 4);
      g.strokeStyle = '#1b1b1b'; g.lineWidth = 3; g.strokeRect(x, y, ww, hh); g.beginPath(); g.moveTo(x, y + hh / 2); g.lineTo(x + ww, y + hh / 2); g.stroke();
      if (rnd() < 0.45) lit.push([x, y, ww, hh]);
    }
    if (storefront) {
      const y = (rows - 1) * mh + mh * 0.12;
      g.fillStyle = '#0d1114'; g.fillRect(W * 0.06, y, W * 0.88, mh * 0.82);
      g.fillStyle = '#3a2a1c'; g.fillRect(W * 0.04, y - 16, W * 0.92, 18);
      g.fillStyle = '#e8d9b0'; g.font = 'bold 15px "Space Mono", monospace'; g.fillText(storefront, W * 0.07, y - 3);
    }
  });
  const emis = canvasTex(W, H, (g) => {
    g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
    for (const [x, y, ww, hh] of lit) { g.fillStyle = rnd() < 0.7 ? '#ffcf8a' : '#cfe6ff'; g.fillRect(x + 2, y + 2, ww - 4, hh - 4); }
    if (storefront) { const mh = H / rows; g.fillStyle = '#ffd9a0'; g.fillRect(W * 0.07, (rows - 1) * mh + mh * 0.16, W * 0.86, mh * 0.74); }
  });
  return { color, emis };
}

// ---------------------------------------------------------------------------
// Materials and lights
// ---------------------------------------------------------------------------
const M = {
  concrete: new THREE.MeshStandardMaterial({ color: 0x55534f, roughness: 0.95, map: canvasTex(256, 256, (g, w, h) => { g.fillStyle = '#7b7873'; g.fillRect(0, 0, w, h); for (let i = 0; i < 1600; i++) { g.fillStyle = `rgba(0,0,0,${rnd() * 0.08})`; g.fillRect(rnd() * w, rnd() * h, 2, 2); } g.strokeStyle = 'rgba(0,0,0,.25)'; for (let i = 0; i <= w; i += 64) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }, [16, 16]) }),
  floor: new THREE.MeshStandardMaterial({ color: 0x7a7670, roughness: 0.42, metalness: 0.12, map: canvasTex(256, 256, (g, w, h) => { g.fillStyle = '#5c5a56'; g.fillRect(0, 0, w, h); for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(0,0,0,${rnd() * 0.12})`; g.beginPath(); g.arc(rnd() * w, rnd() * h, rnd() * 9, 0, 7); g.fill(); } }, [6, 4]) }),
  asphalt: new THREE.MeshStandardMaterial({ color: 0x2b2c2e, roughness: 0.92 }),
  sidewalk: new THREE.MeshStandardMaterial({ color: 0x7c7a75, roughness: 0.9 }),
  steel: new THREE.MeshStandardMaterial({ color: 0x5c6b62, roughness: 0.65, metalness: 0.45 }),
  rust: new THREE.MeshStandardMaterial({ color: 0x4a3a2c, roughness: 0.85, metalness: 0.3 }),
  frame: new THREE.MeshStandardMaterial({ color: 0x121314, roughness: 0.6, metalness: 0.4 }),
  glass: new THREE.MeshPhysicalMaterial({ color: 0x9fb4c4, roughness: 0.08, metalness: 0, transmission: 0.0, transparent: true, opacity: 0.16 }),
  desk: new THREE.MeshStandardMaterial({ color: 0x1a1a1b, roughness: 0.5, metalness: 0.2 }),
  wood: new THREE.MeshStandardMaterial({ color: 0x3a2c22, roughness: 0.7 }),
  chair: new THREE.MeshStandardMaterial({ color: 0x0e0e0f, roughness: 0.7 }),
  leather: new THREE.MeshStandardMaterial({ color: 0x0d0d0e, roughness: 0.35, metalness: 0.1 }),
  plant: new THREE.MeshStandardMaterial({ color: 0x2f5a2a, roughness: 0.8 }),
  pot: new THREE.MeshStandardMaterial({ color: 0x8a8580, roughness: 0.9 }),
  duct: new THREE.MeshStandardMaterial({ color: 0x6c6f72, roughness: 0.4, metalness: 0.8 }),
  bulb: new THREE.MeshStandardMaterial({ color: 0xfff1d0, emissive: 0xffd28a, emissiveIntensity: 2 }),
  lampShade: new THREE.MeshStandardMaterial({ color: 0x0c0c0c, roughness: 0.4, metalness: 0.6, side: THREE.DoubleSide }),
  car: [0x1e2a35, 0x5b1d1d, 0x2c2c2c, 0x6c6f73, 0x203b2a].map((c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.35, metalness: 0.6 })),
  train: new THREE.MeshStandardMaterial({ color: 0xb9bec2, roughness: 0.3, metalness: 0.85 }),
  trainWin: new THREE.MeshStandardMaterial({ color: 0x1b2229, emissive: 0xffe2a8, emissiveIntensity: 0 }),
};
const hemi = new THREE.HemisphereLight(0xb8c4d0, 0x3a352f, 1.0); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xffffff, 1.0);
sun.position.set(-60, 80, 50); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024);
Object.assign(sun.shadow.camera, { left: -40, right: 40, top: 40, bottom: -40, near: 1, far: 260 });
scene.add(sun);
const interior = []; // warm pendant lights inside the HQ
const pendants = [], plants = [], lampGroups = [];
const streetLights = [];
const nightEmissive = []; // materials whose emissive turns on at night

// ---------------------------------------------------------------------------
// Builders
// ---------------------------------------------------------------------------
const box = (w, h, d, mat, x = 0, y = 0, z = 0, parent = scene, shadow = false) => {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.position.set(x, y, z);
  if (shadow) { m.castShadow = true; m.receiveShadow = true; }
  parent.add(m); return m;
};
const cyl = (rt, rb, h, mat, x = 0, y = 0, z = 0, parent = scene, seg = 12) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg), mat); m.position.set(x, y, z); parent.add(m); return m; };

// ground, street, sidewalks
const ground = box(900, 0.2, 900, M.concrete, 0, -0.1, 0); ground.receiveShadow = true;
box(900, 0.06, 13, M.asphalt, 0, 0.02, 24).receiveShadow = true;
for (let x = -440; x < 440; x += 6) box(2.4, 0.07, 0.18, new THREE.MeshBasicMaterial({ color: 0xc9b26a }), x, 0.06, 24);
box(900, 0.22, 5, M.sidewalk, 0, 0.1, 15.5).receiveShadow = true;
box(900, 0.22, 5, M.sidewalk, 0, 0.1, 32.5).receiveShadow = true;

// ---- the HQ: converted brick warehouse, cutaway (no roof) so you can see in
const HQ = new THREE.Group(); scene.add(HQ);
const hqW = 40, hqD = 26, hqH = 9.5;
const wallBrick = new THREE.MeshStandardMaterial({ map: brickTex([120, 62, 46], 6, 3), roughness: 0.9 });
const wallBrickIn = new THREE.MeshStandardMaterial({ map: brickTex([96, 52, 40], 6, 3), roughness: 0.95 });
box(hqW, 0.25, hqD, M.floor, 0, 0.12, 0, HQ).receiveShadow = true;
box(hqW, hqH, 0.6, wallBrickIn, 0, hqH / 2, -hqD / 2, HQ, true); // back wall
const wallBrickSide = wallBrickIn.clone();
[-1, 1].forEach((s) => box(0.6, hqH, hqD, wallBrickSide, s * hqW / 2, hqH / 2, 0, HQ, true)); // side walls
// front wall: brick piers and a big steel window grid facing the street + L tracks
const fz = hqD / 2;
const FRONT = new THREE.Group(); HQ.add(FRONT); // hidden when looking down into the HQ
const wallBand = wallBrick.clone();
box(hqW, 1.1, 0.6, wallBand, 0, 0.55, fz, FRONT, true);
box(hqW, 1.0, 0.6, wallBand, 0, hqH - 0.5, fz, FRONT, true);
for (let i = 0; i <= 5; i++) box(1.2, hqH, 0.7, wallBrick, -hqW / 2 + i * (hqW / 5), hqH / 2, fz, FRONT, true);
for (let b = 0; b < 5; b++) {
  const x0 = -hqW / 2 + b * (hqW / 5) + 0.6, wB = hqW / 5 - 1.2;
  const g = box(wB, hqH - 2.1, 0.06, M.glass, x0 + wB / 2, 1.1 + (hqH - 2.1) / 2, fz, FRONT);
  g.renderOrder = 2;
  for (let k = 1; k < 4; k++) box(0.09, hqH - 2.1, 0.12, M.frame, x0 + k * wB / 4, 1.1 + (hqH - 2.1) / 2, fz, FRONT);
  for (let k = 1; k < 5; k++) box(wB, 0.09, 0.12, M.frame, x0 + wB / 2, 1.1 + k * (hqH - 2.1) / 5, fz, FRONT);
}
// steel columns, ceiling ducts, pendant lamps
[-15.5, -5.5, 5.5, 15.5].forEach((x) => [-0.4, 11.8].forEach((z) => { const c = box(0.5, hqH, 0.5, M.rust, x, hqH / 2, z, HQ); c.castShadow = true; }));
const duct = cyl(0.32, 0.32, hqW - 2, M.duct, 0, hqH - 0.5, -hqD / 2 + 1.4, HQ, 16); duct.rotation.z = Math.PI / 2;
for (let x = -16; x <= 16; x += 8) box(0.18, 0.18, hqD - 1, M.rust, x, hqH - 0.2, 0, HQ);
[[-12, -6], [0, -6], [12, -6], [-12, 4], [0, 2], [12, 4]].forEach(([x, z]) => {
  cyl(0.02, 0.02, 2.2, M.frame, x, hqH - 1.1, z, HQ, 4);
  const shade = new THREE.Mesh(new THREE.ConeGeometry(0.7, 0.55, 18, 1, true), M.lampShade); shade.position.set(x, hqH - 2.4, z); HQ.add(shade); pendants.push({ x, z, shade });
  const b = new THREE.Mesh(new THREE.SphereGeometry(0.16, 10, 8), M.bulb); b.position.set(x, hqH - 2.6, z); HQ.add(b);
  const l = new THREE.PointLight(0xffe2bf, 0, 24, 1.3); l.position.set(x, hqH - 2.8, z); HQ.add(l); interior.push(l);
});
// lounge: leather couch, coffee table, rug, plants
const rug = box(7, 0.03, 4.5, new THREE.MeshStandardMaterial({ color: 0x2a2826, roughness: 1 }), 12, 0.26, 9.2, HQ); rug.receiveShadow = true;
const couch = new THREE.Group(); couch.position.set(15.5, 0.25, 9.2); couch.rotation.y = -Math.PI / 2; HQ.add(couch);
box(5, 0.55, 1.6, M.leather, 0, 0.45, 0, couch, true); box(5, 1.1, 0.4, M.leather, 0, 0.9, -0.7, couch, true); [-1, 1].forEach((s) => box(0.4, 0.8, 1.6, M.leather, s * 2.4, 0.65, 0, couch, true));
const ctable = new THREE.Group(); HQ.add(ctable);
box(2.6, 0.12, 1.3, M.desk, 11.5, 0.75, 9.2, ctable, true); [[-1.1, -0.5], [1.1, -0.5], [-1.1, 0.5], [1.1, 0.5]].forEach(([a, b]) => box(0.08, 0.5, 0.08, M.frame, 11.5 + a, 0.45, 9.2 + b, ctable));
box(0.8, 0.12, 0.55, new THREE.MeshStandardMaterial({ color: 0xe8e6e0 }), 11.2, 0.87, 9.1, ctable);
function plant(x, z, s = 1) {
  const g = new THREE.Group(); g.position.set(x, 0.25, z); g.scale.setScalar(s); HQ.add(g); plants.push({ g, s });
  cyl(0.35, 0.28, 0.7, M.pot, 0, 0.35, 0, g, 14);
  for (let i = 0; i < 9; i++) { const l = new THREE.Mesh(new THREE.SphereGeometry(0.42, 7, 5), M.plant); l.scale.set(0.5, 1.4, 0.18); l.position.set(Math.cos(i) * 0.25, 1.15 + rnd() * 0.5, Math.sin(i) * 0.25); l.rotation.set(rnd() - 0.5, i, rnd() * 0.8 - 0.4); l.castShadow = true; g.add(l); }
}
plant(-18.5, 11.5, 1.6); plant(9, 11.5, 1.3); plant(18.5, 4.5, 1.2); plant(-18.5, -11, 1.4);

