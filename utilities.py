import sys
import configparser
from os import system
import json
from pathlib import Path
import MyGame
import MyAsset

def stat_initialize(config_file: str) -> dict:
    # Reading from config file
    configParser = configparser.RawConfigParser()
    configFilePath = config_file
    configParser.sections()
    configParser.read(configFilePath)

    filePaths = {}

    for x in configParser['Paths']:
            filePaths[x] = configParser['Paths'][x]
    return filePaths

def get_user_int(upper_limit: int, prompt: str, examples: str) -> int:
    valid = False
    while not valid:
        print(prompt, examples, sep="\n")
        input_variable = input("Enter the value and press enter: ").strip()
        try:
            input_variable = int(input_variable)
        except ValueError:
            print(
                f"Supplied value is not an integer: {input_variable!r}",
                "Please try again.",
                sep="\n",
            )
        else:
            if input_variable > upper_limit:
                print(
                    f"Supplied value is too large: {input_variable} > {upper_limit}",
                    "Please try again.",
                    sep="\n",
                )
            else:
                valid = True

    return input_variable

# asset Set to List handler
# takes in an arry of assets (assets[]), and a key.
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
def list_compare(initialList: list, secondList: list):
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
        print("TODO: handle conflict custom in utilities merge_lists()")
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

def convert_obj_to_json(object: dict) -> dict:
    print("TODO: Error_handling")
    json_obj = json.dumps(object, indent=4)

    return json_obj

def handler_result_builder(missing_default: bool, missing_name: str, missing_objects: list,
                            converted_name: str, converted_objects: list )-> dict:
    handler_result = {"missing_default": missing_default, missing_name: missing_objects, 
                      converted_name: converted_objects}
    return handler_result

# INPUTS FROM USER
# basic user confirmation y/n
def user_confirm(prompt: str) -> bool:
    valid = False
    bln_continue = bool

    while not valid:
        print(prompt, sep="\n")
        input_variable = input("Are you sure you want to continue? (Yes/No) ").strip().upper()
        if input_variable == "NO":
            bln_continue = False
            valid = True
        elif input_variable == "YES":
            bln_continue = True
            valid = True
        else:
            print(
                    f"Type yes to continue or no to cancel.",
                    "Please try again.",
                    sep="\n",
                )
    return bln_continue

# get an integer from the user with error handling.
def get_user_int(prompt: str) -> int:
    valid = False
    while not valid:
        print(prompt, sep="\n")
        input_variable = input("Enter the value and press enter: ").strip()
        try:
            input_variable = int(input_variable)
        except ValueError:
            print(
                f"Supplied value is not an integer: {input_variable!r}",
                "Please try again.",
                sep="\n",
            )

    return input_variable

