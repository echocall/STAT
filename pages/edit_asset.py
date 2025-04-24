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

        assets_as_dict = {}
        asset_names = []
        asset_json = {}
        name_result = {}

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

     # if the dictionaries are not empty
        if bool(selected_save) and bool(selected_game):
            assets = asset_handler(selected_game['asset_default_path'],
                                       selected_game['default_assets'],
                                       selected_save['asset_customs'],
                                       selected_save['asset_customs_path'])
        if bool(selected_game):
            assets  = asset_handler(selected_game['asset_default_path'],
                                       selected_game['default_assets'],
                                       selected_save['asset_customs'],
                                       '')
               
        try:
            await assets_to_dictionary(assets, assets_as_dict)
        except:
            ui.notify("Error: creating assets_as_dict", type='negative', position="top",)    

        ui.label(selected_game['name'])
        ui.label(selected_asset['name'])
    
# gets the assets as a dictionary
async def assets_to_dictionary(assets: list, assets_as_dict: dict) -> dict:
    for asset in assets:
        assets_as_dict[asset['name']] = asset
 
    return assets_as_dict
