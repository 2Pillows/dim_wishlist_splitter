# write_to_wishlists.py

import concurrent.futures
from collections import Counter
from typing import TYPE_CHECKING, List, Dict, Set

# Load Keys class without importing to avoid cyclic import
if TYPE_CHECKING:
    from main import Keys


# Main function called from main.py
def write_to_wishlists(keys: "Keys"):
    # Reads voltron data to add default tags, process perks, and collect counter data
    process_weapon_rolls(keys)

    # Write voltron data to wishlists
    process_wishlists(keys)


# Creates threads to write data to each wishlist
def process_wishlists(keys: "Keys"):

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


# Add tags, process perks, and count perks for each roll in Voltron
def process_weapon_rolls(keys: "Keys"):
    for weapon_roll in keys.VOLTRON_DATA:
        # Adds mouse and pve tag if no input or gamemode tag present
        add_default_tags(weapon_roll, keys)

        # Get core and trimmed perks
        # core is 1st, 2nd, 3rd, 4th column. Used for accurate counting
        # Trimmed doesn't have 1st and 2nd column. Gets core version for counting as well
        process_perks(weapon_roll, keys)

        # Collect weapon and perks Counters
        get_weapon_and_perk_counters(weapon_roll, keys)


# Adds mouse and pve tag if no input or gamemode tag present
def add_default_tags(weapon_roll, keys: "Keys"):
    if not weapon_roll[keys.INC_TAGS_KEY].intersection({"mkb", "controller"}):
        weapon_roll[keys.INC_TAGS_KEY].add("mkb")
    if not weapon_roll[keys.INC_TAGS_KEY].intersection({"pve", "pvp"}):
        weapon_roll[keys.INC_TAGS_KEY].add("pve")


# Create and stores core and trimmed perk strings
def process_perks(weapon_roll, keys: "Keys"):
    # Transform perks into an array of hashes and the string before hashes
    def get_perk_list(roll: Dict[str, object], keys: "Keys"):
        perk_hashes = []  # Holds arrays of perk hashes
        roll_id = ""  # Holds initial string before perk hashes

        for perk_str in roll[keys.PERKS_KEY]:
            PERK_IND = "&perks="
            PERK_START = perk_str.find(PERK_IND)
            if PERK_START != -1:
                PERK_START += len(PERK_IND)
                PERKS_END = perk_str.find("\n", PERK_START)
                perks_substring = perk_str[PERK_START:PERKS_END]

                # Handle edge case for perks#perk_descriptions
                extended_found = perks_substring.find("#")
                if extended_found != -1:
                    perks_substring = perks_substring[:extended_found]

                # Sorted required to ensure consistent comparing for counters
                perk_hashes.append(sorted(perks_substring.split(",")))

                # Get roll_id if not already set
                if not roll_id:
                    roll_id = perk_str[:PERK_START]

        return roll_id, perk_hashes

    # Convert roll id and array of hashes to a line
    def convert_hash_to_string(hashes: Set[str], roll_id: str):
        converted_hashes = []
        for hash_set in hashes:
            converted_hashes.append(roll_id + ",".join(hash_set) + "\n")

        # Need to sort to avoid incorrect update notices
        return sorted(converted_hashes)

    roll_id, perk_hashes = get_perk_list(weapon_roll, keys)

    core_hash_set = set()  # 1st, 2nd, 3rd, 4th column
    trimmed_hash_set = set()  # Hashes without 1st and 2nd
    core_trimmed_hash_set = set()  # Hashes with only 3rd and 4th column

    # Collects core, trimmed, and core_trimmed hashes by referencing frame and origin hashes
    for hashes in perk_hashes:
        core_hashes = []
        trimmed_hashes = []
        core_trimmed_hashes = []

        for hash_value in hashes:
            if hash_value in keys.FRAME_MODS or hash_value in keys.ORIGIN_TRAITS:
                if hash_value not in keys.ORIGIN_TRAITS:
                    core_trimmed_hashes.append(hash_value)
                trimmed_hashes.append(hash_value)

            if hash_value not in keys.ORIGIN_TRAITS:
                core_hashes.append(hash_value)

        # Add hashes to sets to avoid duplicates
        core_hash_set.add(tuple(core_hashes))
        trimmed_hash_set.add(tuple(trimmed_hashes))
        core_trimmed_hash_set.add(tuple(core_trimmed_hashes))

    # Convert hashes to strings and save to current weapon roll
    weapon_roll[keys.CORE_PERKS_KEY] = convert_hash_to_string(core_hash_set, roll_id)
    weapon_roll[keys.TRIMMED_PERKS_KEY] = convert_hash_to_string(
        trimmed_hash_set, roll_id
    )
    weapon_roll[keys.CORE_TRIMMED_PERKS_KEY] = convert_hash_to_string(
        core_trimmed_hash_set, roll_id
    )


# Creates Counter to track number of mentions for each set of perk and weapon hashes
def get_weapon_and_perk_counters(weapon_roll, keys: "Keys"):
    # If roll has no perks, continue
    if len(weapon_roll[keys.PERKS_KEY]) < 1:
        return

    # Update counter for each rolls hashes. Only one set of hashes per roll will count
    keys.CORE_COUNTER.update(weapon_roll[keys.CORE_PERKS_KEY])
    keys.TRIMMED_COUNTER.update(weapon_roll[keys.TRIMMED_PERKS_KEY])
    keys.WEAPON_COUNTER.update([get_weapon_hash(weapon_roll[keys.PERKS_KEY][0])])


# Takes a perk line string and returns the weapon hash
def get_weapon_hash(perk_line: str):
    return perk_line.split("item=")[1].split("&perks=")[0]


