# loop wishlist, then voltron
import concurrent.futures

from collections import Counter

# Import for type hints and intellisense
from typing import TYPE_CHECKING, List, Dict, Set

if TYPE_CHECKING:
    from main import Keys


########################################
# Write voltron_data to wishlist files #
########################################
def write_to_wishlists(keys: "Keys"):
    process_weapon_rolls(keys)

    process_wishlists(keys)


def process_wishlists(keys: "Keys"):

    # Non threaded option
    # for wishlist in keys.WISHLIST_CONFIGS:
    #     write_to_wishlist(wishlist, keys)

    # Run each workflow in a thread
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

        # Collect perks into Counters
        count_perks(weapon_roll, keys)


# Adds mouse and pve tag if no input or gamemode tag present
def add_default_tags(weapon_roll, keys):
    default_input = "mkb"
    default_mode = "pve"
    input_options = {"mkb", "controller"}
    mode_options = {"pve", "pvp"}

    inc_tags = set(weapon_roll[keys.INC_TAG_KEY])

    if not inc_tags.intersection(input_options):
        weapon_roll[keys.INC_TAG_KEY].append(default_input)
    if not inc_tags.intersection(mode_options):
        weapon_roll[keys.INC_TAG_KEY].append(default_mode)


# Create and store core and trimmed perk strings
def process_perks(weapon_roll, keys: "Keys"):
    # Transform perks in roll from a string to an array of hashes and the string before hashes
    def get_perk_list(roll: Dict[str, object], keys: "Keys"):

        roll_perks = roll[keys.PERK_KEY]

        perk_hashes = []
        roll_id = ""

        for perk_str in roll_perks:
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

                perks_list = perks_substring.split(",")
                perks_list.sort()  # sort to ensure accurate comparions
                perk_hashes.append(perks_list)

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

    # Iterate through each hash set in perk_hashes
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

        # Add hashes to sets
        core_hash_set.add(tuple(core_hashes))
        trimmed_hash_set.add(tuple(trimmed_hashes))
        core_trimmed_hash_set.add(tuple(core_trimmed_hashes))

    # Convert hashes to strings
    weapon_roll[keys.CORE_PERKS_KEY] = convert_hash_to_string(core_hash_set, roll_id)
    weapon_roll[keys.TRIMMED_PERKS_KEY] = convert_hash_to_string(
        trimmed_hash_set, roll_id
    )
    weapon_roll[keys.CORE_TRIMMED_PERKS_KEY] = convert_hash_to_string(
        core_trimmed_hash_set, roll_id
    )


# Creates Counter to track number of mentions for each set of perk hashes
def count_perks(weapon_roll, keys: "Keys"):
    # Update counter for each rolls hashes. Only one set of hashes per roll will count
    roll_perks = weapon_roll[keys.PERK_KEY]

    # If roll has no perks, continue
    if len(roll_perks) < 1:
        return

    keys.CORE_COUNTER.update(set(weapon_roll[keys.CORE_PERKS_KEY]))
    keys.TRIMMED_COUNTER.update(set(weapon_roll[keys.TRIMMED_PERKS_KEY]))
    keys.WEAPON_COUNTER.update([get_weapon_hash(roll_perks[0])])


# Takes a perk line string and returns the weapon hash
def get_weapon_hash(perk_line: str):
    return perk_line.split("item=")[1].split("&perks=")[0]


######################################
# Writes data to given wishlist file #
######################################
def write_to_wishlist(
    wishlist,
    keys: "Keys",
):
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
                batch.append(weapon_roll)

            # Check if roll tags match wishlist tags
            elif check_tags(weapon_roll, wishlist, keys):
                # Find correct perks for wishlist and add to batch
                batch.append(find_wishlist_roll(weapon_roll, wishlist, keys))

            if len(batch) >= keys.BATCH_SIZE:
                write_batch_to_wishlist(wishlist_file, batch, keys)
                batch = []

        # Empty batch if any leftover
        if batch:
            write_batch_to_wishlist(wishlist_file, batch, keys)


