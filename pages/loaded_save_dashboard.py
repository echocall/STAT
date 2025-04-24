from nicegui import app, binding,  ui
from elements.message import message
from handlers.assethandler import *
from handlers.gamehandler import *
from elements.CategoryLabel import CategoryLabel
from elements.asset_detail_dialog import asset_detail_dialog
import elements.theme as theme

# Dashboard for after a game has been selected, and a save has been loaded.
# Displays the user's information.
@ui.page('/loadeddash')
async def dashboard():
    with theme.frame('Dashboard'):
        config = app.storage.user.get("config", {})
        paths = config.get("Paths",{})
        game_paths = paths.get("gamespath", "Not Set")

        # Getting assets sorted.
        selected_game = {}
        selected_save = {}
        sorted_assets = {}
        counters = {}
        selected_save = load_from_storage("selected_save")
        selected_game = load_from_storage("selected_game")
        saves_paths = selected_game.get("save_files_path", "Not Set")
        turn_type = ""

        # if the dictionaries are not empty
        if bool(selected_save) and bool(selected_game):
            # Everything has loaded properly, go for it!
            counters = selected_save['counters']

            assets = asset_handler(selected_game['asset_default_path'],
                                       selected_game['default_assets'],
                                       selected_save['asset_customs'],
                                       selected_save['asset_customs_path'])

            # loading in the assets.
            assets_as_dict = {}
            # getting all assets available
            try:
                await assets_to_dictionary(assets, assets_as_dict)
            except:
                ui.notify("Error creating assets_as_dict", type='negative', position="top",)
           
           # sorting all assets by category
            try:
                sorted_assets = sort_assets_by_category(assets_as_dict)
            except:
                ui.notify("Error Sorting Assets", type='negative', position="top",)
           
            # getting all owned assets
            try:
                owned_assets_unsorted = fetch_owned_assets(assets_as_dict, selected_save['assets'])
            except:
                ui.notify("Error Sorting Owned Assets", type='negative', position="top",)
            
            # Sorting the owned assets.
            try:
                sorted_owned_assets = sort_assets_by_category(owned_assets_unsorted)
            except:
                ui.notify("Error Sorting Owned Assets", type='negative', position="top",)

            if selected_game['name'] == "":
                message("Warning: No game loaded. Please select a game to load: ")
            with ui.row().classes('full flex'):
                ui.label('')

            # ON EVERY TAB
            with ui.row().classes('full flex'):
                with ui.column():
                    ui.label('Save Name: ' + selected_save['name'])
                with ui.column():
                    ui.label('Base Game: ' + selected_save['base_game'])
                with ui.column():
                    with ui.row():
                        ui.label('Turns: ').classes('h-4')
                        current_turn = selected_save['current_turn']
                        ui.label(current_turn)
                with ui.column():
                    ui.button(icon='update', on_click=lambda: ui.notify('TODO: implement advancing turns')).props("round")
                ui.space()

            ui.separator()
            # The Counters
            with ui.row().classes('full flex'):
                for counter in counters:
                    await render_counter_bar(counters, counter)
            ui.separator()
            
            # The tabs
            with ui.tabs().classes('w-100') as tabs:
                main_tab = ui.tab('Main')
                assets_tab = ui.tab('Used Assets') 
                all_assets_tab = ui.tab('All Assets')           
            
            # The Tab Panels
            with ui.tab_panels(tabs, value=main_tab).classes('full flex rounded-md'):
                ui.separator()
                with ui.tab_panel(main_tab):
                    with ui.row().classes('basis-full justify-start space-x-4 full-flex'):
                        ui.label("Here's a summary of whats going on!")


                # The Used Assets Tab
                with ui.tab_panel(assets_tab):
                    for owned_category in sorted_owned_assets:
                        asset_container_owned = ui.row().classes('basis-full justify-start space-x-4 full-flex')
                        with asset_container_owned:
                            with ui.column().classes('items-center'):
                                with ui.row().classes("w-100 items-start items-center"):
                                    CategoryLabel(owned_category)
                                # Creates cards for each asset
                                with ui.row().classes("w-100 items-start"):
                                    for owned_asset in sorted_owned_assets[owned_category]:
                                        await render_owned_asset_cards(owned_asset, selected_save['assets'])
                        ui.separator()

                # All Assets Tab
                with ui.tab_panel(all_assets_tab):
                    # Creates each asset_container
                    for category in sorted_assets:
                        asset_container = ui.row().classes('basis-full justify-start space-x-4 full-flex')
                        with asset_container:
                            with ui.column().classes('items-center'):
                                with ui.row().classes("w-100 items-start"):
                                    CategoryLabel(category)
                                # Creates cards for each asset
                                with ui.row().classes("w-100 items-start"):
                                    for asset in sorted_assets[category]:
                                        await render_asset_cards(asset)
                        ui.separator()

        else:
            games = []
            games = get_games_names(game_paths)
            # Didn't load properly from app.storage.user
            # Ask user to pick files to load.
            ui.label("Error loading from selected game! Please pick games from below.").classes('w-40')
            ui.select(options=games, with_input=True, on_change=lambda e: select_game(game_paths, e.value))
            
