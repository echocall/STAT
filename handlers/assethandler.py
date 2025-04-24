from helpers.crud import *
from helpers.utilities import *
from classes.MyAsset import *

# Retrieves all assets associated with a game/save
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

# retrieve a single asset
def single_asset_fetch(asset_file_path: str, file_name: str) -> dict:
    result = {'result': False, 'message': '', 'asset': {}}
    try:
        fetch_result = single_json_getter(file_name, asset_file_path, 'asset')
        result['result'] = True
        result['message'] = "Asset successfully retrieved!"
        result['asset'] = fetch_result
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
def new_asset_gui(is_default: bool, new_asset: dict, game_dict: dict, save_dict: dict, file_name: str) -> dict:
    write_result = { 'result': False, 'message': ''}
    error_message = ""
    save_location = {}

    format_result = format_str_for_filename_super(new_asset['name'])

    if format_result['result']:
        file_name = format_result['string']

        # is this a default asset for a game?
        if is_default: 
            # update the game file
            game_dict['default_assets'].append(new_asset['name'])

            # write asset to appropriate location
            write_result['result'] = create_new_json_file(file_name, game_dict['asset_default_path'], new_asset)
            # Check write_result
            if write_result['result']:
                write_result['message'] = 'Saved asset as .json file successfully!'
                return write_result
            else:
                write_result['message'] = 'Failed to save the default asset as a .json file.'
                return write_result
            
        # Custom asset
        else:
            # update the save file
            save_dict['asset_customs'].append(new_asset['name'])

            #write asset to appropriate location
            write_result['result'] = create_new_json_file(file_name, save_dict['asset_customs_path'], new_asset)
            # Check write result
            if write_result['result']:
                write_result['message'] = 'Saved asset as .json file successfully!'
                return write_result
            else:
                write_result['message'] = 'Failed to save the custom asset as a .json file.'
                return write_result

    else:
        write_result['message'] = 'Formatting the asset name to a file name failed!'
        # could not format the name @_@
    return write_result


# TODO finish
def new_asset_console(is_default: bool, for_new_game: bool, default_path: str,
               custom_path: str, game_name: str, 
               asset_explanations: bool, counters: dict) -> object:
    file_path = ""
    new_asset = {}
    counter_names = []

    for key in counters:
        counter_names.append(key)

    if is_default:
        # TODO: make updates to the Game's object, and .json file.
        # make the file_path point to Default objects
        file_path = default_path
    else:
        # It's a custom! make changes to the save's object and .json file.
        # make the file_path point to Customs objects
        file_path = custom_path
        default_message = "A new custom asset has been added to the save file's data."
    
    # Ask if the user wants explanations for the fields.
    if asset_explanations:
        new_asset = new_asset_assembler_loud(file_path, for_new_game, game_name, counter_names)
    else:
        new_asset = new_asset_assembler_quiet(file_path, for_new_game, game_name, counter_names)

    # try to turn the dictionary into an object
    try:
        asset_object = dict_to_asset_object(new_asset)
    except Exception:
        print(traceback.format_exc())
    else:
     return asset_object
    
# TODO: Finish missing fields: effects, icon, image,
def new_asset_assembler_quiet(file_path: str, for_new_game: bool,
                               game_name: str, counter_names: list) -> dict:
    new_asset = {'name': '', 'category': '', 'description': '', 'source': '', 'asset_type':'',
             'attributes':[], 'buy_costs':{}, 'sell_prices':{}, 'special': '', 
             'effects':[], 'icon':'', 'image':''}
    
    print("Remember: You can always add non-required fields later!")
    
    print()
    name_dict = {}
    name_dict = set_new_asset_name(file_path, for_new_game)
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

    # TODO: Type
    print()
    new_asset['asset_type'] = set_asset_type()
    
    print()
    add_attributes = user_confirm("Do you want to add atrributes now?")
    if add_attributes:
        new_asset['attributes'] = set_attributes()

    print()
    add_costs = user_confirm("Do you want to add buy costs to the asset now?")
    if add_costs:
        new_asset["buy_costs"] = set_buy_costs(counter_names)

    print()
    add_prices = user_confirm("Do you want to add sell prices to the asset now?")
    if add_prices:
        new_asset['sell_prices'] = set_sell_prices(counter_names)

    # TODO: add effects

    # TODO: add icon

    # TODO: add image

    print("Remember: You can always add non-required fields later!")

    # check new_asset against template_asset
    try:
        template_asset = get_template_json("game",".\\statassets\\templates")
        compare_result = dict_key_compare(template_asset, new_asset)
    except:
        error_message = "Problem with comparing game_template and the new_game dict."

    if(compare_result["match"] == True):
        return new_asset
    else:
        error_message = "Warning: missing fields from new template dictionary."
        print("Warning: missing fields from new template dictionary.",
            sep="\n")
        print("Missing Fields: ", sep="\n")
        for field in compare_result["missing_values"]:
            print("Missing from new dictionary: " + field)
        # call something to fix the game or fix those specific fields.
        return error_message
    
