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

def new_asset(default_path: str, custom_path: str, game_name: str) -> dict:
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
    
    new_asset = new_asset_assembler(file_path, game_name)

def new_asset_assembler_quiet(file_path: str, game_name: str) -> object:
    # TODO: Finish
    new_asset = {'name': '', 'category': '', 'description': '', 'source': '', 'type':'',
             'attributes':[], 'buy_costs':{}, 'sell_prices':{}, 'special': '', 
             'effects':[], 'other':'', 'icon':'', 'image':''}
    
    print("Remember: You can always add non-required fields later!")
    
    print()
    name_dict = {}
    name_dict['name'] = set_new_asset_name(file_path)
    new_asset['name'] = name_dict['name']

    # Category for a game
    print()
    new_asset['category'] = set_category()

    print()
    add_description = user_confirm("Do you want to add a description now?")
    if add_description:
        new_asset['description'] = set_description()

    print()
    new_asset['source'] = game_name
    
    print()
    add_attributes = user_confirm("Do you want to add atrributes now?")
    if add_attributes:
        new_asset['attributes'] = set_attributes()

    print()
    print("Remember: You can always add costs later!")
    add_costs = user_confirm("Do you want to add buy costs to the asset now?")
    if add_costs:
        new_asset["buy_costs"] = set_buy_costs()

    print()
    add_prices = user_confirm("Do you want to add sell prices to the asset now?")
    if add_prices:
        new_asset['sell_prices'] = set_sell_prices()

    # TODO: add effects

    # TODO: add icon

    # TODO: add image

    print("Remember: You can always add non-required fields later!")

def new_asset_assembler_loud(file_path: str, game_name: str) -> object:
    # TODO: Finish
    new_asset = {'name': '', 'category': '', 'description': '', 'source': '', 'type':'',
             'attributes':[], 'buy_costs':{}, 'sell_prices':{}, 'special': '', 
             'effects':[], 'other':'', 'icon':'', 'image':''}
   
    print("Remember: You can always add non-required fields later!")
   
    name_dict = {}
    name_dict['name'] = set_new_asset_name(file_path)
    new_asset['name'] = name_dict['name']

    category_explanation()
    print()
    new_asset['category'] = set_category()

    description_explanation()
    print()
    add_description = user_confirm("Do you want to add a description now?")
    if add_description:
        new_asset['description'] = set_description()

    source_explanation()
    print()
    new_asset['source'] = game_name
    
    attributes_explanation()
    print()
    add_attributes = user_confirm("Do you want to add atrributes now?")
    if add_attributes:
        new_asset['attributes'] = set_attributes()

    costs_explanation()
    print()
    add_costs = user_confirm("Do you want to add buy costs to the asset now?")
    if add_costs:
        new_asset["buy_costs"] = set_buy_costs()

    prices_explanation()
    print()
    add_prices = user_confirm("Do you want to add sell prices to the asset now?")
    if add_prices:
        new_asset['sell_prices'] = set_sell_prices()

    
    print("Remember: You can always add non-required fields later!")


def set_new_asset_name(file_path: str) -> dict:
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
                set_new_asset_name(file_path)
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

def category_explanation():
    category_info = """A category is the largest organization chunk for an asset.
    In the GUI, objects will be separated by category. 
    An asset MUST have a category.
    Examples: Unit, Room, Trap, 1st Level."""
    print(category_info)

def set_category() -> str:
    # TODO: Error Handling, maybe allow user to see/pick from already in use
    # categories.
    category = get_user_input_string_variable("Please enter a category for the asset: ", 100)
    return category

def description_explanation():
    description_info = """This is a text field for entering information about 
    the asset you are creating. You can put extra stats that aren't covered by STAT,
    or as a space for flavor text, or notes about the unit itself.

    You don't have to add a description to an asset."""
    print(description_info)

def set_description():
    # TODO: Error Handling
    description = get_user_input_string_variable("Please enter a description for the asset: ", 1500)
    return description

def source_explanation():
    source_info = """The source is simply the name of the game you plan to use this asset with."""
    print(source_info)

def attributes_explanation():
    attributes_info = """Attributes are different from Categories and Type.
    They can be used to describe a unit, and in the future to search for particular units more easily.
    
    You don't need to add attributes to your unit."""
    print(attributes_info)

def set_attributes() -> list:
    # TODO: Error Handling
    game_attributes_int = 0
    game_attributes = []

    game_attributes_int = get_user_int("How many attributes do you want to add to this asset?")
    game_attributes = get_user_input_loop(game_attributes_int, list, str)

    return game_attributes

def costs_explanation():
    costs_info = """Buy costs are subtracted from the associated counters when
    you add another asset of that type. This can represent different types of
    currencies used to purchase the unit, resources used to construct the unit, 
    or something else consumed when the resource goes up.
    
    For example we might mock-up a spell in a tabletop game like so:
    Name: Magic Missile  ||| Buy Costs: First Level Spell Slot: 1 ||| Amount: 10
    Whenever we add 1 to our Amount of Magic Missiles
    we will subtract 1 from our counter of First Level Spell Slots. 
    In this case the Amount of Magic Missiles can stand in for how many times we've cast the spell.
    
    
    Whole Numbers only.
    You can add more than one buy cost to an asset.
    **You don't have to add a buy cost to an asset.**
    Tip: If you set the value of a cost to a negative, you will GAIN that much instead."""
    print(costs_info)

def set_buy_costs() -> dict:
    # TODO: Error Handling
    buy_costs = {}

    game_resources_int = get_user_int("How many different resources do you need to buy or use this asset?")
    buy_costs = get_user_input_loop(game_resources_int, "Enter the resource name and amount needed to buy or use this unit: ", dict, str)

    return buy_costs

def prices_explanation():
    # TODO
    prices_info = """A sell price is made up of the name of one of the counters in the game (ideally) and a number.
    The number is added to the count of the counter of the same name when 'sell' is clicked.
    It basically represents how much you get when you sell an asset or destroy it.

    For example we might mock-up an asset in a tabletop game like so:
    Name: Log Pile  ||| Sell Price: Wood: 20 ||| Amount: 10
    Whenever we sell 1 Log pile we will add 20 to our 'Wood' counter. 

    Whole Numbers only.
    You can add more than one sell price to an asset.
    **You don't have to add a sell price to an asset.**
    Tip: If you set the value of a cost to a negative, you will LOSE that much instead.
    """
    print(prices_info)

def set_sell_prices() -> dict:
    # TODO: Error Handling
    sell_prices = {}
    game_resources_int = get_user_int("How many different resources do you get for selling or destroying this asset?")
    sell_prices = get_user_input_loop(game_resources_int, "Enter the resource name and type you get for selling or destroying this asset: ", dict, str)
    return sell_prices

def special_explanation():
    special_info = """Special is an extra text field that
    isn't required. Its only purpose is to exist in case you want
    to separate some text out of the description."""
    print(special_info)

def set_special() -> str:
    # TODO: Error Handling
    special = get_user_input_string_variable("Please enter the special text for the asset: ", 1500)
    return special

def set_effects():
    d = 4+4
    # TODO: We will want to wait until we have effects made.
    # Make a dictionary of effects & their description

def set_icon() -> str:
    # TODO: make this fetch the file path/move icon file to the images folder.
    e = 5+5

def set_image() -> str:
    # TODO: make this fetch the file path/move the image file to the images folder.
    f = 6+6

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

