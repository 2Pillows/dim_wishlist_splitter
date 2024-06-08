# write_to_wishlists.py

from collections import Counter

# Import for type hints and intellisense
from typing import TYPE_CHECKING, List, Dict, IO

if TYPE_CHECKING:
    from main import Keys


########################################
# Write voltron_data to wishlist files #
########################################
def write_to_wishlists(voltron_data: List[Dict[str, object]], keys: "Keys"):
    # Adds mouse and pve tag if no input or gamemode tag present
    add_default_tags(voltron_data, keys)

    # Get core and trimmed perks
    # core is 1st, 2nd, 3rd, 4th column. Used for accurate counting
    # Trimmed doesn't have 1st and 2nd column. Gets core version for counting as well
    process_perks(voltron_data, keys)

    # Collect perks into Counters
    core_counter, trimmed_counter = count_perks(voltron_data, keys)

    # Write each data to each wishlist
    for config in keys.WISHLIST_CONFIGS:
        write_data_to_config(voltron_data, config, keys, core_counter, trimmed_counter)


# Adds mouse and pve tag if no input or gamemode tag present
def add_default_tags(voltron_data: List[Dict[str, object]], keys: "Keys"):
    for roll in voltron_data:
        default_input = "mkb"
        default_mode = "pve"
        input_options = ["mkb", "controller"]
        mode_options = ["pve", "pvp"]

        if not any(tag in roll[keys.INC_TAG_KEY] for tag in input_options):
            roll[keys.INC_TAG_KEY].append(default_input)
        if not any(tag in roll[keys.INC_TAG_KEY] for tag in mode_options):
            roll[keys.INC_TAG_KEY].append(default_mode)


# Create and store core and trimmed perk strings
def process_perks(voltron_data: List[Dict[str, object]], keys: "Keys"):
    for roll in voltron_data:
        perk_hashes, roll_id = get_perk_list(roll, keys)
        # 1st, 2nd, 3rd, 4th column
        core_hashes = []
        # Hashes without 1st and 2nd
        trimmed_hashes = []
        # Hashes with only 3rd and 4th column
        core_trimmed_hashes = []

        for hash_set in perk_hashes:
            core_hash_set = []
            trimmed_hash_set = []
            core_trimmed_hash_set = []

            for hash in hash_set:
                if hash in keys.FRAME_MODS or hash in keys.ORIGIN_TRAITS:
                    if hash not in keys.ORIGIN_TRAITS:
                        core_trimmed_hash_set.append(
                            hash
                        )  # Frame mod without origin trait

                    trimmed_hash_set.append(hash)  # Frame mod and origins traits

                if hash not in keys.ORIGIN_TRAITS:
                    core_hash_set.append(hash)  # No origin traits

            # Add hash set to list of hashes
            core_hashes.append(core_hash_set)
            trimmed_hashes.append(trimmed_hash_set)
            core_trimmed_hashes.append(core_trimmed_hash_set)

        roll[keys.CORE_PERKS_KEY] = convert_hash_to_string(core_hashes, roll_id)
        roll[keys.TRIMMED_PERKS_KEY] = convert_hash_to_string(trimmed_hashes, roll_id)
        roll[keys.CORE_TRIMMED_PERKS_KEY] = convert_hash_to_string(
            core_trimmed_hashes, roll_id
        )


# Transform perks in roll from a string to an array of hashes and the string before hashes
def get_perk_list(roll: Dict[str, object], keys: "Keys"):
    # Start of hashes
    PERK_IND = "&perks="
    # Indicator of a new line, fixes lines that have notes after hashes
    END_IND = "#"
    perk_hashes = []
    roll_id = ""
    for perk_str in roll[(keys.PERK_KEY)]:
        PERK_START = perk_str.find(PERK_IND) + len(PERK_IND)
        if PERK_START != -1:
            perks_substring = perk_str[PERK_START:]
            perks_end = perks_substring.find(END_IND)
            if perks_end != -1:
                perks_substring = perks_substring[:perks_end]

            perk_hashes.append(perks_substring.split(","))
            roll_id = perk_str[:PERK_START]
    return perk_hashes, roll_id


# Convert roll id and array of hashes to a line
def convert_hash_to_string(hashes: List[str], roll_id: str):
    roll_perks = []
    for hash_list in hashes:
        perk_str = roll_id + ",".join(str(hash) for hash in hash_list)
        roll_perks.append(perk_str)
    return roll_perks


###########################################################################
# Creates Counter to track number of mentions for each set of perk hashes #
###########################################################################
def count_perks(voltron_data: List[Dict[str, object]], keys: "Keys"):
    core_counter = Counter()
    trimmed_counter = Counter()

    # Update counter for each rolls hashes. Only one set of hashes per roll will count
    for roll in voltron_data:
        core_counter.update(set(roll.get(keys.CORE_PERKS_KEY, [])))
        trimmed_counter.update(set(roll.get(keys.TRIMMED_PERKS_KEY, [])))

    return core_counter, trimmed_counter


