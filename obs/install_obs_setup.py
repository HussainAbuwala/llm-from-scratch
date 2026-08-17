#!/usr/bin/env python3
"""Install a ready-to-record OBS setup: screen capture + circular webcam bubble.

Creates a NEW scene collection and a NEW profile, both named "LLM Series".
Your existing "Untitled" collection and profile are left completely alone, and
the whole OBS config directory is backed up first.

OBS must be QUIT before running this — OBS rewrites its config on exit and would
overwrite these files.

    python3 install_obs_setup.py
"""

import json
import os
import shutil
import subprocess
import sys
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
OBS = os.path.expanduser("~/Library/Application Support/obs-studio")
COLLECTION_NAME = "LLM Series"
COLLECTION_FILE = "LLM_Series.json"
PROFILE_NAME = "LLM Series"

MASK = os.path.join(HERE, "bubble_mask.png")
RING = os.path.join(HERE, "bubble_ring_blue.png")

# Bubble geometry on a 1920x1080 canvas: 330px circle, 40px margin, bottom-right.
BUBBLE = 330
MARGIN = 40
BX = 1920 - BUBBLE - MARGIN
BY = 1080 - BUBBLE - MARGIN

# Bounding-box types (libobs enum)
BOUNDS_NONE, BOUNDS_STRETCH, BOUNDS_INNER, BOUNDS_OUTER = 0, 1, 2, 3
ALIGN_TOPLEFT, ALIGN_CENTER = 5, 0


def die(msg):
    print(f"\n  ✗ {msg}\n")
    sys.exit(1)


def preflight():
    if subprocess.run(["pgrep", "-x", "OBS"], capture_output=True).returncode == 0:
        die("OBS is still running. Quit it (Cmd+Q) and run this again.")
    if not os.path.isdir(OBS):
        die(f"No OBS config at {OBS}. Launch OBS once, then quit it.")
    for p in (MASK, RING):
        if not os.path.exists(p):
            die(f"Missing {os.path.basename(p)} — run: python3 make_bubble_assets.py")


def backup():
    dest = f"{OBS}.backup-{time.strftime('%Y%m%d-%H%M%S')}"
    shutil.copytree(OBS, dest)
    print(f"  backup      {dest}")
    return dest


def source(sid, name, settings, filters=None):
    return {
        "prev_ver": 537001985,
        "name": name,
        "uuid": str(uuid.uuid4()),
        "id": sid,
        "versioned_id": sid,
        "settings": settings,
        "mixers": 0 if sid == "scene" else 255,
        "sync": 0,
        "flags": 0,
        "volume": 1.0,
        "balance": 0.5,
        "enabled": True,
        "muted": False,
        "push-to-mute": False,
        "push-to-mute-delay": 0,
        "push-to-talk": False,
        "push-to-talk-delay": 0,
        "deinterlace_mode": 0,
        "deinterlace_field_order": 0,
        "monitoring_type": 0,
        "private_settings": {},
        **({"filters": filters} if filters else {}),
    }


def filt(fid, name, settings):
    f = source(fid, name, settings)
    f["mixers"] = 0
    return f


def item(src, item_id, x, y, w, h, bounds_type=BOUNDS_INNER, crop=False,
         scene_w=1920.0, scene_h=1080.0):
    """One scene item.

    OBS 30.2+ stores scene-item geometry in *relative* coordinates and treats
    those as authoritative — the absolute `pos`/`bounds` are recomputed from them
    on load. The mapping, confirmed by reading back what OBS wrote, is:

        abs_x    = (pos_rel_x + scene_w / scene_h) * (scene_h / 2)
        abs_y    = (pos_rel_y + 1.0)               * (scene_h / 2)
        abs_size = bounds_rel                      * (scene_h / 2)

    Note it is the *containing* scene's dimensions that matter, not the canvas —
    which is why items inside the square 1080x1080 bubble scene need different
    relative values from items on the main 16:9 canvas.
    """
    half = scene_h / 2.0
    aspect = scene_w / scene_h
    return {
        "name": src["name"],
        "source_uuid": src["uuid"],
        "visible": True,
        "locked": False,
        "rot": 0.0,
        "scale_ref": {"x": scene_w, "y": scene_h},
        "align": ALIGN_TOPLEFT,
        "bounds_type": bounds_type,
        "bounds_align": ALIGN_CENTER,
        "bounds_crop": crop,
        "crop_left": 0,
        "crop_top": 0,
        "crop_right": 0,
        "crop_bottom": 0,
        "id": item_id,
        "group_item_backup": False,
        "pos": {"x": float(x), "y": float(y)},
        "pos_rel": {"x": x / half - aspect, "y": y / half - 1.0},
        "scale": {"x": 1.0, "y": 1.0},
        "scale_rel": {"x": 1.0, "y": 1.0},
        "bounds": {"x": float(w), "y": float(h)},
        "bounds_rel": {"x": w / half, "y": h / half},
        "scale_filter": "disable",
        "blend_method": "default",
        "blend_type": "normal",
        "show_transition": {"duration": 300},
        "hide_transition": {"duration": 300},
        "private_settings": {},
    }


