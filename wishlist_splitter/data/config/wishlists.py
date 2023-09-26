# wishlist_configs.py


def get_wishlist_config(
    PATH_KEY, AUTHOR_KEY, INC_TAG_KEY, EXC_TAG_KEY, PERK_KEY, DUPE_PERKS_KEY
):
    # Array of Wishlists
    # Each Wishlist is a Dictionary with
    #   Flag - True / False for Filter Options
    #   Include / Exclude Filter - Using AND logic: PVE, PVP, MKB, Controller, Backup Roll, God, etc.
    #   Logic - ["A", "B"] = A and B, ["A B"] = A or B
    #   Perk Columns - "" or "1, 2, 3, 4" for All or "3, 4" for 3rd and 4th, etc.
    #   Grouping Options - Combines Recommendations per Weapon ex. 0 for all combines or 2 for at least 2 recommendations
    #   Destination Path - Location and Name for Wishlist
    wishlist_configs = [
        # No Filters
        {PATH_KEY: "wishlists/all.txt"},
        # -------------------------------------------
        # gamemode filters
        {INC_TAG_KEY: ["pve"], PATH_KEY: "wishlists/pve.txt"},
        {INC_TAG_KEY: ["pvp"], PATH_KEY: "wishlists/pvp.txt"},
        # -------------------------------------------
        # input filters
        {INC_TAG_KEY: ["mkb"], PATH_KEY: "wishlists/mkb.txt"},
        {INC_TAG_KEY: ["controller"], PATH_KEY: "wishlists/ctr.txt"},
        # -------------------------------------------
        # input filters | 3rd and 4th columns
        {INC_TAG_KEY: ["mkb"], PERK_KEY: True, PATH_KEY: "wishlists/mkb_perks.txt"},
        {
            INC_TAG_KEY: ["controller"],
            PERK_KEY: True,
            PATH_KEY: "wishlists/ctr_perks.txt",
        },
        # -------------------------------------------
        # input filters | 3rd and 4th columns | at least 2 dupes
        {
            INC_TAG_KEY: ["mkb"],
            PERK_KEY: True,
            DUPE_PERKS_KEY: True,
            PATH_KEY: "wishlists/mkb_perks_dupes.txt",
        },
        {
            INC_TAG_KEY: ["controller"],
            PERK_KEY: True,
            DUPE_PERKS_KEY: True,
            PATH_KEY: "wishlists/ctr_perks_dupes.txt",
        },
        # -------------------------------------------
        # input_gamdemode filters
        {INC_TAG_KEY: ["mkb", "pve"], PATH_KEY: "wishlists/mkb_pve.txt"},
        {INC_TAG_KEY: ["mkb", "pvp"], PATH_KEY: "wishlists/mkb_pvp.txt"},
        {INC_TAG_KEY: ["controller", "pve"], PATH_KEY: "wishlists/ctr_pve.txt"},
        {INC_TAG_KEY: ["controller", "pvp"], PATH_KEY: "wishlists/ctr_pvp.txt"},
        # -------------------------------------------
        # pandapaxxy filters
        {AUTHOR_KEY: ["pandapaxxy"], PATH_KEY: "wishlists/panda.txt"},
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["mkb"],
            PATH_KEY: "wishlists/mkb_panda.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["mkb", "pve"],
            PATH_KEY: "wishlists/mkb_panda_pve.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["mkb", "pvp"],
            PATH_KEY: "wishlists/mkb_panda_pvp.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["controller"],
            PATH_KEY: "wishlists/ctr_panda.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["controller", "pve"],
            PATH_KEY: "wishlists/ctr_panda_pve.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["controller", "pvp"],
            PATH_KEY: "wishlists/ctr_panda_pvp.txt",
        },
        {
            AUTHOR_KEY: ["pandapaxxy"],
            INC_TAG_KEY: ["mkb"],
            PERK_KEY: True,
            PATH_KEY: "wishlists/mkb_panda_perks.txt",
        },
        # -------------------------------------------
        # god filters
        {INC_TAG_KEY: ["mkb", "god"], PATH_KEY: "wishlists/mkb_god.txt"},
        # -------------------------------------------
        # exclude backup rolls - input filters
        {
            INC_TAG_KEY: ["mkb"],
            EXC_TAG_KEY: ["backup"],
            PATH_KEY: "wishlists/mkb_!backup.txt",
        },
        {
            INC_TAG_KEY: ["mkb"],
            EXC_TAG_KEY: ["backup"],
            PERK_KEY: True,
            PATH_KEY: "wishlists/mkb_!backup_perks.txt",
        },
        {
            INC_TAG_KEY: ["mkb"],
            EXC_TAG_KEY: ["backup"],
            PERK_KEY: True,
            DUPE_PERKS_KEY: True,
            PATH_KEY: "wishlists/mkb_!backup_perks_dupes.txt",
        },
    ]

    # Iterate through the list of dictionaries
    for wishlist in wishlist_configs:
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
