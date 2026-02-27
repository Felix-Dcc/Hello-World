/**
 * VR Dream Villa — Professional A-Frame Components, Shaders & PBR Material System
 * ================================================================================
 *
 * PBR: Procedural albedo + optional normal maps; roughness/metalness; anisotropy.
 * Shaders: water (pool), fountain-flow (fountain), sky-gradient.
 * Components: pbr-material, door-anim, ceiling-fan, light-toggle, tree-wind, pet-roam,
 *             vehicle-anim, fountain-flow.
 */

/* =====================================================================
   SECTION 1 — Procedural Texture Generation
   ===================================================================== */

const TEX_CACHE = {};

function makeCanvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w || 256;
  c.height = h || 256;
  return c;
}

/* ---- helpers ---- */

function hexToRgb(hex) {
  const n = parseInt(hex.replace('#', ''), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}

function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

/* ---- Wood Plank Floor ---- */
function texWoodPlanks() {
  if (TEX_CACHE.woodPlanks) return TEX_CACHE.woodPlanks;
  const S = 256, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#A07850';
  ctx.fillRect(0, 0, S, S);
  const pH = 32;
  for (let p = 0; p < S / pH; p++) {
    const y = p * pH;
    const v = 0.85 + Math.random() * 0.3;
    ctx.fillStyle = `rgba(${140 * v | 0},${100 * v | 0},${65 * v | 0},0.4)`;
    ctx.fillRect(0, y, S, pH);
    for (let g = 0; g < 18; g++) {
      const gy = y + 2 + Math.random() * (pH - 4);
      ctx.strokeStyle = `rgba(90,60,30,${(0.06 + Math.random() * 0.12).toFixed(2)})`;
      ctx.lineWidth = 0.5 + Math.random() * 1.5;
      ctx.beginPath();
      let cx = 0;
      ctx.moveTo(cx, gy);
      while (cx < S) { cx += 12 + Math.random() * 25; ctx.lineTo(cx, gy + (Math.random() - 0.5) * 1.5); }
      ctx.stroke();
    }
    ctx.strokeStyle = 'rgba(50,30,15,0.5)';
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(S, y); ctx.stroke();
    // occasional knot
    if (Math.random() > 0.65) {
      const kx = 30 + Math.random() * (S - 60), ky = y + pH / 2, kr = 3 + Math.random() * 5;
      ctx.fillStyle = 'rgba(80,50,25,0.35)';
      ctx.beginPath(); ctx.ellipse(kx, ky, kr, kr * 0.6, 0, 0, Math.PI * 2); ctx.fill();
    }
  }
  TEX_CACHE.woodPlanks = c;
  return c;
}

/* ---- Dark Wood (furniture) ---- */
function texWoodDark() {
  if (TEX_CACHE.woodDark) return TEX_CACHE.woodDark;
  const S = 256, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#5C3A1E';
  ctx.fillRect(0, 0, S, S);
  for (let i = 0; i < 90; i++) {
    const y = Math.random() * S;
    ctx.strokeStyle = `rgba(40,25,12,${(0.08 + Math.random() * 0.14).toFixed(2)})`;
    ctx.lineWidth = 0.4 + Math.random() * 1.2;
    ctx.beginPath(); let x = 0; ctx.moveTo(x, y);
    while (x < S) { x += 10 + Math.random() * 20; ctx.lineTo(x, y + (Math.random() - 0.5) * 2); }
    ctx.stroke();
  }
  TEX_CACHE.woodDark = c;
  return c;
}

/* ---- Wall Plaster ---- */
function texWall() {
  if (TEX_CACHE.wall) return TEX_CACHE.wall;
  const S = 256, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#F0EBE0';
  ctx.fillRect(0, 0, S, S);
  for (let i = 0; i < 4000; i++) {
    const x = Math.random() * S, y = Math.random() * S, v = Math.random() * 12;
    ctx.fillStyle = `rgba(${200 + v | 0},${195 + v | 0},${185 + v | 0},0.12)`;
    ctx.fillRect(x, y, 2 + Math.random() * 5, 2 + Math.random() * 5);
  }
  TEX_CACHE.wall = c;
  return c;
}

/* ---- Kitchen / Bathroom Tile ---- */
function texTile() {
  if (TEX_CACHE.tile) return TEX_CACHE.tile;
  const S = 256, tS = 32, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#D8D4CC';
  ctx.fillRect(0, 0, S, S);
  for (let ty = 0; ty < S; ty += tS) {
    for (let tx = 0; tx < S; tx += tS) {
      const v = 0.94 + Math.random() * 0.12;
      ctx.fillStyle = `rgb(${215 * v | 0},${210 * v | 0},${205 * v | 0})`;
      ctx.fillRect(tx + 1, ty + 1, tS - 2, tS - 2);
    }
  }
  ctx.strokeStyle = '#B8B4AC'; ctx.lineWidth = 1;
  for (let i = 0; i <= S; i += tS) {
    ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, S); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(S, i); ctx.stroke();
  }
  TEX_CACHE.tile = c;
  return c;
}

/* ---- Fabric (parametric colour) ---- */
function texFabric(baseHex) {
  const key = 'fabric_' + baseHex;
  if (TEX_CACHE[key]) return TEX_CACHE[key];
  const [br, bg, bb] = hexToRgb(baseHex);
  const S = 128, c = makeCanvas(S, S), ctx = c.getContext('2d');
  const id = ctx.createImageData(S, S);
  for (let i = 0; i < id.data.length; i += 4) {
    const n = (Math.random() - 0.5) * 18;
    id.data[i] = clamp(br + n, 0, 255);
    id.data[i + 1] = clamp(bg + n, 0, 255);
    id.data[i + 2] = clamp(bb + n, 0, 255);
    id.data[i + 3] = 255;
  }
  ctx.putImageData(id, 0, 0);
  // weave overlay
  ctx.globalAlpha = 0.06;
  for (let y = 0; y < S; y += 2) {
    ctx.fillStyle = y % 4 === 0 ? 'white' : 'black';
    ctx.fillRect(0, y, S, 1);
  }
  ctx.globalAlpha = 1;
  TEX_CACHE[key] = c;
  return c;
}

