from crud import *
from utilities import *
import MyGame
import StatInstance

def game_handler(is_game_loaded: bool) -> MyGame:
    print("TODO: fill game_handler in")
    # Check STAT instance for "is_game_loaded"
    if not is_game_loaded:
        print("Does user wnat to create a new game,",
            " start a new save of a game,",
            " or load a prexisting save?", sep="\n"
        )


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

def new_game_assembly(game_path: str, saves_path: str, datapack_path) -> dict:
    print("Fill this out.")
    name_dict = {}
    icon = ""
    turns = {}

    create_actors = False
    created_actors = {}
    create_assets = False
    created_assets = {}
    create_events = False
    created_events = {}
    create_effects = False
    created_effects = {}
    new_game = {}

    # get the name, description, and counters of the game
    name_dict = get_new_game_name(game_path)
    new_game["name"] = name_dict["name"]
    new_game["description"] = str(input("Enter a description for the new game: ")).strip()
    new_game["counters"] = create_counters()

    # TODO: Actors
    create_actors = user_confirm("Do you want to add actors to the game now? ")
    if create_actors == True:
        # call actorsHandler's create Actors.
        # created_actors = createActors()
        new_game["has_actors"] = True
        new_game["actor_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\actors"
        new_game["default_actors"] = multi_json_names_getter(new_game["actor_default_path"], "actors")
    else:
        # not creating actors now.
        print("You can create actors later. ")
        new_game["has_actors"] = False
        new_game["actor_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\actors"
        new_game["default_actors"] = []

    # TODO: Assets
    create_assets = user_confirm("Do you want to add assets to the game now?")
    if create_assets == True:
        # call actorsHandler's create Actors.
        # created_assets = createAssets()
        new_game["has_assets"] = True
        new_game["asset_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\assets"
        new_game["default_asset"] = multi_json_names_getter(new_game["asset_default_path"], "assets")
    else:
        # not creating assets now.
        print("You can create assets later. ")
        new_game["has_assets"] = False
        new_game["asset_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\assets"
        new_game["default_assets"] = []
    
    # TODO: Effect
    create_effects = user_confirm("Do you want to add effects to the game now?")
    if create_effects == True:
        # call effectsHandler's create Effects.
        # created_effects = createEffects()
        new_game["has_effects"] = True
        new_game["effect_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\effects"
        new_game["default_effects"] = multi_json_names_getter(new_game["effect_default_path"], "effects")
    else:
        # not creating effects now.
        print("You can create effects later. ")
        new_game["has_effects"] = False
        new_game["effect_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\effects"
        new_game["default_effects"] = []
    
    # TODO: Events
    create_events = user_confirm("Do you want to add events to the game now?")
    if create_events == True:
        # call eventsHandler's create Events.
        # created_events = createEvents()
        new_game["has_events"] = True
        new_game["event_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\events"
        new_game["default_events"] = multi_json_names_getter(new_game["event_default_path"], "events")
    else:
        # not creating events now.
        print("You can create events later. ")
        new_game["has_events"] = False
        new_game["event_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\events"
        new_game["default_event"] = []

    # TODO: Icon
    new_game["icon"] = ""
    # Save file Path
    new_game["save_files_path"] = saves_path + "\\" + name_dict["file"]

    print()
    # Turns
    turns_prompt = str("Does your game have turns or rounds or a time element? Only whole numbers accepted. \n")
    new_game["has_turns"] = user_confirm(turns_prompt)
    turns = define_turns(name_dict["name"])
    new_game["turn_type"] = turns["turn_type"]
    new_game["start_turn"] = turns["start_turn"]
    
    # Create the folders.
    # TODO: create error_message telling us which of these failed/didn't fail
    game_folder_result = game_folder_creator(name_dict["file"], game_path)
    datapack_folder_result = datapack_folder_creator(name_dict["file"], datapack_path)
    save_folder_result = save_folder_creator(name_dict["file"], saves_path)
    image_folder_result = images_folder_creator(name_dict["file"], game_path)

    print()
    if not game_folder_result:
        print("Warning: Game folder for new game was not created!",
            sep="\n")
    elif not datapack_folder_result:
        print("Warning! Datapack folder for new game was not created!",
            sep="\n")
    elif not save_folder_result:
        print("Warning! Save folder for new game not was created!",
            sep="\n")
    elif not image_folder_result:
        print("Warning! Image folder for new game not was created!",
            sep="\n")
    else:
        print("All needed folders created successfully!", sep="\n")

    # TODO: Add checker for checking every key in a JSON 
    # object against every key in a single dictionary.
    try:
        game_template = get_template_json("game",".\\statassets\\templates")
        result = dict_key_compare(game_template, new_game)
    except:
        error_message = "Problem getting game_template.json file for testing."

    if(result["match"] == True):
        return new_game
    else:
        error_message = "Warning, missing fields from new game dictionary."
        print("Warning, missing fields from new game dictionary.",
            sep="\n")
        print("Missing Fields: ", sep="\n")
        for field in result["missing_values"]:
            print("Missing from new dictionary: " + field)
        # call something to fix the game or fix those specific fields.
        return error_message
    

def get_new_game_name(file_path: str) -> dict:
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

def game_folder_creator(game_file_name: str, file_path: str) -> dict:
    result = False
    game_folder = file_path + "\\" + game_file_name
    result = create_new_directory(game_folder)
    return result

def datapack_folder_creator(game_file_name: str, file_path: str) -> dict:
    result = False
    datapack_folder = file_path + "\\" + game_file_name
    result = create_new_directory(datapack_folder)
    return result

def save_folder_creator(game_file_name: str, file_path: str) -> dict:
    result = False
    save_folder = file_path + "\\" + game_file_name
    result = create_new_directory(save_folder)
    return result

def images_folder_creator(game_file_name: str, file_path: str) -> dict:
    result = False
    image_folder = file_path + "\\" + game_file_name + "\\images\\"
    result = create_new_directory(image_folder)
    return result

