import elements.theme as theme
from classes.Enable import Enable
from elements.new_dict_entry import new_dict_entry
from elements.target_counter_dialog import target_counter_dialog
from elements.select_game_dialog import prompt_select_game
from elements.select_save_dialog import prompt_select_save
from helpers.crud import single_json_getter_fullpath
from nicegui import app, ui

# TODO: Fix returns & passing info in.
# TODO: don't call during the creation of a new game, wait until game has been created?
# COULD pass in the value in the game.name, or have a list of game names passed in in other call cases... hm...
enable = Enable()
@ui.page('/createasset')
async def new_asset():
    # pulling in the information of game etc
    # load in selected_game, if there is one.
    selected_game = app.storage.user.get("selected_game", {})
    selected_save = app.storage.user.get("selected_save", {})

    new_asset_dict = {
        'name': '', 'category':'',
        'description': '', 'source': '',
        'asset_type': '', 'attributes': [],
        'buy_costs':{}, 'sell_prices': {},
        'special':'', 'effects':[],
        'icon':'', 'image':'str'
    }

    bln_is_default = False
    bln_has_buy_costs = False
    bln_has_sell_prices = False

    # getting the buy costs
    async def get_buy_cost():
        result = await target_counter_dialog('Buy Cost for Asset')
        if 'buy_costs' not in new_asset_dict:
            new_asset_dict['buy_costs'] = {}
        new_asset_dict['buy_costs'][result['name']] = int(result['value'])
        print("inside get_buy_cost")
        print(new_asset_dict['buy_costs'])
        render_counter_bar.refresh()
    
    # getting the sell prices
    async def get_sell_price():
        result = await target_counter_dialog('Sell Price for Asset')
        if 'sell_prices' not in new_asset_dict:
            new_asset_dict['sell_prices'] = {}
        new_asset_dict['sell_prices'][result['name']] = int(result['value'])
        render_counter_bar.refresh()

    async def choose_game():
        game_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
        for file in game_files:
            game = single_json_getter_fullpath(file)
            # Get the game from the path
        selected_game = game
        app.storage.user['selected_game'] = game

    async def choose_save():
        save_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
        for file in save_files:
            save = single_json_getter_fullpath(file)
            # Get the game from the path
        selected_save = save
        app.storage.user['selected_save'] = save

    # Calls the methods to write the asset to .json
    async def create_asset(asset_type: str):
        # if Default or Custom pick where to put asset
        if asset_type == 'Default':
            x = 24 + 24
            if not selected_game['has_assets']:
                selected_game['has_assets'] = True
            else:
                file_location = selected_game['asset_default_path']
                # update the selected game's list of assets with the new asset's information
                selected_game['default_assets'].append(new_asset_dict['name'])
            # save the assets information into .json file in appropriate location
            try:
                # save the asset data
                a = 1+1
            except:
                # return some error or call alert_dialog.py
                b = 2+2
            finally:
                # figure this out.
                c = 3+3
        # Asset is a Custom Asset        
        else:
            y = 25 + 25
            if selected_save['asset_customs']:
                file_location = selected_save['asset_customs_path']
            # save the assets information into .json file in appropri
            # save the assets information into .json file in appropriate location
            # update the selected game's list of assets with the new asset's information


    with theme.frame('Create an Asset'):
        buy_costs = new_asset_dict['buy_costs']
        sell_prices = new_asset_dict['sell_prices']

        with ui.column():
            # If no selected_game, open up prompt to select one
            if not selected_game or 'name' not in selected_game:
                with ui.row():
                    ui.icon('warning').classes('text-3xl')
                    ui.label('Warning: No selected game detected.').classes('text-2xl')
                ui.label('Cannot create asset with no game selected.')
                ui.label('Please select a game from \'Select Games\'.')
                with ui.link(target = '/selectgames'):
                    ui.button('Find Game File')
            else:
                # Name the source game
                with ui.column().classes('w-80 items-stretch'):
                    ui.label('Source Game: ').classes('font-bold')
                    ui.label(f'{selected_game['name']}')
                
                # Is this a Default or Custom Asset?
                # If Custom, pick associated Save
                with ui.column():
                    ui.label("Is this for a default asset?")
                    is_default = ui.toggle({True:'Default', False:'Custom'})
                    if not is_default.value:
                        # If no selected_save, open up prompt to select one
                        if not selected_save or 'name' not in selected_save:
                            ui.label('Warning: No selected save detected.')
                            ui.label('Please select a save .json file.')
                            with ui.link(target=f'/selectsaves/{selected_game['name']}'):
                                ui.button('Find Save File')
                        else:
                            # Name the source save
                            with ui.column().classes('w-80 items-stretch'):
                                ui.label('Source Save: ').classes('font-bold')
                                ui.label(f'{selected_save['name']}')
                        
                # Input name for the asset.
                with ui.column().classes('w-80 items-stretch'):
                    ui.label('Enter a name for the new asset: ').classes('font-bold')
                    name_input = ui.input(label='Asset Name', placeholder='50 character limit',
                                on_change=lambda e: name_chars_left.set_text(len(e.value) + ' of 50 characters used.'))
                    name_input.props('clearable')
                    name_input.validation={"Too short!": enable.is_too_short} 
                    name_chars_left = ui.label()

                # Input category for the asset
                with ui.column().classes('w-80 items-stretch'):
                    ui.label('Enter a category for the new asset: ').classes('font-bold')
                    category_input = ui.input(label='Category', placeholder='50 character limit',
                                on_change=lambda e: category_chars_left.set_text(len(e.value) + ' of 50 characters used.'))
                    category_input.props('clearable')
                    category_input.validation={"Too short!": enable.is_too_short} 
                    category_chars_left = ui.label()

                # Input description for the asset.
                with ui.column().classes('w-80 items-stretch'):
                    ui.label('Enter a description for the new asset:').classes('font-bold')
                    description = ui.input(label='Asset Description', placeholder='500 character limit',
                                    on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.')).props('clearable')
                    # this handles the validation of the field.
                    description.validation={"Too long!": lambda b: enable.is_too_long_variable(b, 500)}
                    desc_chars_left = ui.label()
                
                # Create Buy Costs
                ui.label("Do you want to add a Buy Cost to your asset?").classes('font-bold')
                has_buy_costs = ui.switch("Yes")
                has_buy_costs.props('colors="orange"')
                
                # Add Buy Costs
                with ui.column().classes('w-80 items-stretch').bind_visibility_from(has_buy_costs, 'value'):
                    ui.label('You can add more than one buy cost to the asset.')
                    new_buy_cost = ui.button(
                        "Add Buy Cost",
                        icon="create",
                        on_click=get_buy_cost
                    )

                    # TODO: Add way to view added buy costs
                    ui.label('Buy Costs Added:')
                    with ui.row().classes('full flex'):
                        for buy_cost in buy_costs:
                            await render_counter_bar(buy_costs, buy_cost)

                # Add Sell Prices
                ui.label("Do you want to add a Sell Price to your asset?").classes('font-bold')
                has_sell_costs = ui.switch("Yes")
                has_sell_costs.props('color="orange"')
                # display based on above
                with ui.column().classes('w-80 items.stretch').bind_visibility_from(has_sell_costs, 'value'):
                    ui.label("You can add more than one sell price to the asset.")
                    new_sell_cost = ui.button(
                        "Add Sell Cost",
                        icon="create",
                        on_click=get_sell_price
                    )
                    # TODO: Add way to see already added sell costs
                    ui.label('Sell Prices Added:')
                    for sell_price in sell_prices:
                        await render_counter_bar(sell_prices, sell_price)


                # Add any extra special text to the asset.
                with ui.column().classes('w-80 items-stretch'):
                    ui.label('Enter any special text for the new asset:').classes('font-bold')
                    special = ui.input(label='Special Text', placeholder='500 character limit',
                                        on_change=lambda f: special_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.')).props('clearable')
                    # this handles the validation of the field.
                    special.validation={"Too long!": lambda b: enable.is_too_long_variable(b, 500)}
                    special_chars_left = ui.label()
                
                # effects
                """
                with ui.column().classes('w-80 items-stretch'):
                    ui.label("Sorry, this feature hasnt been implemented yet!")
                    # If loaded_game.effects[] == empty: "Please add effects to the game 
                    # before trying to add them to assets."
                """
        
                # Icon selection
                with ui.column().classes('w-80 items-stretch'):
                    ui.label("Select an image you want to use as an icon:").classes('font-bold')
                    ui.label("Suggested icon size: 50x50px")

                    async def choose_icon():
                        icon_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
                        for file in icon_files:
                            asset_icon = file
                        new_asset_dict['icon'] = file
                        return asset_icon
                    
                    ui.button('choose file', on_click=choose_icon)

                # image
                with ui.column().classes('w-80 items-stretch'):
                    ui.label("Select an image you want to associate with the asset:").classes('font-bold')
                    async def choose_image():
                        image_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
                        for file in image_files:
                            asset_image = file
                        new_asset_dict['image'] = asset_image

                    ui.button('choose file', on_click=choose_image)


# Render the counters.
@ui.refreshable
async def render_counter_bar(counters: dict, counter: str) -> ui.element:
    print("inside render_counter_bar")
    current_counter = ui.label(f'{counter}:').classes('text-sm')
    print(counters)
    print(counter)
    # Work around for showing Current Counter amount without being able to fiddle with it.
    temp_current_amount = counters[counter]
    current_amount = ui.label(f'{temp_current_amount}').classes('text-sm')

# Loads the page
@ui.refreshable
def load_page() -> ui.element:
    a = 1+1