from helpers.crud import *
from helpers.utilities import *
from handlers.assethandler import * # TODO: Change this later.
import classes.MyGame as mg
import traceback
import os, shutil

def game_handler(is_game_loaded: bool) -> object:
    print("TODO: fill game_handler in")
     
def new_game_gui(game_path: str,datapack_path: str, save_path: str, configfilename: str, root_path: str, new_game_dict: dict, file_name: str) -> bool:
    write_result = {'result':False,'string':'', 'dict':{}}
    error_message = ""
    save_location = ""

    try:
        # Write the paths for the folder locations
        save_location = game_path + "\\" + file_name
        new_game_dict['actor_default_path'] = datapack_path + "\\" + file_name + "\\default\\actors\\"
        new_game_dict['asset_default_path'] = datapack_path + "\\" + file_name + "\\default\\assets\\"
        new_game_dict['effect_default_path'] = datapack_path + "\\" + file_name + "\\default\\effects\\"
        new_game_dict['event_default_path'] = datapack_path + "\\" + file_name + "\\default\\events\\"
        new_game_dict['save_files_path'] = save_path + "\\" + file_name + "\\"
        new_game_dict['image_file_path'] = game_path + "\\" + file_name + "\\images\\"

        create_new_directory(new_game_dict['actor_default_path'])
        create_new_directory(new_game_dict['asset_default_path'])
        create_new_directory(new_game_dict['effect_default_path'])
        create_new_directory(new_game_dict['event_default_path'])
        create_new_directory(new_game_dict['actor_default_path'])
        
        write_result['result'] = create_new_json_file(file_name, save_location, new_game_dict)
    except Exception:
        print(traceback.format_exc())

    if write_result['result'] == True:
        write_result['string'] = 'Successfully wrote game to file.'
        write_result['dict'] = new_game_dict
        return write_result
    else:
        write_result['string'] = "Warning, could not save new game to JSON file."
        return write_result
     
def get_game(game_name: str, file_path: str, type: str) -> dict:
    game = single_json_getter(game_name, file_path, type)
    return game

# TODO: check get_game part of this for using new filepaths
def get_games(file_path: str, root_path: str) -> dict:
    game_names_result = get_games_names(root_path)
    game_names = []
    get_games_result = {'result': False, 'message': 'Something went wrong...', 'games': {}}
    
    if game_names_result:
        game_names = get_games_names['list']
        all_games = {}
        for name in game_names:
            all_games[name] = get_game(name, file_path, "game")
        get_games_result['result'] = True
        get_games_result['games'] = all_games
    else:
        get_games_result['message'] = "Unable to get the names of the games. Please cheek the gamepath and rootpath in config.txt"
    
    return get_games_result

def get_game_as_obj(game_name: str, file_path: str, type: str) -> object:
    game = single_json_getter(game_name, file_path, type)
    game_object = {}
    game_object = dict_to_game_object(game)
    return game_object

# TODO: Handle errors better as program
def get_games_names(rootpathkey: str) -> dict:
    game_names = []
    game_name_result = {}

    try:
        game_name_result = get_file_names("games", rootpathkey, "gamespath" )
    except Exception as e:
            # TODO: Handle this error better as a progroam
            print(f"An unexpected error occurred while getting game names. See terminal for more.")
            print(f"{e}\n{traceback.format_exc()}")
    finally:
        return game_name_result

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

def counter_explanation():
    counter_info = """Counters are a way to keep track of numerical values.", 
            "They can be used to represent money, health, points,",
            " or other values where all you need is a name and a number.",
            "Example: Health: 20, Gold: 5, First Level Spell Slots: 20
            
            Counters are interacted with the Buy Costs and Sell Prices of assets.

            The value of a counter defined in a game file is the amount a 
            player starts with."""
    print(counter_info)

# TODO: more try catches
def define_turns(game_name: str) -> dict:
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

    game_folder = game_path + "\\" + name_dict["file"] + "\\"
    datapack_folder = datapack_path + "\\" + name_dict["file"] + "\\"
    save_folder = saves_path + "\\" + name_dict["file"] + "\\"
    images_folder = game_path + "\\" + name_dict["file"] + "\\images\\"
    actors_folder = datapack_path + "\\" + name_dict["file"] + "\\default\\actors\\"
    asset_folder = datapack_path + "\\" + name_dict["file"] + "\\default\\assets\\"
    effects_folder = datapack_path + "\\" + name_dict["file"] + "\\default\\effects\\"
    events_folder = datapack_path + "\\" + name_dict["file"] + "\\default\\events\\"

    folders.append(game_folder)
    folders.append(datapack_folder)
    folders.append(save_folder)
    folders.append(images_folder)
    folders.append(actors_folder)
    folders.append(asset_folder)
    folders.append(effects_folder)
    folders.append(events_folder)

    for folder in folders:
        folder_created = create_new_directory(folder)['created']
        folders_created['folder']=folder_created

    if False not in folders_created:
        result = True
    
    return result

# TODO: test
# updates the game's json
def update_game(game_dict: dict, game_path: str, template_path: str):
    template_result = {}
    format_result = {}
    write_result = {}
    # check the template is okay
    try:
        template_result['result'] = check_template_bool(game_dict, template_path)
    except:
        template_result['result'] = False
        template_result['message'] = 'Given object did not match game template.'
  
    # it matches the template!
    if template_result['result']:
        # try formatting the game name for a string
        try:
            format_result = format_str_for_filename_super(game_dict['name'])
        except:
            format_result['result'] = False
            format_result['message'] = 'Formatting name for game update failed.'

        # it formatted the name!
        if format_result['result']:
            # try writing to the json_file
            try:
                write_result = overwrite_json_file(game_dict, game_path, format_result['string'])
            except:
                write_result['success'] = False
                write_result['message'] = 'Overwriting to game json failed.'
            # successfully wrote!
            if write_result['success']:
                return write_result
            # did not successfully write
            else:
                return write_result
        # did not formate name
        else:
            return format_result
    # did not get a match on the template
    else:
        return template_result


# TODO: implement
# delete a game and its files
def delete_all(name: str, game_dict: dict, game_path: str, datapack_path: str, saves_path: str) -> bool:
    bln_result = False
    
    for filename in os.listdir(saves_path):
        file_path = os.path.join(saves_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("failed to delete %s. Reason: %s: " % (file_path, e))

    return bln_result

# TODO:
# This be called AFTER delete_save in save_handler
# and AFTER delete_asset(s) in asset_handler
def delete_game(game_dict: dict):
    omega = "end"
    # ensure no children (assets, saves, or effects) exist
    # delte folder with shutil.rmtree('/path/to/folder')