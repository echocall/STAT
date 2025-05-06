import elements.theme as theme
from nicegui import app, ui
from handlers.assethandler import *
from classes.Enable import *
from helpers.utilities import *
from helpers.crud import *
from handlers.confighandler import config

enable = Enable()

@ui.page('/editasset')
async def content() -> None:
    with theme.frame(f'Asset Details'):
        selected_game = app.storage.user.get("selected_game", {})
        selected_asset = app.storage.user.get("selected_asset", {})
        
        # PATHS PATHS PATHS
        # Get the paths
        paths = config.get("Paths",{})
        root_path = paths.get("osrootpath", "Not Set")
        games_path = paths.get("gamespath", "Not Set")
        assets_path = paths.get("assetspath", "Not Set")
        default_assets_path = paths.get("defaultassetspath", "Not Set")
        custom_assets_path = paths.get("customassetspath", "Not Set")
        str_games_path = root_path + games_path
        str_assets_path = str_games_path + '\\' +  selected_game['name'] + assets_path
        str_default_assets_path = str_games_path + '\\' +  selected_game['name'] + default_assets_path
        str_custom_assets_path = str_games_path + '\\' +  selected_game['name'] + custom_assets_path
        
        assets = {}
        assets_as_dict = {}
        asset_names = []
        asset_default_names = []
        asset_custom_names = []
        asset_json = {}
        name_result = {}
        updated_json = {}
        file_path = ''
        asset_exists = False
        is_default = False

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

        # If no selected_game
        if not selected_game or 'name' not in selected_game:
            with ui.row():
                ui.icon('warning').classes('text-3xl')
                ui.label('Warning: No selected game detected.').classes('text-2xl')
            ui.label('Cannot edit an asset with no game selected.')
            ui.label('Please select a game from \'Select Games\'.')
            ui.label('And be sure to select an asset too.')
            with ui.link(target = '/selectgames'):
                ui.button('Find Game File')
        # If no selected_asset
        elif not selected_asset or 'name' not in selected_asset:
            with ui.row():
                ui.icon('warning').classes('text-3xl')
                ui.label('Warning: No selected asset detected.').classes('text-2xl')
            ui.label('Cannot edit an asset with no asset selected.')
            ui.label('Please select an asset from \'Select Assets\'.')
            with ui.link(target = '/selectassets'):
                ui.button('Find Asset File')
        else:
            try:
                # find the filepath for the asset
                selected_name = selected_asset['name'].lower()
                name_result = format_str_for_filename_super(selected_name)
                asset_default_names_result = multi_file_names_getter(str_default_assets_path, 'assets')
                asset_custom_names_result = multi_file_names_getter(str_custom_assets_path, 'assets')

                if asset_default_names_result['result']:
                    if selected_name in asset_default_names_result['list']:
                        is_default = True
                        asset_exists = True
                else:
                    ui.notify(f"Error! Problem getting the names of the default assets for the game! Please verify files are in folder:  {str_default_assets_path}  then try again.",
                              position='top',
                              type='negative',
                              multi_line=True )
                    
                if asset_custom_names_result['result']:
                        if selected_name in asset_default_names_result['list']:
                            is_default = False
                            asset_exists = True
                else:
                    ui.notify(f"Error! Problem getting the names of the custom assets for the game! Please verify files are in folder: {str_custom_assets_path} then try again.",
                              position='top',
                              type='negative',
                              multi_line=True)
            except:
                ui.notify("Error: Issue with formatting the name result! Please use standard utf8 characters and try again.",
                            position='top',
                            type='warning')
                
            if name_result['result']:
                asset_json_result = single_asset_fetch(file_path,name_result['string'])
                if asset_json_result['result']:
                    asset_json['asset'] = [asset_json_result['asset']]
                try:
                    ui.json_editor({'content': {'json': asset_json['asset']}},
                                on_change=lambda e: ui.notify(f'Change: {e}'))
                except:
                    ui.notify("Error: Problem loading the json into the json editor.")
            else:
                ui.label("Error: Problem converting the asset's name to a file name.")
            
# gets the assets as a dictionary
async def assets_to_dictionary(assets: list, assets_as_dict: dict) -> dict:
    for asset in assets:
        assets_as_dict[asset['name']] = asset
 
    return assets_as_dict
