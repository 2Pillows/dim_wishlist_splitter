# keys.py

from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Set


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super().__call__(*args, **kwargs)
        return self._instances[self]


# Class to store constants that reference keys or values
@dataclass
class Keys(metaclass=Singleton):

    # Main text file with all weapon rolls
    VOLTRON_PATH = "./wishlist_splitter/data/dim-wish-list-sources/voltron.txt"
    # VOLTRON_PATH = "./wishlist_splitter/data/test.txt"
    VOLTRON_DATA: List[Dict[str, object]] = None

    WISHLIST_NAMES_PATH = "./docs/data/wishlist_names.txt"  # Wishlists for website ref

    WISHLIST_DIR = "./wishlists/"

    # Origin traits from Destiny Data Explorer
    ORIGIN_TRAITS_PATH = "./wishlist_splitter/data/weapon_mods/origin_traits.txt"
    ORIGIN_TRAITS: Set[str] = None

    # Frame mods from Destiny Data Explorer, 3rd and 4th column
    FRAME_MODS_PATH = "./wishlist_splitter/data/weapon_mods/frame_mods.txt"
    FRAME_MODS: Set[str] = None

    # Wishlist preferences
    WISHLIST_CONFIGS_KEY = "wishlist_configs"
    WISHLIST_CONFIGS: List[Dict[str, object]] = None

    # All author names in wishlists configs
    AUTHORS_KEY = "authors"
    AUTHORS: Set[str] = None

    # All tags that wishlist want to include
    INC_TAGS_KEY = "include_tags"
    INC_TAGS: Set[str] = None

    # All tags that wishlists want to exclude
    EXC_TAGS_KEY = "exclude_tags"
    EXC_TAGS: Set[str] = None

    # Wishlist and weapon dict keys
    PATH_KEY = "path"

    # Voltron Data keys
    WEAPON_HASH_KEY = "weapon_hash"
    ROLL_ID_KEY = "roll_id"

    DESCRIPTION_KEY = "description"  # Holds description for weapon rolls

    # Keys for perk types for weapon rolls
    PERKS_KEY = "perks"
    TRIMMED_PERKS_KEY = "trimmed_perks"
    PERKS_DUPES_KEY = "perks_dupes"
    TRIMMED_PERKS_DUPES_KEY = "trimmed_perks_dupes"

    # Core perks for counters
    CORE_PERKS_KEY = "core_perks"
    CORE_TRIMMED_PERKS_KEY = "core_trimmed_perks"

    # Flags for wishlist requirements
    REQ_TRIMMED_PERKS = "req_trimmed_perks"  # 3rd, 4th, origin traits
    REQ_DUPES = "req_dupes"  # Rolls appear min_count times

    MIN_ROLL_COUNT = 2  # Minimum number of rolls to for dupe rolls

    BATCH_SIZE = 500  # Numebr of rolls held for wishlist before writing

    # Counters for perks and weapons
    CORE_COUNTER = Counter()  # Counter of core perks
    TRIMMED_COUNTER = Counter()  # Counter for core trimmed perks
    WEAPON_COUNTER = Counter()  # Counter for appearences of weapons
