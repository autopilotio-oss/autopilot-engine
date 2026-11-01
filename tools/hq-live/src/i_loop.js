
// ---------------------------------------------------------------------------
// Loop
// ---------------------------------------------------------------------------
applyLight(); setInterval(() => lightMode === 'auto' && applyLight(), 5 * 60000);
setInterval(() => { renderTop(); renderStatus(); }, 15000);
setInterval(() => { agents.forEach((a) => { if (a.data && a.state !== 'OFFLINE' && !DEMO) { a.shownState = null; setState(a, deriveState(a.data.raw)); } }); renderUI(); }, 30000);
const clock = new THREE.Clock(); let trainX = -200; const tmp = new THREE.Vector3(); let wallT = 0, portT = 0;
function frame() {
  requestAnimationFrame(frame); if (!renderer) return;
  const dt = Math.min(clock.getDelta(), 0.05), t = clock.elapsedTime;
  if (cam.goal) { const k = 1 - Math.exp(-dt * 3.2); cam.target.lerp(cam.goal.t, k); cam.yaw += (cam.goal.yaw - cam.yaw) * k; cam.pitch += (cam.goal.pitch - cam.pitch) * k; cam.dist += (cam.goal.dist - cam.dist) * k; if (Math.abs(cam.dist - cam.goal.dist) < 0.05 && cam.target.distanceTo(cam.goal.t) < 0.05) cam.goal = null; }
  if (!cam.goal && !openId && !replaying && performance.now() - lastInput > 45000) cam.yaw += dt * 0.025; // idle drift
  camera.position.set(cam.target.x + Math.sin(cam.yaw) * Math.cos(cam.pitch) * cam.dist, cam.target.y + Math.sin(cam.pitch) * cam.dist, cam.target.z + Math.cos(cam.yaw) * Math.cos(cam.pitch) * cam.dist);
  camera.lookAt(cam.target);
  trainX += dt * 14; if (trainX > 260) trainX = -320; train.position.x = trainX;
  for (const a of agents.values()) {
    const working = a.state === 'WORKING' || a.state === 'FAILED' || a.state === 'COMPLETED';
    const goal = working ? a.seat : a.stand; const dist = a.pos.distanceTo(goal);
    let kind;
    if (dist > 0.05) { tmp.subVectors(goal, a.pos).normalize(); a.pos.addScaledVector(tmp, Math.min(dist, dt * 1.3)); a.rig.root.rotation.y = Math.atan2(tmp.x, tmp.z); kind = 'walk'; }
    else { a.pos.copy(goal); if (working) { a.rig.root.rotation.y = Math.PI; kind = a.state === 'WORKING' ? 'type' : a.state === 'FAILED' ? 'slump' : 'relax'; } else { a.rig.root.rotation.y = Math.PI * 0.85; kind = a.state === 'IDLE' && (Math.floor((t + a.phase) / 9) % 2) ? 'phone' : 'stand'; } }
    a.rig.root.position.copy(a.pos); if (a.hero) heroPose(a.hero, kind, t, a.phase); else { pose(a.rig, kind, t, a.phase); glbPose(a, kind, dt); }
    if (a.rig.strap) a.rig.strap.rotation.x = kind === 'walk' ? Math.sin(t * 7) * 0.25 : kind === 'type' || kind === 'relax' || kind === 'slump' ? 1.2 : Math.sin(t * 1.3 + a.phase) * 0.04;
    a.desk.glow.material.opacity = a.state === 'WORKING' ? 0.22 + Math.sin(t * 3) * 0.08 : a.state === 'FAILED' ? 0.35 : 0;
    if (a.state === 'WORKING' && Math.floor(t * 4) !== a._f) { a._f = Math.floor(t * 4); a.phase += 0.35; drawMonitor(a); }
  }
  for (let i = packets.length - 1; i >= 0; i--) { const p = packets[i]; p.t += dt; const k = Math.max(0, Math.min(1, p.t / p.dur)); p.m.position.lerpVectors(p.from, p.to, k); p.m.position.y += Math.sin(k * Math.PI) * 3; p.m.rotation.y += dt * 3; if (k >= 1) { HQ.remove(p.m); packets.splice(i, 1); } }
  pins.forEach((p, i) => { const h = p.n ? 0.35 + p.n * 0.35 : 0.02; p.col.scale.y += (h - p.col.scale.y) * Math.min(1, dt * 3); p.col.position.y = 0.98 + p.col.scale.y / 2; const s = 1 + ((t * 0.6 + i * 0.25) % 1) * 1.6; p.ring.scale.set(s, s, s); p.ring.material.opacity = p.n ? 0.8 * (1 - ((t * 0.6 + i * 0.25) % 1)) : 0.15; });
  leds.forEach((l, i) => { l.visible = Math.sin(t * (2 + (i % 7)) + i) > -0.6; });
  neonLight.intensity = 5.5 + Math.sin(t * 9) * 0.25 + (Math.sin(t * 0.7) > 0.995 ? -3 : 0);
  if (t - wallT > 0.12) { wallT = t; drawWalls(t); }
  if (openId && t - portT > 1.5) { portT = t; drawPortrait(); }
  FRONT.visible = !(camera.position.y > hqH + 2 && camera.position.z < hqD / 2 + 45 && Math.abs(camera.position.x) < 60);
  placeCards();
  if (composer && (PROFILES[profileKey].bloom || PROFILES[profileKey].ao)) { if (bloom) bloom.enabled = PROFILES[profileKey].bloom; composer.render(); } else renderer.render(scene, camera);
}
if (!renderer) { document.body.insertAdjacentHTML('beforeend', '<div class="ncard" style="position:fixed;left:50%;top:40%;transform:translateX(-50%);z-index:9">3D view unavailable on this device. All panels still use live data.</div>'); }
// cinematic open: start wide over the street, fly into the HQ
cam.target.set(0, 4, 20); cam.yaw = 0.9; cam.pitch = 0.35; cam.dist = 90; goto('hq');
let lastInput = performance.now(); ['pointerdown', 'wheel', 'keydown'].forEach((ev) => addEventListener(ev, () => (lastInput = performance.now()), { passive: true }));
applyProfile(profileKey); loadEnvironment(); loadHero(); renderDock(); renderUI(); drawWalls(0); frame(); connect(); tryGLB();
window.__hq = { agents, live, cam, events, applyTriggers, applyPosts, openInspector, openView, applyProfile, goto };
</script>
</body>
</html>
