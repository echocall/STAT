from nicegui import ui
from handlers.assethandler import *
from elements.CategoryLabel import CategoryLabel
from elements.AssetContainer import AssetContainer
import elements.theme as theme

def create() -> None:
    @ui.page('/loadeddash')
    def view_saves():
        with theme.frame('View Saves'):
            save_data = {...}  # Existing save data
            assets = {...}  # Existing asset data
            counters = save_data['counters']
            sorted_assets = sort_assets_by_category(assets)
            owned_assets_unsorted = fetch_owned_assets(assets, save_data['assets'])
            sorted_owned_assets = sort_assets_by_category(owned_assets_unsorted)

            with ui.tabs().classes('w-full') as tabs:
                main = ui.tab('Main')
                assets_tab = ui.tab('Assets - Owned')
                store = ui.tab('Assets - Store')
            
            with ui.tab_panels(tabs, value=main).classes('w-full'):
                with ui.tab_panel(main):
                    ui.label('Main Overview').classes('text-2xl font-bold')
                    with ui.row().classes("w-full justify-between"):
                        ui.label(f'Save Name: {save_data["name"]}').classes("text-lg")
                        ui.label(f'Base Game: {save_data["base_game"]}').classes("text-lg")
                    with ui.row():
                        for counter, value in counters.items():
                            with ui.card().tight():
                                ui.label(f'{counter}: {value}').classes('text-md font-semibold')
                
                with ui.tab_panel(assets_tab):
                    ui.label('Your Owned Assets').classes('text-xl font-bold')
                    for category, assets_list in sorted_owned_assets.items():
                        ui.separator()
<<<<<<< Updated upstream
                        asset_container = ui.row().classes("full flex")
                        with asset_container:
                            with ui.row():
                                CategoryLabel(category)
                            # Creates cards for each asset
                            for asset in sorted_assets[category]:
=======
                        with ui.row():
                            CategoryLabel(category)
                        with ui.row().classes("w-full flex-wrap"):
                            for asset in assets_list:
>>>>>>> Stashed changes
                                with ui.card().tight():
                                    with ui.card_section():
                                        ui.label(asset['name']).classes('text-md font-bold')
                                        ui.label(f'Source: {asset["source"]}')
                                        ui.label(f'Buy: {asset["buy_costs"]}')
                                        ui.label(f'Sell: {asset["sell_prices"]}')
                
                with ui.tab_panel(store):
                    ui.label('Assets Store').classes('text-xl font-bold')
                    ui.input('Search Assets').on('input', lambda e: filter_assets(e.value))
                    for category, assets_list in sorted_assets.items():
                        ui.separator()
                        with ui.row():
                            CategoryLabel(category)
                        with ui.row().classes("w-full flex-wrap"):
                            for asset in assets_list:
                                with ui.card().tight():
                                    with ui.card_section():
                                        ui.label(asset['name']).classes('text-md font-bold')
                                        ui.label(f'Source: {asset["source"]}')
                                        ui.label(f'Buy: {asset["buy_costs"]}')
                                        ui.label(f'Sell: {asset["sell_prices"]}')
                                    with ui.card_actions().classes("w-full justify-end"):
                                        ui.button('Add Asset', on_click=lambda asset=asset: ui.notify(f'Added {asset["name"]}'))

    def filter_assets(search_text):
        # Implement logic to filter assets based on search_text
        pass