def scene(name, items, custom=None, filters=None):
    settings = {
        "id_counter": len(items) + 1,
        "custom_size": custom is not None,
        "items": items,
    }
    if custom:
        settings["cx"], settings["cy"] = custom
    s = source("scene", name, settings, filters)
    s["canvas_uuid"] = "6c69626f-6273-4c00-9d88-c5136d61696e"
    return s


def find_existing(base, sid):
    """Reuse the display/camera IDs OBS already discovered on this machine."""
    for s in base.get("sources", []):
        if s["id"] == sid:
            return s["settings"]
    return {}


def build(base):
    screen_settings = dict(find_existing(base, "screen_capture"))
    screen_settings.update({"type": 0, "show_cursor": True, "hide_obs": True})

    cam_settings = dict(find_existing(base, "macos-avcapture"))
    if not cam_settings.get("device"):
        print("  ! no camera device found in the old collection — pick yours from")
        print("    the 'Face (camera)' source properties after OBS opens")

    screen = source("screen_capture", "Canvas (screen)", screen_settings)
    camera = source("macos-avcapture", "Face (camera)", cam_settings)

    # Square-crop the camera inside a fixed 1080x1080 scene, so the round mask
    # stays round whatever resolution the camera reports.
    bubble = scene(
        "· bubble source (ignore)",
        [item(camera, 1, 0, 0, 1080, 1080, BOUNDS_OUTER, crop=True,
              scene_w=1080.0, scene_h=1080.0)],
        custom=(1080, 1080),
        # "mask_color" reads the circle out of the image's colour channel. The
        # mask PNG encodes the circle in colour AND alpha, so this is correct
        # under either mask type if OBS falls back to its default.
        filters=[filt("mask_filter", "Circle mask",
                      {"type": "mask_color", "image_path": MASK,
                       "color": 0xFFFFFFFF, "opacity": 100})],
    )
    rim = source("image_source", "Bubble rim", {"file": RING, "unload": False})

    main = scene("Canvas + bubble", [
        item(screen, 1, 0, 0, 1920, 1080, BOUNDS_OUTER, crop=True),
        item(bubble, 2, BX, BY, BUBBLE, BUBBLE),
        item(rim, 3, BX, BY, BUBBLE, BUBBLE),
    ])

    out = dict(base)
    out["name"] = COLLECTION_NAME
    out["sources"] = [screen, camera, bubble, rim, main]
    out["scene_order"] = [{"name": main["name"]}, {"name": bubble["name"]}]
    out["current_scene"] = main["name"]
    out["current_program_scene"] = main["name"]
    out["groups"] = []
    return out


PROFILE_INI = """[General]
Name={name}

[Video]
BaseCX=1920
BaseCY=1080
OutputCX=1920
OutputCY=1080
FPSType=0
FPSCommon=30
ScaleType=lanczos
ColorFormat=NV12
ColorSpace=709
ColorRange=Partial
SdrWhiteLevel=300
HdrNominalPeakLevel=1000

[Audio]
SampleRate=48000
ChannelSetup=Stereo

[Output]
Mode=Simple
FilenameFormatting=llm-%CCYY-%MM-%DD %hh-%mm-%ss

[SimpleOutput]
FilePath={recdir}
RecFormat2=hybrid_mp4
RecQuality=HQ
RecEncoder=apple_h264
RecAudioEncoder=aac
RecTracks=1
VBitrate=6000
ABitrate=160
UseAdvanced=false
"""


