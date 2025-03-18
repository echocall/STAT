import traceback
from pathlib import PurePath, Path
from crud import *
from utilities import *
from assethandler import *
from gamehandler import *
from savehandler import *
from StatInstance import *
from MyGame import *
from tests import *

# Initialzie the class instance.
currentStat = MyStat("config.txt")
print("Is game loaded: ")
print(currentStat.is_game_loaded)
print("Game loaded: ")
print(currentStat.game_loaded_name)
print()

filePaths = stat_initialize(currentStat.config_file)
print(filePaths)

# === NEW GAME ====
new_game = new_game(filePaths["gamespath"],filePaths["datapackspath"],filePaths["savespath"])
print("After creating new-game: ")
print(type(new_game))
print(new_game)
print()

my_new_game = dict_to_game_object(new_game)

print(type(my_new_game))
print(my_new_game)
print()

currentStat.gameLoaded(my_new_game, my_new_game.get_name())
print("After loading new_game into currentStat: ")
print(currentStat.game_loaded_name)
print()
