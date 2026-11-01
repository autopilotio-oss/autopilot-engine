# Executed by build.py (step=build) inside headless Blender. Builds the AUTOPILOT.OI hooded operative.
import bpy, os, sys, glob, pathlib, math
import numpy as np
mods = install_mpfb(); pkg = mpfb_pkg(); root = str(install_packs(pkg))
HS = __import__(pkg + '.services.humanservice', fromlist=['HumanService']).HumanService
AS_ = __import__(pkg + '.services.assetservice', fromlist=['AssetService']).AssetService
try: AS_.update_all_asset_lists()
except Exception as e: say('asset list update', repr(e))
def find(kind, name, ext):
    hits = glob.glob(os.path.join(root, kind, '**', name, '*' + ext), recursive=True) or glob.glob(os.path.join(root, kind, name, '*' + ext))
    if not hits: hits = glob.glob(os.path.join(root, kind, '**', name + ext), recursive=True)
    say('find', kind, name, ext, '->', hits[:1]); return hits[0] if hits else None
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)

# 1. body: young adult male, athletic
macro = {'gender': 1.0, 'age': 0.5, 'muscle': 0.62, 'weight': 0.48, 'height': 0.56, 'proportions': 0.6, 'cupsize': 0.5, 'firmness': 0.5,
         'race': {'african': 0.6, 'asian': 0.1, 'caucasian': 0.3}}
body = HS.create_human(mask_helpers=True, detailed_helpers=False, extra_vertex_groups=True, feet_on_ground=True, scale=0.1, macro_detail_dict=macro)
say('body', body.name, len(body.data.vertices))
skin = find('skins', 'young_african_male', '.mhmat')
try: HS.set_character_skin(skin, body, skin_type='MAKESKIN'); say('skin ok')
except Exception as e: say('skin fail', repr(e))

# 2. skeleton (Mixamo naming, fingers included) so Mixamo animations can retarget later
rig = HS.add_builtin_rig(body, 'mixamo', import_weights=True); say('rig', rig.name if rig else None, len(rig.data.bones) if rig else 0)

# 3. eyes, eyebrows, eyelashes, clothes
def add(kind, name, asset_type, subdiv=0):
    f = find(kind, name, '.mhclo')
    if not f: return None
    try:
        o = HS.add_mhclo_asset(f, body, asset_type=asset_type, subdiv_levels=subdiv, material_type='MAKESKIN'); say('added', name, o.name, len(o.data.vertices)); return o
    except Exception as e:
        say('add fail', name, repr(e)); return None
eyes = add('eyes', 'high-poly', 'Eyes')
add('eyebrows', 'eyebrow001', 'Eyebrows'); add('eyelashes', 'eyelashes01', 'Eyelashes') or add('eyelashes', 'eyelashes02', 'Eyelashes')
top = add('clothes', 'toigo_fisherman_sweater', 'Clothes')
pants = add('clothes', 'cortu_cargo_pants', 'Clothes')
shoes = add('clothes', 'shoes06', 'Clothes')
mask = None
hood = add('clothes', 'culturalibre_hero-heroine_hood_1', 'Clothes')

# 4. materials: heather black fleece (hoodie and hood), black knit (balaclava), dark pants, black sneakers with white soles
def fleece_image(name, base=0.055, amp=0.035, size=512, seed=1):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (size, size)).astype(np.float32)
    k = np.ones(3, np.float32) / 3
    for _ in range(2):
        n = np.apply_along_axis(lambda r: np.convolve(r, k, 'same'), 1, n); n = np.apply_along_axis(lambda r: np.convolve(r, k, 'same'), 0, n)
    fine = rng.normal(0, 1, (size, size)).astype(np.float32) * 0.35
    v = np.clip(base + (n * 0.7 + fine) * amp, 0, 1)
    px = np.ones((size, size, 4), np.float32); px[..., 0] = v; px[..., 1] = v; px[..., 2] = v * 1.04
    im = bpy.data.images.new(name, size, size, alpha=False); im.pixels[:] = px.ravel(); im.file_format = 'JPEG'; return im
def knit_image(name, size=512):
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    rib = 0.5 + 0.5 * np.sin(x / size * 2 * np.pi * 64) * np.sin(y / size * 2 * np.pi * 96 + np.sin(x / size * 2 * np.pi * 64) * 1.2)
    rng = np.random.default_rng(3); v = 0.025 + rib * 0.03 + rng.normal(0, 0.006, (size, size))
    px = np.ones((size, size, 4), np.float32); px[..., :3] = np.clip(v, 0, 1)[..., None]
    im = bpy.data.images.new(name, size, size, alpha=False); im.pixels[:] = px.ravel(); im.file_format = 'JPEG'; return im
