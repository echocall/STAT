from nicegui import app, binding,  ui
from elements.message import message
from handlers.assethandler import *
from handlers.gamehandler import *
from elements.CategoryLabel import CategoryLabel
from elements.AssetContainer import AssetContainer
import elements.theme as theme

# Dashboard for after a game has been selected, and a save has been loaded.
# Displays the user's information.
@ui.page('/loadeddash')
async def dashboard():
    with theme.frame('View Saves'):
        config = app.storage.user.get("config", {})
        paths = config.get("Paths",{})
        game_paths = paths.get("gamespath", "Not Set")

        # Getting assets sorted.
        loaded_game = {}
        save_data = {}
        sorted_assets = {}
        counters = {}
        save_data = load_from_storage("loaded_save")
        loaded_game = load_from_storage("loaded_game")
        saves_paths = loaded_game.get("save_files_path", "Not Set")
        

        # if the dictionaries are not empty
        if bool(save_data) and bool(loaded_game):
            # Everything has loaded properly, go for it!
            counters = save_data['counters']

            assets = asset_handler(loaded_game['asset_default_path'],
                                       loaded_game['default_assets'],
                                       save_data['asset_customs'],
                                       save_data['asset_customs_path'])
               
            # loading in the assets.
            assets_as_dict = {}
            # getting all assets available
            try:
                await assets_to_dictionary(assets, assets_as_dict)
            except:
                ui.notify("Error creating assets_as_dict", type='negative')
            # sorting all assets by category
            try:
                sorted_assets = sort_assets_by_category(assets_as_dict)
            except:
                ui.notify("Error Sorting Assets", type='negative')
            # getting all owned assets
            try:
                owned_assets_unsorted = fetch_owned_assets(assets, save_data['assets'])
            except:
                ui.notify("Error Sorting Owned Assets", type='negative')
            # Sorting the owned assets.
            try:
                sorted_owned_assets = sort_assets_by_category(owned_assets_unsorted)
            except:
                ui.notify("Error Sorting Owned Assets", type='negative')

            ui.tooltip().default_classes('bg-blue')

            if loaded_game['name'] == "":
                message("Warning: No game loaded. Please select a game to load: ")
            ui.separator()
            # The tabs
            with ui.tabs().classes('w-full') as tabs:
                main_tab = ui.tab('Main')
                assets_tab = ui.tab('Assets - Owned')
                store_tab = ui.tab('Assets - Store')

            # On every tab.
            with ui.row().classes('full flex'):
                ui.separator()
                with ui.column():
                    with ui.label('Save Name: ' + save_data['name']):
                        ui.tooltip(f'The currently loaded save is {save_data['name']}.')
                with ui.column():
                    with ui.label('Base Game: ' + save_data['base_game']):
                        ui.tooltip(f'The base game is {save_data['base_game']}')

            ui.separator()
            # The Counters
            with ui.row().classes('full flex'):
                for counter in counters:
                    await render_counter_bar(counters, counter)
            ui.separator()

            # The Tab Panels
            with ui.tab_panels(tabs, value=main_tab).classes('full flex'):
                ui.separator()
                with ui.tab_panel(main_tab):
                    ui.label("Here's a summary of whats going on!")
                # The Owned Assets Tab
                with ui.tab_panel(assets_tab):
                        ui.label('Owned Assets tab')
                        for category in sorted_owned_assets:
                            ui.separator()
                            asset_container = ui.row().classes("full flex")
                            with asset_container:
                                with ui.row():
                                    CategoryLabel(category)
                                # Creates cards for each asset
                                with ui.row():
                                    for asset in sorted_owned_assets[category]:
                                        await render_asset_cards(asset)
                # The Store Tab
                with ui.tab_panel(store_tab):
                    # Creates each asset_container
                    for category in sorted_assets:
                        asset_container = ui.row().classes("full flex w-full")
                        with asset_container:
                            with ui.row().classes("w-1/4"):
                                CategoryLabel(category)
                            # Creates cards for each asset
                            with ui.row().classes("w-3/4"):
                                for asset in sorted_assets[category]:
                                    await render_asset_cards(asset)
                        
                        ui.separator()

        else:
            games = []
            games = get_games_names(game_paths)
            # Didn't load properly from app.storage.user
            # Ask user to pic files to load.
            ui.label("Error loading from selected game! Please pick games from below.").classes('w-40')
            ui.select(options=games, with_input=True, on_change=lambda e: select_game(game_paths, e.value))
            


