from pathlib import Path, PurePath
from helpers.utilities import *
from helpers.crud import *


# Store as nested dictionary
config = get_config_as_dict('config.txt')
# Get the paths
paths = config.get("Paths",{})
rootpath = paths.get("osrootpath", "Not Set")
games_path = paths.get("gamespath", "Not Set")
templates_path = paths.get("templatespath", "Not Set")
assets_path = paths.get("assetspath", "Not Set")
effects_path = paths.get("effectspath", "Not Set")
events_path = paths.get("eventspath", "Not Set")
images_path = paths.get("imagespath", "Not Set")

testtarget = ''

template_file_name = ''
game_file_name = 'test'
default_asset_file_name = 'inn'
custom_asset_file_name = 'soldier'

str_templates_path = rootpath + templates_path
str_games_path = rootpath + games_path
str_images_path = rootpath + '//' + game_file_name + images_path
# !! IMPORTANT !!
# for these we must further consider if Default or Custom
str_assets_path = rootpath + '//' + game_file_name + assets_path
str_effects_path = rootpath + '//' + game_file_name + effects_path
str_events_path = rootpath + '//' + game_file_name + events_path

testtarget = 'game'
if testtarget == 'game':
    print('== Testing:' + testtarget + ' ==')
    directory_path = Path(str_games_path)
    print('Getting the names of the games with multi_json_names_getter:')
    print(multi_json_names_getter(directory_path, 'games'))

    print()