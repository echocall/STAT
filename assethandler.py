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

def new_asset():
    print("TODO: Create a new asset and make the appropriate file saves.")
    # If it is a New Default asset, update associated game's .json
    # if it is a custom asset, update the save file's .json

# dict_to_object
def dict_to_objects(targetDict: list) -> dict:
    # add class object to dict of class objects. "name":object
    class_objects = {}

    # get name of each item in list. insubstantiate into a class object.
    # add class object to dict of class objects. "name":objectfor asset in targetDict:
    for asset in targetDict:
        classObjName = "c" + asset["name"]
        classObjName = MyAsset(asset)
        class_objects[asset["name"]] = classObjName
    return class_objects

