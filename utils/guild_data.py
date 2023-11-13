import json

def get_guild_level_data(exp):
    """
    The function `get_guild_level_data` calculates the guild level, remaining experience, and total
    experience based on the given experience points.
    
    @param exp The "exp" parameter represents the amount of experience points that a guild has.
    
    @return The function `get_guild_level_data` returns a tuple containing the following values:
    """
    EXP_NEEDED = [
        100000,
        150000,
        250000,
        500000,
        750000,
        1000000,
        1250000,
        1500000,
        2000000,
        2500000,
        2500000,
        2500000,
        2500000,
        2500000,
        3000000,
    ]

    level = 0
    total_exp = 0  # Initialize total experience points

    for i in range(1001):
        if i >= len(EXP_NEEDED):
            need = EXP_NEEDED[-1]
        else:
            need = EXP_NEEDED[i]

        if exp - need < 0:
            exp_needed = need
            exp_remaining = need - exp
            guild_level = round((level + exp / need), 2)
            total_exp += exp  # Accumulate total experience points
            return guild_level, exp, exp_needed, exp_remaining, total_exp
        level += 1
        total_exp += need  # Accumulate total experience points
        exp -= need

    return 1000, 0, 0, 0, total_exp  # Level cap and default values if not found




def search_uuid_and_return_name(json_file, uuid):
    """
    The function searches for a given UUID in a JSON file and returns the corresponding name if found,
    or an error message if not found or if there is an error.
    
    @param json_file The `json_file` parameter is the path to the JSON file that contains the data you
    want to search. It should be a string representing the file path, including the file extension
    (e.g., "data.json").
    @param uuid The `uuid` parameter is a unique identifier that is used to search for a specific entry
    in the JSON file.
    
    @return The function `search_uuid_and_return_name` returns the name associated with the given UUID
    if it is found in the JSON file. If the UUID is not found, it returns the string "UUID not found".
    If the JSON file is not found, it returns the string "JSON file not found". If any other error
    occurs, it returns a string indicating that an error occurred along with the specific error
    """
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            usernames = data.get('usernames', {})
            name = usernames.get(uuid, None)
            return name
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    
    
def update_username(json_path, uuid, new_username):
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        if uuid in data:
            data["usernames"][uuid] = new_username

        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

        # print("Username updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")