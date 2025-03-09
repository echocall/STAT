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


