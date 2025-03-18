from crud import *
from utilities import *
from MyAsset import *

# Need to adjust asset_handler depending on game state.
# Example: New game -> Only call default assets, Load Game -> check for customs
def asset_handler(defaultFilePath: str, defaultAssets: list, hasCustom: bool,
                   customFilePath: str) -> dict:
    default_result = {}
    missing_default= bool
    missing_assets = {}
    custom_assets = {}
    conflict_check = {}
    merged_assets = []
    converted_assets = []
    handler_result = {"missing_default": bool, "missing_assets": [], "merged_assets": []}

    # Check that we have all the default assets.
    default_result = default_assets_fetch(defaultFilePath, defaultAssets)

    # process that result
    if default_result["match"] == True:
        # we have all the default assets.
        missing_default = False
    else:
        missing_default = True
        missing_assets = default_result["missing_values"]

    # customs exist! Handle them. >:V
    if (hasCustom == True):
        custom_assets = custom_asset_fetch(customFilePath)
        # Customs exist, we need to check for overrides and merge the results.
        conflict_check = list_compare(default_result["retrieved_names"], custom_assets["custom_names"])
        merged_assets = merge_assets(default_result["retrieved_list"], custom_assets["custom_list"], conflict_check)
    else:
        merged_assets = default_result["retrieved_list"]

    converted_assets = dict_to_objects(merged_assets)

    # build the result from our handler.
    handler_result = handler_result_builder(missing_default, "missing_assets", missing_assets, "converted_assets", converted_assets)

    return handler_result

# Checks that the default assets exist & match the game file
# retrieves the default files & passes them back + any error message.
def default_assets_fetch(defaultFilePath: str, defaultAssets: list)-> dict:
    retrieved_assets = []
    result = {}

    # call multi_json_getter with the filePath to reurn the default assets in the folder.
    retrieved_assets = multi_json_getter(defaultFilePath, "assets")
    # get the names of the retrieved assets
    retrieved_names = filter_list_value_with_set(retrieved_assets, "name")
    # compare the names of the returned files with the list from the game.json
    result = list_compare(defaultAssets, retrieved_names)

    # return information/messages to user
    if result['match'] == True:
        result["retrieved_list"] = retrieved_assets
        result["retrieved_names"] = retrieved_names
        return result
    else:
        result["retrieved_list"] = retrieved_assets
        result["retrieved_names"] = retrieved_names
        return result

# Retrieve any custom assets
def custom_asset_fetch(customFilePath: str) -> dict:
    custom_assets = {"custom_list": {}, "custom_names": []}
    custom_assets["custom_list"] = multi_json_getter(customFilePath, "assets")
    if len(custom_assets["custom_list"]) > 0:
        custom_assets["custom_names"] = filter_list_value_with_set(custom_assets["custom_list"], 'name')
    return custom_assets

# Handle merging custom assets & default assets
# returns list of asset objects
def merge_assets(fetched_default_assets: list, custom_assets: list, conflict_check: dict) -> list:
    merged_assets_list = merge_dict_lists(fetched_default_assets, custom_assets, conflict_check)
    
    return merged_assets_list

# Asset Loader
def asset_loader(assetObjectsList: dict):
    print("TODO: Load assets.")
    # Organize assets by asset type
    # prep the types for being seen

# asset type organizer
def organize_assets_by_type():
    print("TODO: Organize the assets by asset type.")

def new_asset(default_path: str, custom_path: str) -> dict:
    print("TODO: Create a new asset and make the appropriate file saves.")
    file_path = ""
    new_asset = {}

    # If it is a New Default asset, update associated game's .json
    # if it is a custom asset, update the save file's .json
    is_default = user_confirm("Is this a default asset?")
    default_message = ""
    if is_default:
        # TODO: make updates to the Game's object, and .json file.
        # make the file_path point to Default objects
        file_path = default_path
        default_message = "A new default asset has been added to the game's data."
    else:
        # It's a custom! make changes to the save's object and .json file.
        # make the file_path point to Customs objects
        file_path = custom_path
        default_message = "A new custom asset has been added to the save file's data."
    
    new_asset = new_asset_assembler(file_path)

def new_asset_assembler(file_path: str) -> object:
    # TODO: Finish
    new_asset = {'name': '', 'asset_type': '', 'description': '', 'source': '', 'category':'',
             'in_game_types':[], 'buy_costs':{}, 'sell_prices':{}, 'special': '', 
             'effects':[], 'other':'', 'icon':'', 'image':''}
    name_dict = {}
    name_dict['name'] = get_new_asset_name(file_path)
    new_asset['name'] = name_dict['name']
    
    new_asset['in_game_types'] = set_game_types()

def get_new_asset_name(file_path: str) -> dict:
    file_name = ""
    name = ""
    assets = []
    asset_name = {"name": "", "file":""}
    valid = False
    
    while valid != True:
        # ask the user for the name of the new asset
        name = str(input("Enter the name of the new asset: ")).strip()
        file_name = format_str_for_filename(name)

        # check that a game by that name doesn't already exists
        assets = multi_json_names_getter(file_path, "assets")
        if name in assets:
        # if file_name already exists, ask for another game name and show what games exist.
        # TODO: Make this true part become recursive.
            print("\n" + "An asset of that name already exists. You may experience difficulties creating the file for that asset.", sep="\n")
            if user_confirm("Do you want to enter a new name now?"):
                get_new_asset_name(file_path)
            else:
                print("\n" + "Appending _placeholder to asset name. If further folder creation errors persist, please create a new name. " + "\n")
                valid = True
                asset_name["name"] = name + "_Placeholder"
                asset_name["file"] = file_name + "_placeholder"
        else:
            valid = True
            asset_name["name"] = name
            asset_name["file"] = file_name

    return  asset_name


def asset_type():
    z = 26+26
    # TODO: get the types of assets
    # oooh, should we be saving this as a list in Game file?
    # if non-default asset types, may be better to leave as text field.

def set_source():
    y = 25+25
    # TODO:
    # this is just name of the game.
    # need multiple option

def set_game_types() -> list:
    # TODO: Error Handling
    game_types_int = 0
    game_types = []
    game_types_int = get_user_int("How many types does the game assign to this unit?")
    game_types = get_user_input_loop(game_types_int, list, str)

    return game_types

def set_buy_costs() -> dict:
    # TODO: Error Handling
    buy_costs = {}
    game_resources_int = get_user_int("How many different resources do you need to buy or use this asset?")
    buy_costs = get_user_input_loop(game_resources_int, "Enter the resource name and amount needed to buy or use this unit: ", dict, str)
    return buy_costs

def set_sell_prices() -> dict:
    # TODO: Error Handling
    sell_prices = {}
    game_resources_int = get_user_int("How many different resources do you get for selling or destroying this asset?")
    sell_prices = get_user_input_loop(game_resources_int, "Enter the resource name and type you get for selling or destroying this asset: ", dict, str)
    return sell_prices

def set_effects():
    d = 4+4
    # TODO: We will want to wait until we have effects made.
    # Make a dictionary of effects & their description


# dict_to_object
def dict_to_objects(targetDict: list) -> dict:
    # add class object to dict of class objects. "name":object
    class_objects = {}

    # get name of each item in list. insubstantiate into a class object.
    # add class object to dict of class objects. "name":objectfor asset in targetDict:
    for asset in targetDict:
        classObjName = "c" + asset["name"]
        classObjName = MyAsset(**asset)
        class_objects[asset["name"]] = classObjName
    return class_objects

