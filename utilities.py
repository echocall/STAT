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
def filter_list_with_set(initialList: list, keyInList: str) -> list:
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
            print(item[keyInList])
            filter_set.add(item[keyInList])

        for x in filter_set:
            filtered_list.append(x)
        filter_successful = True

    if filter_successful == True:
        return filtered_list
    else:
        return error_message