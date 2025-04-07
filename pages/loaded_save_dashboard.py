from nicegui import app, ui
from elements.message import message
from handlers.assethandler import *
from elements.CategoryLabel import CategoryLabel
from elements.AssetContainer import AssetContainer
import elements.theme as theme

# Dashboard for after a game has been selected, and a save has been loaded.
# Displays the user's information.

@ui.page('/loadeddash')
async def load_dashboard():
    with theme.frame('View Saves'):
    # Getting assets sorted.
        save_data = app.storage.user.get("loaded_save", {})
        loaded_game = app.storage.user.get("loaded_game", {})

        # getting all the assets available from the game and the saved game.
        assets = multi_json_getter(loaded_game['asset_default_path'], "assets")
        assets_as_dict = {}

        for asset in assets:
            assets_as_dict[asset['name']] = asset

        counters = save_data['counters']
        sorted_assets = sort_assets_by_category(assets_as_dict)

        owned_assets_unsorted = fetch_owned_assets(assets, save_data['assets'])
        sorted_owned_assets = sort_assets_by_category(owned_assets_unsorted)

    
        # The tabs
        with ui.tabs().classes('w-full') as tabs:
            main_tab = ui.tab('Main')
            assets_tab = ui.tab('Assets - Owned')
            store_tab = ui.tab('Assets - Store')
            if loaded_game['name'] == "":
                message("Warning: No game loaded. Please select a game to load: ")

    
        with ui.tab_panels(tabs, value=main_tab).classes('full flex items-left'):
            with ui.tab_panel(main_tab):
                    ui.label('Counters tab')
                    with ui.row():
                        with ui.column():
                            ui.label('Save Name: ' + save_data['name'])
                        with ui.column():
                            ui.label('Base Game: ' + save_data['base_game'])
                    with ui.row():
                        for counter in counters:
                            ui.label(counter + ':  ' + str(counters[counter]))
            with ui.tab_panel(assets_tab):
                    ui.label('Owned Assets tab')
            with ui.tab_panel(store_tab):
                ui.label('Assets Store tab')
                # Creates each asset_container
                for category in sorted_assets:
                    ui.separator()
                    asset_container = ui.row().classes("full flex")
                    with asset_container:
                        with ui.row():
                            CategoryLabel(category)
                        # Creates cards for each asset
                        for asset in sorted_assets[category]:
                            with ui.card():
                                with ui.card_section():
                                    ui.label().bind_text_from(asset, 'name', backward=lambda name: f'Name: {name}')
                                    ui.label().bind_text_from(asset, 'source', backward=lambda source: f'Source: {source}')
                                    ui.label().bind_text_from(asset, 'buy_costs', backward=lambda buy_costs: f'{buy_costs}')
                                    ui.label().bind_text_from(asset, 'sell_prices', backward=lambda sell_prices: f'{sell_prices}')
                                with ui.card_actions().classes("w-full justify-end"):
                                    ui.button('Add Asset', on_click=lambda: ui.notify(f'You tried to add an asset to your owned assets.'))
        