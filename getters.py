import json
from pathlib import PurePath, Path

# Getters for loading in a game.
# gets the names of all the game.py files in the game directory
def games_names_getter(passed_game_path: str) -> list:
    error_message = ""
    games = []
    str_game_directory_path = passed_game_path
    
    fetch_success = False
    # casting to Path 
    game_directory_path = Path(str_game_directory_path)

    if game_directory_path.exists():
        # check each directory in the directory for **/*.json file
        jsonslist = sorted(Path(game_directory_path).glob('**/*.json'))

        for x in (jsonslist):
            y = PurePath(x)
            games.append(y.name)
        fetch_success = True
    else:
         # TODO: change to pass error_message back
        error_message = "Incorrect Path: Game Directory not found!"

    if(fetch_success == True):
        return games
    else:
        print(error_message)

# Handles retrieving a game.json file by name from the game directory
def game_getter(game_name: str, passed_game_path: str) -> dict:
    # This handles loading a game's basic JSON File
    error_message = ""
    str_game_directory_path = passed_game_path + '\\' + game_name
    str_game_file_path = passed_game_path + '\\' + game_name + '\\' + game_name + '.json'
    str_game_file_name = game_name + '.json'
    target_game = ""
    fetch_success = False

    # casting to Path 
    game_directory_path = Path(str_game_directory_path)
    game_file_path = Path(str_game_file_path)

    # test if gamePath is valid path
    if game_directory_path.exists():
        # game directory is valid, got to get game.
        if(game_file_path.exists()):
            # TODO: Change this into message for user.
            # print("Game file exists!")
            with open(str_game_file_path) as f:
                target_game = json.load(f)
            # target_game = game_file_path.read_text()
            fetch_success = True
        else:
            # TODO: change to pass error_message back
            error_message = "Error: " + str_game_file_name + " not found within Directory."
            fetch_success = False
    else:
        # TODO: change to pass error_message back
        error_message = "Incorrect Path: Game Directory not found!"
        fetch_success = False

    if fetch_success == True:
        return target_game
    else:
        print(error_message)

# Getters for loading in a Save

# Getters for loading in assets
#  Get all Assets as JSON objects/dictionaries from a prticular directory path
def assets_getter(passed_directory_path: str) -> list:
    error_message = ""
    str_asset_directory_path = passed_directory_path
    assets = []
    fetch_success = False

    asset_directory_path = Path(str_asset_directory_path)

    if asset_directory_path.exists():
        jsonslist = list(asset_directory_path.glob('**/*.json'))

        for path in jsonslist:
            with open(path) as f:
                assets.append(json.load(f))
        fetch_success = True
    else:
        error_message = "Assets could not be found in directory: " + str_asset_directory_path

    if(fetch_success == True):
        return assets
    else:
        print(error_message)

#  individual asset with specific name & passed filepath
def asset_getter(asset_name: str, passed_file_path: str) -> dict:
    error_message = ""
    str_asset_directory_path = passed_file_path + '\\' + asset_name
    str_asset_file_path = passed_file_path + '\\' + asset_name + '\\' + asset_name + '.json'
    str_asset_file_name = asset_name + '.json'
    target_asset = {}
    fetch_success = False

    # casting to Path 
    asset_directory_path = Path(str_asset_directory_path)
    asset_file_path = Path(str_asset_file_path)

    if asset_directory_path.Exists():
        if asset_file_path.Exists():
            with open(str_game_file_path) as f:
                target_asset = json.load(f)
            fetch_success = True;
        else:
            error_message = "Error: " + str_asset_file_name + " not found within asset directory: " + str_asset_directory_path
            fetch_success = False
    else:
        # TODO: change to pass error_message back
        error_message = "Incorrect Path: Asset Directory not found! Directory Tried: " + str_asset_directory_path
        fetch_success = False

    if fetch_success == True:
        return target_asset
    else:
        print(error_message)

# Getters for loading in Events

# Getters for loading in Effects

# Getters for loading in Actors
