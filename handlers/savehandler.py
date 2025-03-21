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

def load_save(saveName: str, filePath: str, type: str) -> dict:
    save = single_json_getter(saveName, filePath, type)
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

def new_save():
    print("TODO: Create a new save file.")

def save_current():
    print("TODO: save current STAT instance to save file.")
    # Call update save functions in MySave

def save_as_new_file():
    print("TODO: Create a new save file.")
