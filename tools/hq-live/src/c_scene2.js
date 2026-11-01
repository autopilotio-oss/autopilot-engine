// ---- desks: built per agent at runtime
const deskGeo = { top: new THREE.BoxGeometry(2.6, 0.08, 1.2), leg: new THREE.BoxGeometry(0.06, 0.74, 1.1), mon: new THREE.BoxGeometry(0.78, 0.46, 0.04), stand: new THREE.BoxGeometry(0.05, 0.3, 0.05) };
function makeDesk(x, z, rotY) {
  const g = new THREE.Group(); g.position.set(x, 0.25, z); g.rotation.y = rotY; HQ.add(g);
  const top = new THREE.Mesh(deskGeo.top, M.desk); top.position.y = 0.76; top.castShadow = top.receiveShadow = true; g.add(top);
  const proc = [top]; [-1.25, 1.25].forEach((s) => { const l = new THREE.Mesh(deskGeo.leg, M.frame); l.position.set(s, 0.37, 0); g.add(l); proc.push(l); });
  const cv = document.createElement('canvas'); cv.width = 256; cv.height = 150; const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const screenMat = new THREE.MeshBasicMaterial({ map: tex, toneMapped: false });
  const mons = [-0.82, 0, 0.82].map((dx, i) => {
    const m = new THREE.Mesh(deskGeo.mon, M.frame); m.position.set(dx, 1.22, -0.38); m.rotation.y = -dx * 0.35; g.add(m);
    const s = new THREE.Mesh(new THREE.PlaneGeometry(0.74, 0.42), screenMat); s.position.set(0, 0, 0.022); m.add(s);
    const st = new THREE.Mesh(deskGeo.stand, M.frame); st.position.set(dx, 0.95, -0.4); g.add(st);
    return s;
  });
  box(0.9, 0.03, 0.28, M.frame, 0, 0.81, 0.1, g); // keyboard
  box(0.12, 0.012, 0.2, M.frame, 0.65, 0.805, 0.15, g); // mouse
  const mug = cyl(0.055, 0.048, 0.12, new THREE.MeshStandardMaterial({ color: [0xe8e4dc, 0x1a1a1c, 0xC8F53C][(rnd() * 3) | 0], roughness: 0.4 }), -1.0, 0.86, 0.1, g, 14);
  if (rnd() < 0.55) { const hp = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.014, 8, 20, Math.PI), M.frame); hp.position.set(1.0, 0.82, -0.05); hp.rotation.x = -Math.PI / 2; g.add(hp); }
  if (rnd() < 0.5) { box(0.32, 0.06, 0.24, new THREE.MeshStandardMaterial({ color: 0x2c3e50, roughness: 0.8 }), -0.7, 0.83, -0.1, g); }
  // chair
  const chair = new THREE.Group(); chair.position.set(0, 0, 0.95); g.add(chair);
  box(0.62, 0.08, 0.6, M.chair, 0, 0.52, 0, chair, true); box(0.6, 0.75, 0.08, M.chair, 0, 0.95, 0.3, chair, true); cyl(0.03, 0.03, 0.45, M.frame, 0, 0.27, 0, chair, 6);
  const glow = new THREE.Mesh(new THREE.RingGeometry(0.75, 0.86, 40), new THREE.MeshBasicMaterial({ color: 0xD4FF3A, transparent: true, opacity: 0, toneMapped: false }));
  glow.rotation.x = -Math.PI / 2; glow.position.set(0, 0.02, 0.95); g.add(glow);
  decorateDesk(g, proc);
  return { g, cv, tex, glow, chair };
}

// ---- the street: L tracks, train, buildings, lamps, cars, skyline
const L = new THREE.Group(); scene.add(L);
const lz = 40, lh = 7.5;
for (let x = -300; x <= 300; x += 8) { [-2.6, 2.6].forEach((dz) => box(0.4, lh, 0.4, M.steel, x, lh / 2, lz + dz, L)); box(0.4, 0.5, 6, M.steel, x, lh, lz, L); }
box(600, 0.6, 6.2, M.steel, 0, lh + 0.45, lz, L);
[-1.6, 1.6].forEach((dz) => { box(600, 0.25, 0.3, M.rust, 0, lh + 0.85, lz + dz, L); });
for (let x = -300; x <= 300; x += 2) box(0.25, 0.08, 6, M.rust, x, lh + 0.78, lz, L);
const train = new THREE.Group(); scene.add(train);
for (let i = 0; i < 4; i++) {
  const car = new THREE.Group(); car.position.x = i * 15.2; train.add(car);
  box(14.6, 3.1, 3.0, M.train, 0, 0, 0, car, true);
  box(14.2, 0.9, 3.05, M.trainWin, 0, 0.4, 0, car);
  box(14.6, 0.25, 3.05, new THREE.MeshStandardMaterial({ color: 0x1d4f8f }), 0, -0.35, 0, car);
  box(14.6, 0.3, 2.6, M.frame, 0, -1.7, 0, car);
}
train.position.set(-200, lh + 2.6, lz);
nightEmissive.push([M.trainWin, 1.6]);

