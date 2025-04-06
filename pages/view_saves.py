from elements.message import message
import elements.theme as theme
from pathlib import PurePath, Path
from nicegui import app, ui
from handlers.savehandler import *

# get the location of the saves from the loaded game

# call the function to pull in that info of the saves.
@ui.page('/viewsaves')
async def view_saves():
    def load_save(selected_game_name, existing_saves):
        loaded_save = {}
        try:
            for save in existing_saves:
                if save['name'] == selected_game_name:
                    loaded_save = save
        except:
            ui.notify("Unable to load save.")
        finally:
            # pass back empty dict even if nothing is available.
            app.storage.user["loaded_save"] = loaded_save

    with theme.frame('View Saves'):
        # File path for save data
        loaded_game = app.storage.user.get("loaded_game", {})
        saves_paths = loaded_game.get("save_files_path", "Not Set")

        existing_saves = {}
        # getting the existing saves for the loaded game
        existing_saves = get_saves(saves_paths)

        ui.button("Create New Save")

        if not existing_saves:
            ui.label("No saves exist for this game! Create a new save.")
        else: 
            ui.label("Select a save to load!")

            save_card_container = ui.row().classes("full flex items-center")
            with save_card_container:
                for save in existing_saves:
                    with ui.card().tight().style('max-height: 175px; max-width:250px'):
                        with ui.card_section():
                            save_name = ui.label().bind_text_from(save, 'name', 
                                                            backward=lambda name: f'{name}')
                            base_game = ui.label().bind_text_from(save, 'base_game',
                                                                    backward=lambda base: f'Base Game: {base}')
                            create_date = ui.label().bind_text_from(save, 'create_date',
                                                                    backward=lambda create: f'Start Date: {create}')
                            last_saved_date = ui.label().bind_text_from(save, 'date_last_save',
                                                                    backward=lambda last_save: f'Last Save: {last_save}')
                            with ui.card_actions().classes("w-full justify-end"):
                                ui.button('Select Save', on_click=load_save(save_name.name))


