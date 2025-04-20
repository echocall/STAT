import elements.theme as theme
from classes.Enable import Enable
from handlers.savehandler import *
from nicegui import app, ui

enable = Enable()
@ui.page('/viewsave')
async def new_asset():
    # pulling in the information of game etc
    # load in selected_game, if there is one.
    selected_game = app.storage.user.get("selected_game", {})
    selected_save = app.storage.user.get("selected_save", {})

    with theme.frame('View Save'):
        with ui.column().classes("flex content-center w-100"):
            if not selected_game or 'name' not in selected_game:
                with ui.row():
                    ui.icon('warning').classes('text-3xl')
                    ui.label('Warning: No selected game detected.').classes('text-2xl')
                ui.label('Cannot create asset with no game selected.')
                ui.label('Please select a game from \'Select Games\'.')
                with ui.link(target = '/selectgames'):
                    ui.button('Find Game File')
            else:
                # Name the source game
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label('Source Game: ').classes('font-bold')
                        ui.label(f'{selected_game['name']}')

                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        # If no selected_save, open up prompt to select one
                        if not selected_save or 'name' not in selected_save:
                            ui.label('Warning: No selected save detected.')
                            ui.label('Please select a save .json file.')
                            with ui.link(target=f'/selectsaves/{selected_game['name']}'):
                                ui.button('Find Save File')
                        else:
                            # Name the source save
                            with ui.column().classes('items-start'):
                                ui.label('Save Name: ').classes('font-bold')
                                ui.label(f'{selected_save['name']}')