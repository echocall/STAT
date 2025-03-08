import os
import configparser
from pathlib import PurePath, Path
from getters import *
from utilities import *

def unit_test(filePaths: str):
    print("Testing: Getting a single Game Json object with single_json_getter")
    # gets a single game as a dictionary/JSON object
    game = single_json_getter("test", filePaths["gamespath"], "games")

    print(game['name'] == 'test')
    print()
    print("========")
    print() 

    print("======== asset_getter test ========")
    asset = asset_getter("spellstrike", game['assetDefaultPath'])
    print(asset)


    print("======== multi_json_getter test with assets ========")
    # assets gotten
    assets = multi_json_getter(game['assetDefaultPath'], "assets")

    print(assets)