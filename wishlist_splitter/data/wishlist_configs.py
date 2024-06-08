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
        {FILE_PATH: "All_Rolls.txt"},
        # -------------------------------------------
        # Any Input
        {INCLUDE_TAGS: ["pve"], FILE_PATH: "PvE.txt"},
        {INCLUDE_TAGS: ["pvp"], FILE_PATH: "PvP.txt"},
        # -------------------------------------------
        # Mouse and Keyboard
        {INCLUDE_TAGS: ["mkb"], FILE_PATH: "MKB.txt"},
        {INCLUDE_TAGS: ["mkb"], LIMIT_PERKS: True, FILE_PATH: "MKB_Perks.txt"},
        {
            INCLUDE_TAGS: ["mkb"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "MKB_Perks_Dupes.txt",
        },
        {INCLUDE_TAGS: ["mkb", "god"], FILE_PATH: "MKB_God.txt"},
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backups"],
            FILE_PATH: "MKB_!Backups.txt",
        },
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            FILE_PATH: "MKB_!Backups_Perks.txt",
        },
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "MKB_!Backups_Perks_Dupes.txt",
        },
        # Mouse and Keyboard, PvE
        {INCLUDE_TAGS: ["mkb", "pve"], FILE_PATH: "MKB_PvE.txt"},
        {
            INCLUDE_TAGS: ["mkb", "pve"],
            EXCLUDE_TAGS: ["backups"],
            FILE_PATH: "MKB_PvE_!Backups.txt",
        },
        {
            INCLUDE_TAGS: ["mkb", "pve"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            FILE_PATH: "MKB_PvE_!Backups_Perks.txt",
        },
        {
            INCLUDE_TAGS: ["mkb", "pve"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "MKB_PvE_!Backups_Perks_Dupes.txt",
        },
        # Mouse and Keyboard, PvP
        {INCLUDE_TAGS: ["mkb", "pvp"], FILE_PATH: "MKB_PvP.txt"},
        # -------------------------------------------
        # Controller
        {INCLUDE_TAGS: ["ctr"], FILE_PATH: "CTR.txt"},
        {
            INCLUDE_TAGS: ["ctr"],
            LIMIT_PERKS: True,
            FILE_PATH: "CTR_Perks.txt",
        },
        {
            INCLUDE_TAGS: ["ctr"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "CTR_Perks_Dupes.txt",
        },
        {INCLUDE_TAGS: ["ctr", "god"], FILE_PATH: "CTR_God.txt"},
        {
            INCLUDE_TAGS: ["ctr"],
            EXCLUDE_TAGS: ["backups"],
            FILE_PATH: "CTR_!Backups.txt",
        },
        {
            INCLUDE_TAGS: ["ctr"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            FILE_PATH: "CTR_!Backups_Perks.txt",
        },
        {
            INCLUDE_TAGS: ["ctr"],
            EXCLUDE_TAGS: ["backups"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "CTR_!Backups_Perks_Dupes.txt",
        },
        # Controller, PvE
        {INCLUDE_TAGS: ["ctr", "pve"], FILE_PATH: "CTR_PvE.txt"},
        {
            INCLUDE_TAGS: ["ctr", "pve"],
            EXCLUDE_TAGS: ["backups"],
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "CTR_PvE_!Backups_Dupes.txt",
        },
        # Controller, PvP
        {INCLUDE_TAGS: ["ctr", "pvp"], FILE_PATH: "CTR_PvP.txt"},
        {
            INCLUDE_TAGS: ["ctr", "pvp"],
            EXCLUDE_TAGS: ["backups"],
            REQUIRE_DUPLICATES: True,
            FILE_PATH: "CTR_PvP_!Backups_Dupes.txt",
        },
        # -------------------------------------------
        # Pandapaxxy filters
        {AUTHOR_NAME: ["pandapaxxy"], FILE_PATH: "PandaPaxxy.txt"},
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb"],
            FILE_PATH: "PandaPaxxy_MKB.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb", "pve"],
            FILE_PATH: "PandaPaxxy_MKB_PvE.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb", "pvp"],
            FILE_PATH: "PandaPaxxy_MKB_PvP.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb"],
            LIMIT_PERKS: True,
            FILE_PATH: "PandaPaxxy_MKB_Perks.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["ctr"],
            FILE_PATH: "PandaPaxxy_CTR.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["ctr", "pve"],
            FILE_PATH: "PandaPaxxy_CTR_PvE.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["ctr", "pvp"],
            FILE_PATH: "PandaPaxxy_CTR_PvP.txt",
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
