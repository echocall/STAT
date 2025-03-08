import os
import configparser
from pathlib import PurePath, Path
from getters import games_names_getter, game_getter, assets_getter, asset_getter

# Reading from config file
configParser = configparser.RawConfigParser()
configFilePath = 'config.txt'
configParser.sections()
configParser.read(configFilePath)

filePaths = {}

for x in configParser['Paths']:
        filePaths[x] = configParser['Paths'][x]

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

# gets a single game as a dictionary/JSON object
game = game_getter("test", filePaths["gamespath"])

"""
for key in game:
      print(key)
"""

assets = []

assets = assets_getter(game['assetDefaultPath'])

# clearing out unneeded values from our set.
assetTypesSet.clear()
# getting the different Asset Types for later processing.
for asset in assets:
    print(asset['assettype'])
    assetTypesSet.add(asset['assettype'])

for asset in assets:
     if asset['assettype'] == assetTypesSet[0]:
        print(asset)