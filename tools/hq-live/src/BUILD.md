# HQ page source

index.html is the concatenation of these parts, in this order:
head.html a_config.js a2_config.js b_render.js c_scene1.js c_interior.js c_assets.js c_character.js c_scene2.js d_chars.js e_agents.js f_live1.js f_live_hub.js f_live_mid.js f_live2.js g_wall.js g_ui.js h_cam.js h_light.js i_loop.js

Character: built by .github/workflows/character.yml (Blender 4.2 + MPFB2, CC0 MakeHuman assets) from tools/character/build_character.py,
exported to tools/character/out/operative, packed for the artifact host with tools/hq-live/pack_assets.py (glTF as .json, textures as images).