def set_fabric(obj, image, rough=0.95, drop_normal=True):
    if not obj: return
    for slot in obj.material_slots:
        m = slot.material
        if not m: continue
        m.use_nodes = True; nt = m.node_tree
        bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf: continue
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = image
        for l in list(bsdf.inputs['Base Color'].links): nt.links.remove(l)
        nt.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
        for l in list(bsdf.inputs['Roughness'].links): nt.links.remove(l)
        bsdf.inputs['Roughness'].default_value = rough
        if drop_normal:
            for l in list(bsdf.inputs['Normal'].links): nt.links.remove(l)
        say('fabric', obj.name, m.name)
def darken_srgb(obj, target, contrast=0.8, keep_light_above=None):
    if not obj: return
    for slot in obj.material_slots:
        m = slot.material
        if not m or not m.use_nodes: continue
        for n in m.node_tree.nodes:
            if n.type != 'TEX_IMAGE' or not n.image or n.image.colorspace_settings.name != 'sRGB': continue
            im = n.image; w, h = im.size
            if not w: continue
            px = np.array(im.pixels[:], dtype=np.float32).reshape(h, w, 4)
            lum = px[..., 0] * 0.3 + px[..., 1] * 0.59 + px[..., 2] * 0.11
            l2 = (lum - lum.mean()) * contrast + 0.5; out = px.copy()
            for c in range(3): out[..., c] = np.clip(target[c] * (0.55 + l2), 0, 1)
            if keep_light_above is not None:
                keep = lum > keep_light_above; out[keep, :3] = np.clip(px[keep, :3] * 0.95, 0, 1)
            new = bpy.data.images.new(obj.name + '_rc', w, h, alpha=True); new.pixels[:] = out.ravel(); new.file_format = 'JPEG'; n.image = new
            say('darkened', obj.name, im.name)
fleece = fleece_image('fleece_heather')
set_fabric(top, fleece); set_fabric(hood, fleece)
darken_srgb(pants, (0.06, 0.062, 0.07), 0.9)
darken_srgb(shoes, (0.035, 0.035, 0.04), 0.8, keep_light_above=0.62)

import bmesh, mathutils
def offset_along_normals(obj, fn):
    me = obj.data; me.calc_normals_split() if hasattr(me, 'calc_normals_split') else None
    for v in me.vertices:
        v.co += v.normal * fn(v.co)
def smooth(obj, iters, factor=0.5):
    bm = bmesh.new(); bm.from_mesh(obj.data)
    for _ in range(iters): bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=factor, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm.to_mesh(obj.data); bm.free()
# eye reference points from the eyes mesh
ev = [eyes.matrix_world @ v.co for v in eyes.data.vertices] if eyes else []
eye_z = sum(v.z for v in ev) / len(ev) if ev else 1.62
eye_y = min(v.y for v in ev) if ev else -0.09
say('eye ref', round(eye_z, 3), round(eye_y, 3))

# 4b. balaclava: a knit shell grown from the head and neck skin, eye slit open
def from_body(name, keep):
    o = body.copy(); o.data = body.data.copy(); o.name = name; bpy.context.scene.collection.objects.link(o)
    for m in list(o.modifiers):
        if m.type != 'ARMATURE': o.modifiers.remove(m)
    bm = bmesh.new(); bm.from_mesh(o.data); dl = bm.verts.layers.deform.active
    gi = {g.name: g.index for g in o.vertex_groups}
    def w(v, g): return v[dl].get(gi[g], 0.0) if dl and g in gi else 0.0
    kill = [v for v in bm.verts if not keep(v, w, o.matrix_world @ v.co)]
    bmesh.ops.delete(bm, geom=kill, context='VERTS'); bm.to_mesh(o.data); bm.free()
    o.data.materials.clear(); return o
neck_z = eye_z - 0.17
def keep_bala(v, w, co):
    head = w(v, 'mixamorig:Head') + w(v, 'mixamorig:Neck')
    if head < 0.35 and co.z < neck_z: return False
    if co.z < neck_z - 0.04: return False
    if abs(co.z - eye_z) < 0.017 and co.y < eye_y + 0.035 and abs(co.x) < 0.07: return False   # eye slit
    return True
