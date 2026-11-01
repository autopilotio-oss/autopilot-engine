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
mask = add('clothes', 'culturalibre_hero_mask_1', 'Clothes')
hood = add('clothes', 'culturalibre_hero-heroine_hood_1', 'Clothes')

# 4. recolor textures (keep the fabric detail, change the color): heather black fleece, black knit mask, black denim-like pants, black sneakers
def recolor(obj, target, contrast=0.6, keep_light_above=None):
    if not obj: return
    for slot in obj.material_slots:
        m = slot.material
        if not m or not m.use_nodes: continue
        for n in m.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image and ('diff' in n.image.name.lower() or 'color' in n.image.name.lower() or n.outputs['Color'].links and any(l.to_socket.name == 'Base Color' for l in n.outputs['Color'].links)):
                im = n.image; w, h = im.size
                if w == 0: continue
                px = np.array(im.pixels[:], dtype=np.float32).reshape(h, w, 4)
                lum = (px[..., 0] * 0.3 + px[..., 1] * 0.59 + px[..., 2] * 0.11)
                lum = (lum - lum.mean()) * contrast + 0.5
                out = np.empty_like(px); t = np.array(target, np.float32)
                for c in range(3): out[..., c] = np.clip(t[c] * (0.55 + lum), 0, 1)
                if keep_light_above is not None:
                    keep = (px[..., 0] + px[..., 1] + px[..., 2]) / 3 > keep_light_above
                    out[keep, :3] = px[keep, :3]
                out[..., 3] = px[..., 3]
                new = bpy.data.images.new(obj.name + '_' + im.name + '_rc', w, h, alpha=True); new.pixels[:] = out.ravel(); new.file_format = 'JPEG'
                n.image = new; say('recolored', obj.name, im.name)
recolor(top, (0.075, 0.075, 0.08), 0.9)
recolor(hood, (0.07, 0.07, 0.075), 0.9)
recolor(mask, (0.035, 0.035, 0.038), 0.7)
recolor(pants, (0.05, 0.052, 0.058), 0.9)
recolor(shoes, (0.04, 0.04, 0.045), 0.8, keep_light_above=0.8)

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

# 8. export (separate glTF so pack_assets.py can embed geometry as .json)
exp = OUT / 'out' / 'operative'; exp.mkdir(parents=True, exist_ok=True)
for x in bpy.data.objects: x.select_set(x == rig or x.parent == rig or (x.type == 'MESH' and any(m.type == 'ARMATURE' for m in x.modifiers)))
bpy.ops.export_scene.gltf(filepath=str(exp / 'operative_1k.gltf'), export_format='GLTF_SEPARATE', use_selection=True, export_apply=True, export_skins=True,
                          export_animations=False, export_morph=False, export_yup=True, export_image_format='JPEG', export_jpeg_quality=82, export_texture_dir='textures')
say('exported', sorted(os.listdir(exp)))
say('bones', [b.name for b in rig.data.bones][:80])