const facades = [];
function building(x, z, w, h, d, base, cols, rows, store, rotY = 0) {
  const f = facade(cols, rows, base, store);
  const mat = new THREE.MeshStandardMaterial({ map: f.color, emissiveMap: f.emis, emissive: 0xffffff, emissiveIntensity: 0, roughness: 0.9 });
  const side = new THREE.MeshStandardMaterial({ map: brickTex(base, w / 6, h / 6), roughness: 0.95 });
  const top = new THREE.MeshStandardMaterial({ color: 0x2a2624 });
  const mats = [side, side, top, top, mat, side];
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mats); m.position.set(x, h / 2, z); m.rotation.y = rotY; m.receiveShadow = true; scene.add(m);
  box(w + 0.6, 0.6, d + 0.6, new THREE.MeshStandardMaterial({ color: 0x3a3330 }), x, h + 0.3, z);
  nightEmissive.push([mat, 1.1]); facades.push(m); return m;
}
const BR = [[132, 64, 46], [110, 58, 44], [146, 92, 62], [96, 64, 52], [126, 80, 60]];
const stores = ['ON THE WAY', 'GRILL', 'LIQUORS', 'CELL FIX', 'BARBER', 'CORNER STORE', 'LAUNDRY', 'PIZZA', 'NAILS'];
let bx = -150;
for (let i = 0; bx < 150; i++) { const w = 14 + (i % 3) * 5, h = 11 + (i * 7 % 3) * 4; building(bx + w / 2, 52, w, h, 12, BR[i % 5], Math.round(w / 3.4), Math.round(h / 3.6), stores[i % stores.length]); bx += w + 0.4; }
[[-34, 0, 26, 14], [34, 0, 26, 12], [-62, 0, 26, 17], [62, 0, 26, 13], [-90, 0, 26, 11], [90, 0, 26, 16]].forEach(([x, z, w, h], i) => building(x, z, w, h, 24, BR[(i + 2) % 5], 7, Math.round(h / 3.6), i < 2 ? null : stores[(i + 3) % stores.length]));
// mural: CHICAGO + four stars on the side of the building west of HQ
const mural = new THREE.Mesh(new THREE.PlaneGeometry(9, 5), new THREE.MeshStandardMaterial({ roughness: 0.9, map: canvasTex(512, 280, (g, w, h) => {
  g.fillStyle = '#e9e4da'; g.fillRect(0, 0, w, h);
  g.fillStyle = '#9ccde8'; g.fillRect(0, 96, w, 34); g.fillRect(0, 186, w, 34);
  g.fillStyle = '#c8202f'; for (let i = 0; i < 4; i++) { const cx = 90 + i * 110, cy = 158; g.beginPath(); for (let k = 0; k < 12; k++) { const r = k % 2 ? 9 : 22, a = k * Math.PI / 6 - Math.PI / 2; g.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); } g.fill(); }
  g.fillStyle = '#e9e4da'; g.fillRect(0, 0, w, 80); g.fillStyle = '#1a1a1a'; g.font = 'bold 62px "Bebas Neue", Impact, sans-serif'; g.fillText('CHICAGO', 140, 66);
}) }));
mural.position.set(-34, 7, 12.05); scene.add(mural);
// graffiti on the L columns' neighbor wall
const graff = new THREE.Mesh(new THREE.PlaneGeometry(14, 3.2), new THREE.MeshStandardMaterial({ transparent: true, roughness: 0.9, map: canvasTex(512, 120, (g) => {
  const cs = ['#d6d6d6', '#9aa5b1', '#c94f4f', '#e2c044']; g.lineWidth = 6; g.lineCap = 'round';
  for (let i = 0; i < 9; i++) { g.strokeStyle = cs[i % 4]; g.beginPath(); let x = 20 + i * 54, y = 30 + rnd() * 50; g.moveTo(x, y); for (let k = 0; k < 6; k++) g.quadraticCurveTo(x + rnd() * 40, y + rnd() * 50 - 25, (x += 8), (y = 30 + rnd() * 60)); g.stroke(); }
}) }));
graff.position.set(62, 2.2, 12.05); scene.add(graff);
// street lamps
for (let x = -60; x <= 60; x += 20) {
  [15.2, 32.8].forEach((z, k) => {
    const g = new THREE.Group(); g.position.set(x + k * 10, 0.2, z); scene.add(g);
    const pole = cyl(0.08, 0.12, 6, M.frame, 0, 3, 0, g, 8);
    const head = cyl(0.25, 0.4, 0.5, M.frame, 0, 6.1, 0, g, 10); lampGroups.push({ g, pole, head, side: k });
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.22, 10, 8), new THREE.MeshStandardMaterial({ color: 0xffe0a8, emissive: 0xffc070, emissiveIntensity: 0 })); bulb.position.y = 5.8; g.add(bulb);
    streetLights.push(bulb.material);
    if (streetLights.length <= 6) { const pl = new THREE.PointLight(0xffc070, 0, 22, 1.8); pl.position.set(0, 5.6, 0); g.add(pl); streetLights.push(pl); }
  });
}
// parked cars
for (let i = 0; i < 12; i++) {
  const g = new THREE.Group(); const side = i % 2; g.position.set(-70 + i * 12 + rnd() * 3, 0.2, side ? 29.3 : 18.7); g.rotation.y = side ? Math.PI : 0; scene.add(g);
  const mat = M.car[i % M.car.length];
  box(4.4, 0.8, 1.9, mat, 0, 0.7, 0, g, true); box(2.4, 0.7, 1.75, mat, -0.2, 1.4, 0, g, true);
  box(2.3, 0.55, 1.78, new THREE.MeshStandardMaterial({ color: 0x0c1116, roughness: 0.1, metalness: 0.6 }), -0.2, 1.42, 0, g);
  [[-1.4, 0.95], [1.4, 0.95], [-1.4, -0.95], [1.4, -0.95]].forEach(([a, b]) => { const w = cyl(0.36, 0.36, 0.25, M.frame, a, 0.36, b, g, 12); w.rotation.x = Math.PI / 2; });
}
// skyline: far towers, one stepped supertall with twin antennas, one tapered
const sky = new THREE.Group(); scene.add(sky);
const skyMat = new THREE.MeshStandardMaterial({ color: 0x2a3038, roughness: 0.8, emissive: 0xffe2b0, emissiveIntensity: 0, emissiveMap: canvasTex(64, 256, (g, w, h) => { g.fillStyle = '#000'; g.fillRect(0, 0, w, h); for (let y = 4; y < h; y += 6) for (let x = 3; x < w; x += 6) if (rnd() < 0.35) { g.fillStyle = '#fff'; g.fillRect(x, y, 3, 3); } }) });
nightEmissive.push([skyMat, 0.9]);
for (let i = 0; i < 46; i++) { const h = 30 + rnd() * 80, w = 8 + rnd() * 14; const m = box(w, h, w, skyMat, -260 + i * 12 + rnd() * 6, h / 2, -260 - rnd() * 80, sky); }
const tower = new THREE.Group(); tower.position.set(30, 0, -300); sky.add(tower);
[[26, 140], [20, 190], [14, 230], [9, 258]].forEach(([w, h]) => box(w, h, w, skyMat, 0, h / 2, 0, tower));
[-2.5, 2.5].forEach((dx) => cyl(0.5, 0.5, 50, M.frame, dx, 283, 0, tower, 6));
const hancock = new THREE.Mesh(new THREE.CylinderGeometry(7, 14, 200, 4), skyMat); hancock.rotation.y = Math.PI / 4; hancock.position.set(-70, 100, -310); sky.add(hancock);
[-3, 3].forEach((dx) => cyl(0.4, 0.4, 40, M.frame, -70 + dx, 220, -310, sky, 6));

// sky dome gradient
const skyCv = document.createElement('canvas'); skyCv.width = 4; skyCv.height = 256;
const skyTex = new THREE.CanvasTexture(skyCv); skyTex.colorSpace = THREE.SRGBColorSpace;
const dome = new THREE.Mesh(new THREE.SphereGeometry(900, 24, 12), new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide, fog: false, toneMapped: false }));
scene.add(dome);
scene.fog = new THREE.Fog(0xaab4be, 90, 520);

