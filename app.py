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
print("Is game loaded: " + currentStat.is_game_loaded)
print("Game loaded: " + currentStat.game_loaded_name)

filePaths = stat_initialize(currentStat.config_file)

# while currentStat.is_assets_loaded == False
    # call game_handler() for menus.

selected_game = select_game(filePaths["gamespath"])

try:
    print(selected_game.get_name())
    print(type(selected_game))
except Exception:
    print(traceback.format_exc())

currentStat.gameLoaded(selected_game, selected_game.get_name)
print("Is game loaded: " + currentStat.is_game_loaded)
print("Game loaded: " + currentStat.game_loaded_name)
# === NEW GAME ====
currentStat.gameUnloaded()
print(currentStat.is_game_loaded)

new_game = new_game(filePaths["gamespath"],filePaths["savespath"])
print(type(new_game))
print(new_game)

my_new_game = dict_to_game_object(new_game)

print(type(my_new_game))
print(my_new_game)

currentStat.gameLoaded(my_new_game, my_new_game.get_name)
print(currentStat.game_loaded_name)
