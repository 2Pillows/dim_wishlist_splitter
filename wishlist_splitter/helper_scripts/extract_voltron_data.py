# extract_voltron_data.py


import copy
import re

# Import for type hints and intellisense
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from main import Keys


##########################################
# Collect auithors from wishlist configs #
##########################################
def extract_authors(WISHLIST_CONFIGS: List[Dict[str, object]], AUTHOR_KEY: str):
    author_names = set()
    for config in WISHLIST_CONFIGS:
        author_names.update(config.get(AUTHOR_KEY, []))
    return author_names


######################################
# Collect tags from wishlist configs #
######################################
def extract_tags(
    WISHLIST_CONFIGS: List[Dict[str, object]], INC_TAG_KEY: str, EXC_TAG_KEY: str
):
    all_tags = set()
    inc_tags = set()
    exc_tags = set()

    # Iterate through each config and collect INC_TAG_KEY and EXC_TAG_KEY values
    for config in WISHLIST_CONFIGS:
        inc_tags.update(config.get(INC_TAG_KEY, []))
        exc_tags.update(config.get(EXC_TAG_KEY, []))

    # Update ALL_TAGS with tags collected from config
    all_tags.update(inc_tags)
    all_tags.update(exc_tags)

    return all_tags, inc_tags, exc_tags


###############################################################
# Reads Voltron and saves each batch of lines to a dictionary #
# Then writes dictionaries to config files                    #
###############################################################
def extract_voltron_data(keys: "Keys"):
    # Path to voltron file
    file_path = keys.VOLTRON_PATH

    # Holds the dictionaries for each set of lines in Voltron
    voltron_data = []

    # Collect roll data and tags
    current_roll = {
        keys.CREDIT_KEY: [],
        keys.AUTHOR_KEY: [],
        keys.INC_TAG_KEY: [],
        keys.EXC_TAG_KEY: [],
        keys.DESCRIPTION_KEY: [],
        keys.PERK_KEY: [],
    }

    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            line_lower = line.lower()

            # Indicates end of current_roll
            if line == "":
                # Add roll to voltron_data
                voltron_data.append(copy.deepcopy(current_roll))

                # Clear contents of current_roll
                initialize_roll(current_roll, keys)
                continue

            # Line ins't empty so save data to current_roll
            process_rolls(current_roll, line, line_lower, keys)

        # Append last roll when reach end of file
        voltron_data.append(copy.deepcopy(current_roll))

    return voltron_data


# ===========================================
# keys functions for extract_voltron_data =
# ===========================================


# Clear contents of current_roll
def initialize_roll(current_roll: Dict[str, object], keys: "Keys"):
    current_roll[keys.CREDIT_KEY] = []
    current_roll[keys.AUTHOR_KEY] = []
    current_roll[keys.INC_TAG_KEY] = []
    current_roll[keys.EXC_TAG_KEY] = []
    current_roll[keys.DESCRIPTION_KEY] = []
    current_roll[keys.PERK_KEY] = []


# Save line to current_roll[KEY] depending on value in line
def process_rolls(
    current_roll: Dict[str, object], line: str, line_lower: str, keys: "Keys"
):
    dim_item_id = "dimwishlist:item="
    if dim_item_id in line_lower:
        current_roll[keys.PERK_KEY].append(line)
    else:
        # Remove title in heading, replaced with file name
        if "title:This is a compiled collection" in line:
            line = line.replace("title:", "")

        current_roll[keys.DESCRIPTION_KEY].append(line)

        # Collect tags for roll
        process_author(current_roll, line_lower, keys)
        process_tags(current_roll, line_lower, keys)


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
    credit_tags = ["title:", "description:"]
    if any(tag in line_lower for tag in credit_tags) and "//" not in line_lower:
        current_roll[keys.CREDIT_KEY].append(keys.CREDIT_TAG)

    # Fix MKB formatting
    line_lower = line_lower.replace("m+kb", "mkb")

    # All text between '(...)'
    # parentheses_pattern = r"\([^()]*\)"
    # parentheses_matches = re.findall(parentheses_pattern, line_lower)
    parenthesis_content = find_outer_content(line_lower, "(", ")")

    # All text between '[...]'
    # brackets_pattern = r"\[([^[\]]+(\[([^[\]]+)\][^[\]]*)*)\]"
    # brackets_matches = re.findall(brackets_pattern, line_lower)
    bracket_content = find_outer_content(line_lower, "[", "]")

    # Convert matches to strings
    # parentheses_matches = [match[0] for match in parentheses_matches]
    # brackets_matches = [match[0] for match in brackets_matches]

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
