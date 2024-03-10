# write_to_wishlists.py

from collections import Counter

# Import for type hints and intellisense
from typing import TYPE_CHECKING, List, Dict, IO

if TYPE_CHECKING:
    from main import Keys


######################################
# Write voltron_data to config files #
######################################
def write_to_wishlists(voltron_data: List[Dict[str, object]], keys: "Keys"):
    # Process extra, base, and filtered perks
    process_data(voltron_data, keys)

    # Collect perks into Counters
    base_counter, filtered_counter = count_perks(voltron_data, keys)

    # Write each data to each wishlist
    for config in keys.WISHLIST_CONFIGS:
        write_data_to_config(voltron_data, config, keys, base_counter, filtered_counter)


###########################################
# Process extra, base, and filtered perks #
###########################################
def process_data(voltron_data: List[Dict[str, object]], keys: "Keys"):
    # Maximum number of possible base perks
    MAX_BASE_PERKS = 4
    # Number of perks that should be included from right to left
    DESIRED_PERK_COUNT = 2

    # Adds mouse and pve tag if no input or gamemode tag present
    add_default_tags(voltron_data, keys)

    # Set extra perk values for each roll
    # Assumes that if one extra perk is found in a hash set, all hashes have extra perk
    process_extra_perks(voltron_data, keys, MAX_BASE_PERKS)

    # Set base and filtered perks for each roll
    process_perks(voltron_data, keys, DESIRED_PERK_COUNT)


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


# Set extra perk values for each roll
def process_extra_perks(
    voltron_data: List[Dict[str, object]], keys: "Keys", MAX_BASE_PERKS: int
):
    # Check if any roll has an extra perk
    for roll in voltron_data:
        perk_hashes, perk_ids = get_perk_list(roll, keys)

        # Assume there are no extra perks in roll
        roll[keys.EXTRA_PERK_KEY] = False

        # Edge case of no hashes
        if not perk_hashes:
            continue

        # Check if any perk is in extra_perks in voltron
        # or origin_traits from https://data.destinysets.com
        for hash_list in perk_hashes:
            # for each line of hashes check if last hash is an origin trait
            if hash_list[-1] in keys.ORIGIN_TRAITS:
                roll[keys.EXTRA_PERK_KEY] = True


# Transform perks in roll from a string to an array of hashes and the string before hashes
def get_perk_list(roll: Dict[str, object], keys: "Keys"):
    PERK_IND = "&perks="
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


# Create and store base and filtered perk strings
def process_perks(
    voltron_data: List[Dict[str, object]], keys: "Keys", DESIRED_PERK_COUNT: int
):
    for roll in voltron_data:
        perk_hashes, roll_id = get_perk_list(roll, keys)
        # Hashes with no modifications
        base_hashes = perk_hashes.copy()
        # Hashes with only 3rd, 4th, and extra perks
        filtered_hashes = perk_hashes.copy()
        # Hashes with only 3rd, and 4th perks
        base_filtered_hashes = perk_hashes.copy()

        for index in range(len(perk_hashes)):
            extra_perk = ""
            if roll.get(keys.EXTRA_PERK_KEY):
                extra_perk = base_hashes[index].pop()
                # filtered_hashes[index].pop()
                # base_filtered_hashes[index].pop()
            if len(perk_hashes[index]) > DESIRED_PERK_COUNT:
                filtered_hashes[index] = filtered_hashes[index][-DESIRED_PERK_COUNT:]
                base_filtered_hashes[index] = filtered_hashes[index][
                    -DESIRED_PERK_COUNT:
                ]
            if extra_perk:
                filtered_hashes[index].append(extra_perk)

        base_perks = convert_hash_to_string(base_hashes, roll_id)
        filtereded_perks = convert_hash_to_string(filtered_hashes, roll_id)
        base_filtered_hashes = convert_hash_to_string(base_filtered_hashes, roll_id)

        roll[keys.BASE_PERK_KEY] = base_perks
        roll[keys.FILTERED_PERK_KEY] = filtereded_perks
        roll[keys.BASE_FILTERED_PERK_KEY] = base_filtered_hashes


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
    base_counter = Counter()
    filtered_counter = Counter()

    for roll in voltron_data:
        base_counter.update(set(roll[keys.BASE_PERK_KEY]))
        filtered_counter.update(set(roll[keys.FILTERED_PERK_KEY]))

    return base_counter, filtered_counter


################################
# Writes data to each wishlist #
################################
def write_data_to_config(
    voltron_data: List[Dict[str, object]],
    config: List[Dict[str, object]],
    keys: "Keys",
    base_counter: Counter,
    filtered_counter: Counter,
):
    batch_size = 100
    config_path = config.get(keys.PATH_KEY)

    # Can clean b4 and use mode="a"
    with open(config_path, mode="w", encoding="utf-8") as config_file:
        batch = []

        for roll in voltron_data:
            # Always write roll if it is a credit roll
            if contains_credits(roll, keys):
                batch.append(roll)

            # Check if roll tags match config tags
            elif check_tags(roll, config, keys):
                # Find correct perks for config
                config_roll = find_config_roll(
                    roll, config, keys, base_counter, filtered_counter
                )
                batch.append(config_roll)
                # print("a")

            if len(batch) >= batch_size:
                write_batch_to_config(config_file, batch, keys)
                batch = []

        if batch:
            write_batch_to_config(config_file, batch, keys)


def find_config_roll(
    roll: Dict[str, object],
    config: Dict[str, object],
    keys: "Keys",
    base_counter: Counter,
    filtered_counter: Counter,
):
    config_roll = roll.copy()
    config_perks = roll.get(keys.PERK_KEY).copy()
    # Base perks is perks without extra perks
    # Filtered perks is only 3rd and 4th column perks and extras
    # Base filtered is 3rd and 4th column perks without extra perks
    if config.get(keys.PERK_KEY):
        if config.get(keys.DUPE_PERKS_KEY):
            # Config wants 3rd and 4th column perks in at least 2 rolls
            config_perks = get_dupe_perks(
                roll.get(keys.BASE_FILTERED_PERK_KEY),
                roll.get(keys.FILTERED_PERK_KEY),
                keys,
                filtered_counter,
            )
        else:
            # Config wants 3rd and 4th column perks
            config_perks = roll.get(keys.FILTERED_PERK_KEY).copy()

    elif config.get(keys.DUPE_PERKS_KEY):
        # Config wants rolls in at least 2 rolls
        config_perks = get_dupe_perks(
            roll.get(keys.BASE_PERK_KEY),
            roll.get(keys.PERK_KEY),
            keys,
            base_counter,
        )

    config_roll[keys.PERK_KEY] = config_perks
    return config_roll


def get_dupe_perks(
    base_perks: List[str], all_perks: List[str], keys: "Keys", counter: Counter
):
    MIN_COUNT = 2

    # Use base_perks to only get perks with proper count
    # Add and return all_perk values to keep extra perks if included in roll
    dupe = []

    for index in range(len(base_perks)):
        base = base_perks[index]
        all = all_perks[index]

        c = counter[base]
        if counter[base] >= MIN_COUNT:
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
