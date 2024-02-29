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


def main():
    # Dictionary to store constants that reference keys or values
    helper = {
        # Path of voltron file
        "VOLTRON_PATH": "./wishlist_splitter/data/dim-wish-list-sources/voltron.txt",
        ############################
        # Keys for wishlist config #
        ############################
        "PATH_KEY": "path",
        "WISHLIST_DIR": "./wishlists/",
        "CREDIT_KEY": "credits",
        "CREDIT_TAG": "credits",
        "AUTHOR_KEY": "author",
        "INC_TAG_KEY": "include",
        "EXC_TAG_KEY": "exclude",
        "DESCRIPTION_KEY": "description",
        "PERK_KEY": "perks",
        "DUPE_PERKS_KEY": "dupe",
        ######################################
        # Keys for storing data from voltron #
        ######################################
        # Key for storing if a voltron roll includes extra perks
        "EXTRA_PERK_KEY": "extra_perks",
        # Key for storing list of base perks (only 1st, 2nd, 3rd, and 4th columns)
        "BASE_PERK_KEY": "base_perks",
        # Key for storing filtered perks (3rd and 4th columns with any extra perks)
        "FILTERED_PERK_KEY": "filtered_perks",
        # Key for storing base perks that have been filtered (only 3rd and 4th column)
        "BASE_FILTERED_PERK_KEY": "base_filtered_perks",
    }

    # Pass helper keys to get wishlist configs with matching keys
    WISHLIST_CONFIGS = get_wishlist_config(
        helper["PATH_KEY"],
        helper["WISHLIST_DIR"],
        helper["AUTHOR_KEY"],
        helper["INC_TAG_KEY"],
        helper["EXC_TAG_KEY"],
        helper["PERK_KEY"],
        helper["DUPE_PERKS_KEY"],
    )

    # Collect origin trait hashes
    # Path to origin trait file
    origin_traits_path = "./wishlist_splitter/data/origin_traits/origin_traits.txt"
    ORIGIN_TRAITS = get_origin_traits(origin_traits_path)

    # Collect all, include, and exlcude tags from config
    ALL_TAGS, INC_TAGS, EXC_TAGS = extract_tags(
        WISHLIST_CONFIGS,
        helper["INC_TAG_KEY"],
        helper["EXC_TAG_KEY"],
    )

    # Collect all author names in config
    AUTHOR_NAMES = extract_authors(
        WISHLIST_CONFIGS,
        helper["AUTHOR_KEY"],
    )

    # Update helper with new objects
    helper.update(
        {
            # Dictionary storing wishlist information
            "WISHLIST_CONFIGS": WISHLIST_CONFIGS,
            # List of origin trait hashes
            "ORIGIN_TRAITS": ORIGIN_TRAITS,
            # List of tag values for all, include, and exclude
            "ALL_TAGS": ALL_TAGS,
            "INC_TAGS": INC_TAGS,
            "EXC_TAGS": EXC_TAGS,
            # List of author names
            "AUTHOR_NAMES": AUTHOR_NAMES,
        }
    )

    # Collect data from voltron
    voltron_data = extract_voltron_data(helper)

    # Write voltron data to config files
    write_to_wishlists(voltron_data, helper)


if __name__ == "__main__":
    main()
