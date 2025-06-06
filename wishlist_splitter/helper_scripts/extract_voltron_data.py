# extract_voltron_data.py

from typing import Counter, Dict, List, Set

# Import keys
from helper_scripts.keys import Keys


# Read voltron file and collect roll information
def extract_voltron_data(keys: "Keys") -> None:
    # Array for dictionaries for weapon roll in Voltron
    voltron_data = []

    # Dict to hold roll information
    current_roll = initialize_roll(keys)

    with open(keys.VOLTRON_PATH, mode="r", encoding="utf-8") as voltron_file:
        for line_num, line in enumerate(voltron_file):
            # Removed title heading, replaced later with wishlist name
            if line_num == 0:
                line = line.replace("title:", "")

            # End of current roll
            if line == "\n":
                # Check if current roll should be added to voltron data
                if line_num == 2 or current_roll.get(keys.PERKS_KEY):
                    if line_num != 2:  # Isn't the haeding, add tags and update counters
                        process_weapon_roll(current_roll, keys)

                    voltron_data.append(current_roll)

                # Start new roll
                current_roll = initialize_roll(keys)
            else:
                # Collect perk information
                if "dimwishlist:item=" in line:
                    # Collect different perk lines for current perk line
                    set_perk_types(current_roll, line, keys)

                # Add description and collect tags and authors
                else:
                    current_roll[keys.DESCRIPTION_KEY].append(line)

                    line_lower = line.lower()
                    process_author(
                        current_roll[keys.AUTHORS_KEY], line_lower, keys.AUTHORS
                    )
                    process_tags(current_roll, line_lower, keys)

        # Add last roll to voltron data when reach end of file
        if current_roll.get(keys.ROLL_ID_KEY):
            process_weapon_roll(current_roll, keys)
            voltron_data.append(current_roll)

    # Process perks more, get dupe lists and remove duplicate lines from perks and trimmed
    process_perks_dupes(voltron_data, keys)

    keys.VOLTRON_DATA = voltron_data


# Returns empty dict for current roll
def initialize_roll(keys: "Keys") -> Dict[str, object]:
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


def process_weapon_roll(weapon_roll: Dict[str, object], keys: "Keys") -> None:
    # Add tags if none present
    add_default_tags(weapon_roll[keys.INC_TAGS_KEY], keys)

    # Update counters with perks
    get_weapon_and_perk_counters(weapon_roll, keys)


# Adds mouse and pve tag if no input or gamemode tag present
def add_default_tags(roll_tags: Set[str], keys: "Keys") -> None:
    if not roll_tags.intersection({"mkb", "controller"}):
        roll_tags.add("mkb")
    if not roll_tags.intersection({"pve", "pvp"}):
        roll_tags.add("pve")


# Creates Counter to track number of mentions for each set of perk and weapon hashes
def get_weapon_and_perk_counters(weapon_roll: Dict[str, object], keys: "Keys") -> None:
    weapon_hash = weapon_roll[keys.ROLL_ID_KEY].split("item=")[1].split("&perks=")[0]
    weapon_roll[keys.WEAPON_HASH_KEY] = weapon_hash
    # Update counter for each rolls hashes. Only one set of hashes per roll will count
    keys.CORE_COUNTER.update(set(weapon_roll[keys.CORE_PERKS_KEY]))
    keys.TRIMMED_COUNTER.update(set(weapon_roll[keys.CORE_TRIMMED_PERKS_KEY]))
    keys.WEAPON_COUNTER.update([weapon_hash])


# Sets perk line string for each type of perk in current roll
def set_perk_types(
    weapon_roll: List[Dict[str, object]], line: str, keys: "Keys"
) -> None:
    # Get roll id if none present
    if not weapon_roll.get(keys.ROLL_ID_KEY):
        weapon_roll[keys.ROLL_ID_KEY] = line[: line.find("&perks") + 7]

    roll_id = weapon_roll[keys.ROLL_ID_KEY]

    # Get perk hashes from line
    perk_hashes = get_perk_hashes(line)

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

    # Add perk lines to weapon roll
    weapon_roll[keys.PERKS_KEY].append(hashes_to_string(roll_id, perk_hashes))
    weapon_roll[keys.TRIMMED_PERKS_KEY].append(
        hashes_to_string(roll_id, trimmed_hashes)
    )

    weapon_roll[keys.CORE_PERKS_KEY].append(hashes_to_string(roll_id, core_hashes))
    weapon_roll[keys.CORE_TRIMMED_PERKS_KEY].append(
        hashes_to_string(roll_id, core_trimmed_hashes)
    )


