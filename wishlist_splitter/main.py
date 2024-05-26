# main.py

###########################################################
# Called from Github Workflow to start updating wishlist #
# Collects wishlist config and voltron data              #
# Then sorts and writes voltron data to wishlists        #
###########################################################

# Import config file
from data.wishlist_configs import get_wishlist_config

# Import helper function to grab origin trait hashes
from helper_scripts.get_origin_traits import get_origin_traits

# Import helper functions for getting voltron data
from helper_scripts.extract_voltron_data import (
    extract_authors,
    extract_tags,
    extract_voltron_data,
)
from helper_scripts.write_to_wishlists import write_to_wishlists


# Class to store constants that reference keys or values
class Keys:
    # Path of voltron file
    VOLTRON_PATH = "./wishlist_splitter/data/dim-wish-list-sources/voltron.txt"
    # VOLTRON_PATH = "./wishlist_splitter/data/test.txt"
    # Path to origin trait file
    ORIGIN_TRAITS_PATH = "./wishlist_splitter/data/origin_traits/origin_traits.txt"
    ############################
    # Keys for wishlist config #
    ############################
    PATH_KEY = "path"
    WISHLIST_DIR = "./wishlists/"
    CREDIT_KEY = "credits"
    CREDIT_TAG = "credits"
    AUTHOR_KEY = "author"
    INC_TAG_KEY = "include"
    EXC_TAG_KEY = "exclude"
    DESCRIPTION_KEY = "description"
    PERK_KEY = "perks"
    DUPE_PERKS_KEY = "dupe"
    ######################################
    # Keys for storing data from voltron #
    ######################################
    # Key for storing if a voltron roll includes extra perks
    EXTRA_PERK_KEY = "extra_perks"
    # Key for storing list of base perks (only 1st, 2nd, 3rd, and 4th columns)
    BASE_PERK_KEY = "base_perks"
    # Key for storing filtered perks (3rd and 4th columns with any extra perks)
    FILTERED_PERK_KEY = "filtered_perks"
    # Key for storing base perks that have been filtered (only 3rd and 4th column)
    BASE_FILTERED_PERK_KEY = "base_filtered_perks"

    # Keys to be added
    # Dictionary storing wishlist information
    WISHLIST_CONFIGS = None
    # List of origin trait hashes
    ORIGIN_TRAITS = None
    # List of tag values for all, include, and exclude
    ALL_TAGS = None
    INC_TAGS = None
    EXC_TAGS = None
    # List of author names
    AUTHOR_NAMES = None


def main():
    keys = Keys()
    # Pass helper keys to get wishlist configs with matching keys
    WISHLIST_CONFIGS = get_wishlist_config(keys)
    keys.WISHLIST_CONFIGS = WISHLIST_CONFIGS

    # Collect origin trait hashes
    ORIGIN_TRAITS = get_origin_traits(keys.ORIGIN_TRAITS_PATH)
    keys.ORIGIN_TRAITS = ORIGIN_TRAITS

    # Collect all, include, and exlcude tags from config
    ALL_TAGS, INC_TAGS, EXC_TAGS = extract_tags(
        keys.WISHLIST_CONFIGS,
        keys.INC_TAG_KEY,
        keys.EXC_TAG_KEY,
    )
    keys.ALL_TAGS = ALL_TAGS
    keys.INC_TAGS = INC_TAGS
    keys.EXC_TAGS = EXC_TAGS

    # Collect all author names in config
    AUTHOR_NAMES = extract_authors(
        keys.WISHLIST_CONFIGS,
        keys.AUTHOR_KEY,
    )
    keys.AUTHOR_NAMES = AUTHOR_NAMES

    # Collect data from voltron
    voltron_data = extract_voltron_data(keys)

    # Write voltron data to config files
    write_to_wishlists(voltron_data, keys)


if __name__ == "__main__":
    main()
