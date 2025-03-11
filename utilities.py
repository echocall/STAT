import configparser
import json
from pathlib import Path

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

# convert a dictionary to json
def convert_obj_to_json(object: dict) -> dict:
    print("TODO: Error_handling")
    json_obj = json.dumps(object, indent=4)

    return json_obj

# builds the result dictionary
def handler_result_builder(missing_default: bool, missing_name: str,
                            missing_objects: list, converted_name: str,
                              converted_objects: list )-> dict:
    handler_result = {"missing_default": missing_default, missing_name: missing_objects, 
                      converted_name: converted_objects}
    return handler_result


# ==  INPUTS FROM USER ==
# basic user confirmation y/n
def user_confirm(prompt: str) -> bool:
    valid = False
    bln_continue = bool

    while not valid:
        input_variable = input(prompt + "Type (Yes/No): ").strip().upper()
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
            valid = True
        except ValueError:
            print(
                f"Supplied value is not an integer: {input_variable!r}",
                "Please try again.",
                sep="\n",
            )
    return input_variable

def okay_user_int(lower_limit: int, prompt: str) -> int:
    valid = False
    while not valid:
        print(prompt, sep="\n")
        input_variable = input("Enter the value and press enter: ").strip()
        try:
            input_variable = int(input_variable)
            valid = True
        except ValueError:
            print(
                f"Supplied value is not an integer: {input_variable!r}",
                "Please try again.",
                sep="\n",
            )
        else:
            if input_variable < lower_limit:
                print(
                    f"Supplied value is too small: {input_variable} < {lower_limit}",
                    "Please try again.",
                    sep="\n",
                )
            else:
                valid = True
    return input_variable

# get an integer from the user with error handling.
def better_user_int(upper_limit: int, prompt: str) -> int:
    valid = False
    while not valid:
        print(prompt, sep="\n")
        input_variable = input("Enter the value and press enter: ").strip()
        try:
            input_variable = int(input_variable)
            valid = True
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
            elif input_variable < -2:
                print(
                    f"Number out of bounds!",
                    "Please try again.",
                    sep="\n"
                )
            else:
                valid = True
    return input_variable

def best_user_int(upper_limit: int, lower_limit: int, prompt: str) -> int:
    valid = False
    while not valid:
        print(prompt, sep="\n")
        input_variable = input("Enter the value and press enter: ").strip()
        try:
            input_variable = int(input_variable)
            valid = True
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
            elif input_variable < lower_limit:
                print(
                    f"Number below lower limit. Lower limit: {lower_limit}",
                    "Please try again.",
                    sep="\n"
                )
            else:
                valid = True
    return input_variable

# get a single key:value pair from user
def get_single_dict_value(prompt: str, field_name: str, field_type: str) -> dict:
    # example: get_dict_value("Enter a default start value for gold: ", "gold")
    error_message = ""  
    result = {field_name : 0}
    
    # ask user for what value type we are looking for.
    data_type = field_type
    
    print(prompt, sep="\n")
    if data_type == "str":
        # get a string
        try: 
            field_value = str(input("Please enter a string for the value of field "+ field_name + ": ")).strip()
        except:
            error_message = "field_value was not entered as a string."
        else:
            result[field_name] = field_value
            return result
    elif type(data_type == "int"):
        # get an int
        field_value = get_user_int("Please enter a number: ")
        result[field_name] = field_value
        return result
    else:
        error_message = "Error retrieving value from user for dictionary field."
    return error_message

def get_list_value(list_name: str):
    print("TODO: this")

# gets the length of the list or dictionary that needs to be filled
# then asks user for information to fill it that many times.
def get_user_input_loop(loop_length: int, prompt:str, input_type, field_type: str):
    print("TODO: get_user_input_loop finish", sep="\n")
    new_dict = {}
    new_list = []
    field_name = ""
    new_prompt = ""
    error_message = ""
    input_variable = ""

    print(prompt, sep="\n")
    if input_type == "dict":
        for index in range(loop_length):
           field_name = str(input("Enter the name of the field: ")).strip()
           new_prompt = "Enter the value for " + field_name + ":"
           input_variable = get_single_dict_value(new_prompt, field_name, field_type)
           new_dict[field_name] = input_variable
        return new_dict
    elif input_type == "list":
        for index in range(loop_length):
            if field_type == "str":
                input_variable = input("Enter the value and press enter: ").strip()
                new_list.append(str(input_variable))
            elif field_type == "int":
                    input_variable = get_user_int("Enter an integer: ")
                    new_list.append(input_variable)
            else: 
                error_message = "Error! Unrecognized field_type for get_user_input_loop."
        return new_list
    else:
        error_message = "Input Type entered not recognized."
    return error_message

# Turns a list into an enumerated menu.
def list_to_menu(prompt: str, choices: list) -> str:
    get_menu_choice = -1
    valid = False
    options_max = len(choices)
    choices_as_dict = {}
    
    print(prompt, sep="\n")

    for index in range(options_max):
        choices_as_dict[index] = choices[index-1]

    while not valid:
        for key, value in choices_as_dict.items():
            print(str(key) + " - " + value)

        print("-1 will cancel.", sep="\n")
        get_menu_choice = best_user_int(options_max, -2, "Type -1 to cancel.")
        if get_menu_choice == -1:
            print("Cancelling the selection, goodbye.")
            choice_value = "cancel"
            valid = True
        elif get_menu_choice in choices_as_dict:
            input_variable = get_menu_choice
            choice_value = choices_as_dict[input_variable]
            valid = True

    return choice_value

# TODO: legacy code remove.
def string_exists_loop(compare_list: list, original_string: str,
                        message_if_exists: str, append_suffix: str) -> bool:
    appended_string = ""
    valid = False
    confirm_reply = False
    new_name = False

    while not valid:
        # string with name already exits.
        print(message_if_exists)
        reply = user_confirm("Something with that name already exists. Should we append?")
        if reply == True:
            print("Appending" + append_suffix + "to the file name.")
            appended_string = original_string + append_suffix

            print("Checking if new name exists.")
            result = list_compare(compare_list, appended_string)

            if result["match"] == True:
                confirm_reply = user_confirm("Do you want to change the name completely?")
                if confirm_reply == True:
                    new_name = True
                    return new_name
                # already exists, rerun loop.
                valid = string_exists_loop(result, compare_list, appended_string,
                                                message_if_exists, append_suffix)
            else: 
                # break loop
                print("No matches found! Name is valid.")
                valid = True
    return valid