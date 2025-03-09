from crud import *
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
    game = {}
    result = False
    # start by loading in the game
    game = get_game(gameName, filePath, type)

    # Find the value we want to change and change it in the object
    print(game[key])
    game[key] = newValue

    # Write the dict back to the file as JSON object.
    result = overwrite_json_file(game, filePath, gameName)

    return result

def get_game_saves(filePath: str, gameName: str) -> list:
    # get game name
    names_test_path = filePath + gameName
    game_names = multi_json_names_getter(names_test_path)

    return game_names
