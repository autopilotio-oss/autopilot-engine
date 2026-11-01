"""Blender (headless) build of the AUTOPILOT.OI hooded operative with MPFB2 (MakeHuman, CC0 assets).
explore: install MPFB2 and asset packs, list assets, export thumbnails.
build: generate the character and export it (see later steps)."""
import bpy, sys, os, zipfile, shutil, json, glob, pathlib, traceback
STEP = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'explore'
DL = pathlib.Path.home() / 'dl'
OUT = pathlib.Path(os.getcwd()) / 'tools' / 'character'
log = []
def say(*a):
    s = ' '.join(str(x) for x in a); print('[char]', s); log.append(s)

def install_mpfb():
    src = DL / 'mpfb2' / 'src' / 'mpfb'
    z = DL / 'mpfb.zip'
    if not z.exists():
        shutil.make_archive(str(z)[:-4], 'zip', src.parent, 'mpfb')
    try:
        bpy.ops.extensions.package_install_files(filepath=str(z), repo='user_default', enable_on_install=True)
        say('extension installed via package_install_files')
    except Exception as e:
        say('package_install_files failed:', repr(e))
    mods = [m for m in sys.modules if m.endswith('mpfb') or '.mpfb' in m]
    say('mpfb modules loaded:', len(mods), sorted(mods)[:5])
    import addon_utils
    for m in addon_utils.modules():
        if 'mpfb' in m.__name__:
            say('addon module', m.__name__)
            addon_utils.enable(m.__name__, default_set=True)
    return [m for m in sys.modules if m.endswith('.mpfb') or m == 'mpfb']

def mpfb_pkg():
    for name in ('bl_ext.user_default.mpfb', 'mpfb'):
        if name in sys.modules:
            return name
    return None

def install_packs(pkg):
    for p in ['makehuman_system_assets', 'masks01', 'hats01', 'shirts01', 'pants01', 'shoes01', 'skins01', 'eyebrows01']:
        z = DL / f'{p}.zip'
        if not z.exists():
            say('pack missing', p); continue
        try:
            bpy.ops.mpfb.load_library_zip(filepath=str(z))
            say('pack installed', p)
        except Exception as e:
            say('pack install failed', p, repr(e))

def explore():
    mods = install_mpfb(); pkg = mpfb_pkg(); say('pkg', pkg)
    if not pkg: raise SystemExit('mpfb not importable')
    install_packs(pkg)
    LocationService = __import__(pkg + '.services.locationservice', fromlist=['LocationService']).LocationService
    root = LocationService.get_user_data(); say('user data', root)
    found = {}
    for kind in ('clothes', 'proxymeshes', 'eyes', 'eyebrows', 'skins', 'hair'):
        found[kind] = sorted(set(os.path.basename(os.path.dirname(f)) for f in glob.glob(os.path.join(root, kind, '**', '*.*'), recursive=True)))
        say(kind, len(found[kind]), found[kind][:80])
    thumbs = OUT / 'explore'; shutil.rmtree(thumbs, ignore_errors=True); thumbs.mkdir(parents=True)
    for kind in ('clothes',):
        for f in glob.glob(os.path.join(root, kind, '**', '*.thumb'), recursive=True):
            shutil.copy(f, thumbs / (os.path.basename(os.path.dirname(f)) + '.png'))
    (thumbs / 'assets.json').write_text(json.dumps(found, indent=1))
    hs = __import__(pkg + '.services.humanservice', fromlist=['HumanService']).HumanService
    say('HumanService methods', [m for m in dir(hs) if not m.startswith('_')])
    rs = __import__(pkg + '.services.rigservice', fromlist=['RigService']).RigService
    say('RigService methods', [m for m in dir(rs) if not m.startswith('_')][:60])

try:
    if STEP == 'explore':
        explore()
    else:
        exec(open(OUT / 'build_character.py').read())
finally:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f'log_{STEP}.txt').write_text('\n'.join(log))
