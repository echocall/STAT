from handlers.confighandler import config_path, load_config
from nicegui import app, ui
import elements.theme as theme

@ui.page('/')
async def content() -> None:
    with theme.frame('Home'):
    

        ui.label("Welcome to STAT!").classes('text-center accent-text text-lg')
        ui.label("The Snazzy Tabletop Assistant Tracker").classes('text-center')
        ui.label('Do you want to add a new game to STAT or work with a preexisting game?').classes('text-center')
        with ui.row().classes('space-x-4 justify-center'):
            with ui.link(target='/creategame'):
                ui.button("Create New Game", icon="create").props('size=medium').classes('flex-grow')

            with ui.link(target='/selectgames'):
                ui.button("View Games", icon="view_list").props('size=medium').classes('flex-grow')
    