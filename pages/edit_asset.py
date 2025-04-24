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

        # Select a game if none selected
        if not bool(selected_game):
            ui.label("Cannot continue without a game selected.")
            ui.label("Please select a game.")
            
        # Game selected, do things.
        else:
            # no asset selected, select one from list
            if not selected_asset:
                asset_names = assets_as_dict.keyes()
                # Create select of names of assets
                selected_name = ui.select(options=asset_names, with_input=True, on_change=lambda e: e.value)
                
                try:
                    name_result = format_str_for_filename_super(selected_name.value)
                except:
                    ui.notify("Error formatting the name result!",
                               position='top',
                              type='warning')
                if name_result['result']:
                    asset_json = single_asset_fetch(name_result['string'])
                    ui.json_editor({'content': {'json': asset_json}})
                else:
                    ui.label("Error: Problem converting the asset's name to a file name.")

        # use name from selected_asset to get JSON file
            else:
                selected_name = selected_asset['name']
                try:
                    name_result = format_str_for_filename_super(selected_name.value)
                except:
                    ui.notify("Error formatting the name result!",
                               position='top',
                              type='warning')
                if name_result['result']:
                    # Load into json object
                    asset_json = single_asset_fetch(name_result['string'])

                    ui.json_editor({'content': {'json': asset_json}})

                    ui.button('Submit')

                else:
                    ui.label("Error: Problem converting the asset's name to a file name.")

    
# gets the assets as a dictionary
async def assets_to_dictionary(assets: list, assets_as_dict: dict) -> dict:
    for asset in assets:
        assets_as_dict[asset['name']] = asset
 
    return assets_as_dict
