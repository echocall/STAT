from crud import *
from utilities import *
import MyGame

def game_handler():
    print("TODO: fill this in")
    # Check STAT instance for "gameSelected"

def new_game():
    print("TODO: write a new game's info to a class, then save it to .py")

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

def assemble_game(file_path: str):
    print("Fill this out.")
    name = ""
    description = ""
    counters = ""
    turn_reply = ""
    turns_exist = bool
    turns = {}

    # get the guts of the game
    name = get_new_game_name(file_path)
    description = str(input("Enter a description for the new game: ")).strip()
    counters = create_counters()
    # TODO: Actors

    # TODO: Assets

    # TODO: Effects

    # TODO: Events

    # TODO: Icon

    # TODO: savesFilePath

    # TODO: Turns
    turn_reply = list_to_menu
    turns = define_turns(name)
    # format the game name for use in file directory
        # .lower().strip().remove(" ", _)
    # call create file to save the game.

def get_new_game_name(file_path: str) -> str:
    file_name = ""
    name = ""
    games = []
    result = {}
    game_name = {"name": "", "file":""}
    valid = False
    
    while valid != True:
        # ask the user for the name of the new game
        name = str(input("Enter the name of the new game: ")).strip()
        file_name = format_str_for_filename(name)

        # check that a game by that name doesn't already exists
        games = multi_json_names_getter(file_path, "games")
        result = list_compare(games, file_name)

        # if file_name already exists, ask for another game name and show what games exist.
        if result["match"] == True:
           print("A game of that name already exists, pick another one!", sep="\n")
           print("Games that exist: " + games, sep="\n")
        else:
            valid = True
            game_name["name"] = name
            game_name["file"] = file_name
    return  game_name

def create_counters() -> dict:
    # TODO add error handling
    print(
            f"Counters are a way to keep track of numerical values.", 
            "They can be used to represent money, health, points,",
            " or other values where all you need is a name and a number.",
            "Example: Health: 20, Gold: 5",
            sep="\n",
          )
    num_counters = -1
    counters = {}
    # define a counter
    # provide an example of a counter
    # ask for counters
    num_counters = okay_user_int(0, "Enter the number of counters you want to create: ")

    counters = get_user_input_loop(num_counters, "Enter the name then value of the counter: ", "dict", "int")

    return counters

def define_turns(game_name: str) -> dict:
    # TODO: more try catches
    turns = {"turn_type" : "", "start_turn" : 0 }
    prompt = "Pick how " + game_name + " increments through turns."
    type_result = ""

    # define the type of turn
    type_result = list_to_menu(prompt, ["Increasing","Decreasing"])
    if type_result == "cancel":
       print("TODO: handle a cancel from list_to_menu")
    else:
        turns["turn_type"] = "Decreasing"
        turns["start_turn"] = okay_user_int(0, "Enter what turn number your save should start at: ")

    return turns