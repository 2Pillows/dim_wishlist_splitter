import json


#####################################
# Takes data from origin_traits.txt #
#####################################
def get_origin_traits():
    # Empty array to hold origin trait hashes
    origin_traits = []
    # Path to origin trait file
    origin_traits_path = "./src/wishlist_splitter/data/origin_traits/origin_traits.txt"

    # Open and read the JSON file
    with open(origin_traits_path, "r", encoding="utf-8") as file:
        origin_traits = json.load(file)

    return origin_traits
