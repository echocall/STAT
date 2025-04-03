from elements.message import message
from new_game_dialog import new_game_dialog
import elements.theme as theme

from nicegui import app, ui

@ui.page('/')
async def content() -> None:
        ui.label("Welcome to STAT!")

        ui.label('Do you want to add a new game to STAT, or work with a preexisting game?')
        new_game = ui.button(
        "Create New Game",
        icon="create",
        )
        new_game.on("click",
                    lambda: new_game_dialog())

        with ui.link(target='/viewgames'):
            ui.button('View Games')