####################################
# Writes data to given config file #
####################################
def write_data_to_config(
    voltron_data: List[Dict[str, object]],
    config: List[Dict[str, object]],
    keys: "Keys",
    core_counter: Counter,
    trimmed_counter: Counter,
):
    batch_size = 100
    config_path = config.get(keys.PATH_KEY)

    with open(config_path, mode="w", encoding="utf-8") as config_file:
        # Write file name to start of file
        config_file.write("title:" + get_file_name(config_path) + " - ")

        batch = []

        for roll in voltron_data:
            # Always write roll if it is a credit roll
            if contains_credits(roll, keys):
                batch.append(roll)

            # Check if roll tags match config tags
            elif check_tags(roll, config, keys):
                # Find correct perks for config
                config_roll = find_config_roll(
                    roll, config, keys, core_counter, trimmed_counter
                )
                batch.append(config_roll)

            if len(batch) >= batch_size:
                write_batch_to_config(config_file, batch, keys)
                batch = []

        if batch:
            write_batch_to_config(config_file, batch, keys)


def get_file_name(config_path: str):
    # Get core of file path
    label = config_path.replace("./wishlists/", "").replace(".txt", "")

    # Remove underscores
    label = label.replace("_", " ")

    return label


def find_config_roll(
    roll: Dict[str, object],
    config: Dict[str, object],
    keys: "Keys",
    core_counter: Counter,
    trimmed_counter: Counter,
):
    config_roll = roll.copy()
    config_perks = roll.get(keys.PERK_KEY).copy()
    # Core perks is perks without extra perks
    # Filtered perks is only 3rd and 4th column perks and extras
    # Core filtered is 3rd and 4th column perks without extra perks
    if config.get(keys.PERK_KEY):
        if config.get(keys.DUPE_PERKS_KEY):
            # Config wants 3rd and 4th column perks in at least 2 rolls
            config_perks = get_dupe_perks(
                roll.get(keys.CORE_TRIMMED_PERKS_KEY),
                roll.get(keys.TRIMMED_PERKS_KEY),
                keys,
                trimmed_counter,
            )
        else:
            # Config wants 3rd and 4th column perks
            config_perks = roll.get(keys.TRIMMED_PERKS_KEY).copy()

    elif config.get(keys.DUPE_PERKS_KEY):
        # Config wants rolls in at least 2 rolls
        config_perks = get_dupe_perks(
            roll.get(keys.CORE_PERKS_KEY),
            roll.get(keys.PERK_KEY),
            keys,
            core_counter,
        )

    config_roll[keys.PERK_KEY] = config_perks
    return config_roll


# Doesn't work well if only one roll is given for a weapon
# Counter for the occurances of each weapon?
def get_dupe_perks(
    core_perks: List[str], all_perks: List[str], keys: "Keys", counter: Counter
):
    MIN_COUNT = 2

    # Use core_perks to only get perks with proper count
    # Add and return all_perk values to keep extra perks if included in roll
    dupe = []

    for index in range(len(core_perks)):
        core = core_perks[index]
        all = all_perks[index]

        c = counter[core]
        if counter[core] >= MIN_COUNT:
            dupe.append(all)

    return dupe


def check_tags(roll: Dict[str, object], config: Dict[str, object], keys: "Keys"):
    return (
        contains_author_names(roll, config, keys)
        and contains_inc_tags(roll, config, keys)
        and not contains_exc_tags(roll, config, keys)
    )


def contains_credits(roll: Dict[str, object], keys: "Keys"):
    # If config doesn't have an include tag or if roll has a credit tag and no perks, it passes
    if len(roll.get(keys.CREDIT_TAG, [])) > 0 and not roll.get(keys.PERK_KEY):
        return True


def contains_author_names(
    roll: Dict[str, object], config: Dict[str, object], keys: "Keys"
):
    # If config doesn't specify author then all rolls pass
    if keys.AUTHOR_KEY not in config:
        return True

    # If roll has author and any author is in roll return true
    return keys.AUTHOR_KEY in roll and any(
        author in roll[keys.AUTHOR_KEY] for author in config[keys.AUTHOR_KEY]
    )


def contains_inc_tags(roll: Dict[str, object], config: Dict[str, object], keys: "Keys"):
    # If roll doesn't have any include tags but config does, it doesn't pass
    if keys.INC_TAG_KEY not in roll:
        return False

    # Return if all include tags in config are in roll include tags
    return all(
        tag in roll[keys.INC_TAG_KEY] for tag in config.get(keys.INC_TAG_KEY, [])
    )


def contains_exc_tags(roll: Dict[str, object], config: Dict[str, object], keys: "Keys"):
    # If config doesn't have any exlcude tags then roll can't have any exclude tags
    # Or if roll doesn't have any exclude tags then it passes
    if keys.EXC_TAG_KEY not in config or len(roll.get(keys.EXC_TAG_KEY, [])) == 0:
        return False

    # Return if any config exclude tag is in roll exlude tags
    return any(
        tag in roll.get(keys.EXC_TAG_KEY, []) for tag in config[keys.EXC_TAG_KEY]
    )


def write_batch_to_config(
    config_file: IO[str], batch: List[Dict[str, object]], keys: "Keys"
):
    for current_roll in batch:
        write_to_config(config_file, current_roll[keys.DESCRIPTION_KEY])
        write_to_config(config_file, current_roll[keys.PERK_KEY])
        config_file.write("\n")


def write_to_config(config_file: IO[str], lines: List[str]):
    for line in lines:
        config_file.write(f"{line}\n")
