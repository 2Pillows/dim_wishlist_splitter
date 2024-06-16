# write_to_wishlists.py

import concurrent.futures
from typing import TYPE_CHECKING, Dict, Set

# Load Keys class without importing to avoid cyclic import
if TYPE_CHECKING:
    from main import Keys


# Main function called from main.py
def write_to_wishlists(keys: "Keys"):
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
):
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
            elif weapon_roll.get(PREF_PERKS) and check_tags(
                weapon_roll, wishlist, keys
            ):
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
def get_wishlist_perk_prefs(wishlist: Dict[str, object], keys: "Keys"):
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
):

    return (
        # Must contain authors and inc tags
        must_contain_check(
            weapon_roll.get(keys.AUTHORS_KEY), wishlist.get(keys.AUTHORS_KEY)
        )
        and must_contain_check(
            weapon_roll.get(keys.INC_TAGS_KEY), wishlist.get(keys.INC_TAGS_KEY)
        )
        # Cant contain exc tags
        and not cannot_contain_check(
            weapon_roll.get(keys.EXC_TAGS_KEY), wishlist.get(keys.EXC_TAGS_KEY)
        )
    )


# Weapon must contain wishlist pref
def must_contain_check(weapon_prefs: Set[str], wishlist_prefs: Set[str]):
    # If wishlist doesn't have pref, then pass
    if not wishlist_prefs:
        return True

    # If weapon doesn't have pref, then fails
    if not weapon_prefs:
        return False

    # Wishlist must be subset of weapon
    return wishlist_prefs.issubset(weapon_prefs)


# Weapon cannot contain weapon check
def cannot_contain_check(weapon_pref: Set[str], wishlist_pref: Set[str]):
    # If either wishlist or weapon don't have pref, then can't contain
    if not wishlist_pref or not weapon_pref:
        return False

    # Check if wistlist and weapon share any in common
    return wishlist_pref.intersection(weapon_pref)
