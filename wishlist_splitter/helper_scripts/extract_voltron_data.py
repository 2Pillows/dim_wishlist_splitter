# extract_voltron_data.py

from typing import TYPE_CHECKING, Dict

# Load Keys class without importing to avoid cyclic import
if TYPE_CHECKING:
    from main import Keys


# Read voltron file and collect roll information
def extract_voltron_data(keys: "Keys"):
    # Array for dictionaries for weapon roll in Voltron
    voltron_data = []

    current_roll = initialize_roll(keys)

    with open(keys.VOLTRON_PATH, mode="r", encoding="utf-8") as voltron_file:
        for line_num, line in enumerate(voltron_file):
            # Removed title heading, replaced later with wishlist name
            if line_num == 0:
                line = line.replace("title:", "")

            if line == "\n":  # New line signifies end of current weapon roll
                # Process current roll and add to voltron data
                if line_num == 2 or current_roll.get(keys.PERKS_KEY):
                    if line_num != 2:  # Isn't the haeding
                        add_default_tags(current_roll, keys)
                        get_weapon_and_perk_counters(current_roll, keys)

                    voltron_data.append(current_roll)

                # Start new roll
                current_roll = initialize_roll(keys)
            else:
                # Collect perk information
                if "dimwishlist:item=" in line:
                    if not current_roll.get(keys.ROLL_ID_KEY):
                        current_roll[keys.ROLL_ID_KEY] = line[: line.find("&perks") + 7]

                    # Get core and trimmed perks
                    # core is 1st, 2nd, 3rd, 4th column. Used for accurate counting
                    # Trimmed doesn't have 1st and 2nd column. Gets core version for counting as well
                    perk_hashes = get_perk_hashes(line)
                    perk_line, trimmed_line, core_line, core_trimmed_line = (
                        get_perk_types(
                            current_roll[keys.ROLL_ID_KEY], perk_hashes, keys
                        )
                    )
                    current_roll[keys.PERKS_KEY].append(perk_line)
                    current_roll[keys.TRIMMED_PERKS_KEY].append(trimmed_line)

                    current_roll[keys.CORE_PERKS_KEY].append(core_line)
                    current_roll[keys.CORE_TRIMMED_PERKS_KEY].append(core_trimmed_line)

                # Add description and collect tags and authors
                else:
                    current_roll[keys.DESCRIPTION_KEY].append(line)

                    line_lower = line.lower()
                    process_author(current_roll, line_lower, keys)
                    process_tags(current_roll, line_lower, keys)

        # Add last roll to voltron data when reach end of file
        if current_roll.get(keys.ROLL_ID_KEY):
            add_default_tags(current_roll, keys)
            get_weapon_and_perk_counters(current_roll, keys)
            voltron_data.append(current_roll)

    # Process perks more, get dupe lists and remove duplicate lines from perks and trimmed
    process_perks_dupes(voltron_data, keys)

    return voltron_data


# Returns empty dict for current roll
def initialize_roll(keys: "Keys"):
    return {
        keys.AUTHORS_KEY: set(),
        keys.INC_TAGS_KEY: set(),
        keys.EXC_TAGS_KEY: set(),
        keys.ROLL_ID_KEY: "",
        keys.WEAPON_HASH_KEY: "",
        keys.DESCRIPTION_KEY: [],
        keys.PERKS_KEY: [],
        keys.TRIMMED_PERKS_KEY: [],
        keys.CORE_PERKS_KEY: [],
        keys.CORE_TRIMMED_PERKS_KEY: [],
        keys.PERKS_DUPES_KEY: [],
        keys.TRIMMED_PERKS_DUPES_KEY: [],
    }


# Adds dupe perks for perks and trimmed perks. Also removes duplicates from
# perks and trimmed perks
def process_perks_dupes(voltron_data, keys: "Keys"):
    def remove_duplicates(perk_list):
        return list(dict.fromkeys(perk_list))

    for weapon_roll in voltron_data:
        # Needs hash to check perks
        if not weapon_roll.get(keys.WEAPON_HASH_KEY):
            continue

        # Weapon doesn't appear min count times, invalid for roll dupe check
        if keys.WEAPON_COUNTER[weapon_roll[keys.WEAPON_HASH_KEY]] < keys.MIN_ROLL_COUNT:
            perks = remove_duplicates(weapon_roll[keys.PERKS_KEY])
            trimmed_perks = remove_duplicates(weapon_roll[keys.TRIMMED_PERKS_KEY])
            weapon_roll[keys.PERKS_KEY] = perks
            weapon_roll[keys.PERKS_DUPES_KEY] = perks
            weapon_roll[keys.TRIMMED_PERKS_KEY] = trimmed_perks
            weapon_roll[keys.TRIMMED_PERKS_DUPES_KEY] = trimmed_perks

        # Weapon is valid for getting dupe rolls
        else:
            perks_dupes = []
            trimmed_perks_dupes = []

            for index, core_perks in enumerate(weapon_roll[keys.CORE_PERKS_KEY]):
                if keys.CORE_COUNTER[core_perks] >= keys.MIN_ROLL_COUNT:
                    perks_dupes.append(weapon_roll[keys.PERKS_KEY][index])

            for index, core_trimmed_perks in enumerate(
                weapon_roll[keys.CORE_TRIMMED_PERKS_KEY]
            ):
                if keys.TRIMMED_COUNTER[core_trimmed_perks] >= keys.MIN_ROLL_COUNT:
                    trimmed_perks_dupes.append(
                        weapon_roll[keys.TRIMMED_PERKS_KEY][index]
                    )

            weapon_roll[keys.PERKS_KEY] = remove_duplicates(weapon_roll[keys.PERKS_KEY])
            weapon_roll[keys.PERKS_DUPES_KEY] = remove_duplicates(perks_dupes)
            weapon_roll[keys.TRIMMED_PERKS_KEY] = remove_duplicates(
                weapon_roll[keys.TRIMMED_PERKS_KEY]
            )
            weapon_roll[keys.TRIMMED_PERKS_DUPES_KEY] = remove_duplicates(
                trimmed_perks_dupes
            )


