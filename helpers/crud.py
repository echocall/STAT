import json
from pathlib import Path
from helpers.utilities import *
import traceback
import os
import shutil
import datetime
from nicegui import app

# CREATE
def create_new_json_file(full_file_path: str, dict_to_convert: dict, include_debug: bool = False) -> dict:
    result_dict = {
        'result': False,
        'message': '',
        'path': str(full_file_path),
    }

    debug_info = {}

    target_file_path = Path(full_file_path)
    target_directory_path = target_file_path.parent

    try:
        json_obj = convert_obj_to_json(dict_to_convert)
        if include_debug:
            debug_info['json_size'] = len(json_obj)
    except Exception as e:
        result_dict['message'] = f"Error converting dictionary to JSON: {e}"
        if include_debug:
            debug_info['conversion_error'] = str(e)
        result_dict['debug'] = debug_info
        return result_dict

    if include_debug:
        debug_info['directory_exists'] = target_directory_path.exists()
        debug_info['file_exists'] = target_file_path.exists()
        debug_info['directory'] = str(target_directory_path)
        debug_info['filename'] = target_file_path.name

    if not target_directory_path.exists():
        result_dict['message'] = f"Directory not found: {target_directory_path}"
        if include_debug:
            result_dict['debug'] = debug_info
        return result_dict

    if target_file_path.exists():
        result_dict['message'] = f"File already exists: {target_file_path.name}"
        if include_debug:
            result_dict['debug'] = debug_info
        return result_dict

    try:
        with target_file_path.open("w", encoding="utf-8") as f:
            f.write(json_obj)
        result_dict['result'] = True
        result_dict['message'] = "File created successfully."
    except Exception as e:
        result_dict['message'] = f"Error writing file: {e}"
        if include_debug:
            debug_info['write_error'] = str(e)

    if include_debug:
        result_dict['debug'] = debug_info

    return result_dict

# Takes a directory path and tries to create a folder at that location.
def create_new_directory(passed_directory_path: str, debug_mode: bool = False) -> dict:
    result_dict = {
        'result': False,
        'message': '',
    }

    try:
        Path(passed_directory_path).mkdir(parents=True, exist_ok=False)
        result_dict['result'] = True
        result_dict['message'] = "Successfully created the folder."
    except FileExistsError:
        result_dict['message'] = "Directory already exists."
        if debug_mode:
            result_dict['debug'] = f"The path '{passed_directory_path}' already exists."
    except PermissionError as e:
        result_dict['message'] = "Permission denied while creating the folder."
        if debug_mode:
            result_dict['debug'] = str(e)
    except Exception as e:
        result_dict['message'] = "An unexpected error occurred while creating the folder."
        if debug_mode:
            result_dict['debug'] = traceback.format_exc()

    return result_dict

# READ
# single JSON getter with known, full file path
def single_json_getter_fullpath(passed_file_path: str, objectType: str) -> dict:
    """Fetches a json file as part of a result_dict. Result_dict keys: 'result', 'message', 'json'. """
    error_message = ""
    target_object = ""
    fetch_success = False
    get_json_result = {'result': False, 'message': '', 'json': target_object}

    if len(str(passed_file_path)) == 0:
        get_json_result['result'] = False
        get_json_result['message'] = "Error: empty filepath! cannot find " + objectType
        get_json_result['json'] = {}
        return get_json_result
    else:
        target_file_path = Path(passed_file_path)

        if(target_file_path.exists()):
            with open(target_file_path) as f:
                target_object = json.load(f)
            f.close()
            fetch_success = True
        else:
            error_message = "Error: The filepath: " + str(target_file_path) + " for "+ objectType +" does not exist. Please check against values in config.txt"

        if fetch_success == True:
            get_json_result['result']=fetch_success
            get_json_result['message']= "Success!"
            get_json_result['json'] = target_object
        else:
            get_json_result['result']=fetch_success
            get_json_result['message']= error_message
            get_json_result['json'] = target_object

        return get_json_result

def get_default_assets_list(passed_directory_path: str) -> list:
    """Returns a list of parsed default asset JSON objects from the 'default' subfolder of assets."""
    default_assets = []
    default_path = Path(passed_directory_path) 

    if not default_path.exists():
        print("[get_default_assets_list] 'default' path does not exist:", default_path)
        return []

    for json_file in default_path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                default_assets.append(data)
        except Exception as e:
            print(f"[get_default_assets_list] Failed to load {json_file.name}: {e}")

    return default_assets

def get_custom_assets_list(passed_directory_path: str) -> list:
    """Returns a list of parsed custom asset JSON objects from the 'custom' subfolder of assets."""
    custom_assets = []
    custom_path = Path(passed_directory_path)

    if not custom_path.exists():
        print("[get_custom_assets_list] 'custom' path does not exist:", custom_path)
        return []

    for json_file in custom_path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                custom_assets.append(data)
        except Exception as e:
            print(f"[get_custom_assets_list] Failed to load {json_file.name}: {e}")

    return custom_assets

