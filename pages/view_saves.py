from elements.message import message
import elements.theme as theme
from pathlib import PurePath, Path
from nicegui import app, ui
from handlers.savehandler import *

# get the location of the saves from the loaded game

# call the function to pull in that info of the saves.
@ui.page('/viewsaves/{game_name}')
async def view_saves():
    with theme.frame('View Saves'):
        # File path for save data
        loaded_game = app.storage.user.get("loaded_game", {})
        saves_paths = loaded_game.get("save_files_path", "Not Set")
        
        existing_saves = {}
        # getting the existing saves for the loaded game
        existing_saves = get_saves(saves_paths)
        ui.button("Create New Save")

        ui.label("Select a save to load!")
    
        save_card_container = ui.row().classes("full flex items-center")
        with save_card_container:
            for save in existing_saves.values():
                ui.label().bind_text_from(save,'name', backward=lambda name: f'{name}')
                await render_save_cards(existing_saves, save)

def load_save(existing_saves, selected_save_name):
    for name in selected_save_name:
        loaded_save = {}
        save_to_get = convert_save_name(name)
        print(save_to_get)
        print(existing_saves)
        try:
            print(existing_saves[save_to_get])
            loaded_save = existing_saves[save_to_get]
        except:
            ui.notify("Unable to load save.")
        finally:
            # pass back empty dict even if nothing is available.
            app.storage.user["loaded_save"] = loaded_save

async def render_save_cards(existing_saves, save):
    with ui.card().tight().style('max-height: 175px; max-width:250px'):
        with ui.card_section():
            ui.label().bind_text_from(save, 'name', backward=lambda name: f'{name}')
            ui.label().bind_text_from(save, 'base_game',
                                                    backward=lambda base: f'Base Game: {base}')
            ui.label().bind_text_from(save, 'create_date',
                                                    backward=lambda create: f'Start Date: {create}')
            ui.label().bind_text_from(save, 'date_last_save',
                                                    backward=lambda last_save: f'Last Save: {last_save}')
            with ui.card_actions().classes("w-full justify-end"):
                ui.button('Select Save', on_click=lambda: load_save(existing_saves, {save['name']}))