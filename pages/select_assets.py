import elements.theme as theme
from nicegui import app, ui
from handlers.assethandler import *
from elements.alert_dialog import alert_dialog
from helpers.utilities import format_str_for_filename_super
from elements.UserConfirm import *

@ui.page('/selectassets')
async def select_assets():

    def asset_view_details(selected_asset):
        """Take user to view the details of a asset unless user has not selected a asset."""
        if not selected_asset or 'name' not in selected_asset:
            ui.notify("Please select an asset before trying to view its details.",
                    position='top',
                    type='warning')
        else:
            ui.navigate.to(f"/viewasset/")

    def select_target_asset(existing_assets: dict, selected_asset_name: str):
        """Load the selected asset into storage and refresh the page."""
        for name in selected_asset_name:
            # getting the name to be correct.
            file_name = format_str_for_filename_super(name)['string']
            selected_asset = {}

            # trying to get the specified asset
            try:
                selected_asset = existing_assets[file_name]
            except:
                alert_dialog("Problem with loading the asset.",
                            "Please check the asset file exists.")
            finally:
                app.storage.user['selected_asset'] = selected_asset
                ui.notify(f"Success! You selected {name}.", type='positive', position='top')
                ui.navigate.reload()

    def delete_asset(asset):
        """Delete the asset's .json file."""
        for name in selected_asset_name:
            # getting the name to be correct.
            file_name = format_str_for_filename_super(name)['string']
            selected_asset = {}

            # trying to get the specified asset
            try:
                selected_asset = existing_assets[file_name]
            except:
                alert_dialog("Problem with loading the asset.",
                            "Please check the asset file exists.")
            finally:
                app.storage.user['selected_asset'] = selected_asset
                ui.notify(f"Success! You selected {name}.", type='positive', position='top')
                ui.navigate.reload()                

    # Render the cards displaying the existing assets.
    async def render_asset_cards(existing_assets: dict, asset: dict)-> ui.element:
        """Render the cards displaying each asset STAT found a JSON for."""
        with ui.card().classes(
            'w-full max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl p-2 '
            'flex flex-col justify-between h-full'
        ):
            with ui.row().classes('w-full justify-between items-start'):
                ui.label().bind_text_from(asset, 'name', backward=lambda name: f'{name}').classes('text-lg font-bold mb-0')

            # Category
            with ui.column().classes("gap-0.5"):
                with ui.row().classes("items-end"):
                    ui.label("Category: ").classes('mb-0 text-sm')
                    ui.label().bind_text_from(asset, 'category', backward=lambda cat: f'{cat}').classes('mt-0')

            
            # Description
            # Show first 25 characters of description with ellipsis if longer
            with ui.column().classes("gap-0.5"): 
                ui.label("Description").classes('mb-0 text-sm')
                desc = asset.get('description') or ''
                short_desc = (desc[:50] + '...') if len(desc) > 50 else desc
                ui.label(short_desc).classes('mt-0')
            
            # Source
            with ui.column().classes("gap-0.5"): 
                with ui.row().classes("items-end"):
                    ui.label("Source: ").classes('mb-0 text-sm')
                    ui.label().bind_text_from(asset, 'source', backward=lambda source: f'{source}').classes('mt-0')

            # Spacer to push buttons to the bottom
            ui.element('div').classes('flex-grow')

            # Button row anchored bottom-right
            with ui.row().classes('w-full justify-end'):
                with ui.button_group().classes('gap-2'):
                    ui.button('Select', on_click=lambda: select_target_asset(existing_assets, {asset['name']})) \
                        .classes('text-sm px-3 py-1 sm:text-xs sm:px-2 sm:py-1')
                    ui.button('Delete', on_click=lambda: delete_asset(asset)) \
                        .classes('text-sm px-3 py-1 sm:text-xs sm:px-2 sm:py-1 bg-red-500')

    with theme.frame('All Assets'):
        # File path for game data
        user_config = app.storage.user.get("config", {})
        paths = user_config.get("Paths",{})
        root_path = paths.get("osrootpath", "Not Set")
        games_path = paths.get("gamespath", "Not Set")
        assets_path = paths.get("assetspath", "Not Set")
        user_confirm = UserConfirm()
        
        selected_game = app.storage.user.get("selected_game", {})
        selected_asset = app.storage.user.get("selected_asset", {})
        existing_assets = app.storage.user.get("existing_assets", {})

        # No game selected
        if not selected_game or 'name' not in selected_game:
            with ui.row():
                ui.icon('warning').classes('text-3xl')
                ui.label('Warning: No selected game detected.').classes('text-2xl')
            ui.label('Cannot view the saves for a game with no game selected.')
            ui.label('Please select a game from \'View Games\'.')
            ui.label('Then return here to view the save files.')
            with ui.link(target = '/selectgames'):
                ui.button('Find Game File')
        
        # There IS a selected_game
        else:
            # Get the games_directory_path
            game_file_name = format_str_for_filename_super(selected_game.get('name'))['string']
            str_assets_directory_path = root_path + games_path + '\\' + game_file_name + '\\' + assets_path

            try:
                # getting the existing assets from the file path.
                get_assets_result = get_assets(str_assets_directory_path)
                if get_assets_result['result']:
                    existing_assets = get_assets_result['assets']
                    # setting the asset objects into the user storage.
                    app.storage.user['existing_assets'] = existing_assets
                else:
                    ui.notify(f"Error getting existing assets! Reason given: {get_assets_result['message']}", position='top', type='negative')
            except:
                ui.notify("""Error! Unable to retrieve the assets. Please check the path loctions in config.py""",
                        position='top',
                        type='negative',
                        multi_line=True)

            with ui.row():
                with ui.column().classes('items-center w-full gap-4 pt-3 max-w-5xl'):
                    ui.label("Select a asset to get started!").classes('text-xl text-center accent-text')
                    ui.label("Once you selecte a save it will update the 'Selected Asset' in the bottom left of your screen and you may seen yoru screen flash.")

                # Buttons!!!
                with ui.row().classes('w-full justify-center items-start gap-8'):
                    btn_create = ui.button('Create Asset', on_click=lambda: ui.navigate.to("/createasset"))
                    btn_detail = ui.button('View Detail', on_click=lambda: asset_view_details(selected_asset))
                    btn_detail.bind_enabled_from(bool(existing_assets))
                
                # Displaying the assets.
                asset_card_container = ui.row().classes("grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4")
                with asset_card_container:
                    for asset in existing_assets.values():
                        await render_asset_cards(existing_assets, asset)

