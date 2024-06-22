# write_to_wishlists.py

import concurrent.futures
from typing import Dict, Set

# Import keys
from helper_scripts.keys import Keys


# Main function called from main.py
def write_to_wishlists(keys: "Keys") -> None:
    # Non threaded option
    # for wishlist in keys.WISHLIST_CONFIGS:
    #     write_to_wishlist(wishlist, keys)

    # Write to each wishlist in a thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(write_to_wishlist, wishlist, keys)
            for wishlist in keys.WISHLIST_CONFIGS
        ]
        concurrent.futures.wait(futures)


# Writes data to given wishlist file
def write_to_wishlist(
    wishlist: Dict[str, object],
    keys: "Keys",
) -> None:
    # Determine what perks wishlist wants
    PREF_PERKS = get_wishlist_perk_prefs(wishlist, keys)

    with open(wishlist[keys.PATH_KEY], mode="w", encoding="utf-8") as wishlist_file:
        # Write file name to start of file
        wishlist_file.write(
            "title:"
            + wishlist[keys.PATH_KEY]
            .replace("./wishlists/", "")
            .replace(".txt", "")
            .replace("_", " ")
            + " - "
        )

        # Batch to hold keys.BATCH_SIZE number of rolls, will write when full or last loop
        batch = []

        for index, weapon_roll in enumerate(keys.VOLTRON_DATA):

            # Write first line for credits
            if index == 0:
                batch.extend(weapon_roll[keys.DESCRIPTION_KEY])
                batch.append("\n")

            # Check there are perks to write and roll tags match wishlist tags
            elif check_tags(weapon_roll, wishlist, keys):

                # Weapon roll doesn't have any perks to show, give empty perks
                if not weapon_roll.get(PREF_PERKS):
                    batch.extend("//notes: No rolls passed dupe filtering\n")
                    batch.extend(f"{weapon_roll['roll_id']}1,1,1,1\n")
                else:
                    # Add description and correct perks to batch
                    batch.extend(weapon_roll[keys.DESCRIPTION_KEY])
                    batch.extend(weapon_roll[PREF_PERKS])

                batch.append("\n")

            # Write to file if batch size reached
            if len(batch) >= keys.BATCH_SIZE:
                wishlist_file.write("".join(batch))
                batch = []

        # Empty batch if any leftover
        if batch:
            wishlist_file.write("".join(batch))


# Determine what perks the given wishlist wants
# Returns key for weapon roll's perks that wishlist wants
def get_wishlist_perk_prefs(wishlist: Dict[str, object], keys: "Keys") -> str:
    if wishlist.get(keys.REQ_TRIMMED_PERKS):
        if wishlist.get(keys.REQ_DUPES):
            # wishlist wants trimmed perks and dupes
            return keys.TRIMMED_PERKS_DUPES_KEY
        else:
            # wishlist wants trimmed perks
            return keys.TRIMMED_PERKS_KEY
    elif wishlist.get(keys.REQ_DUPES):
        # Wishlist wants dupes
        return keys.PERKS_DUPES_KEY

    # Wishlist wants all perks
    return keys.PERKS_KEY


# Checks author, inc, and exc tags to see if given roll is meets conditions
def check_tags(
    weapon_roll: Dict[str, object], wishlist: Dict[str, object], keys: "Keys"
) -> bool:

    return (
        # Must contain an author in authors
        contains_authors(
            weapon_roll.get(keys.AUTHORS_KEY), wishlist.get(keys.AUTHORS_KEY)
        )
        # Must contain all inc tags
        and contains_inc_tags(
            weapon_roll.get(keys.INC_TAGS_KEY), wishlist.get(keys.INC_TAGS_KEY)
        )
        # Cant contain exc tags
        and not contains_exc_tags(
            weapon_roll.get(keys.EXC_TAGS_KEY), wishlist.get(keys.EXC_TAGS_KEY)
        )
    )


# Weapon must contain an author in wishlist
def contains_authors(weapon_authors: Set[str], wishlist_authors: Set[str]) -> bool:
    # If wishlist doesn't have authors, then pass
    if not wishlist_authors:
        return True

    # If weapon doesn't have authors, then fails
    if not weapon_authors:
        return False

    # Weapon needs a single matching author
    return wishlist_authors.intersection(weapon_authors)


# Weapon must contain wishlist pref
def contains_inc_tags(weapon_tags: Set[str], wishlist_tags: Set[str]) -> bool:
    # If wishlist doesn't have inc tags, then pass
    if not wishlist_tags:
        return True

    # If weapon doesn't have inc tags, then fails
    if not weapon_tags:
        return False

    # Wishlist inc tags must be subset of weapon inc tags
    return wishlist_tags.issubset(weapon_tags)


# Weapon cannot contain weapon check
def contains_exc_tags(weapon_tags: Set[str], wishlist_tags: Set[str]) -> bool:
    # If either wishlist or weapon don't have exc tags, then can't contain
    if not wishlist_tags or not weapon_tags:
        return False

    # Check if wistlist and weapon share any in common exc tags
    return wishlist_tags.intersection(weapon_tags)
