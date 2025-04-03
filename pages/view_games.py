from elements.message import message
import elements.theme as theme
from fastapi import FastAPI, Depends
from nicegui import app, ui
from classes.MyGame import MyGame
from handlers.gamehandler import *

@ui.page('/viewgames')
async def view_games():
    with theme.frame('View Games'):

        # File path for game data
        config = app.storage.user.get("config", {})
        paths = config.get("Paths",{})
        game_paths = paths.get("gamespath", "Not Set")

        existing_games = {}
        # getting the existing games for the file path.
        existing_games = get_games(game_paths)

        # setting the game objects into the user storage.
        app.storage.user['existing_games'] = existing_games

        # Displaying the games.
        game_card_container = ui.row().classes("full flex items-center")
        with game_card_container:
            for game in existing_games.values():
                with ui.card().tight().style('max-height: 175px; max-width:250px'):
                    with ui.card_section():
                        ui.label().bind_text_from(game, 'name', backward=lambda name: f'Name: {name}')
                        ui.label().bind_text_from(game, 'description', backward=lambda description: f'{description}')
                    with ui.card_actions().classes("w-full justify-end"):
                        ui.button('Select Game', on_click=lambda: ui.notify('This will load the game & send to view_saves.'))



            