# wishlist_configs.py

# Import for type hints and intellisense
import json
from typing import TYPE_CHECKING, Set, List

if TYPE_CHECKING:
    from main import Keys


def get_wishlist_config(keys: "Keys"):
    # Array of Wishlists Configs
    wishlist_configs = [
        # -------------------------------------------
        # No Filters
        {keys.PATH_KEY: "All_Rolls.txt"},
        # -------------------------------------------
        # Any Input
        {keys.INC_TAGS_KEY: {"pve"}, keys.PATH_KEY: "PvE.txt"},
        {keys.INC_TAGS_KEY: {"pvp"}, keys.PATH_KEY: "PvP.txt"},
        # -------------------------------------------
        # Mouse and Keyboard
        {keys.INC_TAGS_KEY: {"mkb"}, keys.PATH_KEY: "MKB.txt"},
        {
            keys.INC_TAGS_KEY: {"mkb"},
            keys.PERKS_KEY: True,
            keys.PATH_KEY: "MKB_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb"},
            keys.PERKS_KEY: True,
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "MKB_Perks_Dupes.txt",
        },
        {keys.INC_TAGS_KEY: {"mkb", "god"}, keys.PATH_KEY: "MKB_God.txt"},
        {
            keys.INC_TAGS_KEY: {"mkb"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PATH_KEY: "MKB_!Backups.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PERKS_KEY: True,
            keys.PATH_KEY: "MKB_!Backups_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PERKS_KEY: True,
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "MKB_!Backups_Perks_Dupes.txt",
        },
        # Mouse and Keyboard, PvE
        {keys.INC_TAGS_KEY: {"mkb", "pve"}, keys.PATH_KEY: "MKB_PvE.txt"},
        {
            keys.INC_TAGS_KEY: {"mkb", "pve"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PATH_KEY: "MKB_PvE_!Backups.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb", "pve"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "MKB_PvE_!Backups_Dupes.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb", "pve"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PERKS_KEY: True,
            keys.PATH_KEY: "MKB_PvE_!Backups_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb", "pve"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PERKS_KEY: True,
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "MKB_PvE_!Backups_Perks_Dupes.txt",
        },
        # Mouse and Keyboard, PvP
        {keys.INC_TAGS_KEY: {"mkb", "pvp"}, keys.PATH_KEY: "MKB_PvP.txt"},
        {
            keys.INC_TAGS_KEY: {"mkb", "pvp"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "MKB_PvP_!Backups_Dupes.txt",
        },
        # -------------------------------------------
        # Controller
        {keys.INC_TAGS_KEY: {"ctr"}, keys.PATH_KEY: "CTR.txt"},
        {
            keys.INC_TAGS_KEY: {"ctr"},
            keys.PERKS_KEY: True,
            keys.PATH_KEY: "CTR_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"ctr"},
            keys.PERKS_KEY: True,
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "CTR_Perks_Dupes.txt",
        },
        {keys.INC_TAGS_KEY: {"ctr", "god"}, keys.PATH_KEY: "CTR_God.txt"},
        {
            keys.INC_TAGS_KEY: {"ctr"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PATH_KEY: "CTR_!Backups.txt",
        },
        {
            keys.INC_TAGS_KEY: {"ctr"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PERKS_KEY: True,
            keys.PATH_KEY: "CTR_!Backups_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"ctr"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.PERKS_KEY: True,
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "CTR_!Backups_Perks_Dupes.txt",
        },
        # Controller, PvE
        {keys.INC_TAGS_KEY: {"ctr", "pve"}, keys.PATH_KEY: "CTR_PvE.txt"},
        {
            keys.INC_TAGS_KEY: {"ctr", "pve"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "CTR_PvE_!Backups_Dupes.txt",
        },
        # Controller, PvP
        {keys.INC_TAGS_KEY: {"ctr", "pvp"}, keys.PATH_KEY: "CTR_PvP.txt"},
        {
            keys.INC_TAGS_KEY: {"ctr", "pvp"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.DUPES_KEY: True,
            keys.PATH_KEY: "CTR_PvP_!Backups_Dupes.txt",
        },
        # -------------------------------------------
        # Pandapaxxy filters
        {keys.AUTHOR_KEY: {"pandapaxxy"}, keys.PATH_KEY: "PandaPaxxy.txt"},
        {
            keys.AUTHOR_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"mkb"},
            keys.PATH_KEY: "PandaPaxxy_MKB.txt",
        },
        {
            keys.AUTHOR_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"mkb", "pve"},
            keys.PATH_KEY: "PandaPaxxy_MKB_PvE.txt",
        },
        {
            keys.AUTHOR_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"mkb", "pvp"},
            keys.PATH_KEY: "PandaPaxxy_MKB_PvP.txt",
        },
        {
            keys.AUTHOR_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"mkb"},
            keys.PERKS_KEY: True,
            keys.PATH_KEY: "PandaPaxxy_MKB_Perks.txt",
        },
        {
            keys.AUTHOR_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"ctr"},
            keys.PATH_KEY: "PandaPaxxy_CTR.txt",
        },
        {
            keys.AUTHOR_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"ctr", "pve"},
            keys.PATH_KEY: "PandaPaxxy_CTR_PvE.txt",
        },
        {
            keys.AUTHOR_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"ctr", "pvp"},
            keys.PATH_KEY: "PandaPaxxy_CTR_PvP.txt",
        },
    ]

    # Iterate through the list of dictionaries
    wishlist_paths = []

    # Collect options used in configs
    author_names = set()
    inc_tags = set()
    exc_tags = set()

    for wishlist in wishlist_configs:
        set_wishlist_path(wishlist, wishlist_paths, keys)

        set_wishlist_tags(wishlist, author_names, inc_tags, exc_tags, keys)

    # Write wishlist paths to file for website
    with open(keys.WISHLIST_NAMES_PATH, "w") as file:
        json.dump(wishlist_paths, file)

    return {
        keys.WISHLIST_CONFIGS_KEY: wishlist_configs,
        keys.AUTHOR_KEY: author_names,
        keys.INC_TAGS_KEY: inc_tags,
        keys.EXC_TAGS_KEY: exc_tags,
    }


