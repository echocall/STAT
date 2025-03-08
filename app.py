import os
import configparser
from pathlib import PurePath, Path
from getters import *
from utilities import *

filePaths = stat_initialize()

# ===================================================
unsplitGames = []
splitGames = []
# assetTypes is a set
assetTypesSet = {"set", "set2"}
# as list
assetTypes = []

# gets the unsplit names of all the games.
unsplitGames = games_names_getter(filePaths["gamespath"])
for game in unsplitGames:
    name = game.split(".")
    splitGames.append(name[0].capitalize())

print(splitGames)
# gets a single game as a dictionary/JSON object
game = game_getter("test", filePaths["gamespath"])

# assets gotten
assets = assets_getter(game['assetDefaultPath'])

# ===================================================

