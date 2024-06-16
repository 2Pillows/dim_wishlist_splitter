# wishlist_configs.py

import json

# Import keys
from helper_scripts.keys import Keys


def get_wishlist_config(keys: "Keys"):
    wishlist_configs = [
        # -------------------------------------------
        # All Rolls
        {keys.PATH_KEY: "All_Rolls.txt"},
        {keys.REQ_TRIMMED_PERKS: True, keys.PATH_KEY: "All_Rolls_Perks.txt"},
        # -------------------------------------------
        # Any Input
        {keys.INC_TAGS_KEY: {"pve"}, keys.PATH_KEY: "PvE.txt"},
        {keys.INC_TAGS_KEY: {"pvp"}, keys.PATH_KEY: "PvP.txt"},
        # -------------------------------------------
        # Mouse and Keyboard
        {keys.INC_TAGS_KEY: {"mkb"}, keys.PATH_KEY: "MKB.txt"},
        {
            keys.INC_TAGS_KEY: {"mkb"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.PATH_KEY: "MKB_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.REQ_DUPES: True,
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
            keys.REQ_TRIMMED_PERKS: True,
            keys.PATH_KEY: "MKB_!Backups_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.REQ_DUPES: True,
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
            keys.REQ_DUPES: True,
            keys.PATH_KEY: "MKB_PvE_!Backups_Dupes.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb", "pve"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.PATH_KEY: "MKB_PvE_!Backups_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"mkb", "pve"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.REQ_DUPES: True,
            keys.PATH_KEY: "MKB_PvE_!Backups_Perks_Dupes.txt",
        },
        # Mouse and Keyboard, PvP
        {keys.INC_TAGS_KEY: {"mkb", "pvp"}, keys.PATH_KEY: "MKB_PvP.txt"},
        {
            keys.INC_TAGS_KEY: {"mkb", "pvp"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.REQ_DUPES: True,
            keys.PATH_KEY: "MKB_PvP_!Backups_Dupes.txt",
        },
        # -------------------------------------------
        # Controller
        {keys.INC_TAGS_KEY: {"ctr"}, keys.PATH_KEY: "CTR.txt"},
        {
            keys.INC_TAGS_KEY: {"ctr"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.PATH_KEY: "CTR_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"ctr"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.REQ_DUPES: True,
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
            keys.REQ_TRIMMED_PERKS: True,
            keys.PATH_KEY: "CTR_!Backups_Perks.txt",
        },
        {
            keys.INC_TAGS_KEY: {"ctr"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.REQ_DUPES: True,
            keys.PATH_KEY: "CTR_!Backups_Perks_Dupes.txt",
        },
        # Controller, PvE
        {keys.INC_TAGS_KEY: {"ctr", "pve"}, keys.PATH_KEY: "CTR_PvE.txt"},
        {
            keys.INC_TAGS_KEY: {"ctr", "pve"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.REQ_DUPES: True,
            keys.PATH_KEY: "CTR_PvE_!Backups_Dupes.txt",
        },
        # Controller, PvP
        {keys.INC_TAGS_KEY: {"ctr", "pvp"}, keys.PATH_KEY: "CTR_PvP.txt"},
        {
            keys.INC_TAGS_KEY: {"ctr", "pvp"},
            keys.EXC_TAGS_KEY: {"backups"},
            keys.REQ_DUPES: True,
            keys.PATH_KEY: "CTR_PvP_!Backups_Dupes.txt",
        },
        # -------------------------------------------
        # Pandapaxxy filters
        {keys.AUTHORS_KEY: {"pandapaxxy"}, keys.PATH_KEY: "PandaPaxxy.txt"},
        {
            keys.AUTHORS_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"mkb"},
            keys.PATH_KEY: "PandaPaxxy_MKB.txt",
        },
        {
            keys.AUTHORS_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"mkb", "pve"},
            keys.PATH_KEY: "PandaPaxxy_MKB_PvE.txt",
        },
        {
            keys.AUTHORS_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"mkb", "pvp"},
            keys.PATH_KEY: "PandaPaxxy_MKB_PvP.txt",
        },
        {
            keys.AUTHORS_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"mkb"},
            keys.REQ_TRIMMED_PERKS: True,
            keys.PATH_KEY: "PandaPaxxy_MKB_Perks.txt",
        },
        {
            keys.AUTHORS_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"ctr"},
            keys.PATH_KEY: "PandaPaxxy_CTR.txt",
        },
        {
            keys.AUTHORS_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"ctr", "pve"},
            keys.PATH_KEY: "PandaPaxxy_CTR_PvE.txt",
        },
        {
            keys.AUTHORS_KEY: {"pandapaxxy"},
            keys.INC_TAGS_KEY: {"ctr", "pvp"},
            keys.PATH_KEY: "PandaPaxxy_CTR_PvP.txt",
        },
    ]

    # Paths for all wishlist files, referenced by website
    wishlist_paths = []

    # Collect options used in configs
    author_names = set()
    inc_tags = set()
    exc_tags = set()

    for wishlist in wishlist_configs:
        # Update wishlist names
        wishlist_path = keys.WISHLIST_DIR + wishlist[keys.PATH_KEY]
        wishlist[keys.PATH_KEY] = wishlist_path  # Add path to wishlist name
        wishlist_paths.append(wishlist_path)  # Add full path to array for website

        # Update abreviated wishlist tags
        if keys.INC_TAGS_KEY in wishlist:
            # Update tags
            if "ctr" in wishlist[keys.INC_TAGS_KEY]:
                wishlist[keys.INC_TAGS_KEY].remove("ctr")
                wishlist[keys.INC_TAGS_KEY].update({"controller"})

            inc_tags.update(wishlist[keys.INC_TAGS_KEY])  # Add to all inc tags

        if keys.EXC_TAGS_KEY in wishlist:
            # Update tags
            if "backups" in wishlist[keys.EXC_TAGS_KEY]:
                wishlist[keys.EXC_TAGS_KEY].remove("backups")
                wishlist[keys.EXC_TAGS_KEY].update(
                    {"backup roll", "backup choice roll"}
                )

            exc_tags.update(wishlist[keys.EXC_TAGS_KEY])  # Add to all exc tags

        # Add wishlist preferences to set with all preferences
        if keys.AUTHORS_KEY in wishlist:
            author_names.update(wishlist[keys.AUTHORS_KEY])

    # Write wishlist paths to file for website
    with open(keys.WISHLIST_NAMES_PATH, "w") as file:
        json.dump(wishlist_paths, file)

    return {
        keys.WISHLIST_CONFIGS_KEY: wishlist_configs,
        keys.AUTHORS_KEY: author_names,
        keys.INC_TAGS_KEY: inc_tags,
        keys.EXC_TAGS_KEY: exc_tags,
    }
