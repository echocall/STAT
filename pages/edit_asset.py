import elements.theme as theme
from nicegui import app, ui
from handlers.assethandler import *
from classes.Enable import *

enable = Enable()

@ui.page('/editasset')
async def content() -> None:
    with theme.frame(f'Asset Details'):
        selected_game = app.storage.user.get("selected_game", {})
        selected_save = app.storage.user.get("selected_save", {})
        selected_asset = app.storage.user.get("selected_asset", {})

        assets = {}
        assets_as_dict = {}
        asset_names = []
        asset_default_names = []
        asset_custom_names = []
        asset_json = {}
        name_result = {}
        updated_json = {}
        file_path = ''

        asset_schema = {
                    "name":{
                        'type': 'string', 
                    },
                    "category":{
                        'type': 'string', 
                    },
                    "description":{
                        'type': 'string', 
                    },
                    "source":{
                        'type': 'string', 
                    },
                    "asset_type":{
                        'type': 'string', 
                    },
                    "attributes":{
                        'type': 'array'
                        },
                    "buy_costs":{
                        'type': 'object',
                    },
                    "sell_prices":{
                        'type': 'object', 
                    },
                    "special":{
                        'type': 'string', 
                    },
                    "effects":{
                        'type': 'array', 
                    },
                    "other":{
                        'type': 'string', 
                    },
                    "icon":{
                        'type': 'string', 
                    },
                    "image":{
                        'type': 'string', 
                    },
                } 

        try:
            selected_name = selected_asset['name']
            print(selected_name)
            name_result = format_str_for_filename_super(selected_name)
            asset_default_names = multi_json_names_getter(selected_game['asset_default_path'], 'assets')
            print(asset_default_names)
            asset_custom_names = multi_json_names_getter(selected_save['asset_customs_path'], 'assets')
            print(asset_custom_names)

            if selected_name in asset_default_names:
                file_path = selected_game['default_assets']
            elif selected_name in asset_custom_names:
                file_path = selected_save['asset_customs_path']

        except:
            ui.notify("Error: Issue with formatting the name result!",
                        position='top',
                        type='warning')
            
        if name_result['result']:
            asset_json = single_asset_fetch(file_path,name_result['string'])
            print(asset_json)
            print(type(asset_json))
            try:
                ui.json_editor({'content': {'json': asset_json}})
            except:
                ui.notify("Error: Problem loading the json into the json editor.")
        else:
            ui.label("Error: Problem converting the asset's name to a file name.")
           
# gets the assets as a dictionary
async def assets_to_dictionary(assets: list, assets_as_dict: dict) -> dict:
    for asset in assets:
        assets_as_dict[asset['name']] = asset
 
    return assets_as_dict
