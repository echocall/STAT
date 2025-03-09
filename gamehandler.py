from getters import *
from utilities import *
import json

def game_handler():
    print("TODO: fill this in")

def new_game():
    print("TODO: save a new game's information to <gamename>.py")

def get_game(gameName: str, filePath: str, type: str) -> dict:
    game = single_json_getter(gameName, filePath, type)
    return game

def get_games_names(filePath: str) -> list:
    game_names = []
    game_names = multi_json_names_getter(filePath, "games")

    return game_names

def update_game(gameName: str, filePath: str, type: str, key: str, newValue) -> bool:
    print("TODO: update a game's json")
    game = {}
    game_as_json = {}
    result = False
    # start by loading in the game
    game = get_game(gameName, filePath, type)

    # Find the value we want to change and change it in the object
    print(game[key])
    game[key] = newValue

    # convert file to json object
    game_as_json = json.dumps(game, indent=4)
    # Write the dict back to the file as JSON object.
    result = write_game_file(game_as_json, filePath, gameName)

    return result

def write_game_file(game: dict, directoryPath: str, fileName: str) -> bool:
    print("TODO: write JSON game object to existing .JSON file")
    error_message = ""
    str_target_directory_path = directoryPath + '\\' + fileName
    str_target_file_name = fileName + '.json'
    str_target_file_path = str_target_directory_path + '\\' + str_target_file_name
    write_success = False

     # casting to Path 
    target_directory_path = Path(str_target_directory_path)
    target_file_path = Path(str_target_file_path)

    # test if gamePath is valid path
    if target_directory_path.exists():
        # game directory is valid, check if file exists
        if(target_file_path.exists()):
            # overwrite existing file
            f = open(str_target_file_path, "w")
            f.write(game)
            f.close()
            write_success = True
        else:
            # TODO: create new game file
            error_message = "Error: " + str_target_file_name + " not found within Directory."
    else:
        # TODO: change to pass error_message back
        error_message = "Incorrect Path: games directory not found!"
    if write_success == True:
        return write_success
    else:
        # TODO: make this better
        return error_message
    
def get_game_saves(filePath: str, gameName: str) -> list:
    # get game name
    names_test_path = filePath + gameName
    game_names = multi_json_names_getter(names_test_path)

    return game_names
