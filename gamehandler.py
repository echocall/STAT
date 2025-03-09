from crud import *
from utilities import *
import MyGame

def game_handler():
    print("TODO: fill this in")
    # Check STAT instance for "gameSelected"

def new_game():
    print("TODO: save a new game's information to <gamename>.py")

def get_game(gameName: str, filePath: str, type: str) -> dict:
    game = single_json_getter(gameName, filePath, type)
    game_object = {}
    game_object = load_game(game)
    return game_object

def get_games_names(filePath: str) -> list:
    game_names = []
    game_names = multi_json_names_getter(filePath, "games")

    return game_names

def update_game(gameName: str, filePath: str, type: str, key: str, newValue) -> bool:
    game = {}
    result = False
    # start by loading in the game
    print("TODO: Update this to us the game Class Object instead")
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

def load_game(game: dict) -> dict:
    # TODO 
    game_object = {}
    game_object = dict_to_game_object(game)
    return game_object

# dict_to_game_object
def dict_to_game_object(targetDict: dict) -> dict:
    # get name of the dictionary and insubstantiate into a class object.
    # add class object to dict of class objects. "name":object
    classObjName = "c" + targetDict["name"]
    classObjName = MyGame.MyGame(targetDict)

    return classObjName