/* ---- Grass ---- */
function texGrass() {
  if (TEX_CACHE.grass) return TEX_CACHE.grass;
  const S = 256, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#4A8B3F';
  ctx.fillRect(0, 0, S, S);
  for (let i = 0; i < 6000; i++) {
    const x = Math.random() * S, y = Math.random() * S;
    const g = 100 + Math.random() * 60, r = 50 + Math.random() * 30, b = 30 + Math.random() * 20;
    ctx.fillStyle = `rgba(${r | 0},${g | 0},${b | 0},0.18)`;
    ctx.fillRect(x, y, 1 + Math.random() * 3, 1 + Math.random() * 3);
  }
  // blade hints
  ctx.strokeStyle = 'rgba(30,80,20,0.08)'; ctx.lineWidth = 0.5;
  for (let i = 0; i < 300; i++) {
    const x = Math.random() * S, y = Math.random() * S;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + (Math.random() - 0.5) * 4, y - 3 - Math.random() * 5); ctx.stroke();
  }
  TEX_CACHE.grass = c;
  return c;
}

/* ---- Pool Tile ---- */
function texPoolTile() {
  if (TEX_CACHE.poolTile) return TEX_CACHE.poolTile;
  const S = 256, tS = 32, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#3498DB';
  ctx.fillRect(0, 0, S, S);
  for (let ty = 0; ty < S; ty += tS) {
    for (let tx = 0; tx < S; tx += tS) {
      const v = 0.92 + Math.random() * 0.16;
      ctx.fillStyle = `rgb(${45 * v | 0},${130 * v | 0},${195 * v | 0})`;
      ctx.fillRect(tx + 1, ty + 1, tS - 2, tS - 2);
    }
  }
  ctx.strokeStyle = '#2471A3'; ctx.lineWidth = 1;
  for (let i = 0; i <= S; i += tS) {
    ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, S); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(S, i); ctx.stroke();
  }
  TEX_CACHE.poolTile = c;
  return c;
}

/* ---- Concrete ---- */
function texConcrete() {
  if (TEX_CACHE.concrete) return TEX_CACHE.concrete;
  const S = 256, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#C0BBB0';
  ctx.fillRect(0, 0, S, S);
  for (let i = 0; i < 5000; i++) {
    const x = Math.random() * S, y = Math.random() * S, v = Math.random() * 20 - 10;
    ctx.fillStyle = `rgba(${170 + v | 0},${165 + v | 0},${155 + v | 0},0.15)`;
    ctx.fillRect(x, y, 1 + Math.random() * 4, 1 + Math.random() * 4);
  }
  TEX_CACHE.concrete = c;
  return c;
}

/* ---- Marble (vanity / bathroom counters) ---- */
function texMarble() {
  if (TEX_CACHE.marble) return TEX_CACHE.marble;
  const S = 256, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#F5F0EA';
  ctx.fillRect(0, 0, S, S);
  // marble veins
  for (let v = 0; v < 25; v++) {
    const sx = Math.random() * S, sy = Math.random() * S;
    ctx.strokeStyle = `rgba(${160 + Math.random() * 40 | 0},${150 + Math.random() * 35 | 0},${140 + Math.random() * 30 | 0},${(0.15 + Math.random() * 0.2).toFixed(2)})`;
    ctx.lineWidth = 0.5 + Math.random() * 2;
    ctx.beginPath(); ctx.moveTo(sx, sy);
    let cx = sx, cy = sy;
    for (let s = 0; s < 8; s++) {
      cx += (Math.random() - 0.5) * 60;
      cy += (Math.random() - 0.5) * 60;
      ctx.quadraticCurveTo(cx + (Math.random() - 0.5) * 30, cy + (Math.random() - 0.5) * 30, cx, cy);
    }
    ctx.stroke();
  }
  // subtle noise
  for (let i = 0; i < 2000; i++) {
    const x = Math.random() * S, y = Math.random() * S;
    ctx.fillStyle = `rgba(${220 + Math.random() * 30 | 0},${215 + Math.random() * 30 | 0},${210 + Math.random() * 25 | 0},0.08)`;
    ctx.fillRect(x, y, 2 + Math.random() * 3, 2 + Math.random() * 3);
  }
  TEX_CACHE.marble = c;
  return c;
}

/* ---- Bathroom Tile (white/light) ---- */
function texBathroomTile() {
  if (TEX_CACHE.bathroomTile) return TEX_CACHE.bathroomTile;
  const S = 256, tS = 32, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#ECE8E0';
  ctx.fillRect(0, 0, S, S);
  for (let ty = 0; ty < S; ty += tS) {
    for (let tx = 0; tx < S; tx += tS) {
      const v = 0.96 + Math.random() * 0.08;
      ctx.fillStyle = `rgb(${230 * v | 0},${226 * v | 0},${220 * v | 0})`;
      ctx.fillRect(tx + 1, ty + 1, tS - 2, tS - 2);
    }
  }
  ctx.strokeStyle = '#C8C4BC'; ctx.lineWidth = 1;
  for (let i = 0; i <= S; i += tS) {
    ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, S); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(S, i); ctx.stroke();
  }
  TEX_CACHE.bathroomTile = c;
  return c;
}

/* ---- Roof Tile (terracotta) ---- */
function texRoofTile() {
  if (TEX_CACHE.roofTile) return TEX_CACHE.roofTile;
  const S = 256, tH = 24, c = makeCanvas(S, S), ctx = c.getContext('2d');
  ctx.fillStyle = '#6D4C41';
  ctx.fillRect(0, 0, S, S);
  for (let row = 0; row < S / tH; row++) {
    const y = row * tH;
    const offset = (row % 2) * (S / 6);
    const v = 0.88 + Math.random() * 0.24;
    ctx.fillStyle = `rgb(${105 * v | 0},${72 * v | 0},${60 * v | 0})`;
    ctx.fillRect(0, y + 1, S, tH - 2);
    // tile segment lines
    for (let tx = offset; tx < S; tx += S / 3) {
      ctx.strokeStyle = 'rgba(40,28,20,0.35)';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(tx, y); ctx.lineTo(tx, y + tH); ctx.stroke();
    }
    // row divider
    ctx.strokeStyle = 'rgba(30,20,15,0.5)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(S, y); ctx.stroke();
    // subtle highlight on each tile
    ctx.fillStyle = `rgba(180,140,110,${(0.05 + Math.random() * 0.08).toFixed(2)})`;
    ctx.fillRect(0, y + 2, S, tH / 3);
  }
  TEX_CACHE.roofTile = c;
  return c;
}

