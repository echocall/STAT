
def asset_handler(assets: dict):
    # assetTypes is a set
    assetTypesSet = {"set", "set2"}
    # as list
    assetTypes = []

    # clearing out unneeded values from our set.
    assetTypesSet.clear()
    # getting the different Asset Types for later processing.
    for asset in assets:
        print(asset['assettype'])
        assetTypesSet.add(asset['assettype'])

    for type in assetTypesSet:
        assetTypes.append(type)

# Checks that the default assets exist & match the game file
# retrieves the default files & passes them back + any error message.
def default_asset_fetch():
    print("TODO: Get the default assets for a game & compare what was retrieved to what should exist.")

# Retrieve any override assets
def override_asset_fetch():
    print("TODO: Get the override files.")

# Handle merging override assets & default assets
def merge_assets():
    print("TODO: Merge override and default assets into one list of dictionaries.")

# Asset Loader
def asset_loader():
    print("TODO: Load assets.")