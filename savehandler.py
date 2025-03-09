from getters import *
from utilities import *

def save_handler():
    print("TODO: Handle the saves of various games.")

def get_game_saves(filePath: str) -> list:
    unsplitSaves = []
    splitSaveNames = []
    unsplitSaves = games_names_getter(filePath)
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

def update_save():
    print("TODO: Update a save file.")

def new_save():
    print("TODO: Create a new save file.")

def save_current():
    print("TODO: save current STAT instance to save file.")

def save_as_new_file():
    print("TODO: Create a new save file.")
