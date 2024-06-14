# extract_voltron_data.py

import re

from collections import Counter, defaultdict
from typing import TYPE_CHECKING, Dict, List

# Load Keys class without importing to avoid cyclic import
if TYPE_CHECKING:
    from main import Keys


def extract_voltron_data(keys: "Keys"):
    # Array for dictionaries for weapon roll in Voltron
    voltron_data = []

    # Collects lines until weapon roll finished, then adds to voltron_data and empties
    weapon_perks = []
    weapon_desc = []

    with open(keys.VOLTRON_PATH, mode="r", encoding="utf-8") as voltron_file:
        for line_num, line in enumerate(voltron_file):
            # Removed title heading, replaced later with wishlist name
            if line_num == 0:
                line = line.replace("title:", "")

            if line == "\n":  # New line signifies end of current weapon roll
                # Process current roll and add to voltron data
                if line_num == 2 or weapon_perks:
                    voltron_data.append(process_roll(weapon_desc, weapon_perks, keys))

                # Start new roll
                weapon_perks = []
                weapon_desc = []
            else:
                if "dimwishlist:item=" in line:
                    weapon_perks.append(line)
                else:
                    weapon_desc.append(line)  # Not empty line, add to current roll

        # Add last roll to voltron data when reach end of file
        if weapon_perks:
            voltron_data.append(process_roll(weapon_desc, weapon_perks, keys))

    # Process perks more, get dupes and set perk and trimmed to lists
    process_perks_dupes(voltron_data, keys)

    return voltron_data


# Given array of weapon roll lines
# Save lines as Description or Perks. If Description, find author and tags
def process_roll(weapon_desc, weapon_perks, keys: "Keys"):
    current_roll = {
        keys.AUTHORS_KEY: set(),
        keys.INC_TAGS_KEY: set(),
        keys.EXC_TAGS_KEY: set(),
        keys.WEAPON_HASH_KEY: "",
        keys.DESCRIPTION_KEY: [],
        keys.PERKS_KEY: {},
        keys.TRIMMED_PERKS_KEY: {},
        keys.PERKS_DUPES_KEY: [],
        keys.TRIMMED_PERKS_DUPES_KEY: [],
    }

    current_roll[keys.DESCRIPTION_KEY] = weapon_desc

    # Return if just desc given, no perks to process
    if not weapon_perks:
        return current_roll

    for line in current_roll[keys.DESCRIPTION_KEY]:
        line_lower = line.lower()
        process_author(current_roll, line_lower, keys)
        process_tags(current_roll, line_lower, keys)

    current_roll[keys.WEAPON_HASH_KEY] = (
        weapon_perks[0].split("item=")[1].split("&perks=")[0]
    )

    # Adds mouse and pve tag if no input or gamemode tag present
    add_default_tags(current_roll, keys)

    # Get core and trimmed perks
    # core is 1st, 2nd, 3rd, 4th column. Used for accurate counting
    # Trimmed doesn't have 1st and 2nd column. Gets core version for counting as well
    process_perks(current_roll, weapon_perks, keys)

    # Collect weapon and perks Counters
    get_weapon_and_perk_counters(current_roll, keys)

    return current_roll


# Get array of perk lines that are present min_count times
# Change curent perk and trimed perks from dict to list w/ lines
def process_perks_dupes(voltron_data, keys: "Keys"):
    perk_counter = keys.CORE_COUNTER
    trimmed_perk_counter = keys.TRIMMED_COUNTER
    min_count = keys.MIN_ROLL_COUNT

    for weapon_roll in voltron_data:
        perks = []
        perks_dupes = []
        trimmed_perks = []
        trimmed_perks_dupes = []

        if not weapon_roll.get(keys.PERKS_KEY):
            continue

        for core_perks in weapon_roll[keys.PERKS_KEY].keys():
            perks.extend(weapon_roll[keys.PERKS_KEY][core_perks])
            if perk_counter[core_perks] >= min_count:
                perks_dupes.extend(weapon_roll[keys.PERKS_KEY][core_perks])

        for core_trimmed_perks in weapon_roll[keys.TRIMMED_PERKS_KEY].keys():
            trimmed_perks.extend(
                weapon_roll[keys.TRIMMED_PERKS_KEY][core_trimmed_perks]
            )
            if trimmed_perk_counter[core_trimmed_perks] >= min_count:
                trimmed_perks_dupes.extend(
                    weapon_roll[keys.TRIMMED_PERKS_KEY][core_trimmed_perks]
                )

        weapon_roll[keys.PERKS_KEY] = perks
        weapon_roll[keys.PERKS_DUPES_KEY] = perks_dupes
        weapon_roll[keys.TRIMMED_PERKS_KEY] = trimmed_perks
        weapon_roll[keys.TRIMMED_PERKS_DUPES_KEY] = trimmed_perks_dupes


