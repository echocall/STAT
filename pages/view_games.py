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

        def select_game(selected_game_name: str):
            selected_game = existing_games[selected_game_name]

            # Send the game to the app.storage.user
            app.storage.user['loaded_game'] = selected_game
            ui.navigate.to("/viewsaves/{selected_game_name}")

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
                await render_game_cards(game)

async def render_game_cards(game: dict)-> ui.element:
    with ui.button(color="dark", on_click=lambda: ui.navigate.to(f"/viewsaves/{game['name']}", new_tab=False)).style(
            'max-height: 175px; max-width:250px'
        ) as card:
        card.props("align=center")
        with ui.row():
            ui.icon("people_outlien", color="light", size="64px").classes("p-1")
            with ui.column():
                ui.label().bind_text_from(game, 'name', backward=lambda name: f'{name}')
                ui.label().bind_text_from(game, 'description', backward=lambda description: f'{description}')