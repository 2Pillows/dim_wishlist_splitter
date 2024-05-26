# wishlist_configs.py

# Import for type hints and intellisense
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from main import Keys


def get_wishlist_config(keys: "Keys"):
    FILE_NAME = keys.PATH_KEY
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
        {FILE_NAME: "all.txt"},
        # -------------------------------------------
        # Gamemdoe filters
        {INCLUDE_TAGS: ["pve"], FILE_NAME: "pve.txt"},
        {INCLUDE_TAGS: ["pvp"], FILE_NAME: "pvp.txt"},
        # -------------------------------------------
        # Input filters
        {INCLUDE_TAGS: ["mkb"], FILE_NAME: "mkb.txt"},
        {INCLUDE_TAGS: ["controller"], FILE_NAME: "ctr.txt"},
        # -------------------------------------------
        # Perks
        {INCLUDE_TAGS: ["mkb"], LIMIT_PERKS: True, FILE_NAME: "mkb_perks.txt"},
        {
            INCLUDE_TAGS: ["controller"],
            LIMIT_PERKS: True,
            FILE_NAME: "ctr_perks.txt",
        },
        # -------------------------------------------
        # Perks and Dupes
        {
            INCLUDE_TAGS: ["mkb"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_NAME: "mkb_perks_dupes.txt",
        },
        {
            INCLUDE_TAGS: ["controller"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_NAME: "ctr_perks_dupes.txt",
        },
        # -------------------------------------------
        # Input and Gamemode filters
        {INCLUDE_TAGS: ["mkb", "pve"], FILE_NAME: "mkb_pve.txt"},
        {INCLUDE_TAGS: ["mkb", "pvp"], FILE_NAME: "mkb_pvp.txt"},
        {INCLUDE_TAGS: ["controller", "pve"], FILE_NAME: "ctr_pve.txt"},
        {INCLUDE_TAGS: ["controller", "pvp"], FILE_NAME: "ctr_pvp.txt"},
        # -------------------------------------------
        # Pandapaxxy filters
        {AUTHOR_NAME: ["pandapaxxy"], FILE_NAME: "panda.txt"},
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb"],
            FILE_NAME: "mkb_panda.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb", "pve"],
            FILE_NAME: "mkb_panda_pve.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb", "pvp"],
            FILE_NAME: "mkb_panda_pvp.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["controller"],
            FILE_NAME: "ctr_panda.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["controller", "pve"],
            FILE_NAME: "ctr_panda_pve.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["controller", "pvp"],
            FILE_NAME: "ctr_panda_pvp.txt",
        },
        {
            AUTHOR_NAME: ["pandapaxxy"],
            INCLUDE_TAGS: ["mkb"],
            LIMIT_PERKS: True,
            FILE_NAME: "mkb_panda_perks.txt",
        },
        # -------------------------------------------
        # God filters
        {INCLUDE_TAGS: ["mkb", "god"], FILE_NAME: "mkb_god.txt"},
        {INCLUDE_TAGS: ["controller", "god"], FILE_NAME: "ctr_god.txt"},
        # -------------------------------------------
        # Exclude backup rolls filters
        # --- MKB
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backup"],
            FILE_NAME: "mkb_!backup.txt",
        },
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backup"],
            LIMIT_PERKS: True,
            FILE_NAME: "mkb_!backup_perks.txt",
        },
        {
            INCLUDE_TAGS: ["mkb"],
            EXCLUDE_TAGS: ["backup"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_NAME: "mkb_!backup_perks_dupes.txt",
        },
        {
            INCLUDE_TAGS: ["mkb", "pve"],
            EXCLUDE_TAGS: ["backup"],
            LIMIT_PERKS: True,
            FILE_NAME: "mkb_pve_!backup_perks.txt",
        },
        {
            INCLUDE_TAGS: ["mkb", "pve"],
            EXCLUDE_TAGS: ["backup"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_NAME: "mkb_pve_!backup_perks_dupes.txt",
        },
        # --- Controller
        {
            INCLUDE_TAGS: ["controller"],
            EXCLUDE_TAGS: ["backup"],
            FILE_NAME: "ctr_!backup.txt",
        },
        {
            INCLUDE_TAGS: ["controller"],
            EXCLUDE_TAGS: ["backup"],
            LIMIT_PERKS: True,
            FILE_NAME: "ctr_!backup_perks.txt",
        },
        {
            INCLUDE_TAGS: ["controller"],
            EXCLUDE_TAGS: ["backup"],
            LIMIT_PERKS: True,
            REQUIRE_DUPLICATES: True,
            FILE_NAME: "ctr_!backup_perks_dupes.txt",
        },
    ]

    # Iterate through the list of dictionaries
    for wishlist in wishlist_configs:
        # Add directory to file path
        wishlist[FILE_NAME] = WISHLIST_DIR + wishlist[FILE_NAME]

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
        "backup": {"backup roll", "backup choice roll"},
    }
    for tag, transformed_tags in tag_transformations.items():
        if tag in tag_list:
            tag_list.remove(tag)
            tag_list.extend(transformed_tags)