/* ---- Metal / car body (subtle variation for reflections) ---- */
function texMetal(baseHex) {
  const key = 'metal_' + baseHex;
  if (TEX_CACHE[key]) return TEX_CACHE[key];
  const [br, bg, bb] = hexToRgb(baseHex);
  const S = 256, c = makeCanvas(S, S), ctx = c.getContext('2d');
  const id = ctx.createImageData(S, S);
  for (let i = 0; i < id.data.length; i += 4) {
    const n = (Math.random() - 0.5) * 12;
    id.data[i] = clamp(br + n, 0, 255);
    id.data[i + 1] = clamp(bg + n, 0, 255);
    id.data[i + 2] = clamp(bb + n, 0, 255);
    id.data[i + 3] = 255;
  }
  ctx.putImageData(id, 0, 0);
  TEX_CACHE[key] = c;
  return c;
}

/* ---- Procedural normal map (tangent-space, neutral with slight variation) ---- */
function texNormalMap(strength) {
  const key = 'normal_' + (strength || 0.5);
  if (TEX_CACHE[key]) return TEX_CACHE[key];
  const S = 256, c = makeCanvas(S, S), ctx = c.getContext('2d');
  const id = ctx.createImageData(S, S);
  const str = strength != null ? strength : 0.5;
  for (let y = 0; y < S; y++) {
    for (let x = 0; x < S; x++) {
      const i = (y * S + x) * 4;
      const nx = (Math.random() - 0.5) * 2 * str;
      const ny = (Math.random() - 0.5) * 2 * str;
      const nz = 0.5 + Math.sqrt(Math.max(0, 1 - nx * nx - ny * ny)) * 0.5;
      id.data[i] = (nx * 0.5 + 0.5) * 255;
      id.data[i + 1] = (ny * 0.5 + 0.5) * 255;
      id.data[i + 2] = (nz * 0.5 + 0.5) * 255;
      id.data[i + 3] = 255;
    }
  }
  ctx.putImageData(id, 0, 0);
  TEX_CACHE[key] = c;
  return c;
}

/* ---- Texture dispatcher ---- */
function getTextureCanvas(type) {
  switch (type) {
    case 'wood-floor': return texWoodPlanks();
    case 'wood-dark': return texWoodDark();
    case 'wall': return texWall();
    case 'tile': return texTile();
    case 'fabric-dark': return texFabric('#3B2F2F');
    case 'fabric-beige': return texFabric('#C4A882');
    case 'fabric-white': return texFabric('#E8E0D4');
    case 'fabric-red': return texFabric('#8B2020');
    case 'grass': return texGrass();
    case 'pool-tile': return texPoolTile();
    case 'concrete': return texConcrete();
    case 'marble': return texMarble();
    case 'bathroom-tile': return texBathroomTile();
    case 'metal-car': return texMetal('#1a237e');
    case 'metal-fence': return texMetal('#2c2c2c');
    case 'bark': return texWoodDark();
    case 'roof-tile': return texRoofTile();
    default: return texWall();
  }
}

/* ---- PBR properties per type ---- */
const PBR_PROPS = {
  'wood-floor': { roughness: 0.65, metalness: 0.0, normalStrength: 0.3 },
  'wood-dark': { roughness: 0.70, metalness: 0.0, normalStrength: 0.35 },
  'wall': { roughness: 0.92, metalness: 0.0, normalStrength: 0.2 },
  'tile': { roughness: 0.30, metalness: 0.0, normalStrength: 0.4 },
  'fabric-dark': { roughness: 0.95, metalness: 0.0 },
  'fabric-beige': { roughness: 0.95, metalness: 0.0 },
  'fabric-white': { roughness: 0.95, metalness: 0.0 },
  'fabric-red': { roughness: 0.95, metalness: 0.0 },
  'grass': { roughness: 0.90, metalness: 0.0, normalStrength: 0.25 },
  'pool-tile': { roughness: 0.25, metalness: 0.0, normalStrength: 0.3 },
  'concrete': { roughness: 0.85, metalness: 0.0, normalStrength: 0.35 },
  'marble': { roughness: 0.15, metalness: 0.05, normalStrength: 0.15 },
  'bathroom-tile': { roughness: 0.25, metalness: 0.0, normalStrength: 0.35 },
  'metal-car': { roughness: 0.22, metalness: 0.72, normalStrength: 0.2 },
  'metal-fence': { roughness: 0.45, metalness: 0.65, normalStrength: 0.2 },
  'bark': { roughness: 0.88, metalness: 0.0, normalStrength: 0.4 },
  'roof-tile': { roughness: 0.80, metalness: 0.0, normalStrength: 0.35 },
};

/* =====================================================================
   SECTION 2 — PBR Material Component
   ===================================================================== */

