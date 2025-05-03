from pathlib import Path, PurePath
from helpers.utilities import *
from helpers.crud import *


# Store as nested dictionary
config = get_config_as_dict('config.txt')
# Get the paths
paths = config.get("Paths",{})
rootpath = paths.get("osrootpath", "Not Set")
games_path = paths.get("gamespath", "Not Set")
saves_path = paths.get("savespath", "Not Set")
templates_path = paths.get("templatespath", "Not Set")
assets_path = paths.get("assetspath", "Not Set")
default_assets_path = paths.get("defaultassetspath", "Not Set")
custom_assets_path = paths.get("customassetspath", "Not Set")
effects_path = paths.get("effectspath", "Not Set")
default_effects_path = paths.get("defaulteffectspath", "Not Set")
custom_effects_path = paths.get("customeffectspath", "Not Set")
events_path = paths.get("eventspath", "Not Set")
default_events_path = paths.get("defaulteventspath", "Not Set")
custom_events_path = paths.get("customeventspath", "Not Set")
images_path = paths.get("imagespath", "Not Set")

test_target = ''

template_file_name = ''
game_file_name = 'test'
default_asset_file_name = 'inn'
custom_asset_file_name = 'soldier'

str_templates_path = rootpath + templates_path
str_games_path = rootpath + games_path


str_images_path = str_games_path + '\\' + game_file_name + images_path
str_saves_path = str_games_path + '\\' +  game_file_name + '\\' +  saves_path

str_image_path = ''

"""
print(str_games_path)
print(str_saves_path)
print(str_images_path)

"""

# !! IMPORTANT !!
# for these we must further consider if Default or Custom
str_assets_path = str_games_path + '\\' +  game_file_name + assets_path
str_default_assets_path = str_games_path + '\\' +  game_file_name + default_assets_path
str_custom_assets_path = str_games_path + '\\' +  game_file_name + custom_assets_path

str_effects_path = str_games_path + '\\' + game_file_name + effects_path
str_default_effects_path = str_games_path + '\\' +  game_file_name + default_effects_path
str_custom_effects_path = str_games_path + '\\' +  game_file_name + custom_effects_path

str_events_path = str_games_path + '\\' + game_file_name + events_path
str_default_events_path = str_games_path + '\\' +  game_file_name + default_events_path
str_custom_events_path = str_games_path + '\\' +  game_file_name + custom_events_path

# Individual files

str_game_path = str_games_path + '\\' + game_file_name + '\\' +  'test.json'
str_save_path = str_saves_path + '\\' + "save_a" + '\\' + "save_a.json"
str_default_asset_path = str_default_assets_path + '\\' + 'forge.json'
str_custom_asset_path = str_custom_assets_path + '\\' + 'soldier.json'

print(str_default_asset_path)
print(str_custom_asset_path)

# TODO: fix these with proper names of effects
"""
str_default_effect_path = str_default_effects_path + '\\' + 'forge.json'
str_custom_effect_path = str_custom_effects_path + '\\' + 'soldier.json'
"""

"""
print(str_game_path)

"""

test_targets = ['game', 'image', 'save', 'asset', 'effect']
for test_target in test_targets:
    # GAME
    if test_target == 'game':
        print('== Testing: ' + test_target + ' ==')
        directory_path = Path(str_games_path)
        print(directory_path)
        print('Getting the names of the games with multi_json_names_getter:')
        print(multi_file_names_getter(directory_path, 'games'))
        print()

        print("Getting the file with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(str_game_path, 'game')['result'])
        print()
    # IMAGES
    elif test_target == 'image':
        print('== Testing: ' + test_target + ' ==')
        directory_path = Path(str_images_path)
        print('Getting the names of the games with multi_json_names_getter:')
        print(multi_file_names_getter(directory_path, 'images'))
        print()

        print("Getting the image file with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(str_image_path, 'image')['result'])
        print()
    # SAVE
    elif test_target == 'save':
        print('== Testing: ' + test_target + ' ==')
        directory_path = Path(str_saves_path)
        print('Getting the names of the games with multi_json_names_getter:')
        print(multi_file_names_getter(directory_path, 'saves'))
        print()

        print("Getting the save file with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(str_save_path, 'save')['result'])
        print()
    # ASSETS
    elif test_target == 'asset':
        print('== Testing: ' + test_target + ' ==')
        directory_path = Path(str_assets_path)
        print('Getting the names of the games with multi_json_names_getter:')
        print(multi_file_names_getter(directory_path, 'assets'))
        print()

        print("Getting the default asset with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(str_default_asset_path, 'asset')['result'])
        print()

        print("Getting the custom asset with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(str_custom_asset_path, 'asset')['result'])
        print()

    # EFFECT
    """
    elif test_target == 'effect':
        print('== Testing: ' + test_target + ' ==')
        directory_path = Path(str_effects_path)
        print('Getting the names of the games with multi_json_names_getter:')
        print(multi_file_names_getter(directory_path, 'effects'))
        print()

        default_file_path = Path(str_default_effect_path)
        print("Getting the file with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(default_file_path, 'effect'))
        print()
        custom_file_path = Path(str_custom_effect_path)
        print("Getting the file with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(custom_file_path, 'effect'))
        print()
    """
    # EVENT
    """
    elif test_target == 'event':
        print('== Testing: ' + test_target + ' ==')
        directory_path = Path(str_events_path)
        print('Getting the names of the games with multi_json_names_getter:')
        print(multi_file_names_getter(directory_path, 'assets'))
        print()

        default_file_path = Path(str_default_event_path)
        print("Getting the file with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(default_file_path, 'event'))
        print()
        custom_file_path = Path(str_custom_event_path)
        print("Getting the file with single_json_getter_fullpath:")
        print(single_json_getter_fullpath(custom_file_path, 'event'))
        print()
    """