bala = from_body('Human.balaclava', keep_bala)
offset_along_normals(bala, lambda co: 0.0035)
sol = bala.modifiers.new('thick', 'SOLIDIFY'); sol.thickness = 0.002; sol.offset = 1
knit = knit_image('knit_black'); mat = bpy.data.materials.new('balaclava_knit'); mat.use_nodes = True
b = mat.node_tree.nodes['Principled BSDF']; t = mat.node_tree.nodes.new('ShaderNodeTexImage'); t.image = knit
mat.node_tree.links.new(t.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.97
bala.data.materials.append(mat); say('balaclava verts', len(bala.data.vertices))

# 4c. hood: inflate the CC0 cowl into a loose hoodie hood
if hood:
    hz = eye_z
    offset_along_normals(hood, lambda co: 0.016 + max(0.0, co.z - (hz - 0.02)) * 0.16 + max(0.0, co.y - (eye_y + 0.06)) * 0.05)
    smooth(hood, 12, 0.5)
    hs = hood.modifiers.new('thick', 'SOLIDIFY'); hs.thickness = 0.005; hs.offset = 1
    say('hood inflated')
# 4d. looser fleece body
if top:
    offset_along_normals(top, lambda co: 0.006); smooth(top, 2, 0.4)

# 5. bake shape keys (MPFB keeps body shape as shape keys) so the export is a plain skinned mesh
def bake(o):
    if o.type == 'MESH' and o.data.shape_keys:
        bpy.context.view_layer.objects.active = o
        for x in bpy.context.selected_objects: x.select_set(False)
        o.select_set(True)
        try: bpy.ops.object.shape_key_remove(all=True, apply_mix=True); say('baked keys', o.name)
        except Exception as e: say('bake fail', o.name, repr(e))
for o in list(bpy.data.objects): bake(o)

# 6. downscale textures for the web
for im in bpy.data.images:
    if im.size[0] > 1024:
        try: im.scale(1024, int(1024 * im.size[1] / im.size[0]))
        except Exception as e: say('scale fail', im.name, repr(e))

# 7. test renders (Cycles CPU), front and three quarter, close and full
scene = bpy.context.scene; scene.render.engine = 'CYCLES'; scene.cycles.samples = 48; scene.cycles.device = 'CPU'
scene.render.resolution_x, scene.render.resolution_y = 720, 900; scene.render.film_transparent = False
world = bpy.data.worlds.new('w'); scene.world = world; world.use_nodes = True; world.node_tree.nodes['Background'].inputs[0].default_value = (0.02, 0.02, 0.022, 1); world.node_tree.nodes['Background'].inputs[1].default_value = 0.6
def light(name, loc, energy, size=2, color=(1, 0.95, 0.9)):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.size = size; l.color = color
    o = bpy.data.objects.new(name, l); o.location = loc; scene.collection.objects.link(o)
    o.rotation_euler = (0, 0, 0); c = o.constraints.new('TRACK_TO'); c.target = rig; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
light('key', (1.6, -2.2, 2.2), 500); light('fill', (-2.2, -1.5, 1.4), 160, 3, (0.8, 0.85, 1)); light('rim', (0, 2.5, 2.4), 420, 2, (0.85, 1, 0.6))
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); scene.collection.objects.link(cam); scene.camera = cam
outdir = OUT / 'renders'; outdir.mkdir(parents=True, exist_ok=True)
def shot(name, loc, target_z, lens):
    cam.location = loc; cam.data.lens = lens
    d = np.array([0, 0, target_z]) - np.array(loc); yaw = math.atan2(d[0], -d[1]) if False else 0
    import mathutils
    cam.rotation_euler = (mathutils.Vector((0, 0, target_z)) - mathutils.Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    scene.render.filepath = str(outdir / name); bpy.ops.render.render(write_still=True); say('render', name)
shot('full_front.png', (0, -4.2, 1.0), 0.95, 50)
shot('face_34.png', (0.55, -1.05, 1.68), 1.6, 70)
shot('full_34.png', (2.4, -3.2, 1.2), 0.95, 50)
shot('face_front.png', (0, -1.15, 1.66), 1.62, 70)

# 8. export (separate glTF so pack_assets.py can embed geometry as .json)
exp = OUT / 'out' / 'operative'; exp.mkdir(parents=True, exist_ok=True)
for x in bpy.data.objects: x.select_set(x == rig or x.parent == rig or (x.type == 'MESH' and any(m.type == 'ARMATURE' for m in x.modifiers)))
bpy.ops.export_scene.gltf(filepath=str(exp / 'operative_1k.gltf'), export_format='GLTF_SEPARATE', use_selection=True, export_apply=True, export_skins=True,
                          export_animations=False, export_morph=False, export_yup=True, export_image_format='JPEG', export_jpeg_quality=82, export_texture_dir='textures')
say('exported', sorted(os.listdir(exp)))
say('bones', [b.name for b in rig.data.bones][:80])
