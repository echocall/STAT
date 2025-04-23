from elements.message import message
import elements.theme as theme
from pathlib import PurePath, Path
from nicegui import app, ui
from handlers.savehandler import *

# call the function to pull in that info of the saves.
@ui.page('/selectsaves/{game_name}')
async def view_saves():
    with theme.frame('View Saves'):
        # File path for save data
        selected_game = app.storage.user.get("selected_game", {})
        saves_paths = selected_game.get("save_files_path", "Not Set")
        
        existing_saves = {}
        # getting the existing saves for the loaded game
        try:
            existing_saves = get_saves(saves_paths)
        except Exception as e:
            ui.notify(f"Error loading saves: {str(e)}", type='negative', position="top",)
            return
        
        with ui.link(target='/createsave'):
            ui.button("Create New Save")

        ui.label("Select a save to load:").classes('h-4')
    
        save_card_container = ui.row().classes("full flex items-center")
        with save_card_container:
            if existing_saves:
                for save in existing_saves.values():
                    await render_save_cards(existing_saves, save)
            else:
                ui.label("No saves to display!")

def load_save(existing_saves, selected_save_name):
    for name in selected_save_name:
        selected_save = {}
        save_to_get = convert_save_name(name)
        try:
            selected_save = existing_saves[save_to_get]
            app.storage.user['is_save_loaded']  = True
        except:
            ui.notify("Unable to load save.", type='negative', position="top",)
        finally:
            # pass back empty dict even if nothing is available.
            app.storage.user["selected_save"] = selected_save
            ui.notify(f"Success! You selected save {name}.", type='positive', position='top')
            ui.navigate.reload()

async def render_save_cards(existing_saves, save):
    with ui.card().tight().style('width: 100%; max-width: 250px; aspect-ratio: 4 / 3; max-height: 175px;'):
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

