# main.py
from collections import Counter
from dataclasses import dataclass

from typing import List, Dict, Set

import time

start_time = time.time()

###########################################################
# Called from Github Workflow to start updating wishlist #
# Collects wishlist config and voltron data              #
# Then sorts and writes voltron data to wishlists        #
###########################################################

# Import config file
from data.wishlist_configs import get_wishlist_config

# Import helper function to grab origin trait hashes
from helper_scripts.get_weapon_mods import get_weapon_mods

# Import helper functions for getting voltron data
from helper_scripts.extract_voltron_data import extract_voltron_data

from helper_scripts.write_to_wishlists import write_to_wishlists


# Class to store constants that reference keys or values
@dataclass
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
    WISHLIST_CONFIGS_KEY = "wishlist_configs"
    PATH_KEY = "path"
    WISHLIST_DIR = "./wishlists/"
    CREDIT_KEY = "credits"
    CREDIT_TAG = "credits"
    AUTHOR_KEY = "author"
    ALL_TAG_KEY = "all_tags"
    INC_TAG_KEY = "include_tags"
    EXC_TAG_KEY = "exclude_tags"
    DESCRIPTION_KEY = "description"
    PERK_KEY = "perks"
    DUPE_PERKS_KEY = "dupe"

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

    # Numebr of rolls held for wishlist before writing
    BATCH_SIZE = 1000

    # Keys to be added
    # Voltron text
    VOLTRON_DATA: List[Dict[str, object]] = None
    # Dictionary storing wishlist information
    WISHLIST_CONFIGS: List[Dict[str, object]] = None
    # List of origin trait hashes
    ORIGIN_TRAITS: Set[str] = None
    # List of frame mod hashes, 3rd and 4th column
    FRAME_MODS: Set[str] = None
    # List of tag values for all, include, and exclude
    ALL_TAGS: Set[str] = None
    INC_TAGS: Set[str] = None
    EXC_TAGS: Set[str] = None
    # List of author names
    AUTHOR_NAMES: Set[str] = None

    # Counters
    CORE_COUNTER = Counter()
    TRIMMED_COUNTER = Counter()
    WEAPON_COUNTER = Counter()


def main():
    keys = Keys()

    # Pass helper keys to get wishlist configs with matching keys
    # Wishlists are exported from this function
    config_results = get_wishlist_config(keys)
    keys.WISHLIST_CONFIGS = config_results[keys.WISHLIST_CONFIGS_KEY]
    keys.AUTHOR_NAMES = config_results[keys.AUTHOR_KEY]
    keys.ALL_TAGS = config_results[keys.ALL_TAG_KEY]
    keys.INC_TAGS = config_results[keys.INC_TAG_KEY]
    keys.EXC_TAGS = config_results[keys.EXC_TAG_KEY]

    # Collect origin trait hashes
    keys.ORIGIN_TRAITS = get_weapon_mods(keys.ORIGIN_TRAITS_PATH)

    # Collect frame mod hashes
    keys.FRAME_MODS = get_weapon_mods(keys.FRAME_MODS_PATH)

    # Collect data from voltron
    keys.VOLTRON_DATA = extract_voltron_data(keys)

    # Write voltron data to config files
    write_to_wishlists(keys)


if __name__ == "__main__":
    main()

    end_time = time.time()

    runtime = end_time - start_time
    print(f"Runtime: {runtime} seconds")
