import elements.theme as theme
from nicegui import app, ui
from handlers.gamehandler import *
from elements.select_game_dialog import prompt_select_game
from classes.Enable import *

enable = Enable()

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
            if not selected_game or 'name' not in selected_game:
                with ui.row():
                    ui.icon('warning').classes('text-3xl')
                    ui.label('Warning: No selected game detected.').classes('text-2xl')
                ui.label('Cannot create asset with no game selected.')
                ui.label('Please select a game from \'Select Games\'.')
                with ui.link(target = '/selectgames'):
                    ui.button('Find Game File')
        else:
            # Display the label if a game is already selected
            ui.label("TODO: Fill this in. :) :) :)")
            toggle_edit_name = ui.switch('Edit?').props('color="green"')
            ui.label("Current Name:").classes('h-3')
            game_name = ui.label(f"{selected_game['name']}").bind_text_from(selected_game['name'])

            game_name_edit = ui.input(label='New Name: ', placeholder='50 character limit',
                                        on_change=lambda e: game_name.set_text(e.value))
            game_name_edit.props('clearable')
            game_name_edit.bind_value(selected_game, 'name')
            game_name_edit.validation={"Too short!": enable.is_too_short} 
            game_name_edit.bind_visibility_from(toggle_edit_name, 'value')
            # View the details of the selected game
            # View list of assets of the selected game
                # Split lists into default assets and custom assets
                # TODO: do custom assets AFTER file layout rework
            # view list of effects of the selected game
