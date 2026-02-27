# VR Dream Villa — Professional A-Frame Experience

High-fidelity, realistic VR villa built with A-Frame and WebXR (reference: modern luxury villa with elongated pool, palm trees, and landscape lighting). **Loading speed is optimized for submission**: no heavy external 3D assets by default; procedural textures and low-poly geometry ensure fast load. **3D models (e.g. GLB/GLTF) are supported** if you add them for higher fidelity while keeping load time in check.

## Features

### Perimeter & Security
- **Gated perimeter fence**: Realistic wrought-iron-style fence around the property (villa, pool, driveway). Double gate at the front entrance (pathway); metal posts and three horizontal rails per span with PBR metal material.

### Villa & Interior
- **Living room**: Sofa, coffee table, TV unit, rug, wall art, floor lamp (click to toggle light)
- **Bedroom**: Bed, wardrobe, bedside lamps (toggle), **ceiling fan** (continuous rotation), window
- **Kitchen**: Cabinets, counter, sink, fridge, stove, table
- **Doors & windows**: Animated entrance door (click to open/close); glass windows

### Pool & Fountain (Mandatory)
- **Swimming pool**: Textured pool tiles; **animated water** (custom GLSL vertex displacement + caustics/shimmer)
- **Water fountain** beside the pool: Animated flowing water via custom `fountain-flow` shader (continuous motion)

### Environment & Motion
- **Trees, grass, plants**: Low-poly with PBR bark and foliage
- **Car**: 2019 Lamborghini Aventador SVJ 3D model in front of the villa entrance (`2019_lamborghini_aventador_svj/`); full import with materials and textures, ground-aligned, shadows and reflections.
- **Pet dog**: **Path-based roaming** in front of villa; **turns to look at player** when within proximity (`pet-roam`)

### Graphics & Lighting
- **PBR materials**: Procedural albedo + optional normal maps; roughness/metalness per surface type; anisotropy
- **Lighting**: Low ambient; directional sun with soft shadows; point lights for lamps (real emission)
- **Shadows**: PCF soft shadows where needed; cast/receive only on key objects

### Controls
- **Desktop**: WASD move, mouse look, click door/lamps, Esc toggles HUD
- **VR**: Smooth locomotion (WASD or controllers), camera height 1.65 m; VR button bottom-right

---

## How to Run Locally

1. **Files**: Ensure `index.html` and `components.js` are in the same folder.

2. **Start a local HTTP server** (required for correct loading):

   **Python 3:**
   ```bash
   python -m http.server 8080
   ```

   **Node (npx):**
   ```bash
   npx http-server -p 8080
   ```

3. **Open in browser:**  
   `http://localhost:8080`  
   Use Chrome or Edge for best WebXR/performance.

4. **Optional**: Open `index.html` directly in a browser; some features may be limited without a server.

---

## Optimization Techniques & Graphics Decisions

### Loading speed (critical for submission)
- **No blocking external 3D models** in the default build: scene uses only A-Frame primitives and procedural textures so it loads quickly.
- **Loading screen**: A dedicated loader is shown until the scene fires `loaded`; it is hidden immediately for a fast perceived load.
- **3D models are supported**: You can add GLB/GLTF for furniture or props; keep file size and count low to preserve load time.

### Performance (60+ FPS)
- **Low-poly geometry**: A-Frame primitives (box, cylinder, cone, plane) only in the default scene.
- **Texture reuse**: Single procedural texture per material type (wood, wall, tile, etc.) shared across entities; `TEX_CACHE` avoids regenerating.
- **Shadows**: `cast: true` / `receive: true` only on main structures and key objects; no shadows on small decor to reduce draw cost.
- **Draw calls**: Shared materials and single texture atlases (via repeat) reduce state changes.
- **No physics**: No rigid-body or collision; movement is script-based (pet path, door/fan/vehicle animation).

### Graphics
- **PBR**: `MeshStandardMaterial` with albedo map + optional procedural normal map; roughness/metalness per surface (e.g. metal-car for car body, low roughness for tiles).
- **No flat colors**: Walls, floors, furniture, pool, car body use `pbr-material` or explicit roughness/metalness; trees use bark texture and tinted foliage.
- **Texture filtering**: Anisotropy set to 16 on albedo (and normal where used) to reduce blur on angled surfaces.
- **Water**: Pool uses custom `water` shader (vertex displacement + fragment caustics/shimmer); fountain uses `fountain-flow` shader (scrolling stripe + transparency) for continuous motion without particles.
- **Sky**: Custom `sky-gradient` shader for horizon-to-zenith gradient that works with directional sun.

### Code Structure
- **Custom components**: `pbr-material`, `door-anim`, `ceiling-fan`, `light-toggle`, `pet-roam`, `vehicle-anim`; shaders: `water`, `fountain-flow`, `sky-gradient`.
- **Modular JS**: One `components.js` with sections (textures, PBR, shaders, behaviors); well-commented and easy to extend (e.g. new texture types or path waypoints for the pet).

---

## Custom Components (Reference)

| Component       | Purpose |
|----------------|--------|
| `pbr-material` | Applies procedural albedo (+ optional normal), roughness/metalness, anisotropy |
| `door-anim`    | Click-to-open/close door with hinge rotation |
| `ceiling-fan`  | Continuous Y-axis rotation for fan blades |
| `light-toggle` | Click lamp to toggle point light and bulb emissive |
| `pet-roam`     | Path-based movement; dog turns to face camera when within `proximity` |
| `vehicle-anim` | Idle wheel rotation + headlight blink (sine) for car |
| `gltf-shadow`  | Enables cast/receive shadows on all meshes of a loaded GLTF model |
| `fountain-flow`| Shader only; used on fountain water cylinders for flowing effect |

---

## Browser Support

- **Chrome / Edge**: Full WebXR and best performance (recommended).
- **Firefox**: WebXR supported; enable if required.
- **Safari**: Limited WebXR.

Enjoy the villa.
