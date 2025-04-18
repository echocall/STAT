import elements.theme as theme
from fastapi import FastAPI, Depends
from nicegui import app, ui
from handlers.gamehandler import *
from elements.select_game_dialog import prompt_select_game
from classes.Enable import *

@ui.page('/viewgame/{game_name}')
async def game_detail():
    with theme.frame(f'Game Details'):
        selected_game = app.storage.user.get("selected_game", {})

        with ui.row():
            btn_select = ui.button('Select Game',on_click=prompt_select_game)
            
            with ui.link(target='/createasset'):
                btn_create_asset = ui.button('Create Asset')
            
            with ui.link(target='/createeffect'):
                btn_create_event = ui.button('Create Effect')

        # If no game is selected, prompt the user to select one
        if not selected_game:
            selected_game = await prompt_select_game
        else:
            # Display the label if a game is already selected
            ui.label("TODO: Fill this in. :) :) :)")
            ui.label("Game Name:").classes('h-3')
            ui.label(f"{selected_game['name']}").bind_text_from(selected_game['name'])
            ui.input(label='Game Name: ', )
            ui.button("Edit",icon='edit')
            # View the details of the selected game
            # View list of assets of the selected game
                # Split lists into default assets and custom assets
                # TODO: do custom assets AFTER file layout rework
            # view list of effects of the selected game
