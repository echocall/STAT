from helpers.crud import *
from helpers.utilities import *
from handlers.assethandler import * # TODO: Change this later.
import classes.MyGame as mg
import traceback
from pathlib import Path
import os, shutil

def game_handler(is_game_loaded: bool) -> object:
    print("TODO: fill game_handler in")
     
def new_game_gui(configfilename: str, new_game_dict: dict, file_name: str) -> dict:
    write_result = {'result': False, 'string': '', 'dict': {}, 'debug': []}
    file_name = ""
    try:
        # Load configuration
        config = get_config_as_dict(configfilename)
        paths = config.get("Paths", {})
        root_path = paths.get("osrootpath", "Not Set")
        games_path = paths.get("gamespath", "")
        saves_path = paths.get("savespath", "")
        default_assets_path = paths.get("defaultassetspath", "")
        custom_assets_path = paths.get("customassetspath", "")
        default_effects_path = paths.get("defaulteffectspath", "")
        custom_effects_path = paths.get("customeffectspath", "")
        default_events_path = paths.get("defaulteventspath", "")
        custom_events_path = paths.get("customeventspath", "")
        images_path = paths.get("imagespath", "")

        game_name_result = format_str_for_filename_super(new_game_dict['name'])
        write_result['debug'].append({'game_name_result': game_name_result})
        file_name = game_name_result['string']

        # Assemble full directory paths
        games_directory_path = Path(root_path + games_path)
        game_base_path = Path(root_path + games_path) / file_name
        game_file_path = game_base_path / f"{file_name}.json"
        debug_log_path = games_directory_path / f"{file_name}_debug.log"

        image_dir = game_base_path / images_path.strip("\\")
        saves_dir = game_base_path / saves_path.strip("\\")
        default_assets_dir = game_base_path / default_assets_path.strip("\\")
        custom_assets_dir = game_base_path / custom_assets_path.strip("\\")
        default_effects_dir = game_base_path / default_effects_path.strip("\\")
        custom_effects_dir = game_base_path / custom_effects_path.strip("\\")
        default_events_dir = game_base_path / default_events_path.strip("\\")
        custom_events_dir = game_base_path / custom_events_path.strip("\\")

        # Create required directories
        dir_results = []
        for path in [
            image_dir,
            saves_dir,
            default_assets_dir,
            custom_assets_dir,
            default_effects_dir,
            custom_effects_dir,
            default_events_dir,
            custom_events_dir,
        ]:
            dir_results.append(create_new_directory(str(path)))

        write_result['debug'].append({'created_dirs': dir_results})

        # Write the new game dictionary to file
        json_result = create_new_json_file(str(game_file_path), new_game_dict)
        write_result['debug'].append({'json_result': json_result})

        if json_result['result']:
            write_result['result'] = True
            write_result['string'] = 'Successfully wrote game to file.'
            write_result['dict'] = new_game_dict
        else:
            write_result['string'] = 'Failed to write game to file.'
    except Exception:
        error_info = traceback.format_exc()
        write_result['string'] = "Unhandled exception occurred."
        write_result['debug'].append({'exception': error_info})

    # Save debug info to log file
    try:
        debug_text = json.dumps(write_result['debug'], indent=2)
        debug_log_path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
        with open(debug_log_path, 'w') as log_file:
            log_file.write(debug_text)
    except Exception as log_exception:
        write_result['debug'].append({'log_error': str(log_exception)})

    return write_result

# return a result_dict hopefully with the game in 'json'     
def get_game(file_path: str) -> dict:
    """Get a single game dictionary as part of a result_dict.
     Forwards result_dict: {'result':bool, 'message':str, 'json':dict} """
    get_game_result = single_json_getter_fullpath(file_path, 'game')
    return get_game_result

def get_games(directory_path: str) -> dict:
    """Fetch all the games and package into a
      dictionary of {'game_name':{game_dict}} and put into
        the 'games' field of a result_dict. """
    game_names_result = get_games_names(directory_path)
    game_names = []
    get_games_result = {'result': False, 'message': 'Something went wrong...', 'games': {}}
    
    if game_names_result:
        game_names = game_names_result['list']
        all_games = {}
        for name in game_names:
            str_game_path = directory_path  + '\\' + name + '\\' + name +  '.json'
            all_games[name] = get_game(str_game_path)['json']
        get_games_result['result'] = True
        get_games_result['games'] = all_games
    else:
        get_games_result['message'] = "Unable to get the names of the games. Please cheek the gamepath and rootpath in config.txt"
    
    return get_games_result

