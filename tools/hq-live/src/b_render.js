
// ---------------------------------------------------------------------------
// Renderer, performance profiles, post processing
// ---------------------------------------------------------------------------
const store = { get(k, d) { try { const v = localStorage.getItem('hq.' + k); return v == null ? d : v; } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem('hq.' + k, v); } catch (e) {} } };
const autoProfile = matchMedia('(pointer: coarse)').matches && Math.min(innerWidth, innerHeight) < 820 ? 'mobile' : (navigator.hardwareConcurrency || 4) >= 8 ? 'high' : 'standard';
const PROFILES = {
  high: { label: 'High end desktop', pr: 2, shadows: true, shadowMap: 2048, bloom: true, bloomScale: 1, cards: 'full', ao: true },
  standard: { label: 'Standard desktop', pr: 1.25, shadows: true, shadowMap: 1024, bloom: true, bloomScale: 0.5, cards: 'full', ao: false },
  mobile: { label: 'Mobile', pr: 1, shadows: false, shadowMap: 512, bloom: false, bloomScale: 0.5, cards: 'mini', ao: false },
};
let profileKey = store.get('profile', autoProfile); if (!PROFILES[profileKey]) profileKey = autoProfile;
const canvas = document.getElementById('c');
let renderer = null;
try { renderer = new THREE.WebGLRenderer({ canvas, antialias: profileKey !== 'mobile', powerPreference: 'high-performance' }); } catch (e) { renderer = null; }
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(46, innerWidth / innerHeight, 0.3, 1200);
let composer = null, bloom = null, gtao = null;
if (renderer) {
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
  try {
    composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(innerWidth, innerHeight, { type: THREE.HalfFloatType, samples: profileKey === 'mobile' ? 0 : 4 }));
    composer.addPass(new RenderPass(scene, camera));
    try { gtao = new GTAOPass(scene, camera, innerWidth, innerHeight); gtao.output = GTAOPass.OUTPUT.Default; gtao.blendIntensity = 0.85; gtao.updateGtaoMaterial({ radius: 0.5, distanceExponent: 1.4, thickness: 1.2, scale: 1.0 }); composer.addPass(gtao); } catch (e) { gtao = null; }
    bloom = new UnrealBloomPass(new THREE.Vector2(innerWidth, innerHeight), 0.55, 0.55, 0.82);
    composer.addPass(bloom); composer.addPass(new OutputPass());
  } catch (e) { composer = null; }
}
function applyProfile(key) {
  profileKey = key; store.set('profile', key); const P = PROFILES[key]; if (!renderer) return;
  renderer.setPixelRatio(Math.min(devicePixelRatio, P.pr)); renderer.setSize(innerWidth, innerHeight, false);
  if (renderer.shadowMap.enabled !== P.shadows) { renderer.shadowMap.enabled = P.shadows; scene.traverse((o) => { if (o.material) [].concat(o.material).forEach((m) => (m.needsUpdate = true)); }); }
  try { sun.shadow.mapSize.set(P.shadowMap, P.shadowMap); if (sun.shadow.map) { sun.shadow.map.dispose(); sun.shadow.map = null; } } catch (e) {}
  if (composer) { composer.setPixelRatio(Math.min(devicePixelRatio, P.pr)); composer.setSize(innerWidth, innerHeight); bloom.enabled = P.bloom; if (gtao) gtao.enabled = P.ao; bloom.resolution.set(innerWidth * P.bloomScale, innerHeight * P.bloomScale); }
  document.body.dataset.profile = key;
}
addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); applyProfile(profileKey); });