# Render the counters.
@ui.refreshable
async def render_counter_bar(counters: dict, counter: str) -> ui.element:
    current_counter = ui.label(f'{counter}:').classes('text-sm')

    # Work around for showing Current Counter amount without being able to fiddle with it.
    temp_current_amount = counters[counter]
    current_amount = ui.label(f'{temp_current_amount}').classes('text-sm')

    # Amount to change
    amount_to_change =  ui.number(label=f'Change {counter}: ', value=0, min=0, precision=0)
    # Buttons! :)
    with ui.row().classes('items-center justify-items-center align-middle'):
        btn_add = ui.button(icon='add', on_click=lambda: counter_add(counters, current_counter.text, temp_current_amount, amount_to_change.value), color='green')
        btn_add.props('round dense size=sm')
        btn_sub = ui.button(icon='remove',
                             on_click=lambda: counter_sub(counters, current_counter.text, temp_current_amount, amount_to_change.value), color='orange')
        btn_sub.props('round dense size=sm')

# Function to increase the amount of a counter.
def counter_add(counters: dict, current_counter: str, current_amount: str, amount: int):
    initial_amount = current_amount
    counter_name = current_counter.split(":")
    counter_name = counter_name[0]

    try:
        new_value = initial_amount + amount
        counters[counter_name] = int(new_value)
        app.storage.user['selected_save']['counters'] = counters
    except:
       ui.notify("Error: could not add to the counter!", type='negative', position="top",)

    # refresh the element on the page.
    render_counter_bar.refresh()
    
def counter_sub(counters: dict, current_counter: str, current_amount: str, amount: int):
    initial_amount = current_amount
    counter_name = current_counter.split(":")
    counter_name = counter_name[0]

    try:
        new_value = initial_amount - amount
        counters[counter_name] = int(new_value)
        app.storage.user['selected_save']['counters'] = counters
    except:
       ui.notify("Error: could not remove from the counter!",type='negative', position="top",)

    # refresh the element on the page.
    render_counter_bar.refresh()

@ui.refreshable
def load_from_storage(target:str):
    target_dict = {}
    try:
        target_dict = app.storage.user.get(target, {})
    except:
        ui.notify(f"Could not load {target} from app.storage.user!",type='negative',position="top",)
    
    return target_dict