def get_games_names(directory_path: str) -> dict:
    """Return a result_dict with a 'list' of names."""
    game_name_result = {}
    try:
        game_name_result = multi_file_names_getter(directory_path, "games" )
    except Exception as e:
            # TODO: Handle this error better as a progroam
            print(f"An unexpected error occurred while getting game names. See terminal for more.")
            print(f"{e}\n{traceback.format_exc()}")
    finally:
        return game_name_result

def check_game_template_bool(game_dict: dict) -> bool:
    """"Takes a game dict and template path and checks if the game dict matches the template.
    Only needs the game_dict to be checked."""
    error_message = ''
    result = {}
    try:
        game_template = get_template_json("game")
        result = dict_key_compare(game_template, game_dict)
        return result
    except Exception:
        print(traceback.format_exc())
        return result
    
def dict_to_game_object(targetDict: dict) -> object:
    """"Takes a dictionary and returns it as a MyGame object."""
    # get name of the dictionary and insubstantiate into a class object.
    class_object = {}
    classObjName = "c" + targetDict["name"]
    classObjName = format_str_for_filename(classObjName)
    try: 
        return mg.MyGame(**targetDict)
    except Exception:
        print(traceback.format_exc())

def get_new_game_name(name: str, file_path: str) -> dict:
    """Checks if the given name is already a game's name, returns a result_dict"""
    file_name = ""
    games = []
    games_names_result = {}
    game_name = {"name": "", "file":""}
    valid = False

    while valid != True:
        file_name = format_str_for_filename(name)

        # check that a game by that name doesn't already exists
        games_names_result = multi_file_names_getter(file_path, "games")
        
        if games_names_result['result']:
            games = games_names_result['list']

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


# updates the game's json
def update_game(game_dict: dict):
    """Takes a game dict, a full game_file_path, and a template and attempts to update the json."""
    config = get_config_as_dict('static/config.txt')
    

    paths = config.get("Paths", {})
    root_path = paths.get("osrootpath", "Not Set")
    games_path = paths.get("gamespath", "")
    game_name = ''

    template_result = {}
    format_result = {}
    write_result = {'result':False, 'message':''}
    
    # check against the template
    # Currently bugged so removed for now.
    """
    try:
        template_result = check_game_template_bool(game_dict)['result]']
        
    except:
        template_result['result'] = False
        template_result['message'] = 'Given object did not match game template.'
    """

    # it matches the template!
   # if template_result['result']:
        # try formatting the game name for a string
    try:
        format_result = format_str_for_filename_super(game_dict['name'])
    except:
        format_result['result'] = False
        format_result['message'] = 'Formatting name for game update failed.'

    # it formatted the name!
    if format_result['result']:
        # Create the game path.
        str_game_path = root_path + games_path + '\\' + format_result['string'] + '\\' + format_result['string'] + '.json'

        # try writing to the json_file
        try:
            write_result = overwrite_json_file(game_dict, str_game_path, format_result['string'])
        except:
            write_result['result'] = False
            write_result['message'] = 'Overwriting to game json failed.'
        # successfully wrote!
        if write_result or write_result['result']:
            write_result['result'] = True
            write_result['message'] = 'Successfully wrote to the file!'
        # did not successfully write
        else:
            write_result['message'] = 'Did not successfully update file.'
    # did not format name
    else:
        write_result['message'] = 'Formatting the name failed!'
    # did not get a match on the template
    #else:
    #    write_result['message'] = 'Failed at matching the template.'
    
    return write_result


# delete a game and its files
def delete_all(game_directory_path) -> bool:
    all_delete_result = False
    """ deletes a game's folder and everything inside. Return a bool."""
    try:
        delete_directory(game_directory_path)
        all_delete_result = True
    except Exception:
        print(traceback.format_exc())

    return all_delete_result

# delete a game file at the specified path.
def delete_game_file(game_file_path: str) -> bool:
    """ deletes a game's folder and everything inside. Return a bool."""
    game_delete_result = False
    try:
        delete_file(game_file_path)
        game_delete_result = True
    except Exception:
        print(traceback.format_exc())

    return game_delete_result