import os
import configparser
import datetime
from pathlib import PurePath, Path
from getters import *
from utilities import *
from assethandler import *
from gamehandler import *
from savehandler import *

def unit_test(filePaths: dict):

    print("========================")
    print("==== Game Testing ====")
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
    print(game['assetDefaultPath'])

    print()
    print("======== asset_getter test ========")
    asset = asset_getter("spellstrike", game['assetDefaultPath'])
    print(asset)
    print()

    # assets gotten
    print()
    print("======== multi_json_getter test ========")
    assets = multi_json_getter(game['assetDefaultPath'], "assets")

    print(assets)

    # ===================================================
    print()
    print("======== default_assets_fetch test ========")
    result = {}
    result = default_assets_fetch(game['assetDefaultPath'],game['defaultAssets'])
    print(result['match'])
    print(result['missing_values'])
    print()

    for asset in result['retrieved_list']:
        print(asset)
        print()

    # ===========================================
    print()
    print("======== asset_handler test ========")
    result = {}
    result = asset_handler(game['assetDefaultPath'],game['defaultAssets'], True, "statassets\\datapacks\\test\\overrides\\savea\\assets")

    print(result)