// ---------------------------------------------------------------------------
// Lighting presets: live sky follows Chicago's local time
// ---------------------------------------------------------------------------
let lightMode = 'auto';
const chiHour = () => { const p = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Chicago', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date()); return +p.find((x) => x.type === 'hour').value + p.find((x) => x.type === 'minute').value / 60; };
function applyLight() {
  let mode = lightMode; if (mode === 'auto') { const h = chiHour(); mode = h >= 7 && h < 16 ? 'day' : h >= 16 && h < 18.5 ? 'sunset' : h >= 5.5 && h < 7 ? 'sunset' : 'night'; }
  const P = {
    day: { top: '#7f8fa2', bot: '#cfd4d8', fog: 0xb4bcc4, hemi: [0xd6dee6, 0x4a443c, 2.4], sun: [0xf2f0ea, 2.6], pos: [-60, 90, 60], night: 0, lamps: 0.5, exp: 1.0 },
    sunset: { top: '#2b2f4f', bot: '#e3875a', fog: 0x9a7466, hemi: [0xffb08a, 0x3b3230, 1.4], sun: [0xff9a5a, 2.6], pos: [-120, 22, 40], night: 0.55, lamps: 1.2, exp: 1.05 },
    night: { top: '#03050a', bot: '#1a2233', fog: 0x111722, hemi: [0x46557a, 0x15151a, 0.7], sun: [0x8fa2c8, 0.5], pos: [60, 80, 40], night: 1, lamps: 1.0, exp: 1.1 },
  }[mode];
  const g = skyCv.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, P.top); gr.addColorStop(0.62, P.bot); gr.addColorStop(1, P.bot); g.fillStyle = gr; g.fillRect(0, 0, 4, 256); skyTex.needsUpdate = true;
  scene.fog.color.setHex(P.fog); hemi.color.setHex(P.hemi[0]); hemi.groundColor.setHex(P.hemi[1]); hemi.intensity = P.hemi[2];
  sun.color.setHex(P.sun[0]); sun.intensity = P.sun[1]; sun.position.set(...P.pos);
  nightEmissive.forEach(([m, k]) => (m.emissiveIntensity = P.night * k));
  streetLights.forEach((l) => { if (l.isLight) l.intensity = P.night * 30; else l.emissiveIntensity = P.night * 3; });
  interior.forEach((l) => (l.intensity = P.lamps * 70 + 25));
  if (renderer) renderer.toneMappingExposure = P.exp;
}
