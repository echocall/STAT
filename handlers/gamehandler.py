from helpers.crud import *
from helpers.utilities import *
from handlers.assethandler import * # TODO: Change this later.
import classes.MyGame as mg
import traceback

def game_handler(is_game_loaded: bool) -> object:
    print("TODO: fill game_handler in")
    load_options = ["Create new Game JSON", "Select Game JSON"]
    # Check STAT instance for "is_game_loaded"
    if not is_game_loaded:
        print("Does user want to create a JSON for a new game,",
            " or load a preexisting game JSON?", sep="\n"
        )
     
def new_game_gui(game_path: str,datapack_path: str, save_path: str,  new_game_dict: dict, file_name: str) -> bool:
    write_successful = False
    error_message = ""

    try:
        # Write the paths for the folder locations
        new_game_dict['actor_default_path'] = datapack_path + "\\" + new_game_dict['name'] + "\\actors"
        new_game_dict['asset_default_path'] = datapack_path + "\\" + new_game_dict['name'] + "\\assets"
        new_game_dict['effect_default_path'] = datapack_path + "\\" + new_game_dict['name'] + "\\effects"
        new_game_dict['event_default_path'] = datapack_path + "\\" + new_game_dict['name'] + "\\events"
        new_game_dict['save_files_path'] = save_path + "\\" + new_game_dict['name']
        new_game_dict['image_file_path'] = game_path + "\\" + new_game_dict['name'] + "\\images"

        write_successful = create_new_json_file(file_name, game_path, new_game_dict)
    except Exception:
        print(traceback.format_exc())

    if write_successful == True:
        return True
    else:
        error_message = "Warning, could not save new game to JSON file."
        return False
     
def new_game_console(game_path: str, saves_path: str, datapack_path: str) -> dict:
    new_game_dict = {}
    new_file_name = ""
    write_successful = False
    error_message = ""
    
    want_explanations = user_confirm("Do you want explanations of what each field in a game is or does?")
    if want_explanations:
        # call new_game_assembly_loud
        a = 1+1
    else:
        # call new_game_assembly_quiet
        b = 2+2

    try:
        new_game_dict = new_game_assembly_console(game_path, saves_path, datapack_path)
    except Exception:
        print(traceback.format_exc())
    try:
        new_file_name = format_str_for_filename(new_game_dict["name"])
    except Exception:
        print(traceback.format_exc())
    # Save data in a json file.
    try:
        write_successful = create_new_json_file(new_file_name, game_path, new_game_dict)
    except Exception:
        print(traceback.format_exc())

    if write_successful == True:
        return new_game_dict
    else:
        error_message = "Warning, could not save new game to JSON file."
        return error_message

def get_game(game_name: str, file_path: str, type: str) -> dict:
    game = single_json_getter(game_name, file_path, type)
    return game

def get_games(file_path: str) -> dict:
    game_names = get_games_names(file_path)
    
    all_games = {}
    for name in game_names:
        all_games[name] = get_game(name, file_path, "game")
    
    return all_games

def get_game_as_obj(game_name: str, file_path: str, type: str) -> object:
    game = single_json_getter(game_name, file_path, type)
    game_object = {}
    game_object = dict_to_game_object(game)
    return game_object

def get_games_names(filePath: str) -> list:
    game_names = []
    game_names = multi_json_names_getter(filePath, "games")

    return game_names

# TODO: finish
def update_game(gameName: str, filePath: str, type: str, key: str, newValue) -> bool:
    game = {}
    result = False
    

    # Find the value we want to change and change it in the object
    print(game[key])
    game[key] = newValue

    # Write the dict back to the file as JSON object.
    result = overwrite_json_file(game, filePath, gameName)

    return result

def get_game_saves(filePath: str, gameName: str) -> list:
    # get game name
    game_saves_path = filePath + gameName
    save_names = multi_json_names_getter(game_saves_path)

    return save_names

def check_template(game: dict) -> object:
    error_message = ''
    try:
        game_template = get_template_json("game",".\\statassets\\templates")
        result = dict_key_compare(game_template, game)
    except Exception:
        print(traceback.format_exc())

    if result["match"] == True:
        game_object = dict_to_game_object(game)
        return game_object
    else:
        print(error_message)
        print(result["missing_values"])

def check_template_bool(game: dict, template_path: str) -> bool:
    error_message = ''
    result = False
    try:
        game_template = get_template_json("game", template_path)
        result = dict_key_compare(game_template, game)
        return result
    except Exception:
        print(traceback.format_exc())
        return result
    
