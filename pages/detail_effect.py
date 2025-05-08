import elements.theme as theme
from classes.Enable import Enable
from handlers.effecthandler import *
from nicegui import app, ui

enable = Enable()
@ui.page('/vieweffect/{name}')
async def view_effect():
    # pulling in the information of game etc
    # load in selected_game, if there is one.
    selected_game = app.storage.user.get("selected_game", {})
    selected_save = app.storage.user.get("selected_save", {})

    with theme.frame('View Effect'):
        with ui.column().classes("flex content-center w-100"):
            ui.label("TODO: Make this work")