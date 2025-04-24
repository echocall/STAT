import elements.theme as theme
from nicegui import app, ui
from handlers.gamehandler import *
from classes.Enable import *

enable = Enable()

@ui.page('/editasset/{gasset_name}')
async def content() -> None:
    with theme.frame(f'Asset Details'):
        a = 1+1
        # Get selected asset
        # use name from selected_asset to get JSON file
        # Load into json object

        #put json object into ui.json_editor({'content': {'json':asset_jason}},
        # on_select=lambda e: ui.notify(f'Select: {e}'),
        # on_change_lambda e: ui.notify(f'Change{e}'))