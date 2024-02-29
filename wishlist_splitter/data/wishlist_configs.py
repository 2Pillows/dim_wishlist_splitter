# wishlist_configs.py


def get_wishlist_config(
    PATH_KEY,
    WISHLIST_DIR,
    AUTHOR_KEY,
    INC_TAG_KEY,
    EXC_TAG_KEY,
    PERK_KEY,
    DUPE_PERKS_KEY,
):
    # Array of Wishlists Configs
    wishlist_configs = [
        # No Filters
        {PATH_KEY: "all.txt"},
        # -------------------------------------------
        # Gamemdoe filters
        {INC_TAG_KEY: ["pve"], PATH_KEY: "pve.txt"},
        {INC_TAG_KEY: ["pvp"], PATH_KEY: "pvp.txt"},
        # -------------------------------------------
        # Input filters
        {INC_TAG_KEY: ["mkb"], PATH_KEY: "mkb.txt"},
        {INC_TAG_KEY: ["controller"], PATH_KEY: "ctr.txt"},
        # -------------------------------------------
        # Perks
        {INC_TAG_KEY: ["mkb"], PERK_KEY: True, PATH_KEY: "mkb_perks.txt"},
        {
            INC_TAG_KEY: ["controller"],
            PERK_KEY: True,
            PATH_KEY: "ctr_perks.txt",
        },
        # -------------------------------------------
        # Perks and Dupes
        {
            INC_TAG_KEY: ["mkb"],
            PERK_KEY: True,
            DUPE_PERKS_KEY: True,
            PATH_KEY: "mkb_perks_dupes.txt",
        },
        {
            INC_TAG_KEY: ["controller"],
            PERK_KEY: True,
            DUPE_PERKS_KEY: True,
            PATH_KEY: "ctr_perks_dupes.txt",
        },
        # -------------------------------------------
        # Input and Gamemode filters
        {INC_TAG_KEY: ["mkb", "pve"], PATH_KEY: "mkb_pve.txt"},
        {INC_TAG_KEY: ["mkb", "pvp"], PATH_KEY: "mkb_pvp.txt"},
        {INC_TAG_KEY: ["controller", "pve"], PATH_KEY: "ctr_pve.txt"},
        {INC_TAG_KEY: ["controller", "pvp"], PATH_KEY: "ctr_pvp.txt"},
        # -------------------------------------------
        # Pandapaxxy filters
        {AUTHOR_KEY: ["pandapaxxy"], PATH_KEY: "panda.txt"},
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["mkb"],
            PATH_KEY: "mkb_panda.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["mkb", "pve"],
            PATH_KEY: "mkb_panda_pve.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["mkb", "pvp"],
            PATH_KEY: "mkb_panda_pvp.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["controller"],
            PATH_KEY: "ctr_panda.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["controller", "pve"],
            PATH_KEY: "ctr_panda_pve.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["controller", "pvp"],
            PATH_KEY: "ctr_panda_pvp.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["mkb"],
            PERK_KEY: True,
            PATH_KEY: "mkb_panda_perks.txt",
        },
        # -------------------------------------------
        # God filters
        {INC_TAG_KEY: ["mkb", "god"], PATH_KEY: "mkb_god.txt"},
        # -------------------------------------------
        # Exclude backup rolls filters
        {
            INC_TAG_KEY: ["mkb"],
            EXC_TAG_KEY: ["backup"],
            PATH_KEY: "mkb_!backup.txt",
        },
        {
            INC_TAG_KEY: ["mkb"],
            EXC_TAG_KEY: ["backup"],
            PERK_KEY: True,
            PATH_KEY: "mkb_!backup_perks.txt",
        },
        {
            INC_TAG_KEY: ["mkb"],
            EXC_TAG_KEY: ["backup"],
            PERK_KEY: True,
            DUPE_PERKS_KEY: True,
            PATH_KEY: "mkb_!backup_perks_dupes.txt",
        },
    ]

    # Iterate through the list of dictionaries
    for wishlist in wishlist_configs:
        wishlist[PATH_KEY] = WISHLIST_DIR + wishlist[PATH_KEY]
        if INC_TAG_KEY in wishlist and wishlist[INC_TAG_KEY] is not None:
            transform_tags(wishlist[INC_TAG_KEY])

        if EXC_TAG_KEY in wishlist and wishlist[EXC_TAG_KEY] is not None:
            transform_tags(wishlist[EXC_TAG_KEY])

    return wishlist_configs


def transform_tags(tag_list):
    # Handle tag transformations
    tag_transformations = {
        "god": {"pve-god", "god-pve", "must have pve", "first-choice roll"},
        "backup": {"backup roll", "backup choice roll"},
    }
    for tag, transformed_tags in tag_transformations.items():
        if tag in tag_list:
            tag_list.remove(tag)
            tag_list.extend(transformed_tags)
