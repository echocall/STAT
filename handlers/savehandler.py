from helpers.crud import *
from helpers.utilities import *

def save_handler():
    print("TODO: Handle the saves of various games.")

def get_game_saves(filePath: str) -> list:
    unsplitSaves = []
    splitSaveNames = []
    unsplitSaves = multi_json_names_getter(filePath, "saves")
    for save in unsplitSaves:
        name = save.split(".")
        splitSaveNames.append(name[0].capitalize())

    return splitSaveNames

# return a dictionary of all the saves associated with a game
def get_saves(file_path: str) -> dict:
    save_names = []
    save_names = get_save_names(file_path)
    
    save_files = {}
    for save in save_names:
        save_name = save.lower()
        save_files[save_name] = load_save(save, file_path, "saves")
    
    return save_files

def get_save_names(filePath: str) -> list:
    save_names = []
    save_names = multi_json_names_getter(filePath, "saves")

    return save_names

def convert_save_name(saveName: str) -> str:
    formatted_name = ""
    try:
        formatted_name = saveName.strip()
        formatted_name = formatted_name.lower()
        formatted_name = formatted_name.replace(" ", "_")
    except Exception:
            tb = sys.exception().__traceback__
            print(tb)
    return formatted_name

def load_save(save_name: str, file_path: str, type: str) -> dict:
    save = single_json_getter(save_name, file_path, type)
    return save

def select_save(file_path: str) -> dict:
    saves = []
    target_save = ''
    target_dict = {}
    save_object = {}

    # load list of game names from games folder.
    saves = multi_json_names_getter(file_path, 'saves')

    # call List_to_Menu
    target_save = list_to_menu('Select a save: ', saves)

    # load in the game_dict
    target_dict = single_json_getter(target_save, file_path, 'saves')

    return target_dict

def update_save():
    print("TODO: Update a save file.")

# TODO: Create a new save file
def new_save(save_name: str, game: dict):
    print("TODO: Create a new save file.")
    file_save_name = ""
    new_save_file = {'name': "", 'create_date': "", "date_last_save": "",
                     "description": "", "asset_customs": False, "asset_customs_path": "",
                     "actor_customs": False,"actor_customs_path": "",
                     "event_customs": False, "event_customs_path": "",
                     "effect_customs": False, "effect_customs_path": "",
                     "counters":{}, "assets":{}, "actors":{}, "current_events":{},
                     "current_effects":{},"current_turn":0, "log_file_path":""}
    # build the save dict

    # Convert save_name to file_name friendly format
    file_save_name = format_str_for_filename(save_name)

    # Get default values from the game.
    new_save_file['name'] = save_name;
    new_save_file['']

def save_current():
    print("TODO: save current STAT instance to save file.")
    # Call update save functions in MySave

def save_as_new_file():
    print("TODO: Create a new save file.")
