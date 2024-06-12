# get_weapon_mods.py

import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Keys


#############################
# Gets array from file_path #
#############################
def get_weapon_mods(keys: "Keys") -> set:
    # Empty set to hold frame mod hashes
    origin_traits = set()
    frame_mods = set()

    # Open and read the JSON file
    with open(keys.ORIGIN_TRAITS_PATH, "r", encoding="utf-8") as origin_traits_file:
        origin_traits = set(json.load(origin_traits_file))

    with open(keys.FRAME_MODS_PATH, "r", encoding="utf-8") as frame_mods_file:
        frame_mods = set(json.load(frame_mods_file))

    return origin_traits, frame_mods
