from helpers.crud import *
from helpers.utilities import *
from classes.MyAsset import *

# Retrieves all assets associated with a game/save
def asset_handler(full_default_assets_path: str, defaultAssets: list, hasCustom: bool,
                   full_custom_assets_path: str) -> dict:
    default_result = {}
    missing_default= bool
    missing_assets = {}
    custom_assets = {}
    conflict_check = {}
    merged_assets = []
    converted_assets = []
    handler_result = {"missing_default": bool, "missing_assets": [], "merged_assets": []}

    # Check that we have all the default assets.
    default_result = default_assets_fetch(full_default_assets_path, defaultAssets)

    # process that result
    if default_result["match"] == True:
        # we have all the default assets.
        missing_default = False
    else:
        missing_default = True
        missing_assets = default_result["missing_values"]

    # customs exist! Handle them. >:V
    if (hasCustom == True):
        custom_assets = custom_asset_fetch(full_custom_assets_path)
        # Customs exist, we need to check for overrides and merge the results.
        conflict_check = list_compare(default_result["retrieved_names"], custom_assets["custom_names"])
        merged_assets = merge_assets(default_result["retrieved_list"], custom_assets["custom_list"], conflict_check)
    else:
        merged_assets = default_result["retrieved_list"]

    # turns them into MyAsset objects
    # converted_assets = dict_to_objects(merged_assets)

    # build the result from our handler.
    handler_result = handler_result_builder(missing_default, "missing_assets", missing_assets, "converted_assets", converted_assets)

    return merged_assets

# Checks that the default assets exist & match the game file
# retrieves the default files & passes them back + any error message.
def default_assets_fetch(defaultFilePath: str, defaultAssets: list)-> dict:
    retrieved_assets = []
    result = {}

    # call multi_json_getter with the filePath to reurn the default assets in the folder.
    retrieved_assets = multi_file_getter(defaultFilePath, "assets")
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
def custom_asset_fetch(full_custom_assets_path: str) -> dict:
    custom_assets = {"custom_list": {}, "custom_names": []}
    custom_assets["customs_list"] = multi_file_getter(full_custom_assets_path, "assets")
    # custom_assets["custom_list"] = multi_json_getter(customFilePath, "assets")
    if len(custom_assets["custom_list"]) > 0:
        custom_assets["custom_names"] = filter_list_value_with_set(custom_assets["custom_list"], 'name')
    return custom_assets

# retrieve a single asset
def single_asset_fetch(full_asset_path: str, file_name: str) -> dict:
    result = {'result': False, 'message': '', 'asset': {}}
    try:
        fetch_result = single_json_getter_fullpath(full_asset_path, 'asset')
        result['result'] = True
        result['message'] = "Asset successfully retrieved!"
        result['asset'] = fetch_result['json']
    except:
        result['message'] = f"Failed to get {file_name} from json file."
        return result

    return result


# Handle merging custom assets & default assets
# returns list of asset objects
def merge_assets(fetched_default_assets: list, custom_assets: list,
                  conflict_check: dict) -> list:
    merged_assets_list = merge_dict_lists(fetched_default_assets, custom_assets, conflict_check)
    
    return merged_assets_list

# Asset Loader
def asset_loader(asset_objects: dict):
    print("TODO: Load assets.")
    # Organize assets by asset type
    # prep the types for being seen

# create new asset from the gui
def new_asset_gui(
    is_default: bool,
    new_asset: dict,
    game_dict: dict,
    save_dict: dict,
    default_directory_path: str,
    custom_directory_path: str
) -> dict:
    write_result = {}
    format_result = format_str_for_filename_super(new_asset['name'])

    if format_result['result']:
        formatted_name = format_result['string']

        # Construct full file path using directory + new file name
        if is_default:
            full_file_path = str(Path(default_directory_path).with_name(f"{formatted_name}.json"))
        else:
            full_file_path = str(Path(custom_directory_path).with_name(f"{formatted_name}.json"))

        # Write to file
        write_result = create_new_json_file(full_file_path, new_asset)

        if write_result['result']:
            write_result['message'] = 'Saved asset as .json file successfully!'

            # Update dictionaries only after successful write
            if is_default:
                game_dict['default_assets'].append(new_asset['name'])
            else:
                save_dict['asset_customs'].append(new_asset['name'])

        else:
            write_result['message'] = 'Failed to save the asset as a .json file.'
    else:
        write_result['message'] = 'Formatting the asset name to a file name failed!'

    return write_result


