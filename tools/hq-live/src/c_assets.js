
// ---------------------------------------------------------------------------
// Real assets: Poly Haven (CC0) textures, HDRI light and furniture models, served from this page's own files.
// Everything procedural stays visible until its real replacement has loaded, so a slow or failed load never breaks the HQ.
// ---------------------------------------------------------------------------
const AS = 'assets/';
const assetState = { textures: 0, models: 0, failed: [] };
const texLoader = new THREE.TextureLoader();
const gltfLoader = new GLTFLoader();
const liteAssets = () => profileKey === 'mobile';
function loadTex(path, srgb, rx, ry) {
  return new Promise((res) => texLoader.load(AS + path, (t) => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rx, ry); t.anisotropy = renderer ? Math.min(8, renderer.capabilities.getMaxAnisotropy()) : 1; if (srgb) t.colorSpace = THREE.SRGBColorSpace; res(t); }, undefined, () => res(null)));
}
async function applyPBR(mat, id, rx, ry, { tint = 0xffffff, normal = 1, maps = ['nor_gl', 'Rough'] } = {}) {
  const [d, n, r] = await Promise.all([loadTex(id + '/Diffuse.jpg', true, rx, ry), maps.includes('nor_gl') ? loadTex(id + '/nor_gl.jpg', false, rx, ry) : null, maps.includes('Rough') ? loadTex(id + '/Rough.jpg', false, rx, ry) : null]);
  if (!d) { assetState.failed.push(id); return; }
  mat.map = d; mat.color.set(tint); mat.bumpMap = null; mat.emissiveMap = null;
  if (n) { mat.normalMap = n; mat.normalScale.set(normal, normal); }
  if (r) { mat.roughnessMap = r; mat.roughness = 1; }
  mat.needsUpdate = true; assetState.textures++;
}
const modelCache = {};
function loadModel(id) {
  return modelCache[id] || (modelCache[id] = new Promise((res) => gltfLoader.load(`${AS}${id}/${id}.json`, (g) => {
    g.scene.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; if (o.material && o.material.map) o.material.map.anisotropy = 4; } });
    assetState.models++; res(g.scene);
  }, undefined, () => { assetState.failed.push(id); res(null); })));
}
// clone a model, scale it so one axis matches a target size, sit it on the floor of its parent
async function place(id, parent, { x = 0, y = 0, z = 0, rotY = 0, fit = 'h', size = 1, stretch = null, hide = [] } = {}) {
  const src = await loadModel(id); if (!src) return null;
  const m = src.clone(true); const bb = new THREE.Box3().setFromObject(m); const dim = bb.getSize(new THREE.Vector3());
  const k = size / Math.max(1e-4, fit === 'w' ? Math.max(dim.x, dim.z) : fit === 'x' ? dim.x : dim.y);
  m.scale.setScalar(k); if (stretch) m.scale.multiply(new THREE.Vector3(...stretch));
  const wrap = new THREE.Group(); wrap.add(m); m.position.set(-(bb.min.x + dim.x / 2) * m.scale.x, -bb.min.y * m.scale.y, -(bb.min.z + dim.z / 2) * m.scale.z);
  wrap.position.set(x, y, z); wrap.rotation.y = rotY; parent.add(wrap);
  hide.forEach((o) => (o.visible = false));
  return wrap;
}
// desks: real metal office desk, a little wider so three monitors fit; some get an arm lamp
let deskN = 0;
function decorateDesk(g, proc) {
  const n = deskN++;
  place('metal_office_desk', g, { fit: 'x', size: 2.0, stretch: [1.25, 1.0, 1.15], hide: proc }).then((w) => { if (w) w.traverse((o) => { if (o.isMesh) o.userData.agentId = g.children[0] && g.children[0].userData.agentId; }); });
  if (!liteAssets() && n % 3 === 1) place('desk_lamp_arm_01', g, { x: 1.05, y: 0.79, z: -0.35, rotY: -2.4, size: 0.62 });
}
function loadEnvironment() {
  if (!renderer) return;
  // photographic light from a real brick factory interior (HDRI) for reflections and soft fill
  texLoader.load(AS + 'brick_factory_01/brick_factory_01_env.jpg', (env) => {
    env.mapping = THREE.EquirectangularReflectionMapping; env.colorSpace = THREE.SRGBColorSpace; const pm = new THREE.PMREMGenerator(renderer);
    scene.environment = pm.fromEquirectangular(env).texture; scene.environmentIntensity = 0.7; env.dispose(); pm.dispose(); assetState.textures++;
  }, undefined, () => assetState.failed.push('environment light'));
  applyPBR(wallBrickIn, 'red_brick_03', hqW / 3, hqH / 3, { tint: 0xd8cfc8 });
  applyPBR(wallBrickSide, 'red_brick_03', hqD / 3, hqH / 3, { tint: 0xd8cfc8 });
  applyPBR(wallBrick, 'factory_brick', 1.2 / 3, hqH / 3);
  applyPBR(wallBand, 'factory_brick', hqW / 3, 0.35);
  applyPBR(M.floor, 'concrete_floor_worn_001', hqW / 4, hqD / 4, { tint: 0x8f8a83, normal: 0.6 });
  applyPBR(M.asphalt, 'asphalt_02', 900 / 5, 13 / 5, { tint: 0x9a9a9a });
  applyPBR(M.rust, 'rusty_metal_04', 1, 6, { maps: ['Rough'] });
  // pendant lamps
  pendants.forEach((p) => place('hanging_industrial_lamp', HQ, { x: p.x, y: hqH - 2.95, z: p.z, size: 1.4, hide: [p.shade] }));
  // lounge
  place('sofa_02', HQ, { x: 15.3, y: 0.25, z: 9.2, rotY: -Math.PI / 2, size: 0.9, hide: [couch] });
  place('industrial_coffee_table', HQ, { x: 11.8, y: 0.25, z: 9.2, rotY: Math.PI / 2, size: 0.5, hide: [ctable] });
  // plants
  plants.forEach((p) => place('potted_plant_02', HQ, { x: p.g.position.x, y: 0.25, z: p.g.position.z, rotY: p.g.position.x, size: 1.15 * p.s, hide: [p.g] }));
  // steel shelving on the east wall
  place('steel_frame_shelves_01', HQ, { x: hqW / 2 - 0.75, y: 0.25, z: -1.5, rotY: -Math.PI / 2, size: 2.7, hide: [shelf] });
  place('wall_clock', HQ, { x: hqW / 2 - 0.34, y: 6.2, z: 6.5, rotY: -Math.PI / 2, size: 0.7 });
  if (liteAssets()) return;
  // street: real street lamps and a fire escape on the neighbor building
  lampGroups.forEach((l) => place('street_lamp_01', l.g, { y: 0, rotY: l.side ? 0 : Math.PI, size: 6.4, hide: [l.pole, l.head] }));
  place('modular_fire_escape', scene, { x: 30, y: 0.2, z: 13.4, size: 11 });
}