# Writes data to given wishlist file
def write_to_wishlist(
    wishlist,
    keys: "Keys",
):
    # Determine what perks wishlist wants, avoid repeated calcs
    wishlist_perk_prefs = get_wishlist_perk_prefs(wishlist, keys)

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

        for weapon_roll in keys.VOLTRON_DATA:
            # Always write roll if it is a credit roll
            if contains_credits(weapon_roll, keys):
                # Only add description for credits
                batch.extend(weapon_roll[keys.DESCRIPTION_KEY])
                batch.append("\n")

            # Check if roll tags match wishlist tags
            elif check_tags(weapon_roll, wishlist, keys):
                # Add description and correct perks to batch
                batch.extend(weapon_roll[keys.DESCRIPTION_KEY])
                batch.extend(get_weapon_perks(weapon_roll, wishlist_perk_prefs, keys))
                batch.append("\n")

            # Write to file if batch size reached
            if len(batch) >= keys.BATCH_SIZE:
                wishlist_file.write("".join(batch))
                batch = []

        # Empty batch if any leftover
        if batch:
            wishlist_file.write("".join(batch))


def get_wishlist_perk_prefs(wishlist, keys: "Keys"):
    if wishlist.get(keys.REQ_TRIMMED_PERKS):
        if wishlist.get(keys.REQ_DUPES):
            # wishlist wants perks and dupes
            return {
                keys.PERKS_KEY: keys.TRIMMED_PERKS_KEY,
                keys.CORE_PERKS_KEY: keys.CORE_TRIMMED_PERKS_KEY,
                keys.PERK_COUNTER_KEY: keys.TRIMMED_COUNTER,
            }
        else:
            # wishlist wants perks
            return {
                keys.PERKS_KEY: keys.TRIMMED_PERKS_KEY,
            }
    elif wishlist.get(keys.REQ_DUPES):
        # Wishlist wants dupes
        return {
            keys.PERKS_KEY: keys.PERKS_KEY,
            keys.CORE_PERKS_KEY: keys.CORE_PERKS_KEY,
            keys.PERK_COUNTER_KEY: keys.CORE_COUNTER,
        }

    return {
        keys.PERKS_KEY: keys.PERKS_KEY,
    }


# Returns perks that are present MIN_COUNT
# If the weapon for the roll isn't present MIN_COUNT, its also included
def get_weapon_perks(
    weapon_roll,
    wishlist_prefs,
    keys: "Keys",
):
    perk_hashes = weapon_roll[wishlist_prefs[keys.PERKS_KEY]]

    # If no core perks are given, return the weapon rolls perks according to the pref perk key
    if not wishlist_prefs.get(keys.CORE_PERKS_KEY):
        return perk_hashes

    valid_perks = []

    core_perk_hashes = weapon_roll[wishlist_prefs[keys.CORE_PERKS_KEY]]
    perk_counter = wishlist_prefs[keys.PERK_COUNTER_KEY]

    # Adds valid perk lines to valid_perks
    for index in range(len(core_perk_hashes)):
        # Perk is valid if present at least MIN_COUNT
        # OR weapon isn't present MIN_COUNT
        if (
            perk_counter[core_perk_hashes[index]] >= keys.MIN_ROLL_COUNT
            or keys.WEAPON_COUNTER[get_weapon_hash(perk_hashes[0])]
            < keys.MIN_ROLL_COUNT
        ):
            valid_perks.append(perk_hashes[index])

    return valid_perks


def check_tags(
    weapon_roll: Dict[str, object], wishlist: Dict[str, object], keys: "Keys"
):
    return (
        contains_author_names(weapon_roll, wishlist, keys)
        and contains_inc_tags(weapon_roll, wishlist, keys)
        and not contains_exc_tags(weapon_roll, wishlist, keys)
    )


def contains_credits(weapon_roll: Dict[str, object], keys: "Keys"):
    # If roll has a credit tag and no perks, it passes
    return weapon_roll.get(keys.CREDIT_KEY) and not weapon_roll.get(keys.PERKS_KEY)


def contains_author_names(
    weapon_roll: Dict[str, object], wishlist: Dict[str, object], keys: "Keys"
):
    # If wishlist doesn't specify author then all rolls pass
    if keys.AUTHORS_KEY not in wishlist:
        return True

    # If weapon doesn't have author then fails
    if not weapon_roll.get(keys.AUTHORS_KEY):
        return False

    # Author for wishlist and weapon need to share an author
    return wishlist[keys.AUTHORS_KEY].intersection(weapon_roll.get(keys.AUTHORS_KEY))


def contains_inc_tags(
    weapon_roll: Dict[str, object], wishlist: Dict[str, object], keys: "Keys"
):
    # If wishlist doesn't have inc tags, then passes
    if keys.INC_TAGS_KEY not in wishlist:
        return True

    # If roll doesn't have any include tags but wishlist does, it doesn't pass
    if not weapon_roll.get(keys.INC_TAGS_KEY):
        return False

    # Return if all include tags in wishlist are in roll include tags
    # the tags needed for the wishlist need to be subset of tags for roll
    return wishlist.get(keys.INC_TAGS_KEY).issubset(weapon_roll.get(keys.INC_TAGS_KEY))


def contains_exc_tags(
    weapon_roll: Dict[str, object], wishlist: Dict[str, object], keys: "Keys"
):
    # If wishlist doesn't have any exlcude tags then roll can't have any exclude tags
    # Or if roll doesn't have any exclude tags then it passes
    if keys.EXC_TAGS_KEY not in wishlist or not weapon_roll.get(keys.EXC_TAGS_KEY):
        return False

    # Return if any wishlist exclude tag is in roll exlude tags
    return wishlist.get(keys.EXC_TAGS_KEY).intersection(
        weapon_roll.get(keys.EXC_TAGS_KEY)
    )
