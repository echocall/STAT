from nicegui import app, binding,  ui
from elements.message import message
from handlers.assethandler import *
from handlers.gamehandler import *
from elements.CategoryLabel import CategoryLabel
from elements.asset_detail_dialog import asset_detail_dialog
import elements.theme as theme
from elements.UserConfirm import *
import traceback

# Dashboard for after a game has been selected, and a save has been loaded.
# Displays the user's information.
@ui.page('/loadeddash')
async def dashboard():
    with theme.frame('Dashboard'):
        config = app.storage.user.get("config", {})
        paths = config.get("Paths",{})

        
        def load_from_storage(target:str):
            target_dict = {}
            try:
                target_dict = app.storage.user.get(target, {})
            except:
                ui.notify(f"Could not load {target} from app.storage.user!",type='negative',position="top",)
            
            return target_dict

        # Getting assets sorted.
        selected_game = {}
        selected_save = {}
        sorted_assets = {}
        counters = {}
        selected_save = load_from_storage("selected_save")
        selected_game = load_from_storage("selected_game")
        turn_type = ""

        user_confirm = UserConfirm()

        def buy_asset(asset: dict, counters: dict, owned_assets: dict):
            """
            Buy an asset:
            - Subtract its `buy_costs` from the appropriate counters.
            - Add or increment it in the `owned_assets` dictionary.
            """
            # Deduct buy costs
            for cost in asset.get('buy_costs', []):
                cost_name = cost['name']
                cost_amount = cost['amount']
                if cost_name in counters:
                    counters[cost_name] -= cost_amount
                else:
                    ui.notify(f"Warning: Cost counter '{cost_name}' not found.",
                              position = 'top',
                              type='warning',
                              mulit_line=True)

            # Update owned assets
            name = asset['name']
            if name in owned_assets:
                owned_assets[name]['quantity'] += 1
            else:
                new_asset = asset.copy()
                new_asset['quantity'] = 1
                owned_assets[name] = new_asset

            # Refresh UI/state
            refresh_counters_and_assets()

        def sell_asset(asset: dict, counters: dict, owned_assets: dict):
            """
            Sell an asset:
            - Add its `sell_prices` to the appropriate counters.
            - Decrease its quantity in `owned_assets`, and remove if quantity reaches 0.
            """
            # Add sell prices
            for price in asset.get('sell_prices', []):
                price_name = price['name']
                price_amount = price['amount']
                if price_name in counters:
                    counters[price_name] += price_amount
                else:
                    print(f"Warning: Sell price counter '{price_name}' not found.")

            # Update owned assets
            name = asset['name']
            if name in owned_assets:
                owned_assets[name]['quantity'] -= 1
                if owned_assets[name]['quantity'] <= 0:
                    del owned_assets[name]
            else:
                print(f"Warning: Tried to sell unowned asset '{name}'.")

            # Refresh UI/state
            # refresh_counters_and_assets()

        # TODO
        def save_current_session():
            game_name = selected_game['name']
            save_name = selected_save['name']

            # Format names for safe filenames
            game_formatted = format_str_for_filename_super(game_name)
            save_formatted = format_str_for_filename_super(save_name)

            if not game_formatted['result'] or not save_formatted['result']:
                print("Error: Could not format game or save name for filename.")
                return

            # Construct full save file path
            full_save_path = f"{root_path}{games_path}\\{game_formatted['string']}{saves_path}\\{save_formatted['string']}.json"

            # Save the current selected_save dict to file
            result = overwrite_json_file(selected_save, str_target_file_path=full_save_path, file_name='')

            if result['success']:
                ui.notify("Save successful!", position='top', type='positive')
            else:
                print(f"Save failed: {result['message']}")


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


        # used to create the individual cards.
        @ui.refreshable
        async def render_asset_cards(asset) -> ui.element:
            with ui.card().style('width: 100%; max-width: 350px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;'):
                with ui.card_section().classes('flex-grow'):
                    with ui.row():
                        ui.label('Name: ').classes('font-bold')
                        ui.label().bind_text_from(asset, 'name')

                    with ui.row():
                        ui.label('Source: ').classes('font-bold')
                        ui.label().bind_text_from(asset, 'source')

                    buy_cost_label = ui.label("Buy Costs").classes('font-bold')
                    with buy_cost_label:
                        for name, value in asset['buy_costs'].items():
                            with ui.row():
                                ui.label(f'{name}: ').classes('font-normal')
                                ui.label(f'{value}').classes('font-normal')

                    sell_price_label = ui.label("Sell Prices").classes('font-bold')
                    with sell_price_label:
                        with ui.row():
                            for name, value in asset['sell_prices'].items():
                                ui.label(f'{name}: ').classes('font-normal')
                                ui.label(f'{value}').classes('font-normal')

                with ui.card_actions().classes("w-full justify-end mt-auto"):
                    with ui.row().classes("w-full justify-around"):
                        with ui.button(icon='visibility', on_click=lambda: view_asset_details(asset)).props('round'):
                            ui.tooltip('Select Asset').classes('bg-grey-10 text-white')
                        with ui.button(icon='add', on_click=lambda: ui.notify('TODO: Add asset')).props('round'):
                                ui.tooltip('Add Asset').classes('bg-grey-10 text-white')
                        with ui.button(icon='shopping_cart', on_click=lambda: ui.notify('TODO: Buy asset')).props('round'):
                            ui.tooltip('Buy Asset').classes('bg-grey-10 text-white')
                        with ui.button(icon='sell', on_click=lambda: ui.notify('TODO: Sell asset')).props('round'):
                            ui.tooltip('Sell Asset').classes('bg-grey-10 text-white')
        @ui.refreshable
        # used to create the individual cards.
        async def render_owned_asset_cards(asset, owned_asset_data) -> ui.element:
            with ui.card().style('width: 100%; max-width: 350px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;'):
                with ui.card_section().classes('flex-grow'):
                    with ui.row():
                        ui.label('Name: ').classes('font-bold')
                        ui.label().bind_text_from(asset, 'name')

                    with ui.row():
                        ui.label('Number owned: ').classes('font-bold')
                        ui.label(str(owned_asset_data.get(asset['name'], 0))).classes('font-normal')
                    
                    with ui.row():
                        ui.label("Buy Costs").classes('font-bold')
                        for name, value in asset['buy_costs'].items():
                            with ui.row():
                                ui.label(f'{name}: ').classes('font-normal')
                                ui.label(f'{value}').classes('font-normal')

                    with ui.row():
                        ui.label('Sell Prices: ').classes('font-bold')
                        for name, value in asset['sell_prices'].items():
                            ui.label(f'{name}: {value}').classes('font-normal')

                with ui.card_actions().classes("w-full justify-end mt-auto"):
                    with ui.row().classes("w-full justify-around"):
                        with ui.button(icon='visibility', on_click=lambda: view_asset_details(asset)).props('round'):
                            ui.tooltip('Select Asset').classes('bg-grey-10 text-white')
                        with ui.button(icon='add', on_click=lambda: ui.notify('TODO: Add asset')).props('round'):
                                ui.tooltip('Add Asset').classes('bg-grey-10 text-white')
                        with ui.button(icon='shopping_cart', on_click=lambda: ui.notify('TODO: Buy asset')).props('round'):
                            ui.tooltip('Buy Asset').classes('bg-grey-10 text-white')
                        with ui.button(icon='sell', on_click=lambda: ui.notify('TODO: Sell asset')).props('round'):
                            ui.tooltip('Sell Asset').classes('bg-grey-10 text-white')

        # gets the assets as a dictionary
        async def assets_to_dictionary(assets: list, assets_as_dict: dict) -> dict:
            for asset in assets:
                assets_as_dict[asset['name']] = asset
        
            return assets_as_dict

        # Calling the view_asset dialog box
        async def view_asset_details(asset: dict):
            app.storage.user['selected_asset'] = asset
            # TODO: Solve this reloading the page and messing with tabs, etc
            ui.navigate.reload()
            # viewed_asset = asset_detail_dialog()

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

        # No game or save selected
        if not selected_game or 'name' not in selected_game:
            with ui.row():
                ui.icon('warning').classes('text-3xl text-center')
                ui.label('Warning: No selected game detected.').classes('text-2xl text-center')
            ui.label('Cannot view a save file for a game with no game or save selected.').classes('text-center')
            ui.label('Please select a game from \'View Games\'.').classes('text-center')
            ui.label('Then select a save from \'View Saves\'.').classes('text-center')
            with ui.link(target = '/selectgames'):
                ui.button('Find Game File')
        elif not selected_save or 'name' not in selected_save:
            with ui.row():
                ui.icon('warning').classes('text-3xl text-center')
                ui.label('Warning: No selected save detected.').classes('text-2xl text-center')
            ui.label('Cannot view a save file for a game with no  save selected.').classes('text-center')
            ui.label('Please select a game from \'View Saves\'.').classes('text-center')
            with ui.link(target = '/selectsaves'):
                ui.button('Find Save File')
        # We have a selected_game and a selected_save
        else:
            # Paths for DAYS BAYBEEEE
            root_path = paths.get("osrootpath", "Not Set")
            games_path = paths.get("gamespath", "Not Set") 
            saves_path = paths.get("savespath", "Not Set")
            assets_path = paths.get("assetspath", "Not Set")
            default_assets_path = paths.get("defaultassetspath", "Not Set")
            custom_assets_path = paths.get("customassetspath", "Not Set")
            str_games_path = root_path + games_path
            converted_game_name = ''
            try:
                game_name_result = format_str_for_filename_super(selected_game['name'])
            except Exception as e:
                print("[Converting name] Error converting name to file friendly format:", e)
                traceback.print_exc()
                return game_name_result
            file_name = game_name_result['string']

            str_saves_path =  str_games_path + '\\' +  file_name + '\\' +  saves_path
            str_assets_path = str_games_path + '\\' +  file_name + assets_path
            str_default_assets_path = str_games_path + '\\' +  file_name + default_assets_path
            str_custom_assets_path = str_games_path + '\\' +  file_name + custom_assets_path

            # Everything has loaded properly, go for it!
            if not selected_save or 'counters' not in selected_save:
                ui.notify("Error: No save data or missing 'counters' key.", type='negative', position="top")
                return

            counters = selected_save['counters']

            assets = asset_handler(str_default_assets_path,
                                       selected_game['default_assets'],
                                       selected_save['asset_customs'],
                                       str_custom_assets_path)

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
                with ui.column():
                    ui.button(icon='save', on_click=lambda: save_current_session())
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
                        ui.label("Here's a summary of whats going on!").classes('text-center')


                # The Used Assets Tab
                with ui.tab_panel(assets_tab):
                    for owned_category in sorted_owned_assets:
                        asset_container_owned = ui.row().classes('basis-full justify-start space-x-4 full-flex')
                        with asset_container_owned:
                            with ui.column().classes('items-center'):
                                with ui.row().classes("items-start"):
                                    CategoryLabel(owned_category)
                                # Creates cards for each asset
                                with ui.row().classes("items-start"):
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
                                with ui.row().classes("items-start"):
                                    CategoryLabel(category)
                                # Creates cards for each asset
                                with ui.row().classes("items-start"):
                                    for asset in sorted_assets[category]:
                                        await render_asset_cards(asset)
                        ui.separator()
        
            


