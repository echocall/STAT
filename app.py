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

# assets gotten
assets = multi_json_getter(game['assetDefaultPath'], "assets")

print(assets)

# ===================================================
print()
print("======== default_assets_fetch test ========")
print()
result = {}
result = default_assets_fetch(game['assetDefaultPath'],game['defaultAssets'])

print(result)