AFRAME.registerComponent('pbr-material', {
  schema: {
    type: { type: 'string', default: 'wall' },
    repeatX: { type: 'number', default: 1 },
    repeatY: { type: 'number', default: 1 },
    color: { type: 'string', default: '' }
  },

  init: function () {
    this._applied = false;
    // Poll until the mesh exists then apply once
    this._interval = setInterval(() => {
      if (this._applied) { clearInterval(this._interval); return; }
      const mesh = this.el.getObject3D('mesh');
      if (mesh) { this._applyMaterial(mesh); this._applied = true; clearInterval(this._interval); }
    }, 60);
  },

  _applyMaterial: function (mesh) {
    const canvas = getTextureCanvas(this.data.type);
    const albedo = new THREE.CanvasTexture(canvas);
    albedo.wrapS = albedo.wrapT = THREE.RepeatWrapping;
    albedo.repeat.set(this.data.repeatX, this.data.repeatY);
    albedo.anisotropy = 16;
    albedo.colorSpace = THREE.SRGBColorSpace;

    const props = PBR_PROPS[this.data.type] || { roughness: 0.8, metalness: 0, normalStrength: 0 };
    const cfg = { map: albedo, roughness: props.roughness, metalness: props.metalness, side: THREE.FrontSide };

    if (this.data.color) cfg.color = new THREE.Color(this.data.color);

    if (props.normalStrength && props.normalStrength > 0) {
      const normalCanvas = texNormalMap(props.normalStrength);
      const normalMap = new THREE.CanvasTexture(normalCanvas);
      normalMap.wrapS = normalMap.wrapT = THREE.RepeatWrapping;
      normalMap.repeat.copy(albedo.repeat);
      normalMap.anisotropy = albedo.anisotropy;
      cfg.normalMap = normalMap;
      cfg.normalScale = new THREE.Vector2(1, 1);
    }

    mesh.material = new THREE.MeshStandardMaterial(cfg);
  },

  remove: function () { if (this._interval) clearInterval(this._interval); }
});

/* =====================================================================
   SECTION 3 — Water GLSL Shader
   ===================================================================== */

AFRAME.registerShader('water', {
  schema: {
    color: { type: 'color', is: 'uniform', default: '#0077BE' },
    opacity: { type: 'number', is: 'uniform', default: 0.78 },
    timeMsec: { type: 'time', is: 'uniform' }
  },

  vertexShader: [
    'uniform float timeMsec;',
    'varying vec2 vUv;',
    'varying float vElev;',
    'void main () {',
    '  vUv = uv;',
    '  float t = timeMsec / 1000.0;',
    '  vec3 p = position;',
    '  float w = sin(p.x*2.5+t*1.8)*0.04',
    '         + cos(p.y*3.2+t*1.3)*0.03',
    '         + sin((p.x+p.y)*1.8+t*2.2)*0.025',
    '         + cos(p.x*4.0-t*1.5)*0.015;',
    '  vElev = w;',
    '  p.z += w;',
    '  gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0);',
    '}'
  ].join('\n'),

  fragmentShader: [
    'uniform vec3 color;',
    'uniform float opacity;',
    'uniform float timeMsec;',
    'varying vec2 vUv;',
    'varying float vElev;',
    'void main () {',
    '  float t = timeMsec/1000.0;',
    '  vec3 deep = color*0.55;',
    '  vec3 shallow = color*1.35;',
    '  vec3 wc = mix(deep, shallow, vElev*8.0+0.5);',
    '  float caustic = pow(abs(sin(vUv.x*28.0+t*1.6)*cos(vUv.y*28.0+t*1.3)),4.0)*0.28;',
    '  wc += vec3(caustic*0.7, caustic*0.85, caustic);',
    '  float shimmer = sin(vUv.x*60.0+t*3.0)*sin(vUv.y*60.0+t*2.5)*0.04;',
    '  wc += vec3(shimmer);',
    '  gl_FragColor = vec4(wc, opacity);',
    '}'
  ].join('\n')
});

/* =====================================================================
   SECTION 3b — Jacuzzi Water GLSL Shader (bubbling jets + foam)
   ===================================================================== */

AFRAME.registerShader('jacuzzi-water', {
  schema: {
    color: { type: 'color', is: 'uniform', default: '#4DD0E1' },
    opacity: { type: 'number', is: 'uniform', default: 0.75 },
    timeMsec: { type: 'time', is: 'uniform' }
  },

  vertexShader: [
    'uniform float timeMsec;',
    'varying vec2 vUv;',
    'varying float vElev;',
    'void main () {',
    '  vUv = uv;',
    '  float t = timeMsec / 1000.0;',
    '  vec3 p = position;',
    '  float r = length(p.xy);',
    '  float bubble = sin(p.x*8.0+t*4.5)*0.015',
    '               + cos(p.y*10.0+t*5.2)*0.012',
    '               + sin((p.x+p.y)*6.0+t*6.0)*0.018',
    '               + cos(p.x*12.0-t*3.8)*0.008',
    '               + sin(p.y*14.0+t*7.0)*0.01',
    '               + cos((p.x-p.y)*5.0+t*4.0)*0.014;',
    '  vElev = bubble;',
    '  p.z += bubble;',
    '  gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0);',
    '}'
  ].join('\n'),

  fragmentShader: [
    'uniform vec3 color;',
    'uniform float opacity;',
    'uniform float timeMsec;',
    'varying vec2 vUv;',
    'varying float vElev;',
    'void main () {',
    '  float t = timeMsec/1000.0;',
    '  vec3 deep = color*0.5;',
    '  vec3 shallow = color*1.4;',
    '  vec3 wc = mix(deep, shallow, vElev*12.0+0.5);',
    '  float caustic = pow(abs(sin(vUv.x*40.0+t*2.5)*cos(vUv.y*40.0+t*2.0)),3.0)*0.4;',
    '  wc += vec3(caustic*0.8, caustic*0.9, caustic);',
    '  float foam = pow(abs(sin(vUv.x*25.0+t*3.0)*cos(vUv.y*30.0-t*2.5)),6.0)*0.6;',
    '  wc += vec3(foam);',
    '  float bubble = pow(abs(sin(vUv.x*50.0+t*5.0)*sin(vUv.y*50.0+t*4.0)),8.0)*0.5;',
    '  wc += vec3(bubble*0.9, bubble*0.95, bubble);',
    '  float shimmer = sin(vUv.x*80.0+t*4.0)*sin(vUv.y*80.0+t*3.5)*0.06;',
    '  wc += vec3(shimmer);',
    '  gl_FragColor = vec4(wc, opacity);',
    '}'
  ].join('\n')
});

/* =====================================================================
   SECTION 4 — Sky Gradient Shader
   ===================================================================== */

