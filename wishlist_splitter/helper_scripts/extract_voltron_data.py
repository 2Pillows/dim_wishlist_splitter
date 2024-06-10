# extract_voltron_data.py

import re

# Import for type hints and intellisense
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from main import Keys


##################################################
# Collect authors and tags from wishlist configs #
##################################################
def extract_author_and_tags(WISHLIST_CONFIGS, AUTHOR_KEY, INC_TAG_KEY, EXC_TAG_KEY):
    author_names = set()
    all_tags = set()
    inc_tags = set()
    exc_tags = set()

    # Iterate through each config and collect author names, INC_TAG_KEY, and EXC_TAG_KEY values
    for config in WISHLIST_CONFIGS:
        author_names.update(config.get(AUTHOR_KEY, []))
        inc_tags.update(config.get(INC_TAG_KEY, []))
        exc_tags.update(config.get(EXC_TAG_KEY, []))

    # Update ALL_TAGS with tags collected from config
    all_tags.update(inc_tags)
    all_tags.update(exc_tags)

    return author_names, all_tags, inc_tags, exc_tags


###############################################################
# Reads Voltron and saves each batch of lines to a dictionary #
# Then writes dictionaries to config files                    #
###############################################################
def extract_voltron_data(keys: "Keys"):
    # Holds the dictionaries for each set of lines in Voltron
    voltron_data = []

    current_roll = []

    with open(keys.VOLTRON_PATH, mode="r", encoding="utf-8") as voltron_file:
        for line_num, line in enumerate(voltron_file):
            if line_num == 0:
                # Remove title in heading, replaced later with file name
                line = line.replace("title:", "")

            if line == "\n":
                if current_roll:
                    voltron_data.append(process_roll(current_roll, keys))
                    current_roll = []
            else:
                current_roll.append(line)

        # Append the last roll if any
        if current_roll:
            voltron_data.append(process_roll(current_roll, keys))

    return voltron_data


# Given array for all lines in roll
# Save line to current_roll[KEY] depending on value in line
# Generate tags for roll
def process_roll(roll_lines: Dict[str, object], keys: "Keys"):
    current_roll = {
        keys.CREDIT_KEY: [],
        keys.AUTHOR_KEY: [],
        keys.INC_TAG_KEY: [],
        keys.EXC_TAG_KEY: [],
        keys.DESCRIPTION_KEY: [],
        keys.PERK_KEY: [],
    }

    for index, line in enumerate(roll_lines):
        # Add all perk lines
        if "dimwishlist:item=" in line:
            current_roll[keys.PERK_KEY] = roll_lines[index:]
            break
        # Description line
        else:
            current_roll[keys.DESCRIPTION_KEY].append(line)

            # Collect tags for roll
            line_lower = line.lower()
            process_author(current_roll, line_lower, keys)
            process_tags(current_roll, line_lower, keys)

    return current_roll


# Adds name of author if present in any wishlist config
def process_author(current_roll: Dict[str, object], line_lower: str, keys: "Keys"):
    for author in keys.AUTHOR_NAMES:
        if author in line_lower:
            current_roll[keys.AUTHOR_KEY].append(author)


# Collects any tags if they are in wishlists
def process_tags(current_roll: Dict[str, object], line_lower: str, keys: "Keys"):
    # Uess pattern to select strings between (...) or [...]
    # Also takes string from 'tags:' to end of line

    # Tags that indicate line contains credits
    line_type = re.sub(
        r"[^a-zA-Z]",
        "",
        line_lower[: line_lower.find(":")] if ":" in line_lower else "",
    )
    if "title" == line_type or "description" == line_type:
        current_roll[keys.CREDIT_KEY].append(keys.CREDIT_TAG)

    # Fix MKB formatting
    line_lower = line_lower.replace("m+kb", "mkb")

    # All text between '(...)'
    parenthesis_content = find_outer_content(line_lower, "(", ")")

    # All text between '[...]'
    bracket_content = find_outer_content(line_lower, "[", "]")

    # Combine both matches
    grouped_text = " ".join(parenthesis_content + bracket_content)

    # All text after tags:
    tags_start = line_lower.find("tags:")
    tags_text = ""
    if tags_start != -1:
        tags_text = line_lower[tags_start:].replace("tags:", "").strip()

    # Valuable text is either tags or grouped text if no tags
    valuable_text = tags_text if len(tags_text) > 0 else grouped_text

    # Return if no valuable text
    if len(valuable_text) <= 0:
        return

    # Collect tags if any present
    for tag in keys.ALL_TAGS:
        if tag in valuable_text:
            if tag in keys.INC_TAGS and tag not in current_roll[keys.INC_TAG_KEY]:
                current_roll[keys.INC_TAG_KEY].append(tag)
            elif tag in keys.EXC_TAGS and tag not in current_roll[keys.EXC_TAG_KEY]:
                current_roll[keys.EXC_TAG_KEY].append(tag)


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
