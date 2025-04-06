from elements.message import message
import elements.theme as theme
from fastapi import FastAPI, Depends
from nicegui import app, ui
from classes.MyGame import MyGame
import pages.view_saves as view_saves
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
        app.storage.user["existing_games"] = existing_games

        # Displaying the games.
        game_card_container = ui.row().classes("full flex items-center")
        with game_card_container:
            for game in existing_games.values():
                await render_game_cards(existing_games, game)


def select_game(existing_games: dict, selected_game_name: str):
    for name in selected_game_name:
        selected_game = {}
        try:
            selected_game = existing_games[name]
        except:
            ui.notify("Warning! Problem with loading game. Please check that game file exists.")
        finally:
            app.storage.user['loaded_game'] = selected_game
            ui.navigate.to(f"/viewsaves/{selected_game_name}")

async def render_game_cards(existing_games: dict, game: dict)-> ui.element:
    with ui.card().tight().style('max-height: 175px; max-width:250px'):
        with ui.card_section():
            ui.label().bind_text_from(game, 'name', backward=lambda name: f'{name}')
            ui.label().bind_text_from(game, 'description', backward=lambda description: f'{description}')
        with ui.card_actions().classes("w-full justify-end"):
            ui.button('Select Game', on_click=lambda: select_game(existing_games, {game['name']}))