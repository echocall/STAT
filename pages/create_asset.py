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
    selected_game = {}
    selected_save = {}
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
        new_asset_dict['buy_costs'][result['name']] = result['value']
    
    # getting the sell prices
    async def get_sell_price():
        result = await target_counter_dialog('Sell Price for Asset')
        if 'sell_prices' not in new_asset_dict:
            new_asset_dict['sell_prices'] = {}
        new_asset_dict['sell_prices'][result['name']] = result['value']

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
                selected_game['default_assets'].append(new_asset_dict['name'])
            file_location = selected_game['asset_default_path']
            # save the assets information into .json file in appropriate location
            # update the selected game's list of assets with the new asset's information
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
        with ui.column():
            #with ui.row():
                # btn_select_game = ui.button('Select Game',on_click=prompt_select_game)
                # TODO: make
                # btn_select_save = ui.button('Select Save', on_click=prompt_select_save)
            
            ui.label("An asset is assumed to belong to the selected game.").classes('text-2xl')

            # If no selected_game, open up prompt to select one
            if not selected_game:
                with ui.dialog() as no_game, ui.card():
                    ui.label('Warning: No selected game detected.')
                    ui.label('Please select a game.')
                    ui.button('Find Game File', on_click=choose_game)
                    ui.button('Close', on_click=no_game.close)
            else:
                # Name the source game
                with ui.column().classes('w-80 items-stretch'):
                    ui.label('Source Game: ').classes('font-bold')
                    ui.label(f'{selected_game['name']}')
                
            
                
                # Is this a Default or Custom Asset?
                # If Custom, pick associated Save
                with ui.column().classes('items-stretch'):
                    ui.label("Is this for a default asset?")
                    is_default = ui.toggle({True:'Default', False:'Custom'}).bind_value(bln_is_default)
                    ui.button('set_value', on_click=lambda: is_default)

                    if not bln_is_default:
                        # If no selected_save, open up prompt to select one
                        if not selected_game:
                            with ui.dialog() as no_save, ui.card():
                                ui.label('Warning: No selected save detected.')
                                ui.label('Please select a save.')
                                ui.button('Choose save File', on_click=choose_save)
                                ui.button('Close', on_click=no_save.close)
                            ui.button('Find Save File', on_click=choose_save)
                        else:
                            # Name the source game
                            with ui.column().classes('w-80 items-stretch'):
                                ui.label('Source Save: ').classes('font-bold')
                                ui.label(f'{selected_save['name']}')
                        
                # Input name for the asset.
                with ui.column().classes('w-80 items-stretch'):
                    ui.label('Enter a name for the new asset: ').classes('font-bold')
                    name_input = ui.input(label='Asset Name', placeholder='50 character limit')
                    name_input.props('clearable')
                    name_input.validation={"Too short!": enable.is_too_short} 
                    name_chars_left = ui.label()

                # Input category for the asset
                with ui.column().classes('w-80 items-stretch'):
                    ui.label('Enter a category for the new asset: ').classes('font-bold')
                    category_input = ui.input(label='Category', placeholder='50 character limit',
                                on_change=lambda e: category_chars_left.set_text(len(e) + ' of 50 characters used.'))
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
                has_buy_costs = ui.switch()
                # has_buy_costs.bind_value_to(bln_has_buy_costs)
                # Add Buy Costs
                with ui.column().classes('w-80 items-stretch').bind_visibility_from(has_buy_costs, 'value'):
                    ui.label('You can add more than one buy cost to the asset.')
                    new_buy_cost = ui.button(
                        "Add Buy Cost",
                        icon="create",
                        on_click=get_buy_cost
                    )

                # TODO: Add way to view added buy costs
                display_buy_costs = ui.toggle({'True':'Yes', 'False':'No'})
                with ui.row().bind_visibility_from(display_buy_costs,'key'):
                    for counter in new_asset_dict['buy_costs']:
                        ui.label(counter['name'] + counter['value'])
                    
                    added_buy_costs = ui.aggrid({
                        'defaultColDef': {'flex':1},
                        'columnDefs': [
                            {'headerName': 'Name', 'field': 'name'},
                            {'headerName': 'Cost', 'field': 'value'}
                        ],
                        'rowData': [
                            {'name':'Gold', 'value': 10},
                            {'name':'Silver','value': 50}
                        ],
                        'rowSelection':'multiple',
                    }).classes('max-h-40')

                    def update_buy_costs():
                        print(new_asset_dict['buy_costs'])
                        added_buy_costs.update()
                    ui.button('Update Grid', on_click=update_buy_costs)

                # Add Sell Prices
                ui.label("Do you want to add a Sell Price to your asset?").classes('font-bold')
                has_sell_costs = ui.switch()
                # has_sell_costs.bind_value_to(bln_has_sell_prices)
                # display based on above
                with ui.column().classes('w-80 items.stretch').bind_visibility_from(has_sell_costs, 'value'):
                    ui.label("You can add more than one sell price to the asset.")
                    new_sell_cost = ui.button(
                        "Add Sell Cost",
                        icon="create",
                        on_click=get_sell_price
                    )

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
                        new_asset_dict['icon'] = file;
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


