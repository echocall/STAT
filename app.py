import os
import configparser
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


# Initialzie the class instance.
currentStat = MyStat("config.txt")
print(currentStat.is_assets_loaded)

filePaths = stat_initialize(currentStat.config_file)

print(filePaths)

## from gameInstance feed

# ===================================================
# assetTypes is a set
assetTypesSet = {"set", "set2"}
# as list
assetTypes = []

# ==========================

# selected_game = dict_to_game_object(game)
selected_game = select_game(filePaths["gamespath"])

try:
    print(selected_game.get_name())
except Exception:
    print(traceback.format_exc())


print(type(selected_game))

currentStat.gameLoaded(selected_game, selected_game.get_name)


"""
print("======== new_game_assembly test ========")
# creating a new Game Dict
new_game = new_game_assembly(filePaths["gamespath"],filePaths["savefilepath"],filePaths["datapackpath"])
print(new_game)
print(len(new_game))
"""