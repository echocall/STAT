from elements.message import message
import elements.theme as theme
from pathlib import PurePath, Path
from nicegui import app, ui
from handlers.savehandler import *

# get the location of the saves from the loaded game

# call the function to pull in that info of the saves.
@ui.page('/viewsaves')
async def view_saves():
    with theme.frame('View Saves'):
        """
        saves = [{'name': 'Save A', 'description':'A save for testing purposes.', 
                'base_game': 'Test', 'create_date': '3/8/2025', 'date_last_save':'3/15/2025'}]
        """

        # File path for save data
        config = app.storage.user.get("config", {})
        paths = config.get("Paths",{})
        saves_paths = paths.get("savesspath", "Not Set")

        existing_saves = {}
        # getting the existing games for the file path.
        existing_saves = get_saves(saves_paths)

        # setting the game objects into the user storage.
        app.storage.user['existing_saves'] = existing_saves

        ui.button("Create New Save")


        ui.label("Select a save to load!")

        save_card_container = ui.row().classes("full flex items-center")
        with save_card_container:
            for save in saves:
                with ui.card().tight():
                    with ui.card_section():
                        name = ui.label().bind_text_from(save, 'name', 
                                                        backward=lambda name: f'Name: {name}')
                        description = ui.label().bind_text_from(save, 'description',
                                                                backward=lambda descript: f'Description: {descript}')
                        base_game = ui.label().bind_text_from(save, 'base_game',
                                                                backward=lambda base: f'Base Game: {base}')
                        create_date = ui.label().bind_text_from(save, 'create_date',
                                                                backward=lambda create: f'Start Date: {create}')
                        last_saved_date = ui.label().bind_text_from(save, 'date_last_save',
                                                                backward=lambda last_save: f'Last Save: {last_save}')
                        with ui.card_actions().classes("w-full justify-end"):
                            ui.button('Select Save', on_click=lambda: ui.notify('This will load the save.'))



