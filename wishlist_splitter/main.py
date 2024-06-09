# main.py
from collections import Counter
import time

start_time = time.time()
###########################################################
# Called from Github Workflow to start updating wishlist #
# Collects wishlist config and voltron data              #
# Then sorts and writes voltron data to wishlists        #
###########################################################

# Import config file
from data.wishlist_configs import get_wishlist_config, export_wishlist_names

# Import helper function to grab origin trait hashes
from helper_scripts.get_weapon_mods import get_weapon_mods

# Import helper functions for getting voltron data
from helper_scripts.extract_voltron_data import (
    extract_author_and_tags,
    extract_voltron_data,
)
from helper_scripts.write_to_wishlists import write_to_wishlists


# Class to store constants that reference keys or values
class Keys:
    #########
    # Paths #
    #########
    VOLTRON_PATH = "./wishlist_splitter/data/dim-wish-list-sources/voltron.txt"
    # VOLTRON_PATH = "./wishlist_splitter/data/test.txt"
    ORIGIN_TRAITS_PATH = "./wishlist_splitter/data/weapon_mods/origin_traits.txt"
    FRAME_MODS_PATH = "./wishlist_splitter/data/weapon_mods/frame_mods.txt"
    # Path to all wishlist paths for website
    WISHLIST_NAMES_PATH = "./docs/data/wishlist_names.txt"

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
    FILE_KEY = "file"
    BATCH_KEY = "batch"
    BATCH_SIZE = 30

    ######################################
    # Keys for storing data from voltron #
    ######################################
    # Core perks are used for accurate counts of perks
    # Key for storing list of base perks (only 1st, 2nd, 3rd, and 4th columns)
    CORE_PERKS_KEY = "core_perks"
    # Key for storing trimmed perks (3rd and 4th columns with any extra perks)
    TRIMMED_PERKS_KEY = "trimmed_perks"
    # Key for storing core perks that have been filtered (only 3rd and 4th column)
    CORE_TRIMMED_PERKS_KEY = "core_trimmed_perks"

    # Minimum number of rolls to for dupe rolls
    MIN_ROLL_COUNT = 2

    # Keys to be added
    # Voltron text
    VOLTRON_DATA = None
    # Dictionary storing wishlist information
    WISHLIST_CONFIGS = None
    # List of origin trait hashes
    ORIGIN_TRAITS = None
    # List of frame mod hashes, 3rd and 4th column
    FRAME_MODS = None
    # List of tag values for all, include, and exclude
    ALL_TAGS = None
    INC_TAGS = None
    EXC_TAGS = None
    # List of author names
    AUTHOR_NAMES = None

    # Counters
    CORE_COUNTER = Counter()
    TRIMMED_COUNTER = Counter()
    WEAPON_COUNTER = Counter()


def main():
    keys = Keys()
    # Pass helper keys to get wishlist configs with matching keys
    keys.WISHLIST_CONFIGS = get_wishlist_config(keys)

    # Export wishlists to a txt file for the website
    export_wishlist_names(keys)

    # Collect origin trait hashes
    keys.ORIGIN_TRAITS = get_weapon_mods(keys.ORIGIN_TRAITS_PATH)

    # Collect frame mod hashes
    keys.FRAME_MODS = get_weapon_mods(keys.FRAME_MODS_PATH)

    keys.AUTHOR_NAMES, keys.ALL_TAGS, keys.INC_TAGS, keys.EXC_TAGS = (
        extract_author_and_tags(keys)
    )

    # Collect data from voltron
    keys.VOLTRON_DATA = extract_voltron_data(keys)

    # Write voltron data to config files
    write_to_wishlists(keys)


if __name__ == "__main__":
    main()

    end_time = time.time()

    runtime = end_time - start_time
    print(f"Runtime: {runtime} seconds")