AFRAME.registerShader('sky-gradient', {
  schema: {
    topColor: { type: 'color', is: 'uniform', default: '#1e88e5' },
    bottomColor: { type: 'color', is: 'uniform', default: '#e3f2fd' },
    exponent: { type: 'number', is: 'uniform', default: 0.4 }
  },

  vertexShader: [
    'varying vec3 vWorldPos;',
    'void main(){',
    '  vec4 wp = modelMatrix * vec4(position,1.0);',
    '  vWorldPos = wp.xyz;',
    '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);',
    '}'
  ].join('\n'),

  fragmentShader: [
    'uniform vec3 topColor;',
    'uniform vec3 bottomColor;',
    'uniform float exponent;',
    'varying vec3 vWorldPos;',
    'void main(){',
    '  float h = normalize(vWorldPos).y;',
    '  float t = pow(max(h,0.0), exponent);',
    '  gl_FragColor = vec4(mix(bottomColor, topColor, t),1.0);',
    '}'
  ].join('\n')
});

/* =====================================================================
   SECTION 5 — Door Animation Component
   ===================================================================== */

AFRAME.registerComponent('door-anim', {
  schema: {
    speed: { type: 'number', default: 2.5 },
    openAngle: { type: 'number', default: 100 }
  },

  init: function () {
    this.isOpen = false;
    this.current = 0;
    this.target = 0;
    this.el.classList.add('clickable');
    this.el.addEventListener('click', () => {
      this.isOpen = !this.isOpen;
      this.target = this.isOpen ? this.data.openAngle : 0;
    });
  },

  tick: function (_t, dt) {
    const diff = this.target - this.current;
    if (Math.abs(diff) < 0.2) return;
    const step = this.data.speed * (dt / 1000) * 60;
    this.current += Math.sign(diff) * Math.min(step, Math.abs(diff));
    this.el.object3D.rotation.y = THREE.MathUtils.degToRad(this.current);
  }
});

/* =====================================================================
   SECTION 6 — Ceiling Fan Component
   ===================================================================== */

AFRAME.registerComponent('ceiling-fan', {
  schema: { speed: { type: 'number', default: 120 } },   // deg/sec
  init: function () { this.angle = 0; },
  tick: function (_t, dt) {
    this.angle = (this.angle + this.data.speed * dt / 1000) % 360;
    this.el.object3D.rotation.y = THREE.MathUtils.degToRad(this.angle);
  }
});

/* =====================================================================
   SECTION 7 — Light Toggle Component (click lamp to toggle light)
   ===================================================================== */

AFRAME.registerComponent('light-toggle', {
  schema: {
    on: { type: 'boolean', default: true }
  },

  init: function () {
    this.isOn = this.data.on;
    this.el.classList.add('clickable');
    this.el.addEventListener('click', () => this.toggle());
  },

  toggle: function () {
    this.isOn = !this.isOn;
    // Toggle every child <a-light>
    const lights = this.el.querySelectorAll('[light]');
    lights.forEach(l => l.setAttribute('light', 'intensity', this.isOn ? 0.8 : 0));
    // Toggle emissive on .bulb children
    const bulbs = this.el.querySelectorAll('.bulb');
    bulbs.forEach(b => {
      b.setAttribute('material', 'emissiveIntensity', this.isOn ? 0.6 : 0);
      b.setAttribute('material', 'emissive', this.isOn ? '#FFE4B0' : '#000');
    });
  }
});

/* =====================================================================
   SECTION 8 — Fountain Flow Shader (animated flowing water beside pool)
   ===================================================================== */

AFRAME.registerShader('fountain-flow', {
  schema: {
    color: { type: 'color', is: 'uniform', default: '#87CEEB' },
    opacity: { type: 'number', is: 'uniform', default: 0.82 },
    timeMsec: { type: 'time', is: 'uniform' }
  },

  vertexShader: [
    'uniform float timeMsec;',
    'varying vec2 vUv;',
    'varying float vFall;',
    'void main () {',
    '  vUv = uv;',
    '  float t = timeMsec / 1000.0;',
    '  vFall = uv.y + t * 3.0;',
    '  vec3 p = position;',
    '  float wobble = sin(p.x * 6.0 + t * 5.0) * 0.015 + cos(p.z * 6.0 + t * 4.0) * 0.015;',
    '  p.x += wobble; p.z += wobble;',
    '  gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);',
    '}'
  ].join('\n'),

  fragmentShader: [
    'uniform vec3 color;',
    'uniform float opacity;',
    'varying vec2 vUv;',
    'varying float vFall;',
    'void main () {',
    '  float stripe = sin(vFall * 20.0) * 0.5 + 0.5;',
    '  float edge = smoothstep(0.0, 0.12, vUv.x) * smoothstep(1.0, 0.88, vUv.x);',
    '  float a = opacity * (0.6 + stripe * 0.4) * edge;',
    '  vec3 c = color * (0.9 + stripe * 0.15);',
    '  gl_FragColor = vec4(c, a);',
    '}'
  ].join('\n')
});

/* ----- Component: fix transparent shader materials (pool + fountain) ----- */
AFRAME.registerComponent('transparent-water-fix', {
  schema: { renderOrder: { type: 'int', default: 0 } },
  init: function () { this._fixed = false; },
  tick: function () {
    if (this._fixed) return;
    var mesh = this.el.getObject3D('mesh');
    if (mesh && mesh.material) {
      mesh.material.transparent = true;
      mesh.material.depthWrite = false;
      mesh.material.side = THREE.DoubleSide;
      mesh.material.needsUpdate = true;
      if (this.data.renderOrder !== 0) mesh.renderOrder = this.data.renderOrder;
      this._fixed = true;
    }
  }
});

