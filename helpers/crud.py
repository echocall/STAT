
import json
from pathlib import Path
from helpers.utilities import *
import traceback
import os
import shutil
import datetime

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
# This handles loading a JSON File
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

# DEFUNCT    
# Multi-file getter: all .jsons at known filepath.
def multi_json_getter(passedDirectoryPath: str, objectType: str) -> list:
    error_message = ""
    target_json_objects = []
    str_directory_path = passedDirectoryPath
    fetch_success = False

    # casting to Path 
    directory_path = Path(str_directory_path)

    if directory_path.exists():
        jsonslist = list(directory_path.glob('**/*.json'))

        for path in jsonslist:
            with open(path) as f:
                target_json_objects.append(json.load(f))
        fetch_success = True
    else:
        error_message = "Error getting multiple jsons: \n " + objectType + " could not be found in directory: " + str_directory_path

    if(fetch_success == True):
        return target_json_objects
    else:
        print(error_message)

# takes in a full file path and object type as plural, returns list of jsons.
def multi_file_getter(passedDirectoryPath: str, objectType: str) -> list:
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
                    target_json_objects.append(json_file)
    # If we are looking for assets, effect, or events
    elif objectType.lower() in {"assets", "effects", "events"}:
        # Look in 'default' and 'custom' inside passed-in directory
        for category in ["default", "custom"]:
            category_path = directory_path / category
            if category_path.exists():
                for json_file in category_path.glob("*.json"):
                    target_json_objects.append(json_file)
    # If we are looking for saves
    elif objectType.lower() in {"saves"}:
        for subdir in directory_path.iterdir():
            if subdir.is_dir():
                for json_file in directory_path.glob("*.json"):
                    target_json_objects.append(json_file)
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
            target_json_objects.append(json_file)

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

# get json template as dict, returns template dict
def get_template_json(template_type: str, directory_path: str) -> dict:
    configfilename = 'config.txt'
    # Store as nested dictionary
    config = get_config_as_dict(configfilename)
    # Get the paths
    paths = config.get("Paths",{})
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

# gets the config files as a nested dictionary
def get_config_as_dict(configfilename: str) -> dict:
    # getting config information
    config_data = load_config('config.txt')
    structured_data = {}
    # Create organized nested structure for config.
    for key in config_data:
        structured_data[key] = config_data[key]

    # Store as nested dictionary
    config = structured_data
    return config


# UPDATE
# TODO: test
def overwrite_json_file(data: dict, directory_path: str, file_name: str) -> dict:
    """
    Overwrites or creates a JSON file in the specified directory.

    Args:
        data (dict): The dictionary to write to the JSON file.
        directory_path (str): The directory where the file is located.
        file_name (str): The name of the file (without extension).

    Returns:
        dict: A result dictionary with 'success' (bool) and 'message' (str).
    """
    result = {'success': False, 'message': ''}
    try:
        # Construct paths using pathlib
        target_directory_path = Path(directory_path)
        target_file_path = target_directory_path / f"{file_name}.json"

        # Ensure the directory exists
        if not target_directory_path.exists():
            result['message'] = f"Directory not found: {directory_path}"
            return result

        # Convert the dictionary to a JSON string
        json_obj = json.dumps(data, indent=4)

        # Check if the file exists
        if target_file_path.exists():
            # Add confirmation logic (e.g., user confirmation)
            print(f"File {target_file_path} already exists. Overwriting...")

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

# DELETE

# Logging for file.
def log_debug(message: str):
    """Appends a debug message to the debug log file."""
    # Define root path for logs
    config = get_config_as_dict(config.txt)
    paths = config.get("Paths", {})
    root_path = paths.get("osrootpath", "Not Set")
    osrootpath = Path(root_path)  # Replace with your real root path
    debug_log_path = os.path.join(osrootpath, 'debug.log')
    try:
        os.makedirs(osrootpath, exist_ok=True)
        with open(debug_log_path, 'a') as log_file:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f'[{timestamp}] {message}\n')
    except Exception as e:
        # As a last resort, print to console
        print(f'Failed to log message: {e}')


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