# used to create the individual cards.
async def render_asset_cards(asset) -> ui.element:
    with ui.card().style('width: 100%; max-width: 250px; aspect-ratio: 4 / 3; display: flex; flex-direction: column; justify-content: space-between;'):
        with ui.card_section().classes('flex-grow'):
            with ui.row():
                ui.label('Name: ').classes('font-bold')
                ui.label().bind_text_from(asset, 'name', backward=lambda name: f'{name}')
            with ui.row():
                ui.label('Source: ').classes('font-bold')
                ui.label().bind_text_from(asset, 'source', backward=lambda source: f'{source}')
            buy_cost_label = ui.label("Buy Costs").classes('font-bold')
            with buy_cost_label:
                for name, value in asset['buy_costs'].items():
                    with ui.row():
                        ui.label(f'{name}: ').classes('font-normal')
                        ui.label(f'{value}').classes('font-normal')
            sell_price_label = ui.label("Sell Costs").classes('font-bold')
            with sell_price_label:
                with ui.row():
                    for name, value in asset['sell_prices'].items():
                        ui.label(f'{name}: ').classes('font-normal')
                        ui.label(f'{value}').classes('font-normal')
        with ui.card_actions().classes("w-full justify-end"):
            # TODO: fix this view details button
            with ui.row():
                ui.button('Select Details', on_click=lambda: view_asset_details(asset))
                ui.button('Add Asset', on_click=lambda: ui.notify(f'TODO: Add asset to owned assets.'))

# used to create the individual cards.
async def render_owned_asset_cards(asset, assets_owned) -> ui.element:
    amount_owned = 0
    asset_name = asset['name']
    if assets_owned:
        amount_owned = assets_owned[asset_name]
    with ui.card().style('width: 100%; max-width: 250px; aspect-ratio: 4 / 3; display: flex; flex-direction: column; justify-content: space-between;'):
        with ui.card_section().classes('flex-grow'):
            with ui.row():
                ui.label('Name: ').classes('font-bold')
                ui.label().bind_text_from(asset, 'name', backward=lambda name: f'{name}')
            with ui.row():
                ui.label('Number Owned: ').classes('font-bold')
                ui.label().bind_text_from(amount_owned, backward=lambda source: f'{amount_owned}')
            buy_cost_label = ui.label("Buy Costs").classes('font-bold')
            with buy_cost_label:
                for name, value in asset['buy_costs'].items():
                    with ui.row():
                        ui.label(f'{name}: ').classes('font-normal')
                        ui.label(f'{value}').classes('font-normal')
            sell_price_label = ui.label("Sell Costs").classes('font-bold')
            with sell_price_label:
                with ui.row():
                    for name, value in asset['sell_prices'].items():
                        ui.label(f'{name}: ').classes('font-normal')
                        ui.label(f'{value}').classes('font-normal')
        with ui.card_actions().classes("w-full justify-end"):
            # TODO: fix this view details button
            with ui.row():
                ui.button('Select Asset', on_click=lambda: view_asset_details(asset))

# gets the assets as a dictionary
async def assets_to_dictionary(assets: list, assets_as_dict: dict) -> dict:
    for asset in assets:
        assets_as_dict[asset['name']] = asset
 
    return assets_as_dict

# Calling the view_asset dialog box
async def view_asset_details(asset: dict):
    app.storage.user['selected_asset'] = asset
    # TODO REMOVE THIS WHEN ACTUALLY MANIPULATING DATA
    ui.navigate.reload()
    # viewed_asset = asset_detail_dialog()


def select_game(games_path: str, selected_game_name: str):
    for name in selected_game_name:
        selected_game = {}
        try:
            selected_game = get_game(selected_game_name, games_path, 'games')
            app.storage.user['is_game_loaded']  = True
        except:
            ui.notify("Warning! Problem with loading game. Please check that game file exists.", type='warning', position="top",)
        finally:
            app.storage.user['selected_game'] = selected_game
            render_counter_bar.refresh()

def buy_asset(asset: dict, counters: dict):
    g = 7+7
    # Subtract asset's buy_costs from appropriate counters.
        # if buy_cost['name'] exists in Counters:
        # subtract amount specified in asset
    # if it doesn't exist in the Owned_Assets, add it to there.
    # Increase amount of asset in owned_assets by one.

def save_game():
    c = 3+3
    # TODO: write from app.storage.user to .json file
    # TODO: return result of save.