/* ----- Stylized tree: random Y rotation and scale variation (no cloned look) ----- */
AFRAME.registerComponent('tree-variation', {
  schema: {
    scaleMin: { type: 'number', default: 0.88 },
    scaleMax: { type: 'number', default: 1.12 }
  },
  init: function () {
    const s = this.data;
    const rotY = Math.random() * 360;
    const scaleMult = s.scaleMin + Math.random() * (s.scaleMax - s.scaleMin);
    const base = this.el.getAttribute('scale') || { x: 1, y: 1, z: 1 };
    this.el.setAttribute('rotation', { x: 0, y: rotY, z: 0 });
    this.el.setAttribute('scale', {
      x: base.x * scaleMult,
      y: base.y * scaleMult,
      z: base.z * scaleMult
    });
  }
});

/* ----- Stylized tree: shadows + alpha for leaves (transparent/alphaTest), preserve materials ----- */
AFRAME.registerComponent('tree-material-fix', {
  init: function () {
    this.el.addEventListener('model-loaded', () => {
      this.el.object3D.traverse(node => {
        if (!node.isMesh) return;
        node.castShadow = true;
        node.receiveShadow = true;
        const mats = Array.isArray(node.material) ? node.material : [node.material];
        mats.forEach(m => {
          if (!m) return;
          const needsAlpha = m.transparent || (m.map && m.map.format === 1023) || (m.alphaTest !== undefined && m.alphaTest > 0);
          if (needsAlpha) {
            m.transparent = true;
            m.alphaTest = typeof m.alphaTest === 'number' ? m.alphaTest : 0.5;
            m.depthWrite = true;
            if (m.side !== THREE.DoubleSide) m.side = THREE.DoubleSide;
            m.needsUpdate = true;
          }
        });
      });
    });
  }
});

/* ----- Component: subtle wind sway for tree/palm foliage + polygonOffset to avoid z-fighting ----- */
AFRAME.registerComponent('tree-wind', {
  schema: {
    strength: { type: 'number', default: 1.2 },
    speed: { type: 'number', default: 0.6 }
  },
  init: function () {
    this._foliage = [];
  },
  tick: function (t, dt) {
    const foliage = this.el.querySelectorAll('.tree-foliage');
    if (this._foliage.length !== foliage.length) {
      this._foliage = Array.from(foliage).map(el => {
        const mesh = el.getObject3D('mesh');
        if (mesh && mesh.material) {
          mesh.material.polygonOffset = true;
          mesh.material.polygonOffsetFactor = 1;
          mesh.material.polygonOffsetUnits = 1;
        }
        return {
          el: el,
          baseRot: el.getAttribute('rotation') ? { ...el.getAttribute('rotation') } : { x: 0, y: 0, z: 0 }
        };
      });
    }
    const timeSec = t / 1000;
    const s = Math.sin(timeSec * this.data.speed) * this.data.strength;
    const s2 = Math.sin(timeSec * this.data.speed * 0.7 + 1) * this.data.strength * 0.6;
    this._foliage.forEach((f) => {
      const mesh = f.el.getObject3D('mesh');
      if (mesh && mesh.material && !mesh.material.polygonOffset) {
        mesh.material.polygonOffset = true;
        mesh.material.polygonOffsetFactor = 1;
        mesh.material.polygonOffsetUnits = 1;
      }
      const r = f.baseRot;
      f.el.setAttribute('rotation', {
        x: r.x + s * 0.5,
        y: r.y + s2 * 0.3,
        z: r.z + s * 0.4
      });
    });
  }
});

/* =====================================================================
   SECTION 9 — Pet Roam (smooth path movement, collision, grounding, animation sync)
   ===================================================================== */

