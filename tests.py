import os
import configparser
import datetime
from pathlib import PurePath, Path
from crud import *
from utilities import *
from assethandler import *
from gamehandler import *
from savehandler import *

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
    result = asset_handler(game['assetDefaultPath'],game['defaultAssets'], True, "statassets\\datapacks\\test\\overrides\\savea\\assets")

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
    data_types = ["str", "int"]
    data_type = list_to_menu("Testing for use", data_types)
    print(data_type)

    print()
    print("======== get_single_dict_value test ========")
    result = get_single_dict_value("Enter a default start value for gold.","Gold", "int")
    print(result)

    print()
    print("======== format_str_for_filename test ========")
    newFileName = format_str_for_filename("New Name")
    print(newFileName)
    print(type(newFileName))
    newFileName = format_str_for_filename(123456)
    print(newFileName)
    print(type(newFileName))


    # == CRUD TESTING ==
    # ===================================================
    print()
    print("== CRUD TESTING ==")
    print()
    print("======== create_new_directory test ========")
    file_path = ".\\statassets\\games\\robotest"
    did_create = create_new_directory(file_path)
    print(did_create)
