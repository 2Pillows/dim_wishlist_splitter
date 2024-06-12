# extract_voltron_data.py

import re

from typing import TYPE_CHECKING, Dict

# Load Keys class without importing to avoid cyclic import
if TYPE_CHECKING:
    from main import Keys


def extract_voltron_data(keys: "Keys"):
    # Array for dictionaries for weapon roll in Voltron
    voltron_data = []

    # Collects lines until weapon roll finished, then adds to voltron_data and empties
    current_roll = []

    with open(keys.VOLTRON_PATH, mode="r", encoding="utf-8") as voltron_file:
        for line_num, line in enumerate(voltron_file):
            # Removed title heading, replaced later with wishlist name
            if line_num == 0:
                line = line.replace("title:", "")

            if line == "\n":  # New line signifies end of current weapon roll
                if current_roll:
                    # Process current roll and add to voltron data
                    voltron_data.append(process_roll(current_roll, keys))
                    current_roll = []  # Start new roll
            else:
                current_roll.append(line)  # Not empty line, add to current roll

        # Add last roll to voltron data when reach end of file
        if current_roll:
            voltron_data.append(process_roll(current_roll, keys))

    return voltron_data


# Given array of weapon roll lines
# Save lines as Description or Perks. If Description, find author and tags
def process_roll(weapon_roll: Dict[str, object], keys: "Keys"):
    current_roll = {
        keys.CREDIT_KEY: set(),
        keys.AUTHOR_KEY: set(),
        keys.INC_TAGS_KEY: set(),
        keys.EXC_TAGS_KEY: set(),
        keys.DESCRIPTION_KEY: [],
        keys.PERKS_KEY: [],
    }

    for index, line in enumerate(weapon_roll):
        # When perk line found, assume rest are also perks and add remaining
        if "dimwishlist:item=" in line:
            current_roll[keys.PERKS_KEY] = weapon_roll[index:]
            break
        # Description line
        else:
            current_roll[keys.DESCRIPTION_KEY].append(line)

            # Collect author and tags for roll
            line_lower = line.lower()
            process_author(current_roll, line_lower, keys)
            process_tags(current_roll, line_lower, keys)

    return current_roll


# Check each author present in wishlist configs
# If any found in line, add to current roll
def process_author(current_roll: Dict[str, object], line_lower: str, keys: "Keys"):
    for author in keys.AUTHOR_NAMES:
        if author in line_lower:
            current_roll[keys.AUTHOR_KEY].add(author)


# Checks if any tags in wishlist are in given line
def process_tags(current_roll: Dict[str, object], line_lower: str, keys: "Keys"):
    # Check if line contains any credits
    line_type = re.sub(
        r"[^a-zA-Z]",
        "",
        line_lower[: line_lower.find(":")] if ":" in line_lower else "",
    )
    if "title" == line_type or "description" == line_type:
        current_roll[keys.CREDIT_KEY].add(keys.CREDIT_TAG)

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
