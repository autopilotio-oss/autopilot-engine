// ---------------------------------------------------------------------------
// Characters: faceless streetwear operatives with a simple rig
// ---------------------------------------------------------------------------
// Cloth textures: fleece for hoodies, denim for jeans (procedural, used as color + bump)
const noiseTex = (base, amp, lines, rep) => canvasTex(256, 256, (g, w, h) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 9000; i++) { const v = (rnd() - 0.5) * amp; g.fillStyle = v > 0 ? `rgba(255,255,255,${v})` : `rgba(0,0,0,${-v})`; g.fillRect(rnd() * w, rnd() * h, 1.5, 1.5); }
  if (lines) { g.strokeStyle = 'rgba(255,255,255,.035)'; for (let x = 0; x < w; x += 3) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x + h * 0.4, h); g.stroke(); } }
}, rep);
const fleece = noiseTex('#8a8a8e', 0.16, false, [3, 3]);
const denim = noiseTex('#6a6c72', 0.22, true, [2, 4]);
const C = {
  jeans: new THREE.MeshStandardMaterial({ color: 0x15161a, roughness: 0.82, map: denim, bumpMap: denim, bumpScale: 0.6 }),
  shoe: new THREE.MeshStandardMaterial({ color: 0x0b0b0c, roughness: 0.45 }),
  sole: new THREE.MeshStandardMaterial({ color: 0xe9e7e2, roughness: 0.6 }),
  lace: new THREE.MeshStandardMaterial({ color: 0xdedcd6, roughness: 0.7 }),
  mask: new THREE.MeshPhysicalMaterial({ color: 0x0a0a0b, roughness: 0.9, sheen: 0.5, sheenColor: new THREE.Color(0x3a3a40), sheenRoughness: 0.8, map: fleece, bumpMap: fleece, bumpScale: 0.3 }),
  strap: new THREE.MeshStandardMaterial({ color: 0xf2f2ee, roughness: 0.6 }),
  rip: new THREE.MeshStandardMaterial({ color: 0x2c2d31, roughness: 1 }),
  string: new THREE.MeshStandardMaterial({ color: 0x1c1c1f, roughness: 0.8 }),
  skin: [0x6b4532, 0x8a5c40, 0x9c7052, 0x55362a, 0x7a4f3a].map((c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.55, emissive: c, emissiveIntensity: 0.18 })),
  eye: new THREE.MeshBasicMaterial({ color: 0x1a0f0a }),
  eyeW: new THREE.MeshStandardMaterial({ color: 0xe6e1d8, roughness: 0.3, emissive: 0x3a3833, emissiveIntensity: 0.6 }),
};
function limb(len, r1, r2, mat) { const g = new THREE.Group(); const m = new THREE.Mesh(new THREE.CapsuleGeometry((r1 + r2) / 2, len - (r1 + r2), 4, 10), mat); m.position.y = -len / 2; m.castShadow = true; g.add(m); return g; }
const add = (parent, geo, mat, x, y, z, sx = 1, sy = 1, sz = 1) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.scale.set(sx, sy, sz); m.castShadow = true; parent.add(m); return m; };
// Faceless Chicago streetwear operative: heather black fleece hoodie with the hood up, black balaclava with an eye slit,
// black skinny jeans (ripped knee on some), white strap off the belt loop, black sneakers with white soles, phone in hand.
function makeOperative(i, hue) {
  const tone = new THREE.Color(hue).lerp(new THREE.Color(0x2a2a2e), 0.55);
  const hoodie = new THREE.MeshPhysicalMaterial({ color: tone, roughness: 0.96, sheen: 0.7, sheenColor: new THREE.Color(0x5a5a62), sheenRoughness: 0.75, map: fleece, bumpMap: fleece, bumpScale: 0.5 });
  const rib = new THREE.MeshPhysicalMaterial({ color: tone.clone().multiplyScalar(0.8), roughness: 1, sheen: 0.4, sheenColor: new THREE.Color(0x44444a) });
  const skin = C.skin[i % C.skin.length];
  const root = new THREE.Group();
  const hips = new THREE.Group(); hips.position.y = 0.95; root.add(hips);
  add(hips, new THREE.CapsuleGeometry(0.15, 0.14, 4, 12), C.jeans, 0, 0.02, 0, 1, 1, 0.78).rotation.z = Math.PI / 2;
  add(hips, new THREE.BoxGeometry(0.34, 0.035, 0.22), C.string, 0, 0.12, 0); // belt line under the hem
  const torso = new THREE.Group(); torso.position.y = 0.08; hips.add(torso);
  // boxy fleece body, a little loose: wider shoulders, hem band, kangaroo pocket, drawstrings
  add(torso, new THREE.CapsuleGeometry(0.205, 0.36, 8, 16), hoodie, 0, 0.32, 0, 1.18, 1, 0.74);
  add(torso, new THREE.CapsuleGeometry(0.16, 0.2, 6, 14), hoodie, 0, 0.47, 0, 1.38, 0.6, 0.78); // shoulder yoke
  add(torso, new THREE.CylinderGeometry(0.205, 0.2, 0.07, 20), rib, 0, 0.05, 0, 1.18, 1, 0.76);
  const pocket = add(torso, new THREE.CapsuleGeometry(0.06, 0.2, 4, 10), hoodie, 0, 0.17, 0.142, 1, 1, 0.35); pocket.rotation.z = Math.PI / 2;
  add(torso, new THREE.BoxGeometry(0.012, 0.11, 0.02), C.string, -0.15, 0.17, 0.142).rotation.z = 0.25; // pocket openings
  add(torso, new THREE.BoxGeometry(0.012, 0.11, 0.02), C.string, 0.15, 0.17, 0.142).rotation.z = -0.25;
  [-0.045, 0.045].forEach((dx) => { add(torso, new THREE.CylinderGeometry(0.006, 0.006, 0.2, 5), C.string, dx, 0.5, 0.16); add(torso, new THREE.CylinderGeometry(0.009, 0.009, 0.03, 6), C.lace, dx, 0.39, 0.16); });
  const neck = new THREE.Group(); neck.position.y = 0.68; torso.add(neck);
  add(neck, new THREE.CylinderGeometry(0.075, 0.09, 0.12, 12), C.mask, 0, 0.05, 0.01);
  const head = new THREE.Group(); head.position.y = 0.15; neck.add(head);
  // hood: open in front, slight peak, thick rolled edge
  const hoodIn = new THREE.MeshStandardMaterial({ color: 0x040405, roughness: 1, side: THREE.BackSide });
  const hoodGeo = new THREE.SphereGeometry(0.18, 22, 16, Math.PI / 2 + 0.9, Math.PI * 2 - 1.8, 0, Math.PI * 0.8);
  add(head, hoodGeo, hoodie, 0, 0.035, -0.03, 1.1, 1.24, 1.18);
  add(head, hoodGeo, hoodIn, 0, 0.035, -0.03, 1.08, 1.22, 1.16).castShadow = false;
  add(head, new THREE.SphereGeometry(0.18, 22, 10, 0, Math.PI * 2, 0, Math.PI * 0.22), hoodie, 0, 0.035, -0.03, 1.1, 1.3, 1.18);
  add(head, new THREE.ConeGeometry(0.07, 0.08, 12), hoodie, 0, 0.255, -0.06, 1, 1, 0.8).rotation.x = -0.35;
  add(head, new THREE.TorusGeometry(0.13, 0.034, 12, 30), hoodie, 0, 0.01, 0.113, 1.0, 1.32, 1.25);
  // balaclava with an eye slit; skin only around the eyes
  add(head, new THREE.SphereGeometry(0.112, 22, 16), skin, 0, 0, 0.03, 0.92, 1.14, 0.98);
  add(head, new THREE.SphereGeometry(0.117, 22, 12, 0, Math.PI * 2, 0, Math.PI * 0.42), C.mask, 0, 0, 0.03, 0.92, 1.14, 0.98);
  add(head, new THREE.SphereGeometry(0.117, 22, 12, 0, Math.PI * 2, Math.PI * 0.53, Math.PI * 0.47), C.mask, 0, 0, 0.03, 0.92, 1.14, 0.98);
  add(head, new THREE.SphereGeometry(0.02, 10, 8), C.mask, 0, -0.02, 0.124, 0.75, 1.15, 0.6);
  [-0.037, 0.037].forEach((dx) => {
    add(head, new THREE.SphereGeometry(0.017, 12, 8), C.eyeW, dx, 0.015, 0.131, 1.3, 0.5, 0.45);
    add(head, new THREE.SphereGeometry(0.0095, 10, 8), C.eye, dx, 0.015, 0.137, 1, 1, 0.5);
    add(head, new THREE.SphereGeometry(0.0025, 6, 4), C.eyeW, dx + 0.003, 0.018, 0.1405);
    add(head, new THREE.BoxGeometry(0.034, 0.006, 0.01), C.mask, dx, 0.034, 0.128).rotation.z = dx > 0 ? -0.12 : 0.12;
  });
  const mkArm = (s) => {
    const sh = new THREE.Group(); sh.position.set(s * 0.255, 0.55, 0); torso.add(sh);
    const up = limb(0.32, 0.09, 0.078, hoodie); sh.add(up);
    const el = new THREE.Group(); el.position.y = -0.31; up.add(el);
    const fo = limb(0.27, 0.075, 0.064, hoodie); el.add(fo);
    add(fo, new THREE.CylinderGeometry(0.052, 0.056, 0.06, 12), rib, 0, -0.27, 0);
    const hand = add(fo, new THREE.CapsuleGeometry(0.035, 0.05, 4, 8), skin, 0, -0.33, 0.005, 1, 1, 0.7);
    return { sh, el, hand };
  };
  const ripped = i % 3 !== 1, strap = i % 2 === 0;
  const mkLeg = (s) => {
    const hp = new THREE.Group(); hp.position.set(s * 0.095, -0.02, 0); hips.add(hp);
    const th = limb(0.46, 0.098, 0.074, C.jeans); hp.add(th);
    const kn = new THREE.Group(); kn.position.y = -0.45; th.add(kn);
    const sn = limb(0.44, 0.07, 0.055, C.jeans); kn.add(sn);
    if (ripped && s > 0) add(sn, new THREE.CircleGeometry(0.035, 10), C.rip, 0, -0.03, 0.066, 1, 0.55, 1);
    // sneaker: rounded black upper, white midsole, white laces
    add(sn, new THREE.CapsuleGeometry(0.052, 0.17, 4, 10), C.shoe, 0, -0.45, 0.055, 1, 0.75, 1).rotation.x = Math.PI / 2;
    add(sn, new THREE.BoxGeometry(0.108, 0.03, 0.27), C.sole, 0, -0.5, 0.055);
    add(sn, new THREE.BoxGeometry(0.05, 0.012, 0.08), C.lace, 0, -0.412, 0.09);
    return { hp, kn };
  };
  const rig = { root, hips, torso, neck, head, aL: mkArm(-1), aR: mkArm(1), lL: mkLeg(-1), lR: mkLeg(1), hoodie };
  if (strap) { rig.strap = add(rig.lR.hp, new THREE.BoxGeometry(0.022, 0.42, 0.006), C.strap, 0.06, -0.2, 0.06); }
  const phone = new THREE.Group(); rig.aR.hand.add(phone); phone.position.set(-0.02, -0.03, 0.04); phone.rotation.x = -0.3;
  add(phone, new THREE.BoxGeometry(0.075, 0.15, 0.01), new THREE.MeshStandardMaterial({ color: 0x8c8f94, metalness: 0.9, roughness: 0.3 }), 0, 0, 0);
  add(phone, new THREE.PlaneGeometry(0.066, 0.14), new THREE.MeshBasicMaterial({ color: 0x9fe8ff, toneMapped: false }), 0, 0, 0.0055).castShadow = false;
  phone.visible = false; rig.phone = phone;
  return rig;
}
function pose(r, kind, t, k) {
  const s = Math.sin, z = (o) => { o.rotation.set(0, 0, 0); };
  [r.hips, r.torso, r.neck, r.head, r.aL.sh, r.aL.el, r.aR.sh, r.aR.el, r.lL.hp, r.lL.kn, r.lR.hp, r.lR.kn].forEach(z);
  r.phone.visible = false;
  if (kind === 'sit' || kind === 'type' || kind === 'slump' || kind === 'relax') {
    r.hips.position.y = 0.62;
    r.lL.hp.rotation.x = r.lR.hp.rotation.x = -1.45; r.lL.kn.rotation.x = r.lR.kn.rotation.x = 1.5;
    r.lL.hp.rotation.z = -0.08; r.lR.hp.rotation.z = 0.08;
    if (kind === 'type') {
      r.torso.rotation.x = 0.16 + s(t * 0.7 + k) * 0.02; r.neck.rotation.x = 0.12;
      r.aL.sh.rotation.x = r.aR.sh.rotation.x = -0.55; r.aL.sh.rotation.z = 0.12; r.aR.sh.rotation.z = -0.12;
      r.aL.el.rotation.x = -1.05 + s(t * 14 + k) * 0.06; r.aR.el.rotation.x = -1.05 + s(t * 13 + k + 1.7) * 0.06;
      r.head.rotation.y = s(t * 0.5 + k) * 0.12;
    } else if (kind === 'slump') {
      r.torso.rotation.x = 0.5; r.neck.rotation.x = 0.55; r.aL.sh.rotation.x = r.aR.sh.rotation.x = -2.6; r.aL.el.rotation.x = r.aR.el.rotation.x = -1.9; r.aL.sh.rotation.z = 0.4; r.aR.sh.rotation.z = -0.4;
    } else if (kind === 'relax') {
      r.torso.rotation.x = -0.22; r.neck.rotation.x = -0.1; r.aL.sh.rotation.x = r.aR.sh.rotation.x = -2.9; r.aL.el.rotation.x = r.aR.el.rotation.x = -2.0; r.aL.sh.rotation.z = 0.3; r.aR.sh.rotation.z = -0.3;
    } else { r.torso.rotation.x = 0.05; r.aL.sh.rotation.x = r.aR.sh.rotation.x = -0.35; r.aL.el.rotation.x = r.aR.el.rotation.x = -0.9; }
  } else if (kind === 'walk') {
    r.hips.position.y = 0.95 + Math.abs(s(t * 7)) * 0.03;
    const a = s(t * 7) * 0.55; r.lL.hp.rotation.x = a; r.lR.hp.rotation.x = -a; r.lL.kn.rotation.x = Math.max(0, -a) * 1.1 + 0.1; r.lR.kn.rotation.x = Math.max(0, a) * 1.1 + 0.1;
    r.aL.sh.rotation.x = -a * 0.7; r.aR.sh.rotation.x = a * 0.7; r.aL.el.rotation.x = r.aR.el.rotation.x = -0.35; r.torso.rotation.x = 0.06;
  } else { // stand / phone
    r.hips.position.y = 0.95; r.torso.rotation.x = s(t * 1.4 + k) * 0.015; r.aL.sh.rotation.z = 0.08; r.aR.sh.rotation.z = -0.08; r.aL.el.rotation.x = r.aR.el.rotation.x = -0.15;
    if (kind === 'phone') { r.aR.sh.rotation.x = -0.5; r.aR.sh.rotation.z = -0.3; r.aR.el.rotation.x = -1.6; r.aL.sh.rotation.x = -0.45; r.aL.sh.rotation.z = 0.32; r.aL.el.rotation.x = -1.5; r.neck.rotation.x = 0.42; r.head.rotation.x = 0.1; r.phone.visible = true; }
    else r.head.rotation.y = s(t * 0.3 + k) * 0.3;
  }
}
