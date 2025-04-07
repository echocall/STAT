from nicegui import app, binding,  ui
from elements.message import message
from handlers.assethandler import *
from elements.CategoryLabel import CategoryLabel
from elements.AssetContainer import AssetContainer
import elements.theme as theme

# Dashboard for after a game has been selected, and a save has been loaded.
# Displays the user's information.

@ui.page('/loadeddash')
async def dashboard():
    with theme.frame('View Saves'):
    # Getting assets sorted.
        save_data = {}
        loaded_game = {}
        counters = {}

        save_data = load_from_storage("loaded_save")
        loaded_game = load_from_storage("loaded_game")

        # if the dictionaries are not empty
        if bool(save_data) and bool(loaded_game):
            # Everything has loaded properly, go for it!
            counters = save_data['counters']

            # loading in the assets.
            try:
                # getting all the assets available from the game and the saved game.
                assets = multi_json_getter(loaded_game['asset_default_path'], "assets")
                assets_as_dict = {}
                for asset in assets:
                    assets_as_dict[asset['name']] = asset
                sorted_assets = sort_assets_by_category(assets_as_dict)
                owned_assets_unsorted = fetch_owned_assets(assets, save_data['assets'])
                sorted_owned_assets = sort_assets_by_category(owned_assets_unsorted)
                print("Printing unsorted assets: ")
                print(assets_as_dict)
                print()
                print("Printing sorted assets: ")
                print(sorted_assets)
            except:
                ui.notify("Error loading in assets.")


            if loaded_game['name'] == "":
                message("Warning: No game loaded. Please select a game to load: ")
            ui.tooltip().default_classes('bg-blue')
            ui.separator()
            # The tabs
            with ui.tabs().classes('w-full') as tabs:
                main_tab = ui.tab('Main')
                assets_tab = ui.tab('Assets - Owned')
                store_tab = ui.tab('Assets - Store')

            # On every tab.
            with ui.row().classes('full flex items-left'):
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
                with ui.tab_panel(main_tab):
                        ui.separator()
                        ui.label("Hi")
                        ui.separator()
                # The Owned Assets Tab
                with ui.tab_panel(assets_tab):
                        ui.label('Owned Assets tab')
                # The Store Tab
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
                            with ui.row():
                                for asset in sorted_assets[category]:
                                    await render_asset_cards(asset)

        else:
            # Didn't load properly from app.storage.user
            # Ask user to load them.
            b = 2+2
            ui.notify("Error loading from selected game and save! Please try reloading them.")


# Render the counters.
@ui.refreshable
async def render_counter_bar(counters: dict, counter: str) -> ui.element:
    current_counter = ui.label(f'{counter}:')
    with current_counter:
        ui.tooltip(f'Name of counter. Currently {counter}.')

    # Work around for  showing Current Counter amount without being able to fiddle with it.
    temp_current_amount = counters[counter]
    current_amount = ui.label(f'{temp_current_amount}')
    with current_amount:
        ui.tooltip(f'Amount of {counter}. Currently {counters[counter]}.')

    amount_to_change =  ui.number(label=f'Change {counter} by this amount: ', value=0, precision=0)
    with amount_to_change:
        ui.tooltip(f'Number input for the add and subtract buttons to update the counter by.')
    with ui.row().classes('gap-1'):
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
            ui.label().bind_text_from(asset, 'buy_costs', backward=lambda buy_costs: f'{buy_costs}')
            ui.label().bind_text_from(asset, 'sell_prices', backward=lambda sell_prices: f'{sell_prices}')
        with ui.card_actions().classes("w-full justify-end"):
            ui.button('Add Asset', on_click=lambda: ui.notify(f'You tried to add an asset to your owned assets.'))

