import json


#####################################
# Takes data from origin_traits.txt #
#####################################
def get_origin_traits(file_path: str):
    # Empty array to hold origin trait hashes
    origin_traits = []

    # Open and read the JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        origin_traits = json.load(file)

    return origin_traits
