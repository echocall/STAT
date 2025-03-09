from getters import *
from utilities import *

# Need to adjust asset_handler depending on game state.
# Example: New game -> Only call default assets, Load Game -> check for overrides
def asset_handler(defaultFilePath: str, defaultAssets: list, overrideExists: bool, overrideFilePath: str):
    print("TODO: Handle assets. >:) > :) >:)")
    fetched_default_assets_result = {}
    fetched_default_assets = {}
    fetched_default_assets_names = {}
    missing_default= bool
    missing_assets = {}
    override_assets = {}
    override_assets_as_names = {}
    conflict_check = {}
    merged_assets = []
    handler_result = {"missing_default": "", "missing_assets": [], "merged_assets": []}

    # Check that we have all the default assets.
    fetched_default_assets_result = default_assets_fetch(defaultFilePath, defaultAssets)

    # process that result
    if fetched_default_assets_result["match"] == True:
        # we have all the default assets.
        missing_default = False
        fetched_default_assets = fetched_default_assets_result["retrieved_list"]
        fetched_default_assets_names = defaultAssets
    else:
        missing_default = True
        fetched_default_assets = fetched_default_assets_result["retrieved_list"]
        fetched_default_assets_names = filter_list_value_with_set(fetched_default_assets, 'name')
        missing_assets = fetched_default_assets_result["missing_values"]

    # overrides exist! Handle them. >:V
    if (overrideExists == True):
        override_assets = override_asset_fetch(overrideFilePath)
        if len(override_assets) > 0:
            # override exists, get their names
            override_assets_as_names = filter_list_value_with_set(override_assets, 'name')
        
        # Overrides exist, we need to check for conflicts and merge the results.
        # check list of default assets to see if their name shows up in override or not.
        conflict_check = list_compare(fetched_default_assets_names, override_assets_as_names)
        # merge the lists
        merged_assets = merge_assets(fetched_default_assets, override_assets, conflict_check)
    else:
        # No overrides.
        merged_assets = fetched_default_assets
        
    # build the result from our handler.
    handler_result["missing_default"] = missing_default
    handler_result["missing_assets"] = missing_assets
    handler_result["merged_assets"] = merged_assets
    return handler_result

# Checks that the default assets exist & match the game file
# retrieves the default files & passes them back + any error message.
def default_assets_fetch(defaultFilePath: str, defaultAssets: list)-> dict:
    retrieved_assets = []
    result = {}

    # call multi_json_getter with the filePath to reurn the default assets in the folder.
    retrieved_assets = multi_json_getter(defaultFilePath, "assets")
    # get the names of the retrieved assets
    retrieved_assets_names = filter_list_value_with_set(retrieved_assets, "name")
    # compare the names of the returned files with the list from the game.json
    result = list_compare(defaultAssets, retrieved_assets_names)

    # return information/messages to user
    if result['match'] == True:
        result["retrieved_list"] = retrieved_assets
        return result
    else:
        result["retrieved_list"] = retrieved_assets
        return result

# Retrieve any override assets
def override_asset_fetch(overrideFilePath: str) -> dict:
    print("TODO: Get the override files.")
    override_assets = {}
    override_assets = multi_json_getter(overrideFilePath, "assets")
    return override_assets

# Handle merging override assets & default assets
def merge_assets(fetched_default_assets: list, override_assets: list, conflict_check: dict) -> dict:
    merged_assets_list = merge_dict_lists(fetched_default_assets, override_assets, conflict_check)
    return merged_assets_list

# Asset Loader
def asset_loader(merged_asset_list: list):
    print("TODO: Load assets.")
    # Organize assets by asset type
    # prep the types for being seen

# asset type organizer
def organize_assets_by_type():
    print("TODO: Organize the assets by asset type.")

def new_asset():
    print("TODO: Create a new asset and make the appropriate saves.")
    # If it is a New Default asset, update associated game's .json
    # If it is a b

# asset reader