def find_wishlist_roll(
    weapon_roll: Dict[str, object],
    wishlist: Dict[str, object],
    keys: "Keys",
):
    # Copy weapon roll and perks to avoid changing the source
    wishlist_roll = weapon_roll.copy()
    wishlist_perks = weapon_roll[keys.PERK_KEY].copy()
    # Core perks is perks without extra perks
    # Filtered perks is only 3rd and 4th column perks and extras
    # Core filtered is 3rd and 4th column perks without extra perks
    if wishlist.get(keys.PERK_KEY):
        if wishlist.get(keys.DUPE_PERKS_KEY):
            # wishlist wants 3rd and 4th column perks in at least 2 rolls
            wishlist_perks = get_dupe_perks(
                weapon_roll[keys.CORE_TRIMMED_PERKS_KEY],
                weapon_roll[keys.TRIMMED_PERKS_KEY],
                keys,
                keys.TRIMMED_COUNTER,
            )
        else:
            # wishlist wants 3rd and 4th column perks
            wishlist_perks = weapon_roll[keys.TRIMMED_PERKS_KEY].copy()

    elif wishlist.get(keys.DUPE_PERKS_KEY):
        # wishlist wants rolls in at least 2 rolls
        wishlist_perks = get_dupe_perks(
            weapon_roll[keys.CORE_PERKS_KEY],
            weapon_roll[keys.PERK_KEY],
            keys,
            keys.CORE_COUNTER,
        )

    wishlist_roll[keys.PERK_KEY] = wishlist_perks
    return wishlist_roll


# Returns perks that are present MIN_COUNT
# If the weapon for the roll isn't present MIN_COUNT, its also included
def get_dupe_perks(
    core_perks: List[str],
    full_perks: List[str],
    keys: "Keys",
    perk_counter: Counter,
):
    # Return empty array if no perks given
    if len(full_perks) < 1:
        return []

    weapon_hash = get_weapon_hash(full_perks[0])

    valid_perks = []

    # Adds valid perk lines to valid_perks
    for index in range(len(core_perks)):
        core_line = core_perks[index]
        full_line = full_perks[index]

        # Perk is valid if present at least MIN_COUNT
        # OR weapon isn't present MIN_COUNT
        if (
            perk_counter[core_line] >= keys.MIN_ROLL_COUNT
            or keys.WEAPON_COUNTER[weapon_hash] < keys.MIN_ROLL_COUNT
        ):
            valid_perks.append(full_line)

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
    return weapon_roll.get(keys.CREDIT_TAG) and not weapon_roll.get(keys.PERK_KEY)


def contains_author_names(
    weapon_roll: Dict[str, object], wishlist: Dict[str, object], keys: "Keys"
):
    # If wishlist doesn't specify author then all rolls pass
    if keys.AUTHOR_KEY not in wishlist:
        return True

    # If weapon doesn't have author then fails
    if not weapon_roll.get(keys.AUTHOR_KEY):
        return False

    # Author for wishlist and weapon need to share an author
    return set(wishlist[keys.AUTHOR_KEY]).intersection(
        set(weapon_roll.get(keys.AUTHOR_KEY))
    )


def contains_inc_tags(
    weapon_roll: Dict[str, object], wishlist: Dict[str, object], keys: "Keys"
):
    # If wishlist doesn't have inc tags, then passes
    if keys.INC_TAG_KEY not in wishlist:
        return True

    # If roll doesn't have any include tags but wishlist does, it doesn't pass
    if not weapon_roll.get(keys.INC_TAG_KEY):
        return False

    # Return if all include tags in wishlist are in roll include tags
    # the tags needed for the wishlist need to be subset of tags for roll
    return set(wishlist.get(keys.INC_TAG_KEY)).issubset(
        set(weapon_roll.get(keys.INC_TAG_KEY))
    )


def contains_exc_tags(
    weapon_roll: Dict[str, object], wishlist: Dict[str, object], keys: "Keys"
):
    # If wishlist doesn't have any exlcude tags then roll can't have any exclude tags
    # Or if roll doesn't have any exclude tags then it passes
    if keys.EXC_TAG_KEY not in wishlist or not weapon_roll.get(keys.EXC_TAG_KEY):
        return False

    # Return if any wishlist exclude tag is in roll exlude tags
    return set(wishlist.get(keys.EXC_TAG_KEY)).intersection(
        set(weapon_roll.get(keys.EXC_TAG_KEY))
    )


def write_batch_to_wishlist(wishlist_file, batch, keys: "Keys"):

    file_content = []

    for current_roll in batch:
        # Add roll to file content
        file_content.extend(current_roll[keys.DESCRIPTION_KEY])
        file_content.extend(current_roll[keys.PERK_KEY])
        file_content.append("\n")

    wishlist_file.write("".join(file_content))