(function () {
  const GROUND_Y = 0;
  const TURN_SPEED_DEG = 220;
  const ACCEL_RATE = 3.5;
  const ANGLE_THRESHOLD_DEG = 38;
  const DEFAULT_STRIDE_M = 0.45;
  /* Villa footprint x∈[-6,6] z∈[-5,5]; pool at (10,0); car in front of villa at (0, 7.5) */
  const OBSTACLES = [
    { minX: -6.5, maxX: 6.5, minZ: -5.5, maxZ: 5.5 },
    { minX: 7, maxX: 13, minZ: -2.5, maxZ: 2.5 },
    { minX: -2.2, maxX: 2.2, minZ: 6.4, maxZ: 8.6 }
  ];
  const BOUNDS = { minX: -7.5, maxX: 17.5, minZ: -7.5, maxZ: 13.5 };

  function pointInObstacle(x, z) {
    for (let i = 0; i < OBSTACLES.length; i++) {
      const o = OBSTACLES[i];
      if (x >= o.minX && x <= o.maxX && z >= o.minZ && z <= o.maxZ) return true;
    }
    return false;
  }

  function clampToBounds(p) {
    p.x = Math.max(BOUNDS.minX, Math.min(BOUNDS.maxX, p.x));
    p.z = Math.max(BOUNDS.minZ, Math.min(BOUNDS.maxZ, p.z));
  }

  AFRAME.registerComponent('pet-roam', {
    schema: {
      speed: { type: 'number', default: 0.7 },
      path: { type: 'array', default: [] },
      proximity: { type: 'number', default: 5 },
      turnSpeed: { type: 'number', default: TURN_SPEED_DEG },
      idleTimeScale: { type: 'number', default: 0.2 },
      moveTimeScale: { type: 'number', default: 1 },
      stride: { type: 'number', default: DEFAULT_STRIDE_M },
      accelRate: { type: 'number', default: ACCEL_RATE }
    },

    init: function () {
      this.waypointIndex = 0;
      this.path = this.data.path && this.data.path.length > 0
        ? this.data.path
        : [
          { x: 2, z: 7 }, { x: 3.5, z: 7.5 }, { x: 4, z: 7 }, { x: 3, z: 6.5 },
          { x: 1.5, z: 6.8 }, { x: 0, z: 7.2 }, { x: -1, z: 7 }, { x: 0.5, z: 7.5 }, { x: 2, z: 7 }
        ];
      this.currentRotationY = 0;
      this.currentSpeed = 0;
      this.pos = this.el.getAttribute('position');
      const start = this.path[0];
      this.el.setAttribute('position', { x: start.x, y: this.pos.y, z: start.z });
      this.currentRotationY = Math.atan2((this.path[1]?.x ?? start.x) - start.x, (this.path[1]?.z ?? start.z) - start.z) * (180 / Math.PI);
      this.moving = false;
    },

    tick: function (_t, dt) {
      const path = this.path;
      if (path.length < 2) return;
      const pos = this.el.getAttribute('position');
      if (this._groundOffset === undefined) this._groundOffset = pos.y - GROUND_Y;
      const dtSec = Math.min(dt / 1000, 0.1);
      const idx = this.waypointIndex % path.length;
      const target = path[(idx + 1) % path.length];
      let dx = target.x - pos.x;
      let dz = target.z - pos.z;
      const dist = Math.sqrt(dx * dx + dz * dz);
      const turnSpeed = this.data.turnSpeed * dtSec;

      let headY = Math.atan2(dx, dz) * (180 / Math.PI);
      const cam = document.getElementById('camera');
      if (cam && this.data.proximity > 0) {
        const petWorld = this.el.object3D.getWorldPosition(new THREE.Vector3());
        const camWorld = cam.object3D.getWorldPosition(new THREE.Vector3());
        const d = Math.hypot(camWorld.x - petWorld.x, camWorld.z - petWorld.z);
        if (d < this.data.proximity) headY = Math.atan2(camWorld.x - petWorld.x, camWorld.z - petWorld.z) * (180 / Math.PI);
      }

      let diff = headY - this.currentRotationY;
      while (diff > 180) diff -= 360;
      while (diff < -180) diff += 360;
      this.currentRotationY += Math.sign(diff) * Math.min(Math.abs(diff), turnSpeed);
      this.el.setAttribute('rotation', { x: 0, y: this.currentRotationY, z: 0 });

      const mixerComp = this.el.components['animation-mixer'];
      const hasRootMotion = !!(mixerComp && mixerComp.rootMotionNode);
      const clipDuration = (mixerComp && mixerComp.clipDuration) || 1;
      const angleOk = Math.abs(diff) < ANGLE_THRESHOLD_DEG;

      if (hasRootMotion) {
        if (dist <= 0.6) {
          this.waypointIndex = (this.waypointIndex + 1) % path.length;
          this.moving = false;
          this._setAnimationTimeScale(this.data.idleTimeScale);
        } else {
          this.moving = angleOk;
          this._setAnimationTimeScale(this.moving ? this.data.moveTimeScale : this.data.idleTimeScale);
        }
        const nextPos = { x: pos.x, y: pos.y, z: pos.z };
        clampToBounds(nextPos);
        if (pointInObstacle(nextPos.x, nextPos.z)) {
          this.waypointIndex = (this.waypointIndex + 1) % path.length;
        }
        nextPos.y = GROUND_Y + (typeof this._groundOffset === 'number' ? this._groundOffset : 0);
        this.el.setAttribute('position', nextPos);
        return;
      }

      const stride = this.data.stride;
      const targetSpeedRaw = clipDuration > 0 ? stride / clipDuration : this.data.speed;
      const stopDist = 1.2;
      const targetSpeed = dist <= stopDist ? 0 : (dist < stopDist + 0.8 ? targetSpeedRaw * (dist - stopDist) / 0.8 : targetSpeedRaw);
      const wantMove = angleOk && dist > stopDist && !pointInObstacle(
        pos.x + (dx / dist) * stride * 0.5,
        pos.z + (dz / dist) * stride * 0.5
      );
      const accel = Math.min(1, this.data.accelRate * dtSec);
      const target = wantMove ? targetSpeed : 0;
      this.currentSpeed += (target - this.currentSpeed) * accel;
      this.currentSpeed = Math.max(0, Math.min(targetSpeedRaw * 1.05, this.currentSpeed));

      if (dist <= this.currentSpeed * dtSec * 2 || dist <= stopDist) {
        this.waypointIndex = (this.waypointIndex + 1) % path.length;
        this.moving = false;
        this._setAnimationTimeScale(this.data.idleTimeScale);
        return;
      }

      const moveDist = this.currentSpeed * dtSec;
      let nx = pos.x + (dx / dist) * moveDist;
      let nz = pos.z + (dz / dist) * moveDist;
      const nextPos = { x: nx, y: pos.y, z: nz };
      clampToBounds(nextPos);
      if (pointInObstacle(nextPos.x, nextPos.z)) {
        this.waypointIndex = (this.waypointIndex + 1) % path.length;
        this.moving = false;
        this._setAnimationTimeScale(this.data.idleTimeScale);
        return;
      }
      nextPos.y = GROUND_Y + (typeof this._groundOffset === 'number' ? this._groundOffset : 0);
      this.el.setAttribute('position', nextPos);
      this.moving = this.currentSpeed > 0.01;
      this._setAnimationTimeScale(this.moving ? 1 : this.data.idleTimeScale);
    },

    _setAnimationTimeScale: function (scale) {
      const mixer = this.el.components['animation-mixer'];
      if (mixer && mixer.mixer && mixer.activeAction) mixer.activeAction.timeScale = scale;
    }
  });
})();

/* =====================================================================
   SECTION 10 — Vehicle Animation (wheel rotation, headlight blink)
   ===================================================================== */

AFRAME.registerComponent('gltf-shadow', {
  init: function () {
    this.el.addEventListener('model-loaded', () => {
      this.el.object3D.traverse(node => {
        if (node.isMesh) { node.castShadow = true; node.receiveShadow = true; }
      });
    });
  }
});

/* ----- Car reflection: apply env map to metallic materials (preserves original materials) ----- */
AFRAME.registerComponent('car-reflection', {
  init: function () {
    this.el.addEventListener('model-loaded', () => {
      try {
        const sceneEl = this.el.sceneEl;
        const renderer = sceneEl && sceneEl.renderer;
        if (!renderer) return;
        let envMap = sceneEl.object3D.__carEnvMap;
        if (!envMap) {
          const pmrem = new THREE.PMREMGenerator(renderer);
          const simpleScene = new THREE.Scene();
          simpleScene.background = new THREE.Color(0xb0c4de);
          envMap = pmrem.fromScene(simpleScene).texture;
          pmrem.dispose();
          sceneEl.object3D.__carEnvMap = envMap;
        }
        this.el.object3D.traverse(node => {
          if (node.isMesh && node.material) {
            const m = node.material;
            if (m && m.metalness !== undefined && m.metalness > 0) {
              m.envMap = envMap;
              m.envMapIntensity = 0.45;
              m.needsUpdate = true;
            }
          }
        });
      } catch (e) {
        console.warn('car-reflection:', e);
      }
    });
  }
});

