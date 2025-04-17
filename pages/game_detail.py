import elements.theme as theme
from fastapi import FastAPI, Depends
from nicegui import app, ui
from handlers.gamehandler import *
from elements.select_game_dialog import prompt_select_game



@ui.page('/viewgame/{game_name}')
async def game_detail():
    with theme.frame('Select Games'):
        selected_game = app.storage.user.get("selected_game", {})
        # If no game is selected, prompt the user to select one
        if not selected_game:
            ui.label('No game selected, please select a game.')
            selected_game = await prompt_select_game
        else:
            # Display the label if a game is already selected
            ui.label("TODO: Fill this in. :) :) :)")
            ui.label(f"{selected_game['name']}")
            # View the details of the selected game
            # View list of assets of the selected game
                # Split lists into default assets and custom assets
                # TODO: do custom assets AFTER file layout rework
            # view list of effects of the selected game