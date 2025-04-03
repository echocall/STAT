from fastapi import Depends
from nicegui import ui
from helpers.crud import *
from helpers.utilities import *
from handlers.assethandler import *  # TODO: Change this later.
import classes.MyGame as mg
import traceback
import json
from pathlib import Path

# Dependency to load game session
def get_game_session(file_path: str, game_name: str):
    game_file = Path(file_path) / f"{game_name}.json"
    if game_file.exists():
        with open(game_file, "r") as file:
            return json.load(file)
    return None

def game_handler(is_game_loaded: bool, game_data: dict = Depends(get_game_session)) -> object:
    if not is_game_loaded:
        print("Does user want to create a JSON for a new game or load a preexisting game JSON?")
    return game_data

def new_game(game_path: str, saves_path: str, datapack_path: str) -> dict:
    try:
        new_game_dict = new_game_assembly(game_path, saves_path, datapack_path)
        new_file_name = format_str_for_filename(new_game_dict["name"])
        write_successful = create_new_json_file(new_file_name, game_path, 'game')
        return new_game_dict if write_successful else {"error": "Could not save new game."}
    except Exception:
        print(traceback.format_exc())
        return {"error": "An exception occurred while creating a new game."}

def get_game(game_name: str, file_path: str) -> dict:
    return single_json_getter(game_name, file_path, 'game')

def get_game_as_obj(game_name: str, file_path: str) -> object:
    game_dict = single_json_getter(game_name, file_path, 'game')
    return mg.MyGame(**game_dict) if game_dict else None

def get_games_names(file_path: str) -> list:
    return multi_json_names_getter(file_path, "games")

def update_game(game_name: str, file_path: str, key: str, new_value, game_data: dict = Depends(get_game_session)) -> bool:
    if game_data and key in game_data:
        game_data[key] = new_value
        return overwrite_json_file(game_data, file_path, game_name)
    return False
