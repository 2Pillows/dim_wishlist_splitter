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
    # Determine what perks wishlist wants, avoid repeated calcs
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
# Returns keys for perks and core perks as well as the counter for perks
# If wishlist doesn't want dupes, no core perks or counter is returned
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
        contains_author_names(
            weapon_roll.get(keys.AUTHORS_KEY), wishlist.get(keys.AUTHORS_KEY)
        )
        and contains_inc_tags(
            weapon_roll.get(keys.INC_TAGS_KEY), wishlist.get(keys.INC_TAGS_KEY)
        )
        and not contains_exc_tags(
            weapon_roll.get(keys.EXC_TAGS_KEY), wishlist.get(keys.EXC_TAGS_KEY)
        )
    )


def contains_author_names(weapon_authors: Set[str], wishlist_authors: Set[str]):
    # If wishlist doesn't specify author then all rolls pass
    if not wishlist_authors:
        return True

    # If weapon doesn't have author then fails
    if not weapon_authors:
        return False

    # Author for wishlist and weapon need to share an author
    return wishlist_authors.intersection(weapon_authors)


def contains_inc_tags(weapon_inc: Set[str], wishlist_inc: Set[str]):
    # If wishlist doesn't have inc tags, then passes
    if not wishlist_inc:
        return True

    # If roll doesn't have any include tags but wishlist does, it doesn't pass
    if not weapon_inc:
        return False

    # Return if all include tags in wishlist are in roll include tags
    # the tags needed for the wishlist need to be subset of tags for roll
    return wishlist_inc.issubset(weapon_inc)


def contains_exc_tags(weapon_exc, wishlist_exc: Set[str]):
    # If wishlist doesn't have any exlcude tags then roll can't have any exclude tags
    # Or if roll doesn't have any exclude tags then it passes
    if not wishlist_exc or not weapon_exc:
        return False

    # Return if any wishlist exclude tag is in roll exlude tags
    return wishlist_exc.intersection(weapon_exc)
