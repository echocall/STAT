from getters import assets_getter, asset_getter

def asset_handler(defaultFilePath: str, defaultAssets: list, overrideExists: bool, overrideFilePath: bool):
    print("TODO: Handle assets. >:) > :) >:)")

# Checks that the default assets exist & match the game file
# retrieves the default files & passes them back + any error message.
def default_assets_fetch(defaultFilePath: str, defaultAssets: list):
    print("TODO: Get the default assets for a game & compare what was retrieved to what should exist.")
    # call asset_getter with the filePath to reurn the default assets in the folder.
    
    # compare the names of the returned files with the list from the game.json

    # return information/messages to user


# Retrieve any override assets
def override_asset_fetch():
    print("TODO: Get the override files.")

# Handle merging override assets & default assets
def merge_assets():
    print("TODO: Merge override and default assets into one list of dictionaries.")

# Asset Loader
def asset_loader():
    print("TODO: Load assets.")

# asset Set to List handler
# takes in an arry of assets (assets[]), and a key.
def set_to_list(initial_list: list, key_in_list: str) -> list:
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