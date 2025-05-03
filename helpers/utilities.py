import configparser
import json
from pathlib import Path

# load file paths from config.txt
# Reworked from utilities -> stat_initializer
def load_config(config_file: str):
    # Reading from config file
    configParser = configparser.ConfigParser()
    configFilePath = config_file
    configParser.sections()
    configParser.read(configFilePath)

    config_dict = {}
    # We want to preserve the sections for organization later
    for Section in configParser.sections():
        temp_dict = {}
        # Create a temporary diction that gets added to the Sectiond ictionary
        for key, value in configParser[Section].items():
            temp_dict.update({key:value})
        config_dict[Section] = temp_dict

    # Return the organized dictionary
    return config_dict

def format_str_for_filename(string: str) -> str:
    # TODO: Upgrade this to use regex to strip unwanted characters.
    error_message = ""
    formatted_string = ""
    try:
        formatted_string = str(string).strip().lower().replace(" ", "_")
    except:
        error_message = "An error occured while trying to format the string."
        return error_message
    else:
        return formatted_string

# Returns a result dictionary    
def format_str_for_filename_super(string: str) -> dict:
    # TODO: Upgrade this to use regex to strip unwanted characters.
    result_dict = {'result':False, 'string':""}
    error_message = ""
    formatted_string = ""
    try:
        formatted_string = str(string).strip().lower().replace(" ", "_")
        result_dict['result'] = True
        result_dict['string'] = formatted_string
    except:
        error_message = "An error occured while trying to format the string."
        result_dict['string'] = formatted_string =  error_message
    else:
        return result_dict

# takes in a list of objects (objects[]), and a key, returns all value of key.
def filter_list_value_with_set(initialList: list, keyInList: str) -> list:
    filter_set = {"set", "set2"} 
    filtered_list = []
    error_message = ""
    filter_successful = False

    # clearing out unneeded values from our set.
    filter_set.clear()

    if len(initialList) <= 0:
        error_message = "Initial List empty. Unable to filter list."
    else:
        # getting the different Asset Types for later processing.
        for item in initialList:
            filter_set.add(item[keyInList])
               
        for x in filter_set:
            filtered_list.append(x)
        filter_successful = True

    if filter_successful == True:
        return filtered_list
    else:
        return error_message

# compare two lists, return bool and missing items.
def list_compare(initialList: list, secondList: list) -> dict:
    match = False
    error_message = ""
    missing_objects = []
    initial_list_size = len(initialList)
    second_list_size = len(secondList)
    result = { "match": False, "missing_values": []}
    
    if initial_list_size > 0 and second_list_size > 0: 
        for item in initialList:
            if item in secondList:
                match = True
            else: 
                error_message = f"Supplied value does not exist in second list: {item!r}"
                missing_objects.append(item)
                match = False

        if len(missing_objects) > 0:
            result["match"] = match
            result["missing_values"] = missing_objects
            return(result)
        else:
            # "Check complete. Lists have same objects."
            result["match"] = match
            result["missing_values"] = missing_objects
            return(result)
    else:
        error_message = "Both lists are empty."
        print(error_message)

def dict_key_compare(initialDict: dict, secondDict: dict) -> dict:
    result = { "match": False, "missing_values": []}
    mismatch_found = False
    error_message = ""
    try:
        for key in secondDict.keys():
            if not key in initialDict:
                rmismatch_found = True
                result["missing_values"].append(key)
    except:
        error_message = "Could not compare the dictionaries."
    
    if mismatch_found == False:
        result["match"] = True
    
    return result

def list_to_lowercase(parentList: list) -> list:
    newList = []
    for x in parentList:
        try: 
           newList.append(x.lower())
        except ValueError:
            print(
                f"List has non-string values: {x!r}",
                sep="\n",
            )
    return newList

# merge two lists of dictionaries into one
def merge_dict_lists(defaultList: list, customList: list, conflictCheck: dict) -> list:
    merged_dict_list = []

    if conflictCheck["match"] == False:
        # no conflict, merge the dicts together.
        for item in defaultList:
            merged_dict_list.append(item)
        for item in customList:
                merged_dict_list.append(item)
    else:
        # there's a conflict! Something has an custom.
        print(conflictCheck["missing_list"])
        for item in conflictCheck("missing_list"):
            try:
                # merge in the object from the custom instead
                item_name = item["name"]
                merged_dict_list.append(customList[item_name])
            except ValueError:
                # doesn't exist in the customList
                merged_dict_list.add(item)

    return merged_dict_list

# convert a dictionary to json
def convert_obj_to_json(dict_to_convert: dict) -> str:
    # TODO: look into Pydantic along this line.
    try:
        json_obj = json.dumps(dict_to_convert, indent=4)
        return json_obj
    except Exception as e:
        print(f"Could not convert the dictionary to json file: {e}")
        return ""

# builds the result dictionary
def handler_result_builder(missing_default: bool, missing_name: str,
                            missing_objects: list, converted_name: str,
                              converted_objects: list )-> dict:
    handler_result = {"missing_default": missing_default, missing_name: missing_objects, 
                      converted_name: converted_objects}
    return handler_result
