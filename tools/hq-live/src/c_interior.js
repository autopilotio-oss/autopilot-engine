
// ---- V3 interior: three wall dashboards, neon sign, map table, shelving, rack, rail lights
function screenPanel(w, h, cw, ch, x, y, z, rotY = 0) {
  const cv = document.createElement('canvas'); cv.width = cw; cv.height = ch;
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = rotY; HQ.add(g);
  box(w + 0.3, h + 0.3, 0.14, M.frame, 0, 0, -0.08, g);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false })); g.add(m);
  const edge = new THREE.Mesh(new THREE.PlaneGeometry(w + 0.36, 0.04), new THREE.MeshBasicMaterial({ color: 0xC8F53C, toneMapped: false })); edge.position.set(0, -h / 2 - 0.2, 0.01); g.add(edge);
  return { cv, tex, g: cv.getContext('2d'), W: cw, H: ch };
}
const wallL = screenPanel(10.5, 5.2, 1024, 508, -12.6, 5.5, -hqD / 2 + 0.42);
const wallC = screenPanel(12, 5.6, 1180, 552, 0, 5.7, -hqD / 2 + 0.42);
const wallR = screenPanel(10.5, 5.2, 1024, 508, 12.6, 5.5, -hqD / 2 + 0.42);
// neon sign on the west wall
const neonCv = canvasTex(1024, 220, (g, w, h) => {
  g.clearRect(0, 0, w, h); g.font = '400 170px "Bebas Neue", Impact, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.shadowColor = '#C8F53C'; g.shadowBlur = 28; g.fillStyle = '#e9ff9a'; g.fillText('AUTOPILOT.OI', w / 2, h / 2 + 8); g.shadowBlur = 0; g.fillStyle = '#f6ffd6'; g.fillText('AUTOPILOT.OI', w / 2, h / 2 + 8);
});
const neon = new THREE.Mesh(new THREE.PlaneGeometry(9, 1.95), new THREE.MeshBasicMaterial({ map: neonCv, transparent: true, toneMapped: false, depthWrite: false }));
neon.position.set(-hqW / 2 + 0.36, 6.3, 2); neon.rotation.y = Math.PI / 2; HQ.add(neon);
const neonLight = new THREE.PointLight(0xC8F53C, 6, 12, 1.6); neonLight.position.set(-hqW / 2 + 1.6, 6.2, 2); HQ.add(neonLight);
// central holo map table: Chicago street grid, pins per network sized by real posts published today
const mapTable = new THREE.Group(); mapTable.position.set(0, 0.25, 1.2); HQ.add(mapTable);
box(6.4, 0.9, 3.4, M.desk, 0, 0.45, 0, mapTable, true);
box(6.6, 0.06, 3.6, M.frame, 0, 0.93, 0, mapTable);
const mapCv = document.createElement('canvas'); mapCv.width = 1024; mapCv.height = 540; const mapTex = new THREE.CanvasTexture(mapCv); mapTex.colorSpace = THREE.SRGBColorSpace;
const mapTop = new THREE.Mesh(new THREE.PlaneGeometry(6.2, 3.26), new THREE.MeshBasicMaterial({ map: mapTex, toneMapped: false, transparent: true, opacity: 0.95 }));
mapTop.rotation.x = -Math.PI / 2; mapTop.position.y = 0.97; mapTable.add(mapTop);
const NETS = [['instagram', 'IG', -1.9, -0.6], ['tiktok', 'TT', -0.4, 0.7], ['threads', 'TH', 1.0, -0.8], ['twitter', 'X', 2.2, 0.5]];
const pins = NETS.map(([net, label, x, z]) => {
  const col = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 1, 12), new THREE.MeshBasicMaterial({ color: 0xC8F53C, toneMapped: false, transparent: true, opacity: 0.85 }));
  col.position.set(x, 0.98, z); col.scale.y = 0.02; mapTable.add(col);
  const ring = new THREE.Mesh(new THREE.RingGeometry(0.14, 0.2, 28), new THREE.MeshBasicMaterial({ color: 0xC8F53C, toneMapped: false, transparent: true, opacity: 0.8, side: THREE.DoubleSide }));
  ring.rotation.x = -Math.PI / 2; ring.position.set(x, 0.985, z); mapTable.add(ring);
  return { net, label, col, ring, n: null };
});
const tableGlow = new THREE.PointLight(0xC8F53C, 3, 7, 2); tableGlow.position.set(0, 2.2, 1.2); HQ.add(tableGlow);
// shelving with books and headphones on the east wall, server rack in the systems corner
const shelf = new THREE.Group(); shelf.position.set(hqW / 2 - 0.65, 0.25, -1.5); shelf.rotation.y = -Math.PI / 2; HQ.add(shelf);
for (let k = 0; k < 4; k++) box(4.2, 0.06, 0.6, M.wood, 0, 0.6 + k * 0.85, 0, shelf, true);
[-2.1, 2.1].forEach((s) => box(0.06, 3.3, 0.6, M.frame, s, 1.65, 0, shelf));
const bookCols = [0x7a2e2a, 0x2c3e50, 0xb59b6a, 0x1f1f22, 0x3d5a3a, 0xd9d4c7, 0x55402f];
for (let k = 0; k < 4; k++) { let x = -1.95; while (x < 1.9) { const w = 0.07 + rnd() * 0.07, h = 0.42 + rnd() * 0.28; if (rnd() < 0.86) { const b = box(w, h, 0.38, new THREE.MeshStandardMaterial({ color: bookCols[(rnd() * bookCols.length) | 0], roughness: 0.8 }), x + w / 2, 0.63 + k * 0.85 + h / 2, 0.02, shelf); b.rotation.z = rnd() < 0.08 ? 0.25 : 0; } x += w + 0.012; } }
const rack = new THREE.Group(); rack.position.set(-hqW / 2 + 1.2, 0.25, -hqD / 2 + 1.4); HQ.add(rack);
const leds = [];
for (let r = 0; r < 2; r++) { box(0.9, 3.2, 1.0, M.frame, r * 1.0, 1.6, 0, rack, true); for (let u = 0; u < 14; u++) { const led = new THREE.Mesh(new THREE.PlaneGeometry(0.05, 0.05), new THREE.MeshBasicMaterial({ color: u % 5 ? 0x3bd16f : 0x7fd6ff, toneMapped: false })); led.position.set(r * 1.0 - 0.3 + (u % 3) * 0.08, 0.4 + u * 0.2, 0.505); rack.add(led); leds.push(led); } }
// Edison bulb string across the lounge
for (let i = 0; i < 9; i++) { const x = 6 + i * 1.5, y = hqH - 1.6 - Math.sin(i / 8 * Math.PI) * 0.6; cyl(0.006, 0.006, 0.5, M.frame, x, y + 0.25, 9.2, HQ, 3); const b = new THREE.Mesh(new THREE.SphereGeometry(0.09, 10, 8), M.bulb); b.position.set(x, y, 9.2); HQ.add(b); }
plant(-4.2, 11.4, 1.1); plant(4.4, -11.4, 1.0); plant(18.5, -11, 1.3);
// soft environment light for metals and glass (built locally, no downloads)
if (renderer) {
  try {
    const envScene = new THREE.Scene(); const room = new THREE.Mesh(new THREE.BoxGeometry(30, 12, 30), new THREE.MeshBasicMaterial({ color: 0x15171a, side: THREE.BackSide })); envScene.add(room);
    [[0, 5.5, -14, 18, 2, 0xffe2bf], [-14, 4, 0, 2, 6, 0xC8F53C], [14, 4, 0, 2, 6, 0x9fd8ff], [0, -5.8, 0, 20, 0.2, 0x332f2a]].forEach(([x, y, z, w, h, c]) => { const p = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.2), new THREE.MeshBasicMaterial({ color: c })); p.position.set(x, y, z); p.lookAt(0, 0, 0); envScene.add(p); });
    const pm = new THREE.PMREMGenerator(renderer); scene.environment = pm.fromScene(envScene, 0.04).texture; scene.environmentIntensity = 0.45; pm.dispose();
  } catch (e) {}
}