# Add directory to file path and add path to wishlist and wishlist_paths
def set_wishlist_path(wishlist, wishlist_paths: List[str], keys: "Keys"):
    wishlist_path = keys.WISHLIST_DIR + wishlist[keys.PATH_KEY]
    wishlist[keys.PATH_KEY] = wishlist_path  # Add path to wishlist name

    wishlist_paths.append(wishlist_path)  # Add full path to array for website


# Set inc and exc tags. Add tags and author names to set that holds all wishlist options
def set_wishlist_tags(
    wishlist,
    author_names: Set[str],
    inc_tags: Set[str],
    exc_tags: Set[str],
    keys: "Keys",
):
    # Extend include and exclude tags
    if keys.INC_TAGS_KEY in wishlist and wishlist.get(keys.INC_TAGS_KEY):
        transform_tags(wishlist[keys.INC_TAGS_KEY])

    if keys.EXC_TAGS_KEY in wishlist and wishlist.get(keys.EXC_TAGS_KEY):
        transform_tags(wishlist[keys.EXC_TAGS_KEY])

    author_names.update(wishlist.get(keys.AUTHOR_KEY, []))
    inc_tags.update(wishlist.get(keys.INC_TAGS_KEY, []))
    exc_tags.update(wishlist.get(keys.EXC_TAGS_KEY, []))


# Extend tags to catch all rolls
def transform_tags(tag_list: Set[str]):
    # Handle tag transformations
    tag_transformations = {
        "backups": {"backup roll", "backup choice roll"},
        "ctr": {"controller"},
    }
    for tag, transformed_tags in tag_transformations.items():
        if tag in tag_list:
            tag_list.remove(tag)
            tag_list.update(transformed_tags)
