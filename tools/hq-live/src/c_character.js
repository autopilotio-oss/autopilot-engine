
// ---------------------------------------------------------------------------
// Production character: MakeHuman body (CC0) + modeled balaclava and hood, Mixamo-named skeleton with fingers.
// Built by tools/character in the repo. Poses are solved by aiming bones at target directions, so they hold for any rest pose.
// ---------------------------------------------------------------------------
const heroState = { loaded: false, failed: false };
const B = (n) => 'mixamorig' + n;
const LIMBS = [ // bone, child used for direction
  ['Spine', 'Spine1'], ['Spine1', 'Spine2'], ['Spine2', 'Neck'], ['Neck', 'Head'],
  ['LeftArm', 'LeftForeArm'], ['LeftForeArm', 'LeftHand'], ['RightArm', 'RightForeArm'], ['RightForeArm', 'RightHand'],
  ['LeftUpLeg', 'LeftLeg'], ['LeftLeg', 'LeftFoot'], ['RightUpLeg', 'RightLeg'], ['RightLeg', 'RightFoot'],
];
const _v1 = new THREE.Vector3(), _v2 = new THREE.Vector3(), _q1 = new THREE.Quaternion(), _q2 = new THREE.Quaternion(), _q3 = new THREE.Quaternion();
function aim(bone, child, dirRoot, rootQ) { // rotate bone so bone->child points along dirRoot (root space)
  bone.updateWorldMatrix(true, false); child.updateWorldMatrix(false, false);
  bone.getWorldPosition(_v1); child.getWorldPosition(_v2); const cur = _v2.sub(_v1).normalize();
  const want = _v1.copy(dirRoot).normalize().applyQuaternion(rootQ);
  _q1.setFromUnitVectors(cur, want); bone.getWorldQuaternion(_q2); _q2.premultiply(_q1);
  bone.parent.getWorldQuaternion(_q3); bone.quaternion.copy(_q3.invert().multiply(_q2));
}
const V = (x, y, z) => new THREE.Vector3(x, y, z);
function heroPose(h, kind, t, k) {
  const b = h.bones; if (!b.Hips) return;
  for (const [n, bn] of Object.entries(b)) bn.quaternion.copy(h.rest[n]);
  b.Hips.position.copy(h.restHip);
  const s = Math.sin, P = {};
  const seated = kind === 'sit' || kind === 'type' || kind === 'slump' || kind === 'relax';
  if (seated) {
    b.Hips.position.y = h.restHip.y - h.sitDrop; b.Hips.position.z = h.restHip.z - 0.06 * h.scale;
    P.LeftUpLeg = V(0.08, -0.12, 1); P.RightUpLeg = V(-0.08, -0.12, 1); P.LeftLeg = V(0.03, -1, 0.12); P.RightLeg = V(-0.03, -1, 0.12);
    if (kind === 'type') {
      const lean = 0.18 + s(t * 0.7 + k) * 0.02;
      P.Spine = V(0, 1, lean); P.Spine1 = V(0, 1, lean); P.Spine2 = V(0, 1, lean * 0.6); P.Neck = V(s(t * 0.5 + k) * 0.08, 1, 0.35);
      P.LeftArm = V(0.28, -0.75, 0.6); P.RightArm = V(-0.28, -0.75, 0.6);
      P.LeftForeArm = V(-0.12, -0.3 + s(t * 14 + k) * 0.05, 1); P.RightForeArm = V(0.12, -0.3 + s(t * 13 + k + 1.7) * 0.05, 1);
    } else if (kind === 'slump') {
      P.Spine = V(0, 1, 0.45); P.Spine1 = V(0, 1, 0.5); P.Spine2 = V(0, 1, 0.4); P.Neck = V(0, 0.6, 1);
      P.LeftArm = V(0.2, -0.3, 1); P.RightArm = V(-0.2, -0.3, 1); P.LeftForeArm = V(-0.6, 0.6, 0.6); P.RightForeArm = V(0.6, 0.6, 0.6);
    } else if (kind === 'relax') {
      P.Spine = V(0, 1, -0.22); P.Spine1 = V(0, 1, -0.12); P.Neck = V(0, 1, 0.05);
      P.LeftArm = V(0.6, 0.75, -0.25); P.RightArm = V(-0.6, 0.75, -0.25); P.LeftForeArm = V(-0.75, 0.25, -0.35); P.RightForeArm = V(0.75, 0.25, -0.35);
    } else { P.LeftArm = V(0.2, -1, 0.25); P.RightArm = V(-0.2, -1, 0.25); P.LeftForeArm = V(0, -0.4, 1); P.RightForeArm = V(0, -0.4, 1); }
  } else if (kind === 'walk') {
    const a = s(t * 6.2 + k), c = s(t * 6.2 + k + Math.PI / 2);
    b.Hips.position.y = h.restHip.y + Math.abs(c) * 0.025 * h.scale;
    P.LeftUpLeg = V(0.05, -1, a * 0.5); P.RightUpLeg = V(-0.05, -1, -a * 0.5);
    P.LeftLeg = V(0.02, -1, a * 0.5 - Math.max(0, -a) * 0.9); P.RightLeg = V(-0.02, -1, -a * 0.5 - Math.max(0, a) * 0.9);
    P.LeftArm = V(0.16, -1, -a * 0.35); P.RightArm = V(-0.16, -1, a * 0.35); P.LeftForeArm = V(0.06, -1, -a * 0.2 + 0.35); P.RightForeArm = V(-0.06, -1, a * 0.2 + 0.35);
    P.Spine = V(0, 1, 0.05); P.Neck = V(0, 1, 0.08);
  } else {
    const br = s(t * 1.4 + k) * 0.012;
    P.LeftUpLeg = V(0.07, -1, 0.02); P.RightUpLeg = V(-0.07, -1, 0.02); P.LeftLeg = V(0.02, -1, 0); P.RightLeg = V(-0.02, -1, 0);
    P.Spine = V(0, 1, br); P.Spine2 = V(0, 1, 0.02);
    if (kind === 'phone') {
      P.LeftArm = V(0.25, -1, 0.35); P.RightArm = V(-0.25, -1, 0.35); P.LeftForeArm = V(-0.55, 0.45, 0.8); P.RightForeArm = V(0.55, 0.45, 0.8); P.Neck = V(0, 0.75, 0.75);
    } else {
      P.LeftArm = V(0.17, -1, 0.04); P.RightArm = V(-0.17, -1, 0.04); P.LeftForeArm = V(0.05, -1, 0.18); P.RightForeArm = V(-0.05, -1, 0.18);
      P.Neck = V(s(t * 0.3 + k) * 0.25, 1, 0.05);
    }
  }
  h.root.updateWorldMatrix(true, false); const rq = h.holder.getWorldQuaternion(new THREE.Quaternion());
  for (const [n, c] of LIMBS) if (P[n] && b[n] && b[c]) { P[n].x *= h.lx; P[n].z *= h.fz; aim(b[n], b[c], P[n], rq); }
  if (h.phone) h.phone.visible = kind === 'phone';
}
// Rebind: the MakeHuman mesh is modeled in an A-pose while the skeleton rests in a T-pose. Measure the real joint
// positions from the skin weights (elbow = verts shared by upper and lower arm, etc.), turn the bones to match, recompute inverses.
function rebindToMesh(src) {
  src.updateMatrixWorld(true);
  let body = null; src.traverse((o) => { if (o.isSkinnedMesh && (!body || o.geometry.attributes.position.count > body.geometry.attributes.position.count)) body = o; });
  if (!body) return;
  const sk = body.skeleton, idx = {}; sk.bones.forEach((b, i) => (idx[b.name.replace('mixamorig', '').replace(':', '')] = i));
  const P = body.geometry.attributes.position, SI = body.geometry.attributes.skinIndex, SW = body.geometry.attributes.skinWeight;
  const joint = (a, b2, lo = 0.2) => { const ia = idx[a], ib = idx[b2]; if (ia == null || ib == null) return null; const c = new THREE.Vector3(); let n = 0; const v = new THREE.Vector3();
    for (let i = 0; i < P.count; i++) { let wa = 0, wb = 0; for (let k = 0; k < 4; k++) { const j = SI.getComponent(i, k), w = SW.getComponent(i, k); if (j === ia) wa = w; if (j === ib) wb = w; }
      if (wa > lo && wb > lo) { c.add(v.fromBufferAttribute(P, i).applyMatrix4(body.matrixWorld)); n++; } }
    return n ? c.divideScalar(n) : null; };
  const tip = (a) => { const ia = idx[a]; if (ia == null) return null; const c = new THREE.Vector3(); let n = 0; const v = new THREE.Vector3();
    for (let i = 0; i < P.count; i++) for (let k = 0; k < 4; k++) if (SI.getComponent(i, k) === ia && SW.getComponent(i, k) > 0.7) { c.add(v.fromBufferAttribute(P, i).applyMatrix4(body.matrixWorld)); n++; }
    return n ? c.divideScalar(n) : null; };
  const turn = (name, childName, target) => { const b = sk.bones[idx[name]], c = sk.bones[idx[childName]]; if (!b || !c || !target) return;
    b.updateWorldMatrix(true, false); c.updateWorldMatrix(false, false); const p0 = b.getWorldPosition(new THREE.Vector3()), p1 = c.getWorldPosition(new THREE.Vector3());
    const q = new THREE.Quaternion().setFromUnitVectors(p1.sub(p0).normalize(), target.clone().sub(p0).normalize()); const wq = b.getWorldQuaternion(new THREE.Quaternion()).premultiply(q);
    const pq = b.parent.getWorldQuaternion(new THREE.Quaternion()).invert(); b.quaternion.copy(pq.multiply(wq)); b.updateWorldMatrix(false, true); };
  for (const s2 of ['Left', 'Right']) {
    const elbow = joint(s2 + 'Arm', s2 + 'ForeArm'), wrist = joint(s2 + 'ForeArm', s2 + 'Hand'), fingers = tip(s2 + 'HandMiddle1');
    turn(s2 + 'Arm', s2 + 'ForeArm', elbow); turn(s2 + 'ForeArm', s2 + 'Hand', wrist); turn(s2 + 'Hand', s2 + 'HandMiddle1', fingers);
  }
  src.updateMatrixWorld(true);
  src.traverse((o) => { if (o.isSkinnedMesh) o.skeleton.calculateInverses(); });
}
async function loadHero() {
  if (!renderer) return;
  try {
    const SU = await import('three/addons/utils/SkeletonUtils.js');
    const src = await loadModel('operative'); if (!src) { heroState.failed = true; return; }
    rebindToMesh(src);
    const bb = new THREE.Box3().setFromObject(src); const hgt = bb.max.y - bb.min.y; const scale = 1.78 / hgt;
    for (const a of agents.values()) attachHero(a, src, SU, scale);
    heroState.loaded = true; heroState.src = src; heroState.SU = SU; heroState.scale = scale;
  } catch (e) { heroState.failed = true; console.warn('hero', e); }
}
function attachHero(a, src, SU, scale) {
  if (a.hero) return;
  const m = SU.clone(src); m.scale.setScalar(scale);
  const bones = {}; m.traverse((o) => { if (o.isBone && o.name.startsWith('mixamorig')) bones[o.name.replace('mixamorig', '').replace(':', '')] = o; if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; o.userData.agentId = a.id; } });
  const rest = {}; for (const [n, b] of Object.entries(bones)) rest[n] = b.quaternion.clone();
  m.traverse((o) => { if (o.isMesh) [].concat(o.material).forEach((mt) => { mt.side = THREE.DoubleSide; mt.transparent = false; mt.alphaTest = 0.5; mt.depthWrite = true; }); });
  const holder = new THREE.Group(); holder.add(m); a.rig.root.add(holder);
  a.rig.root.traverse((o) => { if (o.isMesh && !holder.getObjectById(o.id)) o.visible = false; });
  const restHip = bones.Hips ? bones.Hips.position.clone() : new THREE.Vector3();
  const phone = new THREE.Group(); if (bones.RightHand) { bones.RightHand.add(phone); phone.position.set(0, 0.09 / scale, 0.03 / scale); phone.scale.setScalar(1 / scale); }
  phone.add(new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.15, 0.01), new THREE.MeshStandardMaterial({ color: 0x1b1c1f, metalness: 0.6, roughness: 0.35 })));
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(0.066, 0.14), new THREE.MeshBasicMaterial({ color: 0x9fe8ff, toneMapped: false })); scr.position.z = 0.0055; phone.add(scr);
  // which way is the skeleton's left and forward, measured in the holder's space (so pose directions never come out mirrored)
  holder.updateWorldMatrix(true, true); const inv = holder.matrixWorld.clone().invert(); const wp = (bn) => bn.getWorldPosition(new THREE.Vector3()).applyMatrix4(inv);
  const lx = bones.LeftArm && bones.RightArm ? Math.sign(wp(bones.LeftArm).x - wp(bones.RightArm).x) || 1 : 1;
  const fz = bones.LeftToeBase && bones.LeftFoot ? Math.sign(wp(bones.LeftToeBase).z - wp(bones.LeftFoot).z) || 1 : 1;
  a.hero = { root: m, holder, bones, rest, restHip, scale, sitDrop: (restHip.y * scale - 0.62) / scale, phone, lx, fz };
}
