# get_weapon_mods.py

import json

# Import keys
from helper_scripts.keys import Keys


def get_weapon_mods(keys: "Keys") -> tuple[set, set]:
    # Empty set to hold file data
    origin_traits = set()
    frame_mods = set()

    # Get origin traits from file
    with open(keys.ORIGIN_TRAITS_PATH, "r", encoding="utf-8") as origin_traits_file:
        origin_traits = set(json.load(origin_traits_file))

    # Get frame mods from file
    with open(keys.FRAME_MODS_PATH, "r", encoding="utf-8") as frame_mods_file:
        frame_mods = set(json.load(frame_mods_file))

    return origin_traits, frame_mods
