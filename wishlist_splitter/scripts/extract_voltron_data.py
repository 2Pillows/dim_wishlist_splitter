# extract_voltron_data.py


import copy
import re


##########################################
# Collect auithors from wishlist configs #
##########################################
def extract_authors(WISHLIST_CONFIGS, AUTHOR_KEY):
    author_names = set()
    for config in WISHLIST_CONFIGS:
        author_names.update(config.get(AUTHOR_KEY, []))
    return author_names


######################################
# Collect tags from wishlist configs #
######################################
def extract_tags(WISHLIST_CONFIGS, INC_TAG_KEY, EXC_TAG_KEY):
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
def extract_voltron_data(helper):
    # Path to voltron file
    file_path = helper["VOLTRON_PATH"]

    # Holds the dictionaries for each set of lines in Voltron
    voltron_data = []

    # Collect roll data and tags
    current_roll = {
        helper["CREDIT_KEY"]: [],
        helper["AUTHOR_KEY"]: [],
        helper["INC_TAG_KEY"]: [],
        helper["EXC_TAG_KEY"]: [],
        helper["DESCRIPTION_KEY"]: [],
        helper["PERK_KEY"]: [],
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
                initialize_roll(current_roll, helper)
                continue

            # Line ins't empty so save data to current_roll
            process_rolls(current_roll, line, line_lower, helper)

        # Append last roll when reach end of file
        voltron_data.append(copy.deepcopy(current_roll))

    return voltron_data


# ===========================================
# Helper functions for extract_voltron_data =
# ===========================================


# Clear contents of current_roll
def initialize_roll(current_roll, helper):
    current_roll[helper["CREDIT_KEY"]] = []
    current_roll[helper["AUTHOR_KEY"]] = []
    current_roll[helper["INC_TAG_KEY"]] = []
    current_roll[helper["EXC_TAG_KEY"]] = []
    current_roll[helper["DESCRIPTION_KEY"]] = []
    current_roll[helper["PERK_KEY"]] = []


# Save line to current_roll[KEY] depending on value in line
def process_rolls(current_roll, line, line_lower, helper):
    dim_item_id = "dimwishlist:item="
    if dim_item_id in line_lower:
        current_roll[helper["PERK_KEY"]].append(line)
    else:
        current_roll[helper["DESCRIPTION_KEY"]].append(line)

        # Collect tags for roll
        process_author(current_roll, line_lower, helper)
        process_tags(current_roll, line_lower, helper)


# Adds name of author if present in any wishlist config
def process_author(current_roll, line_lower, helper):
    for author in helper["AUTHOR_NAMES"]:
        if author in line_lower:
            current_roll[helper["AUTHOR_KEY"]].append(author)


# Collects any tags if they are in wishlists
def process_tags(current_roll, line_lower, helper):
    # Uess pattern to select strings between (...) or [...]
    # Also takes string from 'tags:' to end of line

    # Tags that indicate line contains credits
    credit_tags = ["title:", "description:"]
    if any(tag in line_lower for tag in credit_tags) and "//" not in line_lower:
        current_roll[helper["CREDIT_KEY"]].append(helper["CREDIT_TAG"])

    # Fix MKB formatting
    line_lower = line_lower.replace("m+kb", "mkb")

    # All text between '(...)'
    parentheses_pattern = r"\(([^()]+(\(([^()]+)\)[^()]*)*)\)"
    parentheses_matches = re.findall(parentheses_pattern, line_lower)

    # All text between '[...]'
    brackets_pattern = r"\[([^[\]]+(\[([^[\]]+)\][^[\]]*)*)\]"
    brackets_matches = re.findall(brackets_pattern, line_lower)

    # All text after tags:
    tags_start = line_lower.find("tags:")
    tags_text = ""
    if tags_start != -1:
        tags_text = line_lower[tags_start + len("tags:") :].strip()

    # Combine all viable sections of line
    combined_text = ""
    # Extract matched groups from parentheses_matches and brackets_matches
    matched_groups = [group[0] for group in parentheses_matches] + [
        group[0] for group in brackets_matches
    ]
    # Append the text from matched_groups and tags_text to combined_text
    combined_text += " ".join(matched_groups + [tags_text])

    # Collect tags if any present
    for tag in helper["ALL_TAGS"]:
        if tag in combined_text:
            if (
                tag in helper["INC_TAGS"]
                and tag not in current_roll[helper["INC_TAG_KEY"]]
            ):
                current_roll[helper["INC_TAG_KEY"]].append(tag)
            elif (
                tag in helper["EXC_TAGS"]
                and tag not in current_roll[helper["EXC_TAG_KEY"]]
            ):
                current_roll[helper["EXC_TAG_KEY"]].append(tag)
