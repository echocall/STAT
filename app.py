import traceback
from helpers.crud import *
from helpers.utilities import *
from handlers.assethandler import *
from handlers.gamehandler import *
from handlers.savehandler import *
from classes.StatInstance import *
from classes.MyGame import *
from tests import *

# Initialzie the class instance.
currentStat = MyStat("config.txt")
print("Is game loaded: ")
print(currentStat.is_game_loaded)
print("Game loaded: ")
print(currentStat.game_loaded_name)
print()

# filePaths = stat_initialize(currentStat.config_file)
# print(filePaths)

check_load_config = load_config(currentStat.config_file)
print(check_load_config)
print()
print()


# === NEW GAME ====

game_template = single_json_getter('template_game','C:\\Users\\strip\\Documents\\github\\STAT\\statassets\\templates','template')
print(game_template)

new_game_dict = {'name': '','description':'', 'has_counters': False,
                'counters': {}, 'has_actors': False,
                'actor_default_path':'', 'default_actors':[],
                'has_assets': False, 'asset_default_path':'',
                'default_assets':[], 'has_events': False, 
                'event_default_path':'', 'default_events':[],
                'has_effects': False, 'effect_default_path':'',
                'default_effects':[],'icon':'',
                  'save_files_path':'', 'has_turns':False,
                'turn_type':'', 'start_turn':0}


template_check = check_template_bool(new_game_dict, 'C:\\Users\\strip\\Documents\\github\\STAT\\statassets\\templates')
print(template_check)