# TODO: Finish missing fields: effects, icon, image,
def new_asset_assembler_silent(file_path: str, for_new_game: bool,
                               game_name: str,new_asset_values: dict) -> dict:
    new_asset = {'name': '', 'category': '', 'description': '', 'source': '', 'asset_type':'',
             'attributes':[], 'buy_costs':{}, 'sell_prices':{}, 'special': '', 
             'effects':[], 'icon':'', 'image':''}
    
    name_dict = {}
    name_dict = set_new_asset_name(file_path, for_new_game)
    new_asset['name'] = name_dict['name']

    # Category for a game
    new_asset['category'] = new_asset_values['category']

    add_description = user_confirm("Do you want to add a description now?")
    if add_description:
        new_asset['description'] = new_asset_values['description']

    new_asset['source'] = game_name

    # TODO: Type
    new_asset['asset_type'] = new_asset_values['asset_type']
    
    new_asset['attributes'] = new_asset_values['attributes']

    
    new_asset['buy_costs'] = new_asset_values['buy_costs']

    new_asset['sell_prices'] = new_asset_values['sell_prices']

    # TODO: add effects
    new_asset['effects'] = new_asset_values['effects']

    # TODO: add icon
    new_asset['icon'] = new_asset_values['icon_filepath']

    # TODO: add image
    new_asset['image'] = new_asset_values['image_filepath']

    # check new_asset against template_asset
    try:
        template_asset = get_template_json("game",".\\statassets\\templates")
        compare_result = dict_key_compare(template_asset, new_asset)
    except:
        error_message = "Problem with comparing game_template and the new_game dict."

    return new_asset

# TODO: Finish missing fields: icon, image
def new_asset_assembler_loud(file_path: str, for_new_game: bool,
                              game_name: str, counter_names: list) -> dict:
    # TODO: Finish
    new_asset = {'name': '', 'category': '', 'description': '', 'source': '', 'asset_type':'',
             'attributes':[], 'buy_costs':{}, 'sell_prices':{}, 'special': '', 
             'effects':[], 'other':'', 'icon':'', 'image':''}
   
    print("Remember: You can always add non-required fields later!")
   
    name_dict = {}
    name_dict['name'] = set_new_asset_name(file_path, for_new_game)
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
    
    # TODO: Typeset_asset_type
    asset_type_explanation()
    print()
    new_asset['asset_type'] = set_asset_type()
    
    attributes_explanation()
    print()
    add_attributes = user_confirm("Do you want to add atrributes now?")
    if add_attributes:
        new_asset['attributes'] = set_attributes()

    costs_explanation()
    print()
    add_costs = user_confirm("Do you want to add buy costs to the asset now?")
    if add_costs:
        new_asset["buy_costs"] = set_buy_costs(counter_names)

    prices_explanation()
    print()
    add_prices = user_confirm("Do you want to add sell prices to the asset now?")
    if add_prices:
        new_asset['sell_prices'] = set_sell_prices(counter_names)

    # TODO: add effects

    # TODO: add icon

    # TODO: add image
    print("Remember: You can always add non-required fields later!")
    
     # check new_asset against template_asset
    try:
        template_asset = get_template_json("game",".\\statassets\\templates")
        compare_result = dict_key_compare(template_asset, new_asset)
    except:
        error_message = "Problem with comparing game_template and the new_game dict."

    if(compare_result["match"] == True):
        return new_asset
    else:
        error_message = "Warning: missing fields from new template dictionary."
        print("Warning: missing fields from new template dictionary.",
            sep="\n")
        print("Missing Fields: ", sep="\n")
        for field in compare_result["missing_values"]:
            print("Missing from new dictionary: " + field)
        # call something to fix the game or fix those specific fields.
        return error_message

# Checks that the asset doesn't already exist.
def set_new_asset_name(file_path: str, for_new_game: bool) -> dict:
    file_name = ""
    name = ""
    assets = []
    asset_name = {"name": "", "file":"", "message": ""}
    valid = False
    
    while valid != True:
        # ask the user for the name of the new asset
        name = str(input("Enter the name of the new asset: ")).strip()
        file_name = format_str_for_filename(name)

        # If for a new game, don't look for already existing asset.
        if for_new_game:
                valid = True
                asset_name["name"] = name
                asset_name["file"] = file_name
        else:
            # check that an asset by that name doesn't already exists
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

