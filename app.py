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

currentStat.gameLoaded(selected_game, selected_game.get_name)
print("Is game loaded: ")
print(currentStat.is_game_loaded)
print("Game loaded: ")
print(currentStat.game_loaded_name)
print()

# == SAVES ==

load_save = select_save(filePaths["savefilepath"])
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

# === NEW GAME ====
currentStat.gameUnloaded()
print("After calling currentStat.gameUnloaded():")
print(currentStat.is_game_loaded)
print()

new_game = new_game(filePaths["gamespath"],filePaths["savespath"])
print("After creating new-game: ")
print(type(new_game))
print(new_game)
print()

my_new_game = dict_to_game_object(new_game)

print(type(my_new_game))
print(my_new_game)
print()

currentStat.gameLoaded(my_new_game, my_new_game.get_name)
print("After loading new_game into currentStat: ")
print(currentStat.game_loaded_name)
print()
