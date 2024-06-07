# wishlist_configs.py

# Import for type hints and intellisense
import json
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from main import Keys


def get_wishlist_config(keys: "Keys"):
    FILE_PATH = keys.PATH_KEY
    WISHLIST_DIR = keys.WISHLIST_DIR
    AUTHOR_NAME = keys.AUTHOR_KEY
    INCLUDE_TAGS = keys.INC_TAG_KEY
    EXCLUDE_TAGS = keys.EXC_TAG_KEY
    LIMIT_PERKS = keys.PERK_KEY
    REQUIRE_DUPLICATES = keys.DUPE_PERKS_KEY

    # Array of Wishlists Configs
    wishlist_configs = [
        # -------------------------------------------
        # No Filters
        {FILE_PATH: "all.txt"},
        # -------------------------------------------
        # Any Input
        {INCLUDE_TAGS: ["pve"], FILE_PATH: "pve.txt"},
        {INCLUDE_TAGS: ["pvp"], FILE_PATH: "pvp.txt"},
        # -------------------------------------------
        # Mouse and Keyboard
        {INCLUDE_TAGS: ["mkb"], FILE_PATH: "mkb.txt"},
        {INCLUDE_TAGS: ["mkb"], LIMIT_PERKS: True, FILE_PATH: "mkb_perks.txt"},
        {
            INCLUDE_TAGS: ["mkb"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "mkb_perks_dupes.txt",
        },
        {INCLUDE_TAGS: ["mkb", "god"], FILE_PATH: "mkb_god.txt"},
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backups"],
            FILE_PATH: "mkb_!backups.txt",
        },
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            FILE_PATH: "mkb_!backups_perks.txt",
        },
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "mkb_!backups_perks_dupes.txt",
        },
        # Mouse and Keyboard, PvE
        {INCLUDE_TAGS: ["mkb", "pve"], FILE_PATH: "mkb_pve.txt"},
        {
            INCLUDE_TAGS: ["mkb", "pve"],
            EXCLUDE_TAGS: ["backups"],
            FILE_PATH: "mkb_pve_!backups.txt",
        },
        {
            INCLUDE_TAGS: ["mkb", "pve"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            FILE_PATH: "mkb_pve_!backups_perks.txt",
        },
        {
            INCLUDE_TAGS: ["mkb", "pve"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "mkb_pve_!backups_perks_dupes.txt",
        },
        # Mouse and Keyboard, PvP
        {INCLUDE_TAGS: ["mkb", "pvp"], FILE_PATH: "mkb_pvp.txt"},
        # -------------------------------------------
        # Controller
        {INCLUDE_TAGS: ["ctr"], FILE_PATH: "ctr.txt"},
        {
            INCLUDE_TAGS: ["ctr"],
            LIMIT_PERKS: True,
            FILE_PATH: "ctr_perks.txt",
        },
        {
            INCLUDE_TAGS: ["ctr"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "ctr_perks_dupes.txt",
        },
        {INCLUDE_TAGS: ["ctr", "god"], FILE_PATH: "ctr_god.txt"},
        {
            INCLUDE_TAGS: ["ctr"],
            EXCLUDE_TAGS: ["backups"],
            FILE_PATH: "ctr_!backups.txt",
        },
        {
            INCLUDE_TAGS: ["ctr"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            FILE_PATH: "ctr_!backups_perks.txt",
        },
        {
            INCLUDE_TAGS: ["ctr"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "ctr_!backups_perks_dupes.txt",
        },
        # Controller, PvE
        {INCLUDE_TAGS: ["ctr", "pve"], FILE_PATH: "ctr_pve.txt"},
        {
            INCLUDE_TAGS: ["ctr", "pve"],
            EXCLUDE_TAGS: ["backups"],
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "ctr_pve_!backups_dupes.txt",
        },
        # Controller, PvP
        {INCLUDE_TAGS: ["ctr", "pvp"], FILE_PATH: "ctr_pvp.txt"},
        {
            INCLUDE_TAGS: ["ctr", "pvp"],
            EXCLUDE_TAGS: ["backups"],
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "ctr_pvp_!backups_dupes.txt",
        },
        # -------------------------------------------
        # Pandapaxxy filters
        {AUTHOR_NAME: ["pandapaxxy"], FILE_PATH: "pandapaxxy.txt"},
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb"],
            FILE_PATH: "pandapaxxy_mkb.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb", "pve"],
            FILE_PATH: "pandapaxxy_mkb_pve.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb", "pvp"],
            FILE_PATH: "pandapaxxy_mkb_pvp.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb"],
            LIMIT_PERKS: True,
            FILE_PATH: "pandapaxxy_mkb_perks.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["ctr"],
            FILE_PATH: "pandapaxxy_ctr.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["ctr", "pve"],
            FILE_PATH: "pandapaxxy_ctr_pve.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["ctr", "pvp"],
            FILE_PATH: "pandapaxxy_ctr_pvp.txt",
        },
    ]

    # Iterate through the list of dictionaries
    for wishlist in wishlist_configs:
        # Add directory to file path
        wishlist[FILE_PATH] = WISHLIST_DIR + wishlist[FILE_PATH]

        # Extend include and exclude tags
        if INCLUDE_TAGS in wishlist and wishlist[INCLUDE_TAGS] is not None:
            transform_tags(wishlist[INCLUDE_TAGS])

        if EXCLUDE_TAGS in wishlist and wishlist[EXCLUDE_TAGS] is not None:
            transform_tags(wishlist[EXCLUDE_TAGS])

    return wishlist_configs


# Extend tags to catch all rolls
def transform_tags(tag_list: List[str]):
    # Handle tag transformations
    tag_transformations = {
        # "god": {"god"},
        "backups": {"backup roll", "backup choice roll"},
        "ctr": {"controller"},
    }
    for tag, transformed_tags in tag_transformations.items():
        if tag in tag_list:
            tag_list.remove(tag)
            tag_list.extend(transformed_tags)


# Write the file names to separate txt file for website
def export_wishlist_names(keys: "Keys"):
    # Create array with the file names
    wishlist_paths = []
    for config in keys.WISHLIST_CONFIGS:
        wishlist_paths.append(config[keys.PATH_KEY])

    # Write names to file
    with open(keys.WISHLIST_NAMES_PATH, "w") as file:
        json.dump(wishlist_paths, file)