# takes in a full file path and object type as plural, returns list of jsons.
def multi_file_getter(passedDirectoryPath: str, objectType: str) -> list:
    """Takes a directory path and an object type as a plural and returns a list of jsons.
    IF using with effects, assets, or events: do NOT send in the directory path for the custom or default 
    directories. It already handles that and returns both default and custom objects as a shared list."""
    directory_path = Path(passedDirectoryPath)
    # Path does not exist
    if not directory_path.exists():
        print(f"Incorrect Path: {objectType} directory for names not found!")
        return []

    target_json_objects = []

    # if the looked for objectType is game, only go down to the GAMES folder
    if objectType.lower() == "games":
        # Look for *.json in each game folder directly under 'games'
        for subdir in directory_path.iterdir():
            if subdir.is_dir():
                json_files = list(subdir.glob("*.json"))
                for json_file in json_files:
                    with json_file.open('r', encoding='utf-8') as f:
                        try:
                            target_json_objects.append(json.load(f))
                        except json.JSONDecodeError as e:
                            print(f"Error decoding {json_file}: {e}")
    # If we are looking for assets, effect, or events
    elif objectType.lower() in {"assets", "effects", "events"}:
        # Look in 'default' and 'custom' inside passed-in directory
        for category in ["default", "custom"]:
            category_path = directory_path / category
            if category_path.exists():
                for json_file in category_path.glob("*.json"):
                    with json_file.open('r', encoding='utf-8') as f:
                        try:
                            target_json_objects.append(json.load(f))
                        except json.JSONDecodeError as e:
                            print(f"Error decoding {json_file}: {e}")
    # If we are looking for saves
    elif objectType.lower() in {"saves"}:
        for subdir in directory_path.iterdir():
            if subdir.is_dir():
                for json_file in directory_path.glob("*.json"):
                    with json_file.open('r', encoding='utf-8') as f:
                        try:
                            target_json_objects.append(json.load(f))
                        except json.JSONDecodeError as e:
                            print(f"Error decoding {json_file}: {e}")
    # Getting images.
    elif objectType.lower() == "images":
        allowed_extensions = {".png", ".bmp", ".gif", ".jpeg"}
        for subdir in directory_path.iterdir():
            if subdir.is_dir():
                for file in subdir.iterdir():
                    if file.suffix.lower() in allowed_extensions:
                        target_json_objects.append(file)
    else:
        # Default: scan all .json files recursively
        for json_file in directory_path.rglob("*.json"):
            with json_file.open('r', encoding='utf-8') as f:
                try:
                    target_json_objects.append(json.load(f))
                except json.JSONDecodeError as e:
                    print(f"Error decoding {json_file}: {e}")

    return target_json_objects

# Get the names of the targetted object types
# objectType = 'games' or 'assets'
# targetpathkey = 'osrootpath' or 'gamespath' or 'assetspath'
def multi_file_names_getter(passedDirectoryPath: str, objectType: str, debug: bool = False) -> dict:
    """Gets all the file names. Takes objectType as a plural. returns a result_dict of 'result':bool, 'message":'str', and 'list':[]"""
    result = {
        'result': False,
        'message': '',
        'list': []
    }
    if debug:
        result['debug'] = []

    object_names = []
    directory_path = Path(passedDirectoryPath)

    if not directory_path.exists():
        result['message'] = f"Incorrect Path: {objectType} directory not found at {passedDirectoryPath}"
        return result

    try:
        if objectType.lower() == "games":
            for subdir in directory_path.iterdir():
                if subdir.is_dir():
                    for json_file in subdir.glob("*.json"):
                        object_names.append(json_file.stem)
                        if debug:
                            result['debug'].append(f"Found game JSON: {json_file}")

        elif objectType.lower() in {"assets", "effects", "events"}:
            for category in ["default", "custom"]:
                category_path = directory_path / category
                if category_path.exists():
                    for json_file in category_path.glob("*.json"):
                        object_names.append(json_file.stem)
                        if debug:
                            result['debug'].append(f"Found {objectType} JSON in {category}: {json_file}")

        elif objectType.lower() == "saves":
            for subdir in directory_path.iterdir():
                if subdir.is_dir():
                    for json_file in subdir.glob("*.json"):
                        object_names.append(json_file.stem)
                        if debug:
                            result['debug'].append(f"Found save JSON: {json_file}")

        elif objectType.lower() == "images":
            allowed_extensions = {".png", ".bmp", ".gif", ".jpeg"}
            for subdir in directory_path.iterdir():
                if subdir.is_dir():
                    for file in subdir.iterdir():
                        if file.suffix.lower() in allowed_extensions:
                            object_names.append(file.stem)
                            if debug:
                                result['debug'].append(f"Found image: {file}")

        else:
            for json_file in directory_path.rglob("*.json"):
                object_names.append(json_file.stem)
                if debug:
                    result['debug'].append(f"Found JSON: {json_file}")

        result['result'] = True
        result['message'] = "Success!"
        result['list'] = sorted(object_names)

    except Exception as e:
        result['message'] = f"An unexpected error occurred while getting {objectType} names."
        print(f"{e}\n{traceback.format_exc()}")
        if debug:
            result['debug'].append(f"Exception: {e}\n{traceback.format_exc()}")

    return result