# Returns sorted array of perk hashes in given line
def get_perk_hashes(perk_line):
    # Convert perk lines into arrays with hashes
    perks_substring = perk_line[perk_line.find("&perks=") + 7 :]

    # Normal ending for substring
    perks_end = perks_substring.find("\n")
    if perks_end != -1:
        perks_substring = perks_substring[:perks_end]

    # Handle edge case for perks#perk_descriptions
    perks_end = perks_substring.find("#")
    if perks_end != -1:
        perks_substring = perks_substring[:perks_end]

    # Sorted required to ensure consistent comparing for counters
    return sorted(perks_substring.split(","))


# Returns the perk line string for each type of perk
def get_perk_types(roll_id, perk_hashes, keys: "Keys"):
    def hashes_to_string(roll_id, perk_hashes):
        return roll_id + ",".join(perk_hashes) + "\n"

    # Filter the perk hashes based on type of perks
    trimmed_hashes = []
    core_hashes = []
    core_trimmed_hashes = []

    for hash_value in perk_hashes:
        if hash_value in keys.FRAME_MODS or hash_value in keys.ORIGIN_TRAITS:
            if hash_value not in keys.ORIGIN_TRAITS:
                core_trimmed_hashes.append(hash_value)
            trimmed_hashes.append(hash_value)

        if hash_value not in keys.ORIGIN_TRAITS:
            core_hashes.append(hash_value)

    return (
        hashes_to_string(roll_id, perk_hashes),
        hashes_to_string(roll_id, trimmed_hashes),
        hashes_to_string(roll_id, core_hashes),
        hashes_to_string(roll_id, core_trimmed_hashes),
    )


# Creates Counter to track number of mentions for each set of perk and weapon hashes
def get_weapon_and_perk_counters(weapon_roll, keys: "Keys"):
    weapon_hash = weapon_roll[keys.ROLL_ID_KEY].split("item=")[1].split("&perks=")[0]
    weapon_roll[keys.WEAPON_HASH_KEY] = weapon_hash
    # Update counter for each rolls hashes. Only one set of hashes per roll will count
    keys.CORE_COUNTER.update(set(weapon_roll[keys.CORE_PERKS_KEY]))
    keys.TRIMMED_COUNTER.update(set(weapon_roll[keys.CORE_TRIMMED_PERKS_KEY]))
    keys.WEAPON_COUNTER.update([weapon_hash])


# Adds mouse and pve tag if no input or gamemode tag present
def add_default_tags(weapon_roll, keys: "Keys"):
    if not weapon_roll[keys.INC_TAGS_KEY].intersection({"mkb", "controller"}):
        weapon_roll[keys.INC_TAGS_KEY].add("mkb")
    if not weapon_roll[keys.INC_TAGS_KEY].intersection({"pve", "pvp"}):
        weapon_roll[keys.INC_TAGS_KEY].add("pve")


# Check each author present in wishlist configs
# If any found in line, add to current roll
def process_author(current_roll: Dict[str, object], line_lower: str, keys: "Keys"):
    for author in keys.AUTHORS:
        if author in line_lower:
            current_roll[keys.AUTHORS_KEY].add(author)


# Checks if any tags in wishlist are in given line
def process_tags(current_roll: Dict[str, object], line_lower: str, keys: "Keys"):
    # Fix MKB formatting
    line_lower = line_lower.replace("m+kb", "mkb")

    # Check if line has "tags:"
    tags_start = line_lower.find("tags:")
    valuable_text = ""
    if tags_start != -1:
        valuable_text = line_lower[tags_start:].replace("tags:", "").strip()
    # If no "tags:" found, find text between "(...)" or "[...]"
    else:
        # All text between '(...)'
        if "(" in line_lower:
            valuable_text += "".join(find_outer_content(line_lower, "(", ")"))
        if "[" in line_lower:
            valuable_text += "".join(find_outer_content(line_lower, "[", "]"))

    # Return if no valuable text
    if not valuable_text:
        return

    # Collect tags if any present
    for tag in keys.INC_TAGS:
        if tag in valuable_text:
            current_roll[keys.INC_TAGS_KEY].add(tag)

    for tag in keys.EXC_TAGS:
        if tag in valuable_text:
            current_roll[keys.EXC_TAGS_KEY].add(tag)


# Find outer content of a line given the open and closing delimiters
def find_outer_content(line: str, open_delim: str, close_delim: str):
    stack = []
    content = []
    content_start = -1

    for i, char in enumerate(line):
        if char == open_delim:
            # If open delim and no stack present, new content
            if not stack:
                content_start = i
            # Open delim but inside content
            stack.append(char)
        elif char == close_delim:
            # Close delim and last delim was open, then pop to close
            if stack and stack[-1] == open_delim:
                stack.pop()
                # If pop removed last stack open and starting index present outer content found, add to content
                if not stack and content_start != -1:
                    content.append(line[content_start + 1 : i])
                    content_start = -1

    return content
