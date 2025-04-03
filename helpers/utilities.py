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

def stat_initialize(config_file: str) -> dict:
    # Reading from config file
    configParser = configparser.RawConfigParser()
    configFilePath = config_file
    configParser.sections()
    configParser.read(configFilePath)
    print("Printing ConfigParser:")
    print(configParser.sections())

    config_dict = {}
    for Section in configParser.sections():
        temp_dict = {}
        for key, value in configParser[Section].items():
            temp_dict.update({key:value})
        config_dict[Section] = temp_dict

    print("Priting Config_Dict")
    print(config_dict)

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
    # TODO: look into Pydantic along this line.
    try:
        json_obj = json.dumps(object, indent=4)
        return json_obj
    except:
        print("Could not convert object to json file.")

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
        input_variable = input(prompt + " Type (Yes/No): ").strip().upper()
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

# Turns a list into an enumerated menu.
def list_to_menu(prompt: str, choices: list) -> str:
    get_menu_choice = -1
    valid = False
    options_max = len(choices)
    choices_as_dict = {}
    
    print()
    print(prompt, sep="\n")
    for index in range(options_max):
        choices_as_dict[index] = choices[index-1]

    while not valid:
        for key, value in choices_as_dict.items():
            print(str(key) + " - " + value)

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

def get_user_input_string_variable(prompt: str, character_limit: int) -> str:
    valid = False
    length_check = False
    exists_check = False
    print("There is a " + str(character_limit) + " character limit. Leading and trailing whitespaces will be removed.")
    while not valid:
        user_input = str(input(prompt)).strip()

        if len(user_input) > character_limit:
            print("The text entered is over the character limit, shrinking string: ")
            user_input = user_input[:character_limit]
            print("Input shrunk to: " + user_input)
            length_check = True
        else:
            length_check = True

        if len(user_input) < 1:
            print("You must enter at least one character for this input.")
        else:
            exists_check = True
        
        if exists_check and length_check:
            valid = True

    return user_input    

# validation
def validate_user_input_variable(user_input: str, max_limit: int, min_limit: int) -> str:
    valid = False
    length_check = False
    exists_check = False
    error_message = ''

    while not valid:
        if len(user_input) > max_limit:
            error_message = "The text entered is over the character limit, please correct the length."
        else:
            length_check = True

        if len(user_input) < min_limit:
            error_message = "You do not meet the required minimum length for this field. Min length is = " + str(min_limit) + " characters."
        else:
            exists_check = True
        
        if exists_check and length_check:
            error_message = 'None'

    return error_message    

# gets the length of the list or dictionary that needs to be filled with ints
# then asks user for ints to fill it that many times.
def get_user_input_loop(loop_length: int, prompt:str, input_type: str, field_type: str):
    # TODO: get_user_input_loop finish
    new_dict = {}
    new_list = []
    field_name = ""
    new_prompt = ""
    error_message = ""
    input_variable = ""

    print(prompt, sep="\n")
    # if the input_type is dictionary, prepare to get name of field and value of field
    if input_type == "dict":
        for index in range(loop_length):
           print("At " + str(index) + " of " + str(loop_length))
           field_name = str(input("\n" + "Enter the name: ")).strip()
           new_prompt = "Enter the value for " + field_name + ": "
           input_variable = get_single_dict_value(new_prompt, field_name, field_type)
           new_dict[field_name] = input_variable[field_name]
        return new_dict
    # if input type is list, prepare to get the # of items in the list.
    elif input_type == "list":
        for index in range(loop_length):
            print("\n" + str(index) + " of " + str(loop_length) + " to go: ")
            if field_type == "str":
                input_variable = input("Enter the string and press enter: ").strip()
                new_list.append(str(input_variable))
            elif field_type == "int":
                    input_variable = get_user_int("Enter an integer and press enter: ")
                    new_list.append(input_variable)
            else: 
                error_message = "Error! Unrecognized field_type for get_user_input_loop."
        return new_list
    else:
        error_message = "Input Type entered not recognized."
    return error_message

def get_user_input_loop_list(loop_length: int, prompt:str, input_type: str, field_type: str, options_list: list):
    # TODO: get_user_input_loop finish
    new_dict = {}
    new_list = []
    field_name = ""
    new_prompt = ""
    error_message = ""
    input_variable = ""

    print(prompt, sep="\n")
    # if the input_type is dictionary, prepare to get name of field and value of field
    if input_type == "dict":
        for index in range(loop_length):
           print("At " + str(index) + " of " + str(loop_length))
           field_name = list_to_menu("Select the name of the field: ", options_list)
           new_prompt = "Enter the value for " + field_name + ": "
           input_variable = get_single_dict_value(new_prompt, field_name, field_type)
           new_dict[field_name] = input_variable[field_name]
        return new_dict
    # if input type is list, prepare to get the # of items in the list.
    elif input_type == "list":
        for index in range(loop_length):
            print("\n" + str(index) + " of " + str(loop_length) + " to go: ")
            if field_type == "str":
                input_variable = input("Enter the string and press enter: ").strip()
                new_list.append(str(input_variable))
            elif field_type == "int":
                    input_variable = get_user_int("Enter an integer and press enter: ")
                    new_list.append(input_variable)
            else: 
                error_message = "Error! Unrecognized field_type for get_user_input_loop."
        return new_list
    else:
        error_message = "Input Type entered not recognized."
    return error_message
