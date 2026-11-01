// ---------------------------------------------------------------------------
// Camera: touch + mouse orbit, pinch zoom, two-finger pan, presets
// ---------------------------------------------------------------------------
const cam = { target: new THREE.Vector3(0, 0.5, 0.5), yaw: 0.0, pitch: 0.78, dist: 33, goal: null };
const PRESETS = {
  street: { t: [0, 4.5, 24], yaw: 1.25, pitch: 0.1, dist: 38 }, hq: { t: [0, 0.8, -1.2], yaw: 0.0, pitch: 0.8, dist: 38 },
  exec: { t: [DEPTS.exec.x, 1.2, DEPTS.exec.z + 1.5], yaw: 0.15, pitch: 0.95, dist: 15 }, content: { t: [DEPTS.content.x, 1.2, DEPTS.content.z + 1.5], yaw: 0.3, pitch: 0.95, dist: 15 },
  care: { t: [DEPTS.care.x, 1.2, DEPTS.care.z + 1.5], yaw: -0.3, pitch: 0.95, dist: 15 }, finance: { t: [DEPTS.finance.x, 1.2, DEPTS.finance.z + 1.5], yaw: -0.3, pitch: 0.95, dist: 15 },
  systems: { t: [DEPTS.systems.x, 1.2, DEPTS.systems.z + 1.5], yaw: 0.3, pitch: 0.95, dist: 15 },
};
function goto(name) { const p = { ...PRESETS[name] }; if (innerWidth < innerHeight && name !== 'street') { p.dist *= name === 'hq' ? 2.1 : 1.35; p.pitch = Math.min(1.2, p.pitch + 0.2); } cam.goal = { t: new THREE.Vector3(...p.t), yaw: p.yaw, pitch: p.pitch, dist: p.dist }; }
const ptrs = new Map(); let lastPinch = null, moved = 0;
canvas.addEventListener('pointerdown', (e) => { canvas.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY }); moved = 0; cam.goal = null; });
canvas.addEventListener('pointermove', (e) => {
  if (!ptrs.size && e.pointerType === 'mouse' && performance.now() - (window.__hv || 0) > 90) { window.__hv = performance.now(); const v = new THREE.Vector2((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1); ray.setFromCamera(v, camera); const h = ray.intersectObjects(HQ.children, true).find((x) => x.object.userData.agentId); hoverId = h ? h.object.userData.agentId : null; canvas.style.cursor = h ? 'pointer' : ''; }
  if (!ptrs.has(e.pointerId)) return; const p = ptrs.get(e.pointerId); const dx = e.clientX - p.x, dy = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY; moved += Math.abs(dx) + Math.abs(dy);
  if (ptrs.size === 1 && !(e.buttons & 2)) { cam.yaw -= dx * 0.005; cam.pitch = Math.min(1.45, Math.max(0.04, cam.pitch + dy * 0.004)); }
  else if (ptrs.size === 1) pan(dx, dy);
  else if (ptrs.size === 2) {
    const [a, b] = [...ptrs.values()]; const d = Math.hypot(a.x - b.x, a.y - b.y);
    if (lastPinch) { cam.dist = Math.min(140, Math.max(4, cam.dist * lastPinch / d)); pan(dx / 2, dy / 2); }
    lastPinch = d;
  }
});
const up = (e) => { ptrs.delete(e.pointerId); if (ptrs.size < 2) lastPinch = null; if (moved < 6 && e.type === 'pointerup') pick(e); };
canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
canvas.addEventListener('contextmenu', (e) => e.preventDefault());
canvas.addEventListener('wheel', (e) => { e.preventDefault(); cam.goal = null; cam.dist = Math.min(140, Math.max(4, cam.dist * (1 + Math.sign(e.deltaY) * 0.1))); }, { passive: false });
function pan(dx, dy) { const f = cam.dist * 0.0016; const right = new THREE.Vector3(Math.cos(cam.yaw), 0, -Math.sin(cam.yaw)); const fwd = new THREE.Vector3(Math.sin(cam.yaw), 0, Math.cos(cam.yaw)); cam.target.addScaledVector(right, -dx * f).addScaledVector(fwd, -dy * f); }
const ray = new THREE.Raycaster();
function pick(e) {
  const v = new THREE.Vector2((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1); ray.setFromCamera(v, camera);
  const hit = ray.intersectObjects(HQ.children, true).find((h) => h.object.userData.agentId);
  if (hit) openInspector(hit.object.userData.agentId, true);
}

