from helpers.crud import *
from helpers.utilities import *
from pathlib import Path
import json
from datetime import datetime
import traceback

def save_handler():
    print("TODO: Handle the saves of various games.")

# return a dictionary of all the saves associated with a game
def get_saves(saves_directory_path: str) -> dict:
    save_names = []
    save_names = get_save_names(saves_directory_path)
    full_save_path = ''
    get_save_result = {}
    save_files = {}

    for save in save_names:
        save_name = save.lower()
        full_save_path = Path(saves_directory_path + '\\' + save_name + '\\' + save_name + ".json")
        get_save_result = single_json_getter_fullpath(full_save_path, 'save')

        ## checking the saves
        if get_save_result['result']:
            save_files[save] = get_save_result['json']
        else:
            get_save_result['message'] = "Failed! Could not retrieve the saves."

    if save_files:
        return save_files
    else:
        return {}

# for creating a new save from the gui
def new_save_gui(game_name: str, new_save_dict: dict) -> dict:
    write_result = {'result': False, 'string': '', 'dict': {}, 'debug': []}
    create_result = {'result': False, 'message': '', 'dict':{}}
    try:
        # Format game name
        game_name_result = format_str_for_filename_super(game_name)
        write_result['debug'].append({'game_name_result': game_name_result})
        if not game_name_result['result']:
            raise ValueError("Failed to format game name.")
        game_name_formatted = game_name_result['string']

        # Format save name
        save_format_result = format_str_for_filename_super(new_save_dict['name'])
        
        # Load config and paths
        user_config = app.storage.user.get("config", {})
        paths = user_config.get("Paths", {})
        root_path = paths.get("osrootpath", "")
        games_path = paths.get("gamespath", "")
        saves_path = paths.get("savespath", "")

        write_result['debug'].append({'save_format_result': save_format_result})
        if not save_format_result['result']:
            raise ValueError("Failed to format save name.")
        file_name = save_format_result['string']

        # Build full save directory path: <root>/<games>/<game>/<saves>/<file_name>/
        str_save_directory = root_path + games_path + '//' + game_name_formatted + saves_path + '//' + file_name 
        str_saves_path = root_path + games_path + '//' + game_name_formatted + saves_path
        save_directory = Path(str_save_directory) 
        saves_path = Path(str_saves_path)
        save_file_path = Path(save_directory / f"{file_name}.json")
        debug_log_path = Path(saves_path / f"{file_name}_debug.log")

        # Create directory
        dir_create_result = create_new_directory(str(save_directory), debug_mode=True)
        write_result['debug'].append({'directory_creation': dir_create_result})

        # Check if directory creation failed in a meaningful way
        if not dir_create_result['result'] and "already exists" not in dir_create_result['message'].lower():
            write_result['string'] = "Failed to create save folder."
            return write_result

        # Ensure the save name is updated/unique
        new_save_name = new_save_dict['name']
        resolved_name = get_new_save_name(str(save_directory.parent), new_save_name)
        write_result['debug'].append({'resolved_save_name': resolved_name})

        # Set timestamps
        date_created = datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        new_save_dict['create_date'] = date_created
        new_save_dict['date_last_save'] = date_created

        # Write save file
        create_result = create_new_json_file(str(save_file_path), new_save_dict)
        write_result['debug'].append({'save_path': str(save_file_path)})

        if create_result['result']:
            create_result['string'] = 'Successfully wrote save to file.'
            create_result['dict'] = new_save_dict
        else:
            create_result['string'] = "Warning, could not write new save to JSON file."

    except Exception:
        error_info = traceback.format_exc()
        write_result['string'] = "Unhandled exception occurred."
        write_result['debug'].append({'exception': error_info})

    # Write debug log
    try:
        debug_text = json.dumps(write_result['debug'], indent=2)
        debug_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(debug_log_path, 'w') as log_file:
            log_file.write(debug_text)
    except Exception as log_exception:
        write_result['debug'].append({'log_error': str(log_exception)})

    return create_result