def category_explanation() -> str:
    category_info = """A category is the largest organization chunk for an asset.
    In the GUI, objects will be separated by category. 
    An asset MUST have a category.
    Examples: Unit, Room, Trap, 1st Level."""
    return category_info

def description_explanation()-> str:
    description_info = """This is a text field for entering information about 
    the asset you are creating. You can put extra stats that aren't covered by STAT,
    or as a space for flavor text, or notes about the unit itself.

    You don't have to add a description to an asset."""
    return description_info

def source_explanation() -> str:
    source_info = """The source is simply the name of the game you plan to use this asset with."""
    return source_info

def asset_type_explanation() -> str:
    type_info = """ Asset Type is another way to categorize and asset.
    Its another way to further break assets into small parts withing categories.
    For example if we had animal based assets and we wanted to make a lion we could model it like so:
    Name: Lion ||| Category: Mammal ||| Asset Type: Predator"""
    return type_info


def attributes_explanation() -> str:
    attributes_info = """Attributes are different from Categories and Type.
    They can be used to describe a asset, and in the future to search
      for particular assets more easily.
      
    For example if we had animal based assets and we wanted to make a lion:
    Name: Lion ||| Category: Mammal ||| Asset Type: Predator 
      Attributes: [Carnivore, Predator, Fur, Claws, Fangs, Feline]
    
    You don't need to add attributes to your asset."""
    return attributes_info

