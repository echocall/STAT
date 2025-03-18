import json
from pathlib import PurePath, Path
from utilities import *
import traceback

# CREATE
def create_new_json_file(passedFileName: str, passedDirectoryPath: str, object: dict) -> bool:
    result = False
    error_message = ""
    str_target_directory_path = passedDirectoryPath + '\\' + passedFileName
    str_target_file_name = passedFileName + '.json'
    str_target_file_path = str_target_directory_path + '\\' + str_target_file_name
    json_obj = {}

    json_obj = convert_obj_to_json(object)

    # casting to Path 
    target_directory_path = Path(str_target_directory_path)
    target_file_path = Path(str_target_file_path)

    if target_directory_path.exists():
        if(target_file_path.exists()):
            error_message = "Error: " + str_target_file_name + " already exists."
        else:
            f = open(str_target_file_name, "w")
            f.write(json_obj)
            f.close()
            result = True
    else:
        error_message = "Incorrect Path: directory not found!"

    if result == True:
        return result
    else:
        print(error_message)

# Takes a file path and tries to create it at that location.
def create_new_directory(passed_directory_path: str) -> dict:
    # TODO: Fix this one's error handling.
    result = { 'created': False, 'create_folder_message': '' }
    error_message = ""

    try:
        Path(passed_directory_path).mkdir(parents=False, exist_ok=False)
        result['created'] = True
        result['create_folder_message'] = "Successfully created the folder!"
    except Exception:
        result['create_folder_message'] = traceback.format_exc()
        result['created'] = False;
    
    return result

# READ
# Singe file getter with known file name & file path.
def single_json_getter(passedFileName: str, passedDirectoryPath: str, objectType: str) -> dict:
# This handles loading a JSON File
    error_message = ""
    target_object = ""
    fetch_success = False

    if objectType == 'template':
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
def multi_json_names_getter(passedDirectoryPath: str, objectType: str) -> list:
    error_message = ""
    unsplit_objects = []
    objects = []
    str_directory_path = passedDirectoryPath
    fetch_success = False

    # casting to Path 
    directory_path = Path(str_directory_path)

    if directory_path.exists():
        # check each directory in the directory for **/*.json file
        jsonslist = sorted(Path(directory_path).glob('**/*.json'))

        for x in (jsonslist):
            y = PurePath(x)
            unsplit_objects.append(y.name)
        fetch_success = True
        
    for object in unsplit_objects:
        name = object.split(".")
        objects.append(name[0].capitalize())

    else:
         # TODO: change to pass error_message back
        error_message = "Incorrect Path: " + objectType + " Directory not found!"

    if(fetch_success == True):
        return objects
    else:
        print(error_message)

# get json template as dict
def get_template_json(template_type: str, directory_path: str) -> dict:
    template_file = ""
    template = {}
    error_message = ""
    
    template_file = 'template_' + template_type
    if template_type == 'game':
       template = single_json_getter(template_file, directory_path, "template")
    elif template_type =='save':
       template = single_json_getter(template_file, directory_path, "template")
    elif template_type == 'asset':
       template = single_json_getter(template_file, directory_path, "template")
    elif template_type == 'effect':
       template = single_json_getter(template_file, directory_path, "template")
    elif template_type == 'event':
       template = single_json_getter(template_file, directory_path, "template")
    else:
        error_message = "Template type not recognized."
        return error_message
    return template

# UPDATE
def overwrite_json_file(object: dict, directoryPath: str, fileName: str) -> bool:
    error_message = ""
    str_target_directory_path = directoryPath + '\\' + fileName
    str_target_file_name = fileName + '.json'
    str_target_file_path = str_target_directory_path + '\\' + str_target_file_name
    result = False
    json_obj = {}

    json_obj = convert_obj_to_json(object)

     # casting to Path 
    target_directory_path = Path(str_target_directory_path)
    target_file_path = Path(str_target_file_path)

    # test if gamePath is valid path
    if target_directory_path.exists():
        # game directory is valid, check if file exists
        if(target_file_path.exists()):
            # TODO: Add "are you sure you want to overwrite?" forgiveness
            # overwrite existing file
            f = open(str_target_file_path, "w")
            f.write(json_obj)
            f.close()
            result = True
        else:
            error_message = "Error: " + str_target_file_name + " not found within Directory. Creating new file."
            f = open(str_target_file_name, "w")
            f.write(json_obj)
            f.close()
            result = True
    else:
        error_message = "Incorrect Path: games directory not found!"

    if result == True:
        print(error_message)
        return result
    else:
        print(error_message)

def append_json_file(object: dict, directoryPath: str, fileName: str) -> bool:
    print("TODO: fill this in.")

# DELETE

# Delete a folder & contents
def delete_directory(directoryPath: str,):
   result =  user_confirm("Are you sure you want to do this?")
    

# TODO: Save this for when Error Handler is more up and running >__> 
# And the forgiveness helpers. wtb confirm boxes.