AFRAME.registerComponent('animation-mixer', {
  schema: {
    clip: { type: 'string', default: '*' },
    loop: { type: 'string', default: 'repeat' },
    crossFadeDuration: { type: 'number', default: 0.3 },
    timeScale: { type: 'number', default: 1 }
  },
  init: function () {
    this.mixer = null;
    this.activeAction = null;
    this.clipDuration = 0;
    this.rootMotionNode = null;
    this._prevRootWorld = new THREE.Vector3();
    this._rootDelta = new THREE.Vector3();
    this._quat = new THREE.Quaternion();
    this._scale = new THREE.Vector3();
    this.el.addEventListener('model-loaded', e => {
      const model = e.detail.model;
      const clips = model.animations || [];
      if (clips.length === 0) return;
      let clip = this.data.clip === '*' ? clips[0] : (THREE.AnimationClip.findByName(clips, this.data.clip) || clips[0]);
      if (!clip) return;
      this.mixer = new THREE.AnimationMixer(model);
      this.clipDuration = clip.duration;
      this.rootMotionNode = null;
      for (let i = 0; i < clip.tracks.length; i++) {
        const t = clip.tracks[i];
        const name = t.name || '';
        if (name.endsWith('.position') || name.endsWith('/position')) {
          const nodeName = name.replace(/\.position$/i, '').replace(/\/position$/i, '');
          const obj = model.getObjectByName(nodeName) || model.getObjectByProperty('name', nodeName);
          if (obj) {
            this.rootMotionNode = obj;
            break;
          }
        }
      }
      if (!this.rootMotionNode && clip.tracks.length > 0) {
        const first = clip.tracks[0];
        const n = first.name && first.name.split('.')[0];
        if (n) {
          const obj = model.getObjectByName(n) || model.getObjectByProperty('name', n);
          if (obj && /position|translation/i.test(first.name)) this.rootMotionNode = obj;
        }
      }
      const loopMode = this.data.loop === 'once' ? THREE.LoopOnce :
                        this.data.loop === 'pingpong' ? THREE.LoopPingPong : THREE.LoopRepeat;
      this.activeAction = this.mixer.clipAction(clip);
      this.activeAction.setLoop(loopMode);
      this.activeAction.timeScale = this.data.timeScale;
      this.activeAction.play();
    });
  },
  tick: function (_t, dt) {
    if (!this.mixer) return;
    const dtSec = dt / 1000;
    const root = this.rootMotionNode;
    const entity = this.el;
    if (root) {
      root.getWorldPosition(this._prevRootWorld);
    }
    this.mixer.update(dtSec);
    if (root) {
      root.getWorldPosition(this._rootDelta);
      this._rootDelta.sub(this._prevRootWorld);
      const pos = entity.getAttribute('position');
      entity.setAttribute('position', {
        x: pos.x + this._rootDelta.x,
        y: pos.y + this._rootDelta.y,
        z: pos.z + this._rootDelta.z
      });
      root.position.set(0, 0, 0);
    }
  },
  remove: function () {
    if (this.mixer) this.mixer.stopAllAction();
  }
});

AFRAME.registerComponent('ground-align', {
  schema: {
    offset: { type: 'number', default: 0 },
    skipSizeFilter: { type: 'boolean', default: false }
  },
  init: function () {
    this.el.addEventListener('model-loaded', () => {
      requestAnimationFrame(() => {
        this.el.object3D.updateMatrixWorld(true);
        let lowestY = Infinity;
        const v = new THREE.Vector3();
        const skipFilter = this.data.skipSizeFilter;
        this.el.object3D.traverse(node => {
          if (!node.isMesh || !node.geometry) return;
          node.geometry.computeBoundingBox();
          const bb = node.geometry.boundingBox;
          const sx = bb.max.x - bb.min.x, sy = bb.max.y - bb.min.y, sz = bb.max.z - bb.min.z;
          if (!skipFilter && (sx > 15 || sy > 15 || sz > 15)) return;
          const posAttr = node.geometry.getAttribute('position');
          if (!posAttr) return;
          for (let i = 0; i < posAttr.count; i++) {
            v.fromBufferAttribute(posAttr, i);
            node.localToWorld(v);
            if (v.y < lowestY) lowestY = v.y;
          }
        });
        if (lowestY !== Infinity) {
          const pos = this.el.getAttribute('position');
          pos.y += -lowestY + this.data.offset;
          this.el.setAttribute('position', pos);
        }
      });
    });
  }
});

AFRAME.registerComponent('vehicle-anim', {
  schema: {
    wheelSpeed: { type: 'number', default: 25 },
    blinkSpeed: { type: 'number', default: 1.5 },
    blinkIntensity: { type: 'number', default: 0.35 }
  },

  init: function () {
    this.wheelEls = this.el.querySelectorAll('.vehicle-wheel');
    this.lightEls = this.el.querySelectorAll('.vehicle-headlight');
    this.phase = 0;
  },

  tick: function (_t, dt) {
    const dtSec = dt / 1000;
    this.phase += this.data.blinkSpeed * dtSec * Math.PI * 2;
    const blink = 0.15 + (Math.sin(this.phase) * 0.5 + 0.5) * this.data.blinkIntensity;
    this.lightEls.forEach(l => l.setAttribute('material', 'emissiveIntensity', blink));
    const angleDeg = (this.phase * 0.5 * this.data.wheelSpeed) % 360;
    this.wheelEls.forEach((w) => {
      const rot = w.getAttribute('rotation') || { x: 0, y: 0, z: 90 };
      w.setAttribute('rotation', { x: angleDeg, y: rot.y, z: 90 });
    });
  }
});