# select game
def select_game(file_path: str) -> object:
    games = []
    target_game = ''
    target_dict = {}
    game_object = {}
    # load list of game names from games folder.
    games = multi_json_names_getter(file_path, 'games')

    # call List_to_Menu
    target_game = list_to_menu('Select a game: ', games)

    # load in the game_dict
    target_dict = get_game(target_game, file_path, 'game')

    # turn the game dict into a game_object
    game_object = dict_to_game_object(target_dict)

    return game_object

# dict_to_game_object
def dict_to_game_object(targetDict: dict) -> object:
    # get name of the dictionary and insubstantiate into a class object.
    class_object = {}
    classObjName = "c" + targetDict["name"]
    classObjName = format_str_for_filename(classObjName)
    try: 
        return mg.MyGame(**targetDict)
    except Exception:
        print(traceback.format_exc())

# TODO: Finish Assets, Events, Effects, and Actors
# TODO: Make 'quiet' and 'loud' variants
def new_game_assembly_console(game_path: str, datapack_path: str, saves_path: str) -> dict:
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

    # TODO: separate explantion of counters for loud/quiet split
    new_game["counters"] = create_counters()

    # TODO: Actors
    print()
    print("You can create actors later.")
    create_actors = user_confirm("Do you want to add actors to the game now? ")
    if create_actors == True:
        # call actorsHandler's create Actors.
        # created_actors = createActors()
        new_game["has_actors"] = True
        new_game["actor_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\actors"
        new_game["default_actors"] = multi_json_names_getter(new_game["actor_default_path"], "actors")
    else:
        # not creating actors now.
        new_game["has_actors"] = False
        new_game["actor_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\actors"
        new_game["default_actors"] = []

    # TODO: Assets
    print()
    print("You can create assets later.")
    create_assets = user_confirm("Do you want to add default assets to the game now?")
    if create_assets == True:
        # created_assets = createAssets()
        new_game["has_assets"] = True
        new_game["asset_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\assets"
        asset_explanations = user_confirm("Do you want explanations of the asset fields?")

        # call assetsHandler's create Assets.
        assets_to_create = okay_user_int(0,"How many default assets do you want to create?")
        for index in range(assets_to_create):
            created_asset = new_asset(True, True, new_game["asset_default_path"], "", new_game["name"], asset_explanations,
                                      new_game['counters'])
            created_assets[created_asset.get_name()] = created_asset
        
        print(created_assets)
        print(type(created_assets))
        # TODO: Need to get the names of the assets.
        new_asset_names = []
        for key in created_assets:
            new_asset_names.append(key)

        new_game["default_assets"] = new_asset_names

    else:
        # not creating assets now.
        new_game["has_assets"] = False
        new_game["asset_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\assets"
        new_game["default_assets"] = []
    
    # TODO: Effect
    print()
    print("You can create effects later. ")
    create_effects = user_confirm("Do you want to add effects to the game now?")
    if create_effects == True:
        # call effectsHandler's create Effects.
        # created_effects = createEffects()
        new_game["has_effects"] = True
        new_game["effect_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\effects"
        new_game["default_effects"] = multi_json_names_getter(new_game["effect_default_path"], "effects")
    else:
        # not creating effects now.
        new_game["has_effects"] = False
        new_game["effect_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\effects"
        new_game["default_effects"] = []
    
    # TODO: Events
    print()
    print("You can create events later. ")
    create_events = user_confirm("Do you want to add events to the game now?")
    if create_events == True:
        # call eventsHandler's create Events.
        # created_events = createEvents()
        new_game["has_events"] = True
        new_game["event_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\events"
        new_game["default_events"] = multi_json_names_getter(new_game["event_default_path"], "events")
    else:
        # not creating events now.
        new_game["has_events"] = False
        new_game["event_default_path"] = datapack_path + "\\" + name_dict["file"] + "\\events"
        new_game["default_events"] = []

    # TODO: Icon
    new_game["icon"] = ""
    
    # Save file Path
    new_game["save_files_path"] = saves_path + "\\" + name_dict["file"]

    print()
    # Turns
    turns_prompt = str("Does your game have turns or rounds or a time element? Only whole numbers accepted." + "\n")
    new_game["has_turns"] = user_confirm(turns_prompt)
    if new_game["has_turns"] == True:
        turns = define_turns(name_dict["name"])
        new_game["turn_type"] = turns["turn_type"]
        new_game["start_turn"] = turns["start_turn"]
    else:
        new_game["turn_type"] = ""
        new_game["start_turn"] = 0
    
    # Create the folders.
    # TODO: create more error handling within this chain.
    create_result = create_folders(name_dict, game_path, datapack_path, saves_path)
    if not create_result:
        error_message = "Creating folders failed for new game."

    print()
    try:
        template_game = get_template_json("game",".\\statassets\\templates")
        compare_result = dict_key_compare(template_game, new_game)
    except:
        error_message = "Problem with comparing game_template and the new_game dict."

    if(compare_result["match"] == True):
        return new_game
    else:
        error_message = "Warning: missing fields from new game dictionary."
        print("Missing Fields: ", sep="\n")
        for field in compare_result["missing_values"]:
            print("Missing from new dictionary: " + field)
        # call something to fix the game or fix those specific fields.
        return error_message
    
def get_new_game_name(name: str, file_path: str) -> dict:
    file_name = ""
    games = []
    game_name = {"name": "", "file":""}
    valid = False

    while valid != True:
        file_name = format_str_for_filename(name)

        # check that a game by that name doesn't already exists
        games = multi_json_names_getter(file_path, "games")
        
        if name in games:
    # if file_name already exists, append placeholder and alert user
            valid = True
            game_name["name"] = name + "_Placeholder"
            game_name["file"] = file_name + "_placeholder"
        else:
            valid = True
            game_name["name"] = name
            game_name["file"] = file_name

    return  game_name

def get_new_game_name_console(file_path: str) -> dict:
    file_name = ""
    name = ""
    games = []
    game_name = {"name": "", "file":""}
    valid = False
    
    while valid != True:
        # ask the user for the name of the new game
        name = str(input("Enter the name of the new game: ")).strip()
        file_name = format_str_for_filename(name)

        # check that a game by that name doesn't already exists
        games = multi_json_names_getter(file_path, "games")
        if name in games:
        # if file_name already exists, ask for another game name and show what games exist.
            "A game of that name already exists. You may experience difficulties creating folders for this game."
            if user_confirm("Do you want to enter a new name now?"):
                get_new_game_name_console(file_path)
            else:
                print("\n" + "Appending _placeholder to game name. If further folder creation errors persist, please create a new name. " + "\n")
                valid = True
                game_name["name"] = name + "_Placeholder"
                game_name["file"] = file_name + "_placeholder"
        else:
            valid = True
            game_name["name"] = name
            game_name["file"] = file_name

    return  game_name

def counter_explanation():
    counter_info = """Counters are a way to keep track of numerical values.", 
            "They can be used to represent money, health, points,",
            " or other values where all you need is a name and a number.",
            "Example: Health: 20, Gold: 5, First Level Spell Slots: 20
            
            Counters are interacted with the Buy Costs and Sell Prices of assets.

            The value of a counter defined in a game file is the amount a 
            player starts with."""
    print(counter_info)

def create_counters() -> dict:
    # TODO add error handling
    num_counters = -1
    counters = {}
    # ask for counters
    num_counters = okay_user_int(0, "Enter the number of counters you want to create: ")

    counters = get_user_input_loop(num_counters, "Enter the name then the starting value of the counter: ", "dict", "int")

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

# create the folders for a new game.
def create_folders(name_dict: dict, game_path: str, datapack_path: str, saves_path: str) -> bool:
    folder_created = False
    folders_created = {}
    result = False
    folders = []
    game_folder = game_path + "\\" + name_dict["file"]
    datapack_folder = datapack_path + "\\" + name_dict["file"]
    save_folder = saves_path + "\\" + name_dict["file"]
    images_folder = game_path + "\\" + name_dict["file"] + "\\images\\"

    folders.append(game_folder)
    folders.append(datapack_folder)
    folders.append(save_folder)
    folders.append(images_folder)

    for folder in folders:
        folder_created = create_new_directory(folder)['created']
        folders_created['folder']=folder_created

    if False not in folders_created:
        result = True
    
    return result

# delete a game and its files
def delete_all(name: str, game_path: str, datapack_path: str, saves_path: str) -> bool:
    bln_result = False


    return bln_result

# delete a save
def delete_save(save_name: str, saves_path: str) -> bool:
    bln_result = False


    return bln_result

# delete an asset
def delete_asset(game_name: str, save_name: str, datapack_path: str) -> bool:
    bln_result = False



    return bln_result