# Render the counters.
@ui.refreshable
async def render_counter_bar(counters: dict, counter: str) -> ui.element:
    current_counter = ui.label(f'{counter}:')
    with current_counter:
        ui.tooltip(f'Name of counter. Currently {counter}.')

    # Work around for  showing Current Counter amount without being able to fiddle with it.
    temp_current_amount = counters[counter]
    current_amount = ui.label(f'{temp_current_amount}')#.classes("size-0.5")
    with current_amount:
        ui.tooltip(f'Amount of {counter}. Currently {counters[counter]}.')

    # Amount to change
    amount_to_change =  ui.number(label=f'Change {counter} by this amount: ', value=0, min=0, precision=0)
    with amount_to_change:
        ui.tooltip(f'Number input for the add and subtract buttons to update the counter by.')
    # Buttons! :)
    with ui.row().classes('items-center justify-items-center align-middle'):
        with ui.chip(icon='add', on_click=lambda: counter_add(counters, current_counter.text, temp_current_amount, amount_to_change.value), color='green'):
           ui.tooltip(f'Add the amount in the number input to {counter}.')
        with ui.chip(icon='remove', on_click=lambda: counter_sub(counters, current_counter.text, temp_current_amount, amount_to_change.value), color='orange'):
            ui.tooltip(f'Subtract the amount in the number input from {counter}.')

# Function to increase the amount of a counter.
def counter_add(counters: dict, current_counter: str, current_amount: str, amount: int):
    initial_amount = current_amount
    counter_name = current_counter.split(":")
    counter_name = counter_name[0]

    try:
        new_value = initial_amount + amount
        counters[counter_name] = new_value
        app.storage.user['loaded_save']['counters'] = counters
    except:
       ui.notify("Error: could not update the counter!")

    # refresh the element on the page.
    render_counter_bar.refresh()
    
def counter_sub(counters: dict, current_counter: str, current_amount: str, amount: int):
    initial_amount = current_amount
    counter_name = current_counter.split(":")
    counter_name = counter_name[0]

    try:
        new_value = initial_amount - amount
        counters[counter_name] = new_value
        app.storage.user['loaded_save']['counters'] = counters
    except:
       ui.notify("Error: could not update the counter!")

    # refresh the element on the page.
    render_counter_bar.refresh()

@ui.refreshable
def load_from_storage(target:str):
    target_dict = {}
    try:
        target_dict = app.storage.user.get(target, {})
    except:
        ui.notify(f"Could not load {target} from app.storage.user!")
    
    return target_dict

async def render_asset_cards(asset) -> ui.element:
    with ui.card():
        with ui.card_section():
            ui.label().bind_text_from(asset, 'name', backward=lambda name: f'Name: {name}')
            ui.label().bind_text_from(asset, 'source', backward=lambda source: f'Source: {source}')
            buy_cost_label = ui.label("Buy Costs").classes('font-bold')
            with buy_cost_label:
                for name, value in asset['buy_costs'].items():
                    ui.label(f'{name}: ').classes('font-normal')
                    ui.label(f'{value}').classes('font-normal')
            sell_price_label = ui.label("Sell Costs").classes('font-bold')
            with sell_price_label:
                for name, value in asset['sell_prices'].items():
                    ui.label(f'{name}: ').classes('font-normal')
                    ui.label(f'{value}').classes('font-normal')
        with ui.card_actions().classes("w-full justify-end"):
            ui.button('Add Asset', on_click=lambda: ui.notify(f'You tried to add an asset to your owned assets.'))

async def assets_to_dictionary(assets: list, assets_as_dict: dict) -> dict:
    for asset in assets:
        assets_as_dict[asset['name']] = asset
 
    return assets_as_dict

def select_game(games_path: str, selected_game_name: str):
    for name in selected_game_name:
        selected_game = {}
        try:
            selected_game = get_game(selected_game_name, games_path, 'games')
            app.storage.user['is_game_loaded']  = True
        except:
            ui.notify("Warning! Problem with loading game. Please check that game file exists.")
        finally:
            app.storage.user['loaded_game'] = selected_game
            render_counter_bar.refresh()
