# main.py

from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Set

# Import helper functions
from data.wishlist_configs import get_wishlist_config
from helper_scripts.get_weapon_mods import get_weapon_mods
from helper_scripts.extract_voltron_data import extract_voltron_data
from helper_scripts.write_to_wishlists import write_to_wishlists

# Timer to test script performance
# import time
# start_time = time.time()


# Class to store constants that reference keys or values
@dataclass
class Keys:

    # Main text file with all weapon rolls
    VOLTRON_PATH = "./wishlist_splitter/data/dim-wish-list-sources/voltron.txt"
    # VOLTRON_PATH = "./wishlist_splitter/data/test.txt"

    # Origin traits and frame mods from Destiny Data Explorer
    ORIGIN_TRAITS_PATH = "./wishlist_splitter/data/weapon_mods/origin_traits.txt"
    FRAME_MODS_PATH = "./wishlist_splitter/data/weapon_mods/frame_mods.txt"

    WISHLIST_NAMES_PATH = "./docs/data/wishlist_names.txt"  # Wishlists for website ref

    WISHLIST_DIR = "./wishlists/"

    # Keys to reference wishlist config and voltron data
    WISHLIST_CONFIGS_KEY = "wishlist_configs"
    PATH_KEY = "path"
    CREDIT_KEY = "credits"
    CREDIT_TAG = "credits"
    AUTHOR_KEY = "author"
    INC_TAGS_KEY = "include_tags"
    EXC_TAGS_KEY = "exclude_tags"
    DESCRIPTION_KEY = "description"
    PERKS_KEY = "perks"
    DUPES_KEY = "dupes"

    TRIMMED_PERKS_KEY = "trimmed_perks"  # Only 3rd, 4th, and origin traits
    # Core perks are used to ensure accurate count for perks when filtering dupes
    CORE_PERKS_KEY = "core_perks"  # No origin traits
    CORE_TRIMMED_PERKS_KEY = "core_trimmed_perks"  # Only 3rd and 4th column

    MIN_ROLL_COUNT = 2  # Minimum number of rolls to for dupe rolls

    BATCH_SIZE = 1000  # Numebr of rolls held for wishlist before writing

    # Placeholder objects to hold values from voltron and wishlists
    VOLTRON_DATA: List[Dict[str, object]] = None  # Voltron rolls sorted and tagged
    WISHLIST_CONFIGS: List[Dict[str, object]] = None  # Wishlist preferences
    ORIGIN_TRAITS: Set[str] = None  # List of origin trait hashes
    FRAME_MODS: Set[str] = None  # List of frame mod hashes, 3rd and 4th column
    INC_TAGS: Set[str] = None  # All tags that wishlist want to include
    EXC_TAGS: Set[str] = None  # All tags that wishlists want to exclude
    AUTHOR_NAMES: Set[str] = None  # All author names in wishlists configs

    # Counters for perks and weapons
    CORE_COUNTER = Counter()  # Counter of core_perks
    TRIMMED_COUNTER = Counter()  # Counter for trimmed perks
    WEAPON_COUNTER = Counter()  # Counter for appearences of weapons


def main():
    # Create object for Keys
    keys = Keys()

    # Get wishlist data and save to keys
    # Wishlist names are exported as well
    config_results = get_wishlist_config(keys)
    keys.WISHLIST_CONFIGS = config_results[keys.WISHLIST_CONFIGS_KEY]
    keys.AUTHOR_NAMES = config_results[keys.AUTHOR_KEY]
    keys.INC_TAGS = config_results[keys.INC_TAGS_KEY]
    keys.EXC_TAGS = config_results[keys.EXC_TAGS_KEY]

    # Collect origin trait and frame mod hashes to keys
    keys.ORIGIN_TRAITS, keys.FRAME_MODS = get_weapon_mods(keys)

    # Collect data from voltron to keys
    keys.VOLTRON_DATA = extract_voltron_data(keys)

    # Write voltron data to wishlist files
    write_to_wishlists(keys)


if __name__ == "__main__":
    main()

    # Timer to see main script performance
    # end_time = time.time()
    # runtime = end_time - start_time
    # print(f"Runtime: {runtime} seconds")