def write_profile():
    d = os.path.join(OBS, "basic", "profiles", PROFILE_NAME)
    os.makedirs(d, exist_ok=True)
    recdir = os.path.expanduser("~/Movies/llm-series")
    os.makedirs(recdir, exist_ok=True)
    with open(os.path.join(d, "basic.ini"), "w") as fh:
        fh.write(PROFILE_INI.format(name=PROFILE_NAME, recdir=recdir))
    print(f"  profile     {d}/basic.ini")
    print(f"  recordings  {recdir}")


def point_obs_at_it():
    """Update [Basic] in user.ini so OBS opens straight into the new setup."""
    path = os.path.join(OBS, "user.ini")
    lines = open(path).read().splitlines()
    want = {
        "Profile": PROFILE_NAME,
        "ProfileDir": PROFILE_NAME,
        "SceneCollection": COLLECTION_NAME,
        "SceneCollectionFile": COLLECTION_FILE.removesuffix(".json"),
    }
    out, section, seen = [], None, set()
    for ln in lines:
        if ln.startswith("["):
            if section == "Basic":
                out += [f"{k}={v}" for k, v in want.items() if k not in seen]
                seen |= set(want)
            section = ln.strip("[]")
        if section == "Basic":
            key = ln.split("=", 1)[0].strip()
            if key in want:
                seen.add(key)
                out.append(f"{key}={want[key]}")
                continue
        if section == "General" and ln.startswith("FirstRun="):
            out.append("FirstRun=false")  # don't let the wizard overwrite us
            continue
        out.append(ln)
    if section == "Basic":
        out += [f"{k}={v}" for k, v in want.items() if k not in seen]
    with open(path, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"  user.ini    now opens '{COLLECTION_NAME}'")


def verify(collection):
    """Recompute geometry the way OBS does and assert it matches our intent.

    Guards against the relative-coordinate mistake that put the camera at
    pos.x = -420 and half size on the first attempt.
    """
    for s in collection["sources"]:
        if s["id"] != "scene":
            continue
        sw, sh = (1080.0, 1080.0) if s["settings"].get("custom_size") else (1920.0, 1080.0)
        half, aspect = sh / 2.0, sw / sh
        for it in s["settings"]["items"]:
            got = ((it["pos_rel"]["x"] + aspect) * half,
                   (it["pos_rel"]["y"] + 1.0) * half,
                   it["bounds_rel"]["x"] * half,
                   it["bounds_rel"]["y"] * half)
            want = (it["pos"]["x"], it["pos"]["y"],
                    it["bounds"]["x"], it["bounds"]["y"])
            if any(abs(a - b) > 0.51 for a, b in zip(got, want)):
                die(f"geometry check failed for '{it['name']}' in '{s['name']}': "
                    f"OBS would render {got}, we intended {want}")
    print("  geometry    verified against OBS's relative-coordinate maths")


if __name__ == "__main__":
    print("\nInstalling OBS setup: canvas + corner face\n")
    preflight()
    backup()

    base_path = os.path.join(OBS, "basic", "scenes", "Untitled.json")
    base = json.load(open(base_path)) if os.path.exists(base_path) else {"version": 2}

    collection = build(base)
    verify(collection)

    dest = os.path.join(OBS, "basic", "scenes", COLLECTION_FILE)
    with open(dest, "w") as fh:
        json.dump(collection, fh, indent=1)
    print(f"  collection  {dest}")

    write_profile()
    point_obs_at_it()

    print(f"""
Done. Open OBS — it will start in the "{COLLECTION_NAME}" collection with one
scene, "Canvas + bubble":

  Canvas (screen)   your whole display, filled to 16:9
  Bubble            your face, circular, bottom-right
  Bubble rim        the blue ring + shadow

Two things worth doing by hand (10 seconds each):

  1. Canvas (screen) → double-click → Method: Window → pick your browser.
     Cleaner than display capture: no menu bar, no notification banners.
  2. Settings → Hotkeys → set "Pause Recording". Pause between scenes instead
     of stopping and you get one clean file.

To go back: OBS → Scene Collection → Untitled, and Profile → Untitled.
""")