def process_perks(weapon_roll, perk_lines, keys: "Keys"):
    def get_perk_hashes(perk_lines):
        PERK_START = perk_lines[0].find("&perks=") + 7

        perk_hashes = []

        # Convert perk lines into arrays with hashes
        for perk_line in perk_lines:
            perks_substring = perk_line[PERK_START:]

            # Normal ending for substring
            perks_end = perk_line.find("\n")
            if perks_end != -1:
                perks_substring = perk_line[PERK_START:perks_end]

            # Handle edge case for perks#perk_descriptions
            perk_end = perks_substring.find("#")
            if perk_end != -1:
                perks_substring = perks_substring[:perk_end]

            # Sorted required to ensure consistent comparing for counters
            perk_hashes.append(sorted(perks_substring.split(",")))
        return perk_hashes

    def get_perk_dicts(perk_hashes, keys: "Keys"):
        def hashes_to_string(roll_id, perk_hashes):
            return roll_id + ",".join(perk_hashes) + "\n"

        def remove_duplicates(perks):
            seen = set()
            for core_perks, perk_lines in perks.items():
                perks[core_perks] = [
                    perk for perk in perk_lines if not (perk in seen or seen.add(perk))
                ]
            return perks

        perks = defaultdict(list)
        trimmed_perks = defaultdict(list)

        # Filter the perk hashes based on type of perks
        for hashes in perk_hashes:
            trimmed_hashes = []
            core_hashes = []
            core_trimmed_hashes = []

            for hash_value in hashes:
                if hash_value in keys.FRAME_MODS or hash_value in keys.ORIGIN_TRAITS:
                    if hash_value not in keys.ORIGIN_TRAITS:
                        core_trimmed_hashes.append(hash_value)
                    trimmed_hashes.append(hash_value)

                if hash_value not in keys.ORIGIN_TRAITS:
                    core_hashes.append(hash_value)

            # Append perks to corresponding core perks
            perks[hashes_to_string(roll_id, core_hashes)].append(
                hashes_to_string(roll_id, hashes)
            )

            # Change trimmed hashes to string and append to correspoding core trimmed perks
            trimmed_perks[hashes_to_string(roll_id, core_trimmed_hashes)].append(
                hashes_to_string(roll_id, trimmed_hashes)
            )

        # Remove duplicates, keeping order
        perks = remove_duplicates(perks)
        trimmed_perks = remove_duplicates(trimmed_perks)

        return perks, trimmed_perks

    # Holds initial string before perk hashes
    roll_id = perk_lines[0][: perk_lines[0].find("&perks") + 7]

    perk_hashes = get_perk_hashes(perk_lines)  # Holds arrays of perk hashes

    weapon_roll[keys.PERKS_KEY], weapon_roll[keys.TRIMMED_PERKS_KEY] = get_perk_dicts(
        perk_hashes, keys
    )


# Creates Counter to track number of mentions for each set of perk and weapon hashes
def get_weapon_and_perk_counters(weapon_roll, keys: "Keys"):
    # Update counter for each rolls hashes. Only one set of hashes per roll will count
    keys.CORE_COUNTER.update(weapon_roll[keys.PERKS_KEY].keys())
    keys.TRIMMED_COUNTER.update(weapon_roll[keys.TRIMMED_PERKS_KEY].keys())
    keys.WEAPON_COUNTER.update([weapon_roll[keys.WEAPON_HASH_KEY]])


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
        parenthesis_content = find_outer_content(line_lower, "(", ")")

        # All text between '[...]'
        bracket_content = find_outer_content(line_lower, "[", "]")

        # Combine both matches
        valuable_text = " ".join(parenthesis_content + bracket_content)

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
