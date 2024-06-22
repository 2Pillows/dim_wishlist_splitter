# main.py

# Import keys
from helper_scripts.keys import Keys

# Import helper functions
from data.wishlist_configs import get_wishlist_config
from helper_scripts.get_weapon_mods import get_weapon_mods
from helper_scripts.extract_voltron_data import extract_voltron_data
from helper_scripts.write_to_wishlists import write_to_wishlists

# Timer to test script performance
import time

start_time = time.time()


def main() -> None:
    # Create object for Keys
    keys = Keys()

    # Get wishlist data and save to keys
    # Wishlist names are exported as well
    get_wishlist_config(keys)

    # Collect origin trait and frame mod hashes to keys
    get_weapon_mods(keys)

    # Collect data from voltron to keys
    extract_voltron_data(keys)

    # Timer for script performance before writing
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Runtime before write: {runtime} seconds")

    # Write voltron data to wishlist files
    write_to_wishlists(keys)


if __name__ == "__main__":
    main()

    # Timer for script performance
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Runtime: {runtime} seconds")