# RThe list of names.
def get_save_names(directory_path: str) -> list:
    save_names = []
    save_names_result = {'result': False, 'message':"", 'list': []}
    save_names_result = multi_file_names_getter(directory_path, "saves")
    if save_names_result['result']:
        save_names = save_names_result['list']
    else:
        print("Error! Problem with fetching save names.")
    return save_names

# Convert the save name into a file friendly format.
def convert_save_name(saveName: str) -> str:
    formatted_name = ""
    try:
        formatted_name = saveName.strip()
        formatted_name = formatted_name.lower()
        formatted_name = formatted_name.replace(" ", "_")
    except Exception:
            print(traceback.format_exc())
    return formatted_name

# return a result dictionary from getting a single json file
def load_save(full_save_path: str) -> dict:
    load_save_result = {}
    load_save_result = single_json_getter_fullpath(full_save_path, 'save')
    if load_save_result['result']:
        save = load_save_result
        return save
    else:
        print("Error with returning save!")
        return {}

# Checks the save dict's keys against the keys of the save template.
def check_save_template_bool(save: dict, template_path: str) -> bool:
    error_message = ''
    result = False
    try:
        save_template = get_template_json("save", template_path)
        result = dict_key_compare(save_template, save)
        return result
    except Exception:
        print(traceback.format_exc())
        return result

# Returne a dictionary of {"name": "", "file":""} of formatted save name
def get_new_save_name(directory_path: str, name: str, ) -> dict:
    file_name = ""
    saves = []
    save_name = {"name": "", "file":""}
    valid = False

    while not valid:
        file_name = format_str_for_filename(name)

        # check that a game by that name doesn't already exists
        saves_result = multi_file_names_getter(directory_path, "saves")
        
        if saves_result['result']:
            saves = saves_result['list']
        else:
            print("Error! Could not get the file saves name.")
        
        if name in saves:
    # if file_name already exists, append placeholder and alert user
            valid = True
            save_name["name"] = name + "_Placeholder"
            save_name["file"] = file_name + "_placeholder"
        else:
            valid = True
            save_name["name"] = name
            save_name["file"] = file_name

    return  save_name

# TODO: Test
# Save a save dictionary to a JSON file
def update_save(save_dict: dict, save_path: str, template_path: str) -> dict:
    template_result = {}
    format_result = {}
    write_result = {}
    # check the template is okay
    try:
        template_result = check_save_template_bool(save_path, template_path)
    except:
        template_result['result'] = False
        template_result['message'] = 'Given object did not match save template.'
  
    # it matches the template!
    if template_result['result']:
        # try formatting the save name for a file
        try:
            format_result = format_str_for_filename_super(save_path['name'])
        except:
            format_result['message'] = 'Formatting name for save update failed.'

        # it formatted the name!
        if format_result['result']:
            # try writing to the json_file
            try:
                write_result = overwrite_json_file(save_dict, save_path, format_result['string'])
            except:
                write_result['success'] = False
                write_result['message'] = 'Overwriting to save json failed.'
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

# TODO:
def save_current(old_save: dict, new_save: dict):
    print("TODO: save current STAT instance to save file.")
    # Call update save functions in MySave

# TODO
def save_as_new_file():
    print("TODO: Create a new save file.")

# delete a directory and its files
def delete_all_saves(save_directory_path) -> bool:
    all_delete_result = False
    """ deletes a save's folder and everything inside. Return a bool."""
    try:
        delete_directory(save_directory_path)
        all_delete_result = True
    except Exception:
        print(traceback.format_exc())

    return all_delete_result

# delete a save file at the specified path.
def delete_save_file(asve_file_path: str) -> bool:
    """ deletes a save's file. Return a bool."""
    save_delete_result = False
    try:
        delete_file(asve_file_path)
        save_delete_result = True
    except Exception:
        print(traceback.format_exc())

    return save_delete_result