# Returns sorted array of perk hashes in given line
def get_perk_hashes(perk_line: str) -> List[str]:
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


def hashes_to_string(roll_id: str, perk_hashes: List[str]) -> str:
    return roll_id + ",".join(perk_hashes) + "\n"


# Check each author present in wishlist configs
# If any found in line, add to current roll
def process_author(roll_authors: Set[str], line_lower: str, authors: Set[str]) -> None:
    for author in authors:
        if author in line_lower:
            roll_authors.add(author)


# Checks if any tags in wishlist are in given line
def process_tags(
    current_roll: Dict[str, object], line_lower: str, keys: "Keys"
) -> None:
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
        valuable_text += "".join(find_outer_content(line_lower, "(", ")"))
        valuable_text += "".join(find_outer_content(line_lower, "[", "]"))

    # Return if no valuable text
    if not valuable_text:
        return

    # Collect tags if any present
    add_tags(keys.INC_TAGS, current_roll[keys.INC_TAGS_KEY], valuable_text)
    add_tags(keys.EXC_TAGS, current_roll[keys.EXC_TAGS_KEY], valuable_text)


# Add tags found in valuable text to roll
def add_tags(tags: Set[str], roll_tags: Set[str], valuable_text: str) -> None:
    for tag in tags:
        if tag in valuable_text:
            roll_tags.add(tag)


# Find outer content of a line given the open and closing delimiters
def find_outer_content(line: str, open_delim: str, close_delim: str) -> List[str]:
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
        elif char == close_delim and stack and stack[-1] == open_delim:
            # Close delim and last delim was open, then pop to close
            stack.pop()
            # If pop removed last stack open and starting index present outer content found, add to content
            if not stack and content_start != -1:
                content.append(line[content_start + 1 : i])
                content_start = -1

    return content


# Adds dupe perks for perks and trimmed perks. Also removes duplicates from
# perks and trimmed perks
def process_perks_dupes(voltron_data: List[Dict[str, object]], keys: "Keys") -> None:
    for weapon_roll in voltron_data:
        # Needs hash to check perks
        if not weapon_roll.get(keys.WEAPON_HASH_KEY):
            continue

        # Get min count needed for rolls, assume 1 unless weapon appears min_count times
        roll_count = (
            keys.MIN_ROLL_COUNT
            if keys.WEAPON_COUNTER[weapon_roll[keys.WEAPON_HASH_KEY]]
            >= keys.MIN_ROLL_COUNT
            else 1
        )

        set_unique_perk_lists(
            weapon_roll[keys.PERKS_KEY],
            weapon_roll[keys.CORE_PERKS_KEY],
            weapon_roll[keys.PERKS_DUPES_KEY],
            keys.CORE_COUNTER,
            roll_count,
        )
        set_unique_perk_lists(
            weapon_roll[keys.TRIMMED_PERKS_KEY],
            weapon_roll[keys.CORE_TRIMMED_PERKS_KEY],
            weapon_roll[keys.TRIMMED_PERKS_DUPES_KEY],
            keys.TRIMMED_COUNTER,
            roll_count,
        )


# Set perk list and perk dupes list to unique perks
def set_unique_perk_lists(
    perk_list: List[str],
    core_perk_list: List[str],
    perk_dupe_list: List[str],
    perk_counter: Counter,
    min_count: int,
) -> None:
    seen = set()

    unique_perk_list = []
    unique_perk_dupe_list = []

    for perk, core_perk in zip(perk_list, core_perk_list):
        if perk not in seen:
            seen.add(perk)
            unique_perk_list.append(perk)
            if perk_counter[core_perk] >= min_count:
                unique_perk_dupe_list.append(perk)

    # Set unique lists to base lists
    perk_list.clear()
    perk_list.extend(unique_perk_list)

    perk_dupe_list.extend(unique_perk_dupe_list)
