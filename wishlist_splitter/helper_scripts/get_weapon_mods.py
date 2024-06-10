# get_weapon_mods.py

import json


#############################
# Gets array from file_path #
#############################
def get_weapon_mods(file_path: str) -> set:
    # Empty set to hold frame mod hashes
    weapon_mods_set = set()

    # Open and read the JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        weapon_mods_list = json.load(file)
        weapon_mods_set = set(weapon_mods_list)

    return weapon_mods_set