def costs_explanation() -> str:
    costs_info = """Buy costs are subtracted from the associated counters when
    you add another asset of that kind. This can represent different types of
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
    return cost_info


def prices_explanation() -> str:
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
    return prices_info

# TODO: error handling
def set_sell_prices(counter_names: list) -> dict:
    sell_prices = {}
    list_size = 0
    list_size = len(counter_names)
    
    if list_size == 0:
        # no list, manual input of value names.
        game_resources_int = okay_user_int(0,"How many different cost do"
        " you get for selling or destroying this asset?")
        sell_prices = get_user_input_loop(game_resources_int, "Enter the cost name and "
        "type you get for selling or destroying this asset: ", "dict", "str")
    else:
        game_resources_int = okay_user_int(0,"How many different cost do"
        " you get for selling or destroying this asset?")
        sell_prices = get_user_input_loop_list(game_resources_int, "Enter the cost name and "
        "type you get for selling or destroying this asset: ", "dict", "str", counter_names)
    return sell_prices

def special_explanation() -> str:
    special_info = """Special is an extra text field that
    isn't required. Its only purpose is to exist in case you want
    to separate some text out of the description."""
    return special_explanation


# ###################################
# Takes singular asset dictionary and returns
# a singular asset object.
def dict_to_asset_object(targetDict: dict) -> object:
    # get name of the dictionary and insubstantiate into a class object.
    classObjName = "c" + targetDict["name"]
    classObjName = format_str_for_filename(classObjName)
    try: 
        return MyAsset(**targetDict)
    except Exception:
        print(traceback.format_exc())

# takes a dictionary of asset dicts and returns
# a dictionary of objects.
def dict_to_objects(targetDict: dict) -> dict:
    # add class object to dict of class objects. "name":object
    class_objects = {}

    # get name of each item in list. insubstantiate into a class object.
    # add class object to dict of class objects. "name":objectfor asset in targetDict:
    for asset in targetDict:
        classObjName = "c" + asset["name"]
        classObjName = MyAsset(**asset)
        class_objects[asset["name"]] = classObjName
    return class_objects

    # Sort the assets by category

# gets an asset_name, converts it to file format, checks if already exists.
def get_new_asset_name(name: str, directory_path: str) -> dict:
    file_name = ""
    assets = []
    asset_name = {"name": "", "file":""}
    valid = False

    while valid != True:
        format_result = format_str_for_filename_super(name)
        if format_result['result']:
            # check that a game by that name doesn't already exists
            # Send the Directory Path
            assets_result = multi_file_names_getter(directory_path, "assets")
            
            if assets_result['results']:
                assets = assets_result['list']
            else:
                print("Warning! Could not retrieve the names of assets.")
            
            if format_result['string'] in assets:
        # if file_name already exists, append placeholder and alert user
                valid = True
                asset_name["name"] = name + "_Placeholder"
                asset_name["file"] = file_name + "_placeholder"
            else:
                valid = True
                asset_name["name"] = name
                asset_name["file"] = file_name

    return  asset_name

# SORTING
# Sorts assets by category
def sort_assets_by_category(assets_to_sort: dict) -> dict:
        sorted_assets = {}
        # Make a set of all the different category types.
        categories_set = {}
        categories_list = []

        categories_set = set(categories_set)

        for key in assets_to_sort:
            if assets_to_sort[key]['category'] not in categories_set:
                categories_set.add(assets_to_sort[key]['category'])
                
       # Change set into list for more consistent sorting.
        categories_list = list(categories_set)
        categories_list.sort()

        # now that we have the set, create dictionary.
        sorted_assets = asset_sorter(assets_to_sort, categories_list, 'category')

        return sorted_assets

# actually sorts the assets
def asset_sorter(assets_to_sort: dict, sort_by_list: list, sort_field: str) -> dict:
        #sorted_assets = {'category':[<asset1>,<asset2>]}
        sorted_assets = {}

        # initialize the dictionary of lists by field
        for each in sort_by_list:
            sorted_assets[each] = []
        for key in assets_to_sort:
        # if the asset's category is in the sorted dictionary, add it.
            if assets_to_sort[key][sort_field] in sorted_assets:
                # get the field we're sorting into
                sort_field_name = assets_to_sort[key][sort_field]
                # get the asset and add it to the dictionary for that field.
                sorted_assets[sort_field_name].append(assets_to_sort[key])
        return sorted_assets

# gets owned assets            
def fetch_owned_assets(assets: dict, assets_owned: dict) -> dict:
        # TODO: return an unsorted dictionary of owned assets.
        owned_assets = {}
        error_message = ''
        
        for name in assets_owned:
            # checking if the owned asset is in the asset list.
                if name in assets:
                    owned_assets[name] = assets.get(name)
                else:
                # TODO: error handling
                    error_message = 'Owned asset not in list of assets.'
                    print(error_message)
        return owned_assets

# TODO: maybe fill in?
def fetch_assets() -> dict:
    a = 1+1

def check_template_bool(asset: dict, template_path: str) -> bool:
    error_message = ''
    result = False
    try:
        asset_template = get_template_json("asset", template_path)
        result = dict_key_compare(asset_template, asset)
        return result
    except Exception:
        print(traceback.format_exc())
        return result

# TODO: implement
# delete an asset
# Call BEFORE deleting save or a game if not deleting all.
def delete_asset(asset_dict: dict, asset_path: str) -> dict:
    result = {}
    format_result
    # Remove targeted asset from its parents (save and game)
        # What if asset is used in multiple saves?
        # What if asset is a default asset?

    # delete the asset's file
        # Get file path to asset
    try: 
        # try formatting the name for a file
        try:
            format_result = format_str_for_filename_super(asset_path['name'])
        except:
            format_result['result'] = False
            format_result['message'] = 'Formatting name for save update failed.'


    except:
        result['message'] = "Deleting the file failed."
    # call: shutil.rmtree('/path/to/folder')
    # set bln_result to True

    return result
