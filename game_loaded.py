from message import message
import theme
from pathlib import PurePath, Path
from nicegui import ui
from handlers.savehandler import *

# get the location of the saves from the loaded game

# call the function to pull in that info of the saves.

def create() -> None:
    @ui.page('/viewsaves')
    def view_saves():
        with theme.frame('- View Saves -'):
            saves = {'name': 'Save A', 'description':'A save for testing purposes.', 
                 'base_game': 'Test', 'create_date': '3/8/2025', 'date_last_save':'3/15/2025'}

            ui.label("Select a save to load!")

            with ui.row():
                with ui.card().tight():
                    with ui.card_section():
                        name = ui.label().bind_text_from(saves, 'name', 
                                                         backward=lambda name: f'Name: {name}')
                        description = ui.label().bind_text_from(saves, 'description',
                                                                 backward=lambda descript: f'Description: {descript}')
                        base_game = ui.label().bind_text_from(saves, 'base_game',
                                                                 backward=lambda base: f'Base Game: {base}')
                        create_date = ui.label().bind_text_from(saves, 'create_date',
                                                                 backward=lambda create: f'Start Date: {create}')
                        last_saved_date = ui.label().bind_text_from(saves, 'date_last_save',
                                                                 backward=lambda last_save: f'Last Save: {last_save}')
                        source = ui.button('Select Game', on_click=lambda: ui.notify('This will load the game.'))


