import elements.theme as theme
from classes.Enable import Enable
from elements.target_counter_dialog import target_counter_dialog
from elements.new_string_dialog import new_string_dialog
from helpers.utilities import format_str_for_filename_super
from handlers.assethandler import *
from elements.explanation import explanation
import traceback
from nicegui import app, ui

# TODO: Fix returns & passing info in.
enable = Enable()
@ui.page('/createasset')
async def new_asset():
    # pulling in the information of game etc
    # load in selected_game, if there is one.
    selected_game = app.storage.user.get("selected_game", {})
    selected_save = app.storage.user.get("selected_save", {})

    config = app.storage.user.get("config", {})
    paths = config.get("Paths",{})
    template_paths = paths.get("templatefilepath", "Not Set")

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
        render_counter_bar.refresh()
    
    # getting the sell prices
    async def get_sell_price():
        result = await target_counter_dialog('Sell Price for Asset')
        if 'sell_prices' not in new_asset_dict:
            new_asset_dict['sell_prices'] = {}
        new_asset_dict['sell_prices'][result['name']] = int(result['value'])
        render_counter_bar.refresh()

    # Calls the methods to write the asset to .json
    async def create_asset_json(is_default: bool):
        # if Default or Custom pick where to put asset
        create_result = {}

        try:
            # Ensure the game matches the template
            matches_template = check_template_bool(new_asset_dict, template_paths)
            if matches_template:
                # Try to format the name.
                new_asset_name = new_asset_dict['name']

                format_result = {}
                name_result = {}

                format_result = format_str_for_filename_super(new_asset_dict['name'])

                if format_result['result']:
                    file_name = format_result['string']
                    # check for duplicates
                    if is_default:
                        asset_name = get_new_asset_name(new_asset_dict['name'], selected_game['asset_default_path'])
                    else:
                        asset_name = get_new_asset_name(new_asset_dict['name'], selected_save['asset_customs_path'])
                
                    if "_Placeholder" in asset_name['name']:
                        with ui.dialog() as name_existed, ui.card():
                            ui.label("Notice!").classes('h3')
                            ui.label("A game by the same name already exists.")
                            ui.label(f"Your game will be saved as: {asset_name['name']}")
                            ui.button('Close', on_click=name_existed.close)
                        name_existed.open
                    # attempt to create asset here.
                    try:
                        create_result = new_asset_gui(is_default, new_asset_dict, selected_game, selected_save, asset_name['file'])
                        if create_result['result']:
                            with ui.dialog() as success_create, ui.card():
                                ui.label('Success!').classes('font-bold')
                                ui.label(create_result['message'])
                                ui.label('Feel free to leave this page now.')
                                ui.button('Close', on_click=success_create.close)
                            success_create.open
                            ui.notify("Congrats! Asset created!", 
                                      type='positive', 
                                      position="top",)
                            # clear page somehow
                    except:
                        # failed to create the asset
                        with ui.dialog() as fail_create, ui.card():
                            ui.label('Oh no!').classes('font-bold')
                            ui.label(create_result['message'])
                            ui.label("Please check that the necesscary folders exist, and STAT has permission to write to them.")
                            ui.label(f'Default Asset Path:  {selected_game['default_assets']}')
                            ui.label(f'Custom Asset Path: {selected_save['asset_customs_path']}')
                            ui.button('Close', on_click=fail_create.close)
                        fail_create.open
            # Template Mismatch
            else:
                with ui.dialog() as template_error, ui.card():
                    ui.label("Error!").classes('h3')
                    ui.label("The new asset dictionary does not match the expected asset template.")
                    ui.label("Unable to save the asset.")
                    ui.button('Close', on_click=template_error.close())
                template_error.open

        except FileNotFoundError as e:
            print(traceback.format_exc())
            with ui.dialog() as file_error, ui.card():
                ui.label("Error!").classes('h3')
                ui.label("File not found.")
                ui.label(f"Details: {str(e)}")
                ui.label("Please ensure the specified file paths are correct.")
                ui.button('Close', on_click=file_error.close)
            file_error.open

        except PermissionError as e:
            print(traceback.format_exc())
            with ui.dialog() as permission_error, ui.card():
                ui.label("Error!").classes('h3')
                ui.label("Permission denied.")
                ui.label(f"Details: {str(e)}")
                ui.label("Please ensure the application has the necessary permissions.")
                ui.button('Close', on_click=permission_error.close)
            permission_error.open

        except Exception as e:
            with ui.dialog() as general_error, ui.card():
                ui.label("Error!").classes('h3')
                ui.label("An unexpected error occurred.")
                ui.label(f"Details: {str(e)}")
                ui.label("Please check the application logs for more information.")
                ui.button('Close', on_click=general_error.close)
            general_error.open

    with theme.frame('Create an Asset'):
        buy_costs = new_asset_dict['buy_costs']
        sell_prices = new_asset_dict['sell_prices']

        with ui.column().classes("full-flex content-center w-100"):
            # If no selected_game, open up prompt to select one
            if not selected_game or 'name' not in selected_game:
                with ui.row():
                    ui.icon('warning').classes('text-3xl')
                    ui.label('Warning: No selected game detected.').classes('text-2xl')
                ui.label('Cannot create asset with no game selected.')
                ui.label('Please select a game from \'View Games\'.')
                with ui.link(target = '/selectgames'):
                    ui.button('Find Game File')
            else:
                # Name the source game
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label('Source Game: ').classes('font-bold')
                        ui.icon('info')
                        source_game = ui.label(f'{selected_game['name']}')
                        source_game.bind_text(new_asset_dict, 'source_game')
                    
                # Is this a Default or Custom Asset?
                # If Custom, pick associated Save
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label("Is this for a default asset?").classes('font-semibold')
                        is_default = ui.toggle({True:'Default', False:'Custom'})
                        is_default.classes('bg-blue-600')
                        if not is_default.value:
                            # If no selected_save, open up prompt to select one
                            if not selected_save or 'name' not in selected_save:
                                ui.label('Warning: No selected save detected.')
                                ui.label('Please select a save .json file.')
                                with ui.link(target=f'/selectsaves/{selected_game['name']}'):
                                    ui.button('Find Save File')
                            else:
                                # Name the source save
                                with ui.column().classes('items-start'):
                                    ui.label('Source Save: ').classes('font-bold')
                                    ui.label(f'{selected_save['name']}')
                            
                # Input name for the asset.
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label('Enter a name for the new asset: ').classes('font-bold')
                        name_input = ui.input(label='Asset Name', placeholder='50 character limit',
                                    on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                        name_input.props('clearable')
                        name_input.validation={"Too short!": enable.is_too_short} 
                        name_input.bind_value(new_asset_dict, 'name')
                        name_chars_left = ui.label()

                # Input category for the asset
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label('Enter a category for the new asset: ').classes('font-bold')
                        category_input = ui.input(label='Category', placeholder='50 character limit',
                                    on_change=lambda e: category_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                        category_input.props('clearable')
                        category_input.validation={"Too short!": enable.is_too_short} 
                        category_chars_left = ui.label()
                        category_input.bind_value(new_asset_dict, 'category')

                # Input description for the asset.
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label('Enter a description for the new asset:').classes('font-bold')
                        description = ui.textarea(label='Asset Description', placeholder='type here',
                                        on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' characters used.')).props('clearable')
                        description.classes('hover:border-solid border-dotted hover:border-4 border-l-4 border-orange-500 rounded')
                        # this handles the validation of the field.
                        desc_chars_left = ui.label()
                        description.bind_value(new_asset_dict, 'description')

                # Asset Type
                with ui.row().classes('items-center justify-start space-x-4'): 
                    with ui.column().classes('items-start'):
                        ui.label("Asset Type").classes('font-bold')
                        asset_type_input = ui.input(label='Asset Type', placeholder='type here',
                                            on_change=lambda f: asset_type_chars_left.set_text(str(len(f.value)) + ' used.')).props('clearable')
                        asset_type_chars_left = ui.label()
                        asset_type_input.bind_value(new_asset_dict, 'asset_type')

                # Attributes
                with ui.row().classes('items-center justify-start space-x-4'): 
                    with ui.column().classes('items-start'):
                        ui.label("Do you want to add an attribute to your asset?").classes('font-bold')
                        ui.button(
                            "Add Attribute", 
                                  icon="create", 
                                  on_click=lambda: new_string_dialog('Attribute')
                                  )

                # Add Buy Costs
                with ui.row().classes('items-left justify-start space-x-4'): 
                    with ui.column().classes('items-start'):
                        ui.label("Do you want to add a Buy Cost to your asset?").classes('font-bold')
                        has_buy_costs = ui.switch("Yes")
                        has_buy_costs.props('color="positive"')
                        with ui.column().bind_visibility_from(has_buy_costs, 'value'):
                            # Add Buy Costs
                            ui.label('You can add more than one buy cost to the asset.')
                            new_buy_cost = ui.button(
                                "Add Buy Cost",
                                icon="create",
                                on_click=get_buy_cost
                            )
                            # TODO: Add way to view added buy costs
                            # ui.label('Buy Costs Added:')
                            with ui.row().classes('full flex'):
                                for buy_cost in buy_costs:
                                    await render_counter_bar(buy_costs, buy_cost)
                    
                # Add Sell Prices
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label("Do you want to add a Sell Price to your asset?").classes('font-bold')
                        has_sell_prices = ui.switch("Yes")
                        has_sell_prices.props('color="positive"')
                        # display based on above
                        with ui.column().bind_visibility_from(has_sell_prices, 'value'):
                            ui.label("You can add more than one sell price to the asset.")
                            new_sell_cost = ui.button(
                                "Add Sell Cost",
                                icon="create",
                                on_click=get_sell_price
                            )
                            # TODO: Add way to see already added sell costs
                            # ui.label('Sell Prices Added:')
                            with ui.row().classes('full flex'):
                                for sell_price in sell_prices:
                                    await render_counter_bar(sell_prices, sell_price)


                # Add any extra special text to the asset.
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label('Enter any special text for the new asset:').classes('font-bold')
                        special = ui.textarea(label='Special Text', placeholder='type here',
                                            on_change=lambda f: special_chars_left.set_text(str(len(f.value)) + ' characters used.')).props('clearable')
                        special.classes('hover:border-solid border-dotted hover:border-4 border-l-4 border-orange-500 rounded')
                        special.bind_value(new_asset_dict, 'special')
                        special_chars_left = ui.label()
                
                # effects
                """
                with ui.column().classes('items-start'):
                    ui.label("Sorry, this feature hasnt been implemented yet!")
                    # If loaded_game.effects[] == empty: "Please add effects to the game 
                    # before trying to add them to assets."
                """
        
                # Icon selection
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label("Select an image you want to use as an icon:").classes('font-bold')

                        async def choose_icon():
                            icon_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
                            for file in icon_files:
                                asset_icon = file
                            new_asset_dict['icon'] = asset_icon
                        
                        ui.button('choose file', on_click=choose_icon)

                # image
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label("Select an image you want to associate with the asset:").classes('font-bold')
                        async def choose_image():
                            image_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
                            for file in image_files:
                                asset_image = file
                            new_asset_dict['image'] = asset_image

                        ui.button('choose file', on_click=choose_image)

                # submit
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label("Done?")
                        ui.button("Sumbit", on_click=lambda: create_asset_json(is_default.value))

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