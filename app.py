import os
import configparser
from pathlib import PurePath, Path
from getters import *
from utilities import *
from assethandler import *
import tests

filePaths = stat_initialize()

# ===================================================
unsplitGames = []
splitGames = []
# assetTypes is a set
assetTypesSet = {"set", "set2"}
# as list
assetTypes = []

# ====================================================
# gets the unsplit names of all the games.
unsplitGames = games_names_getter(filePaths["gamespath"])
for game in unsplitGames:
    name = game.split(".")
    splitGames.append(name[0].capitalize())

print(splitGames)

# gets a single game as a dictionary/JSON object
game = single_json_getter("test", filePaths["gamespath"], "games")

# print(game)
print()
print("========")
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