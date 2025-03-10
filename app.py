import os
import configparser
import datetime
from pathlib import PurePath, Path
from crud import *
from utilities import *
from assethandler import *
from gamehandler import *
from savehandler import *
import StatInstance
import tests


# Initialzie the class instance.
currentStat = StatInstance.MyStat("config.txt")

filePaths = stat_initialize(currentStat.config_file)

print(filePaths)

# ===================================================
# assetTypes is a set
assetTypesSet = {"set", "set2"}
# as list
assetTypes = []

print("======== single_json_getter test ========")
# gets a single game as a dictionary/JSON object
game = get_game("test", filePaths["gamespath"], "games")

currentStat.gameLoaded(game, "test")

print(currentStat.is_game_loaded)