def set_description() -> str:
    # TODO: Error Handling
    description = get_user_input_string_variable("Please enter a description for the asset: ", 1500)
    return description

def source_explanation():
    source_info = """The source is simply the name of the game you plan to use this asset with."""
    print(source_info)

def asset_type_explanation():
    type_info = """ Asset Type is another way to categorize and asset.
    Its another way to further break assets into small parts withing categories.
    For example if we had animal based assets and we wanted to make a lion:
    Name: Lion ||| Category: Mammal ||| Asset Type: Predator"""
    print(type_info)

# TODO: Error Handling
def set_asset_type() -> str:
    asset_type = get_user_input_string_variable("Please enter a type for the asset: ", 100)
    return asset_type

def attributes_explanation():
    attributes_info = """Attributes are different from Categories and Type.
    They can be used to describe a unit, and in the future to search
      for particular units more easily.
      
    For example if we had animal based assets and we wanted to make a lion:
    Name: Lion ||| Category: Mammal ||| Asset Type: Predator 
      Attributes: [Carnivore, Predator, Fur, Claws, Fangs, Feline]
    
    You don't need to add attributes to your unit."""
    print(attributes_info)
# TODO: Error Handling
def set_attributes() -> list:
    # TODO: Error Handling
    game_attributes_int = 0
    game_attributes = []

    game_attributes_int = okay_user_int(0,"How many attributes do you want to add to this asset?")
    game_attributes = get_user_input_loop(game_attributes_int, 'list', 'str')

    return game_attributes

def costs_explanation():
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
    print(costs_info)

# TODO: Error Handling
def set_buy_costs(counter_names: list) -> dict:
    # TODO: Error Handling
    buy_costs = {}
    list_size = 0
    list_size = len(counter_names)
    
    if list_size == 0:
        print("No precreated counters found. Manual input required.")
        game_resources_int = okay_user_int(0,"How many different costs do you need"
        " to buy or use this asset?")
        buy_costs = get_user_input_loop(game_resources_int, "Enter the field name"
        " and amount needed to buy or use this unit: ", "dict", "str")
    else:
        # we have a list of counters, use that for the field names.
        game_resources_int = okay_user_int(0,"How many different costs do you need"
        " to buy or use this asset?")
        buy_costs = buy_costs = get_user_input_loop_list(game_resources_int, "Enter the"
        " field name and amount needed to buy or use this unit: ", "dict", "str", counter_names)

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

def special_explanation():
    special_info = """Special is an extra text field that
    isn't required. Its only purpose is to exist in case you want
    to separate some text out of the description."""
    print(special_info)

def set_special() -> str:
    # TODO: Error Handling
    special = get_user_input_string_variable("Please enter the special text for the asset: ", 1500)
    return special

# TODO: finish
def set_effects():
    d = 4+4
    # TODO: We will want to wait until we have effects made.
    # Make a dictionary of effects & their description

# TODO: finish
def set_icon() -> str:
    # TODO: make this fetch the file path/move icon file to the images folder.
    e = 5+5

# TODO: finish
def set_image() -> str:
    # TODO: make this fetch the file path/move the image file to the images folder.
    f = 6+6

def update_asset(asset_dict: dict, asset_path: str, template_path: str) -> dict:
    template_result = {}
    format_result = {}
    write_result = {}
    # check the template is okay
    try:
        template_result['result'] = check_template_bool(asset_path, template_path)
    except:
        template_result['result'] = False
        template_result['message'] = 'Given object did not match save template.'
  
    # it matches the template!
    if template_result['result']:
        # try formatting the game name for a string
        try:
            format_result = format_str_for_filename_super(asset_path['name'])
        except:
            format_result['result'] = False
            format_result['message'] = 'Formatting name for asset update failed.'

        # it formatted the name!
        if format_result['result']:
            # try writing to the json_file
            try:
                write_result = overwrite_json_file(asset_dict, asset_path, format_result['string'])
            except:
                write_result['success'] = False
                write_result['message'] = 'Overwriting to asset json failed.'
            # successfully wrote!
            if write_result['success']:
                return write_result
            # did not successfully write
            else:
                return write_result
        # did not formate name
        else:
            return format_result
    # did not get a match on the template
    else:
        return template_result



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
def get_new_asset_name(name: str, file_path: str) -> dict:
    file_name = ""
    assets = []
    asset_name = {"name": "", "file":""}
    valid = False

    while valid != True:
        format_result = format_str_for_filename_super(name)
        if format_result['result']:
            # check that a game by that name doesn't already exists
            # Send the Directory Path
            assets = multi_json_names_getter(file_path, "assets")
            
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
