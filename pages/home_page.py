from elements.message import message
from new_game_dialog import new_game_dialog
import elements.theme as theme
from helpers.utilities import *

from nicegui import app, ui

@ui.page('/')
async def content() -> None:

        config_data = load_config('config.txt')
        structured_data = {}
        
        # Create organized nested structure.
        for key in config_data:
            structured_data[key] = config_data[key]

        # Store as nested dictionary
        app.storage.user["config"] = structured_data
        
        ui.label("Welcome to STAT!")

        ui.label('Do you want to add a new game to STAT, or work with a preexisting game?')
        with ui.link(target='/creategame'):
            ui.button("Create New Game", icon="create")

        with ui.link(target='/viewgames'):
            ui.button("Load Games", icon="view_list")