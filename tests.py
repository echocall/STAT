import datetime
import traceback
from pathlib import PurePath, Path
from crud import *
from utilities import *
from assethandler import *
from gamehandler import *
from savehandler import *
from StatInstance import *
from MyGame import *
import tests

def unit_test(filePaths: dict):
    print("== Unit Testing ==")
    print()
    # == GAME TESTING ==
    # ===================================================
    print("== GAME TESTING ==")
    print("== get_games_names test ==")
    # gets the names of all the games.
    game_Names = get_games_names(filePaths["gamespath"])
    print(game_Names)
    print()

    print("======== single_json_getter test ========")
    # gets a single game as a dictionary/JSON object
    game = get_game("test", filePaths["gamespath"], "games")
    print(game)
    print()
    
    print("======== new_game_assembly test ========")
    # creating a new Game Dict
    new_game = new_game_assembly(filePaths["gamespath"],filePaths["savefilepath"],filePaths["datapackpath"])
    print(new_game)
    print(len(new_game))
    print()

    # == ASSET TESTING ==
    # ===================================================
    print("== ASSET TESTING ==")
    print()
    print("======== asset_getter test ========")
    asset = single_json_getter("spellstrike", game['assetDefaultPath'], "assets")
    print(asset)
    print()

    # assets gotten
    print()
    print("======== multi_json_getter test ========")
    assets = multi_json_getter(game['assetDefaultPath'], "assets")

    print(assets)

    print ()
    print("======== default_assets_fetch test ========")
    result = {}
    result = default_assets_fetch(game['assetDefaultPath'],game['defaultAssets'])
    print(result['match'])
    print(result['missing_values'])
    print()

    for asset in result['retrieved_list']:
        print(asset)
        print()

    print()
    print("======== asset_handler test ========")
    result = {}
    print("Testing asset_handler's ability to handle merging default assets with custom assets and handling overrides.")
    print()
    print("First asset path: ")
    result = default_assets_fetch(game['assetDefaultPath'],game['defaultAssets'])
    print(result['match'])
    print(result['missing_values'])
    print()

    for asset in result['retrieved_list']:
        print(asset, sep="\f")
        print()
    result = asset_handler(game['assetDefaultPath'],game['defaultAssets'], True, "statassets\\datapacks\\test\\overrides\\savea\\assets")
    print("The result dict object should contain: missing default assets, missing assets, and a list of assets converted to a Clas Object.")
    print(result)
    converted_assets = {}
    converted_assets= result["converted_assets"]

    print(converted_assets["Barracks"])
    print(converted_assets["Barracks"].description)
    
    # == SAVE TESTING ==
    # ===================================================
    print("== SAVE TESTING ==")
    print("======== get_saves_names test ========")
    save_names = get_game_saves(game["saveFilesPath"])
    print(save_names)

    print()
    print("======== load_save test ========")
    save = load_save("save_a", game["saveFilesPath"], "saves")
    print(save)

    # == UTILITY TESTING ==
    # ===================================================
    print()
    print("== UTILITY TESTING ==")
    print()
    print("======== list_to_menut test ========")
    data_types = ["str", "int", "dict", "list"]
    print("Testing turning a list into a ennumerated menu: ")
    for value in data_types:
        print(" " + value + " ")
    print("Calling list_to_menu")
    data_type = list_to_menu("Testing for use", data_types)
    print(data_type)

    print()
    print("======== get_single_dict_value test ========")
    result = get_single_dict_value("Enter a default start value for gold.","Gold", "int")
    print(result)

    print()
    print("======== format_str_for_filename test ========")
    newFileName = format_str_for_filename("New Name")
    print(" The new file name: " + newFileName + " and the type " + type(newFileName))
    print()
    print("Testing formatting an int as a string.")
    newFileName = format_str_for_filename(2059582)
    print(" The new file name: " + newFileName + " and the type " + type(newFileName))


    # == CRUD TESTING ==
    # ===================================================
    print()
    print("== CRUD TESTING ==")
    print()
    print("======== create_new_directory test ========")
    file_path = ".\\statassets\\games\\robotest"
    did_create = create_new_directory(file_path)
    print("Attempted to create " + file_path + ". Result: ")
    print(did_create)
    print()
    print("== create_new_directory test 2 ==")
    file_path = ".\\statassets\\games\\robotest"
    did_create = create_new_directory(file_path)
    print("Attempted to create " + file_path + ". Result: ")
    print(did_create)

def regression_test(filePaths: dict):
    # Initialzie the class instance.
    currentStat = MyStat("config.txt")
    print("Is game loaded: ")
    print(currentStat.is_game_loaded)
    print("Game loaded: ")
    print(currentStat.game_loaded_name)
    print()

    filePaths = stat_initialize(currentStat.config_file)
    print(filePaths)

    # while currentStat.is_assets_loaded == False
    # call game_handler() for menus.

    selected_game = select_game(filePaths["gamespath"])
    print()

    try:
        print("Print the variables from the MyGame object.")
        print(selected_game.get_name())
        print(type(selected_game))
    except Exception:
        print(traceback.format_exc())

    selected_name = selected_game.get_name()
    currentStat.gameLoaded(selected_game, selected_name)
    print("Is game loaded: ")
    print(currentStat.is_game_loaded)
    print("Game loaded: ")
    print(currentStat.game_loaded_name)
    print()

    # == SAVES ==
    save_path = selected_game.get_savepath()
    load_save = select_save(save_path)
    print(load_save)

    currentStat.saveLoaded(load_save, load_save["name"])
    print("Is save loaded: ")
    print(currentStat.is_save_loaded)
    print("Save loaded: ")
    print(currentStat.save_loaded_name)
    print()

    # == ASSETS ==
    handler_result = asset_handler(selected_game.asset_default_path, 
                selected_game.default_assets, load_save["asset_customs"], 
                load_save["asset_customs_path"])

    print("Any missing default assets: \n")
    print(handler_result["missing_default"])
    print()
    print("The assets converted: ")
    print(handler_result["converted_assets"])
    converted_assets = handler_result["converted_assets"]
    print()
    print(type(converted_assets))

    currentStat.gameUnloaded()
    print("After calling currentStat.gameUnloaded():")
    print(currentStat.is_game_loaded)
    print()


    # === NEW GAME ====
    new_game = new_game(filePaths["gamespath"],filePaths["datapackspath"],filePaths["savespath"])
    print("After creating new-game: ")
    print(type(new_game))
    print(new_game)
    print()

    my_new_game = dict_to_game_object(new_game)

    print(type(my_new_game))
    print(my_new_game)
    print()

    currentStat.gameLoaded(my_new_game, my_new_game.get_name())
    print("After loading new_game into currentStat: ")
    print(currentStat.game_loaded_name)
    print()