def get_default_assets_names(full_base_path: str) -> list:
    """Returns a list of default asset JSON files from the 'default' subfolder of assets."""
    default_assets = []
    default_path = Path(full_base_path)

    if not default_path.exists():
        print("[get_default_assets_list] 'default' path does not exist:", default_path)
        return []

    for json_file in default_path.glob("*.json"):
        default_assets.append(json_file)

    return default_assets


def get_custom_assets_names(full_base_path: str) -> list:
    """Returns a list of custom asset JSON files from the 'custom' subfolder of assets."""
    custom_assets = []
    custom_path = Path(full_base_path)

    if not custom_path.exists():
        print("[get_custom_assets_list] 'custom' path does not exist:", custom_path)
        return []

    for json_file in custom_path.glob("*.json"):
        custom_assets.append(json_file)

    return custom_assets

# get json template as dict, returns template dict
def get_template_json(template_type: str) -> dict:
    """Takes the Template type, and return the template dict.
    Handles calculating the template path itself."""
    # Get the paths
    user_config = app.storage.user.get("config", {})
    paths = user_config.get("Paths",{})
    rootpath = paths.get('osrootpath', "Not Set")
    targetted_path = paths.get('templatespath', "Not Set")
    str_directory_path = rootpath + targetted_path
    str_full_path = ''
    template = {}
    error_message = ""
    
    if template_type == 'game':
       str_full_path = str_directory_path + '\\' + 'template_game.json'
    elif template_type =='save':
       str_full_path = str_directory_path + '\\' + 'template_save.json'
    elif template_type == 'asset':
       str_full_path = str_directory_path + '\\' + 'template_asset.json'
    elif template_type == 'effect':
       str_full_path = str_directory_path + '\\' + 'template_effect.json'
    elif template_type == 'event':
       str_full_path = str_directory_path + '\\' + 'template_event.json'
    else:
        error_message = "Template type not recognized."
        return error_message
    
    full_path = Path(str_full_path)
    try:
        template_result = single_json_getter_fullpath(full_path, 'template')
        if template_result['result']:
            template = template_result['json']
        else:
            print("Error fetching template.")
            template = {}
        return template
    except Exception as e:
        # TODO: Handle this error better as a progroam
        print(f"An unexpected error occurred while getting game names. See terminal for more.")
        print(f"{e}\n{traceback.format_exc()}")
        return template

# UPDATE
def overwrite_json_file(data: dict, str_target_file_path: str, file_name: str) -> dict:
    """
    Overwrites or creates a JSON file at the file path.
        data (dict): The dictionary to write to the JSON file.
        directory_path (str): The directory where the file is located.
        file_name (str): The name of the file (without extension).

    Returns:
        dict: A result dictionary with 'success' (bool) and 'message' (str).
    """
    result = {'success': False, 'message': ''}
    try:
        # Convert the dictionary to a JSON string
        json_obj = json.dumps(data, indent=4)

        target_file_path = Path(str_target_file_path)
        print(target_file_path)

        # Write the JSON data to the file
        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(json_obj)

        result['success'] = True
        result['message'] = f"File successfully written to {target_file_path}"
        return result

    except FileNotFoundError as e:
        result['message'] = f"FileNotFoundError: {e}"
    except PermissionError as e:
        result['message'] = f"PermissionError: {e}"
    except Exception as e:
        result['message'] = f"An unexpected error occurred: {e}\n{traceback.format_exc()}"

    return result


# Logging for file.
def log_debug(message: str):
    """Appends a debug message to the debug log file."""
    # Define root path for logs
    user_config = app.storage.user.get("config", {})
    paths = user_config.get("Paths", {})
    root_path = paths.get("osrootpath", "Not Set")
    debug_piece = paths.get('debugpath', "Not Set")
    str_debug_path = root_path + debug_piece
    debug_path = Path(str_debug_path)
    debug_log_path = os.path.join(debug_path, 'debug.log')
    try:
        os.makedirs(debug_path, exist_ok=True)
        with open(debug_log_path, 'a') as log_file:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f'[{timestamp}] {message}\n')
    except Exception as e:
        # As a last resort, print to console
        print(f'Failed to log message: {e}')

# DELETE
def delete_directory(directory_path: str):
    """Deletes a directory and all its contents."""
    try:
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            shutil.rmtree(directory_path)
            log_debug(f"Successfully deleted directory: {directory_path}")
        else:
            log_debug(f"Directory not found: {directory_path}")
    except Exception as e:
        log_debug(f"Error deleting directory '{directory_path}': {e}")


def delete_file(file_path: str):
    """Deletes a single file."""
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            log_debug(f"Successfully deleted file: {file_path}")
        else:
            log_debug(f"File not found: {file_path}")
    except Exception as e:
        log_debug(f"Error deleting file '{file_path}': {e}")

