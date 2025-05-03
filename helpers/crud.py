import os
import json
from pathlib import PurePath, Path
from helpers.utilities import *
import traceback

# CREATE
def create_new_json_file(passedFileName: str, passedDirectoryPath: str, dict_to_convert: dict) -> bool:
    result = False
    error_message = ""
    str_target_directory_path = passedDirectoryPath
    str_target_file_name = passedFileName + '.json'
    str_target_file_path = str_target_directory_path + '\\' + str_target_file_name
    json_obj = ''

    json_obj = convert_obj_to_json(dict_to_convert)

    # casting to Path 
    target_directory_path = Path(str_target_directory_path)
    target_file_path = Path(str_target_file_path)

    if target_directory_path.exists():
        if(target_file_path.exists()):
            error_message = "Error: " + str_target_file_name + " already exists."
        else:
            f = open(str_target_file_path, "w")
            f.write(json_obj)
            f.close()
            result = True
    else:
        error_message = "Incorrect Path: directory not found for file creation!"

    if result == True:
        return result
    else:
        print(error_message)
        return result

# Takes a file path and tries to create it at that location.
def create_new_directory(passed_directory_path: str) -> dict:
    # TODO: Fix this one's error handling.
    result = { 'created': False, 'create_folder_message': '' }
    error_message = ""

    try:
        Path(passed_directory_path).mkdir(parents=True, exist_ok=False)
        result['created'] = True
        result['create_folder_message'] = "Successfully created the folder!"
    except Exception:
        result['create_folder_message'] = traceback.format_exc()
        result['created'] = False
    
    return result

# READ
# Single JSON getter with known file name & file path.
def single_json_getter(passedFileName: str, passedDirectoryPath: str, objectType: str) -> dict:
# This handles loading a JSON File
    error_message = ""
    target_object = ""
    fetch_success = False


    if objectType == 'template':
        str_target_directory_path = passedDirectoryPath
        str_target_file_name = passedFileName + '.json'
        str_target_file_path = str_target_directory_path + '\\' + str_target_file_name
    elif objectType == 'asset':
        str_target_directory_path = passedDirectoryPath
        str_target_file_name = passedFileName + '.json'
        str_target_file_path = str_target_directory_path + '\\' + str_target_file_name
    else:
        str_target_directory_path = passedDirectoryPath + '\\' + passedFileName
        str_target_file_name = passedFileName + '.json'
        str_target_file_path = str_target_directory_path + '\\' + str_target_file_name


    # casting to Path 
    target_directory_path = Path(str_target_directory_path)
    target_file_path = Path(str_target_file_path)

    if target_directory_path.exists():
        if(target_file_path.exists()):
            with open(str_target_file_path) as f:
                target_object = json.load(f)
            f.close()
            fetch_success = True
        else:
            error_message = "Error: " + str_target_file_name + " not found within Directory."
    else:
        error_message = "Error getting JSON File: \n Incorrect Path. " + objectType + " directory not found!"

    if fetch_success == True:
        return target_object
    else:
        print(error_message)

# single JSON getter with known, full file path
def single_json_getter_fullpath(passed_file_path: str, objectType: str) -> dict:
# This handles loading a JSON File
    error_message = ""
    target_object = ""
    fetch_success = False
    get_json_result = {'result': False, 'message': '', 'json': target_object}

    if len(passed_file_path) == 0:
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

# Multi-file names getter: all the names with .json of the files at known filepath
# TODO: better error handling
def multi_json_names_getter(passedDirectoryPath: str, objectType: str) -> list:
    error_message = ""
    unsplit_objects = []
    object_names = []
    str_directory_path = passedDirectoryPath
    fetch_success = False

    # casting to Path 
    directory_path = Path(str_directory_path)

    if directory_path.exists():
        # check each directory in the directory for **/*.json file
        jsonslist = sorted(Path(directory_path).glob('**/*.json'))
        
        # for each json file in the list, get the name.
        for x in (jsonslist):
            y = PurePath(x)
            unsplit_objects.append(y.name)
        fetch_success = True
        # Split the names
        for object in unsplit_objects:
            name = object.split(".")
            object_names.append(name[0])
    else:
         # TODO: change to pass error_message back
        print("Incorrect Path: " + objectType + " directory for names not found!")

    if(fetch_success == True):
        return object_names
    else:
        print(error_message)

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

# Get the names of the targetted object types
# objectType = 'games' or 'assets'
# targetpathkey = 'osrootpath' or 'gamespath' or 'assetspath'
def multi_file_names_getter(passedDirectoryPath: str, objectType: str, debug: bool = False) -> dict:
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
            for category in ["Defaults", "Customs"]:
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

# get json template as dict
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
       str_full_path = str_directory_path + 'template_game.json'
    elif template_type =='save':
       str_full_path = str_directory_path + 'template_save.json'
    elif template_type == 'asset':
       str_full_path = str_directory_path + 'template_asset.json'
    elif template_type == 'effect':
       str_full_path = str_directory_path + 'template_effect.json'
    elif template_type == 'event':
       str_full_path = str_directory_path + 'template_event.json'
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
# Delete a folder & contents
# TODO: this
def delete_directory(directory_path: str,):
   result =  user_confirm("Are you sure you want to do this?")

# TODO: this
def delete_file(file_path: str):
    a = 1+1

# TODO: Save this for when Error Handler is more up and running >__> 
# And the forgiveness helpers. wtb confirm boxes.