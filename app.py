import os
import configparser
import datetime
from pathlib import PurePath, Path
from getters import *
from utilities import *
from assethandler import *
from gamehandler import *
from savehandler import *
import tests

filePaths = stat_initialize()

print(filePaths)

# ===================================================
# assetTypes is a set
assetTypesSet = {"set", "set2"}
# as list
assetTypes = []



print("======== single_json_getter test ========")
# gets a single game as a dictionary/JSON object
game = get_game("test", filePaths["gamespath"], "games")

print(game)
print()

# ====================================================
print()
print("======== get_saves_names test ========")
save_names = get_game_saves(game["saveFilesPath"])
print(save_names)

print()
print("======== load_save test ========")
save = load_save("save_a", game["saveFilesPath"], "saves")
print()
print(save)

# ====================================================
print()
print("======== get_games_names with multi_json_names_getter test ========")
names_test_path = filePaths["gamespath"]
game_names = get_games_names(names_test_path)

print(game_names)

# ===========================================
print()
print("======== asset_handler test ========")
result = {}
result = asset_handler(game['assetDefaultPath'],game['defaultAssets'], True, "statassets\\datapacks\\test\\overrides\\savea\\assets")

converted_assets = {}
converted_assets= result["converted_assets"]

# print(converted_assets["Barracks"])
# print(converted_assets["Barracks"].description)