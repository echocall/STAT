from getters import *
from utilities import *

def asset_handler(defaultFilePath: str, defaultAssets: list, overrideExists: bool, overrideFilePath: str):
    print("TODO: Handle assets. >:) > :) >:)")
    fetched_default_assets_result = {}
    fetched_default_assets = {}
    missing_default= bool
    missing_assets = {}
    override_assets = {}
    conflict_check = {}
    merged_assets = {}

    fetched_default_assets_result = default_assets_fetch(defaultFilePath, defaultAssets)
    # Check that we have all the default assets.
    if fetched_default_assets_result["match"] == True:
        # we have all the default assets.
        fetched_default_assets = fetched_default_assets_result["retrieved_list"]
        missing_default = False
    else:
        missing_default = True
        fetched_default_assets = fetched_default_assets_result["retrieved_list"]
        missing_assets = fetched_default_assets_result["missing_values"]

    # overrides exist! Handle them. >:V
    if (overrideExists == True):
        override_assets = override_asset_fetch()
        print(override_assets)
        
        # Overrides exist, we need to check for conflicts and merge the results.
        conflict_check = list_compare(override_assets["retrieved_list"], fetched_default_assets)
        
        if conflict_check["match"] == True:
            # no conflict, add the dicts to each other.
            for asset in fetched_default_assets:
                merged_assets.update(asset)
            for asset in conflict_check["retrieved_list"]:
                merged_assets.update(asset)
        else:
            # there's a conflict! Something has an override.
            print("TODO: handle override")
            for asset in fetched_default_assets:
                try:
                    index = override_assets["retrieved_list"].index(asset)
                    # Skip this asset
                except ValueError:
                    # doesn't exist in the override_assets["retrieved_list"]
                    index = -1
                    merged_assets.update(asset)


        if len(conflict_check["missing_values"]) > 0:
            # these values don't have an override! :)
            print("These don't have a conflict! :)")

    if missing_default == True:
        print("TODO: fill in if missing == True: in asset_handler")
        # Return list of missing assets as a warning value
        # Return the list of assets that /do/ exist.


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
        return result

# Retrieve any override assets
def override_asset_fetch(overrideFilePath: str) -> dict:
    print("TODO: Get the override files.")
    override_assets = {}
    override_assets = multi_json_getter(overrideFilePath, "assets")
    return override_assets

# Handle merging override assets & default assets
def merge_assets():
    print("TODO: Merge override and default assets into one list of dictionaries.")

# Asset Loader
def asset_loader():
    print("TODO: Load assets.")

    filter_set = {"set", "set2"} 
    filtered_list = []
    errorMessage = ""
    filterSuccessful = False

    # clearing out unneeded values from our set.
    filter_set.clear()

    if len(initial_list) <= 0:
        errorMessage = "Initial List empty. Unable to filter list."
    else:
        # getting the different Asset Types for later processing.
        for item in initial_list:
            print(item[key_in_list])
            filter_set.add(item[key_in_list])

        for x in filter_set:
            filtered_list.append(x)
        filterSuccessful = True

    if filterSuccessful == True:
        return filtered_list
    else:
        return errorMessage