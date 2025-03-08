import sys
import configparser
from os import system

def stat_initialize() -> dict:
    # Reading from config file
    configParser = configparser.RawConfigParser()
    configFilePath = 'config.txt'
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
    
# compare two lists
def list_compare(initialList: list, secondList: list):
    match = False
    error_message = ""
    missing_objects = []
    initial_list_size = len(initialList)
    second_list_size = len(secondList)
    result = { "match": False, "missing values": []}

    if(initial_list_size != second_list_size):
        error_message = "Lists do not match."
        compare_done = True
    else:
        if(initial_list_size <= 0):
            error_message = "First list passed to list_compare is empty."
        else:
            if(second_list_size <= 0):
                error_message = "Second list passed to list_compare is empty."
            else:
                print("Compare the Lists.")
                for item in initialList:
                    try:
                        secondList.index(item)
                    except ValueError:
                        error_message = f"Supplied value does not exist in second list: {item!r}"
                        missing_objects.append(item)

    if len(missing_objects) > 0:
        print(error_message,
                sep="\n",)
        result["match"] = False
        result["missing_values"] = missing_objects
        return(result)
    else:
        # "Check complete. Lists have same objects."
        result["match"] = True
        result["missing_values"] = []
        return(result)
        
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
