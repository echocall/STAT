import elements.theme as theme
from classes.Enable import Enable
from elements.target_counter_dialog import target_counter_dialog
from elements.new_string_dialog import new_string_dialog
from handlers.assethandler import *
from elements.explanation import explanation
from elements.UserConfirm import *
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

    user_confirm = UserConfirm()

    config = app.storage.user.get("config", {})
    paths = config.get("Paths",{})
    templates_paths = paths.get("templatefilepath", "Not Set")
    root_path = paths.get("osrootpath", "Not Set")
    games_path = paths.get("gamespath", "Not Set")
    assets_path = paths.get("assetspath", "Not Set")
    default_assets_path = paths.get("defaultassetspath", "Not Set")
    custom_assets_path = paths.get("customassetspath", "Not Set")

    str_templates_path = root_path + templates_paths
    str_games_path = root_path + games_path
    str_assets_path = str_games_path + '\\' +  selected_game['name'] + assets_path

    new_asset_dict = {
        'name': '', 'category':'',
        'description': '', 'source': '',
        'asset_type': '', 'attributes': [],
        'buy_costs':{}, 'sell_prices': {},
        'special':'', 'effects':[],
        'icon':'', 'image':''
    }

    # Render the buy_costs.
    @ui.refreshable
    def render_all_buy_costs() -> ui.element:
        with ui.row().classes('gap-2') as buy_cost_display_case:
            for buy_cost, value in new_asset_dict['buy_costs'].items():
                with ui.row().classes('items-center gap-2'):
                    ui.label(f'{buy_cost}:').classes('font-medium')
                    ui.label(str(value)).classes()

                    # Add delete button
                    ui.button(icon='delete', color='red', 
                            on_click=lambda b_cost=buy_cost:  
                            user_confirm.show(f'Are you sure you want to delete {b_cost}?', 
                                        lambda: delete_buy_cost(new_asset_dict, b_cost))).props('flat dense')
        return buy_cost_display_case

    # get the new Counter from New Counter Dialog
    async def add_buy_cost():
        result = await target_counter_dialog('Buy Cost for Asset')
        if result:
            if 'buy_costs' not in new_asset_dict:
                new_asset_dict['buy_costs'] = {}
            new_asset_dict['buy_costs'][result['name']] = int(result['value'])
            render_all_buy_costs.refresh()
        else:
            ui.notify("""No buy costs added, dialog canceled. If you want to add buy costs use the submit button.""",
                      type='warning',
                      position='top',
                      multi_line=True)

    # Delete a buy_cost.
    def delete_buy_cost(new_asset_dict, buy_cost_name: str) -> ui.element:
        if buy_cost_name in new_asset_dict['buy_costs']:
            del new_asset_dict['buy_costs'][buy_cost_name]
            render_all_buy_costs.refresh()

    # Render the buy_costs.
    @ui.refreshable
    def render_all_sell_prices() -> ui.element:
        with ui.row().classes('gap-2') as sell_price_display_case:
            for sell_price, value in new_asset_dict['sell_prices'].items():
                with ui.row().classes('items-center gap-2'):
                    ui.label(f'{sell_price}:').classes('font-medium')
                    ui.label(str(value)).classes()

                    # Add delete button
                    ui.button(icon='delete', color='red', 
                            on_click=lambda s_price=sell_price:  
                            user_confirm.show(f'Are you sure you want to delete {s_price}?', 
                                        lambda: delete_sell_price(new_asset_dict, s_price))).props('flat dense')
        return sell_price_display_case

    # get the new Counter from New Counter Dialog
    async def add_sell_price():
        result = await target_counter_dialog('Sell Price for Asset') 
        if result:
            if 'sell_prices' not in new_asset_dict:
                new_asset_dict['sell_prices'] = {}
            new_asset_dict['sell_prices'][result['name']] = int(result['value'])
            render_all_sell_prices.refresh()
        else:
            ui.notify("""No sell prices added, dialog canceled. If you want to add sell prices use the submit button.""",
                      type='warning',
                      position='top',
                      multi_line=True)

    # Delete a buy_cost.
    def delete_sell_price(new_asset_dict, sell_price_name: str) -> ui.element:
        if sell_price_name in new_asset_dict['sell_prices']:
            del new_asset_dict['sell_prices'][sell_price_name]
            render_all_sell_prices.refresh()

    # Render the actors.
    @ui.refreshable
    def render_all_attributes(User_confirm, new_asset_dict) -> ui.element:
        with ui.row().classes('gap-2') as attributes_display_case:
            for value in new_asset_dict.get('attributes',[]):
                with ui.row().classes('items-center gap-2'):
                    ui.label(str(value)).classes('font-medium')

                    # Add delete button
                    ui.button(icon='delete', color='red', 
                        on_click=lambda v = value:
                        User_confirm.show(f'Are you sure you want to delete {v}?', 
                                    lambda: delete_attribute(new_asset_dict, v))
                                    ).props('flat dense')
        return attributes_display_case

    # adding an attribute
    async def add_attribute():
        result = await new_string_dialog('Attribute')
        if result:
            if 'attributes' not in new_asset_dict:
                new_asset_dict['attributes'] = []
            new_asset_dict['attributes'].append(result['name'])
            render_all_attributes.refresh()
        else:
            ui.notify("""Warning: Dialog cancelled. No Attributes added.""",
                      type='warning',
                      psoition='top',
                      multi_line=True)

    # Delete an attribute.
    def delete_attribute(new_game_dict: dict, attribute_name: str) -> ui.element:
        """Deletes an attribute from the new_game_dict's attribute list and refreshes the attribute section."""
        if attribute_name in new_game_dict['attributes']:
            target_index = new_game_dict['attributes'].index(attribute_name)
            del new_game_dict['attributes'][target_index]
            render_all_attributes.refresh()

    # Calls the methods to write the asset to .json
    async def create_asset_json(is_default: bool):
        """Calls the methods in assethandler to write the asset to .json"""
        create_result = {}
        try:
            # Ensure the asset matches the template
            matches_template = check_template_bool(new_asset_dict, str_templates_path)
            if matches_template['match']:
                # check for duplicates
                asset_name = get_new_asset_name(str_assets_path, new_asset_dict['name'])

                if "_Placeholder" in asset_name['name']:
                    ui.notify(f"""Notice! An asset by the same name already exists. 
                              Could not save asset. 
                              Check the log file in folder where the asset would be created for more details.""",
                                type='warning',
                                position='top',
                                multi_line=True)
                # attempt to create asset here.
                try:
                    create_result = new_asset_gui(is_default, 'config.txt', new_asset_dict, selected_game, selected_save)
                    if create_result['result']:
                        ui.notify("Congrats! Asset created!", 
                                    type='positive', 
                                    position="top")
                        # clear page somehow
                except:
                    # failed to create the asset
                    with ui.dialog() as fail_create, ui.card():
                        ui.label('Oh no!').classes('font-bold text-large')
                        ui.label(create_result['message'])
                        ui.label("Please check that the necesscary folders exist, and STAT has permission to write to them.")
                        ui.label(f'Default Asset Path:  {selected_game['default_assets']}')
                        ui.label(f'Custom Asset Path: {selected_save['asset_customs_path']}')
                        ui.button('Close', on_click=fail_create.close)
                    fail_create.open
            # Template Mismatch
            else:
                ui.notify("Error: Coule not save. The new asset dictionary does not match expected asset template. Unable to save.", 
                          position='top', 
                          type='negative',
                            multi_line=True)

        except FileNotFoundError as e:
            ui.notify("""Error: could not save. STAT cound not find the file. Please check the file paths in config.txt are correct.""",
                      position='top',
                      type='negative',
                      multi_line=True)

        except PermissionError as e:
            print(traceback.format_exc())
            ui.notify("Error: Could not save. STAT does not have permission to write to the folder in those locations. Please check the file paths in config.txt are correct.",
                      position='top',
                      type='negative',
                      multi_line=True)

        except Exception as e:
            print(traceback.format_exc())
            ui.notify("""Error: Could not save. An unexpected error has occured. Please check application logs for more information.""",
                      position='top',
                      type='negative',
                      multi_line=True)

    with theme.frame('Create an Asset'):
        # If no selected_game, open up prompt to select one
        if not selected_game or 'name' not in selected_game:
            with ui.row():
                ui.icon('warning').classes('text-3xl')
                ui.label('Warning: No selected game detected.').classes('text-2xl text-center')
            ui.label('Cannot create asset with no game selected.').classes('text-center')
            ui.label('Please select a game from \'View Games\'.').classes('text-center')
            with ui.link(target = '/selectgames'):
                ui.button('Find Game File')
        else:
            # Name the source game
            with ui.row().classes():
                with ui.column().classes():
                    with ui.row():
                        ui.label('Source Game: ').classes('text-lg')
                        ui.icon('info')
                    source_game = ui.label(f'{selected_game['name']}').classes()
                    source_game.bind_text(new_asset_dict, 'source')
                    new_asset_dict['source'] = selected_game['name']
                
            # Is this a Default or Custom Asset?
            # If Custom, pick associated Save
            with ui.row().classes():
                with ui.column().classes():
                    ui.label("Is this for a default asset?").classes('text-lg')
                    is_default = ui.toggle({True:'Default', False:'Custom'})
                    is_default.props('color="secondary"')
                        
            # Input name for the asset.
            with ui.row().classes():
                with ui.column().classes():
                    ui.label('Enter a name for the new asset: ').classes('text-lg')
                    name_input = ui.input(label='Asset Name', placeholder='50 character limit',
                                on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                    name_input.props('clearable')
                    name_input.validation={"Too short!": enable.is_too_short} 
                    name_input.bind_value(new_asset_dict, 'name')
                    name_chars_left = ui.label()

            # Input category for the asset
            with ui.row().classes():
                with ui.column().classes():
                    ui.label('Enter a category for the new asset: ').classes('text-lg')
                    category_input = ui.input(label='Category', placeholder='50 character limit',
                                on_change=lambda e: category_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                    category_input.props('clearable')
                    category_input.validation={"Too short!": enable.is_too_short} 
                    category_chars_left = ui.label()
                    category_input.bind_value(new_asset_dict, 'category')

            # Input description for the asset.
            with ui.row().classes():
                with ui.column().classes('w-full max-w-screen-md'):
                    ui.label('Enter a description for the new asset:').classes('text-lg')
                    description = ui.textarea(label='Asset Description', placeholder='type here',
                                    on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' characters used.')).props('clearable')
                    description.classes('hover:border-solid border-dotted hover:border-4 border-l-4 border-orange-500 rounded w-full')
                    # this handles the validation of the field.
                    desc_chars_left = ui.label()
                    description.bind_value(new_asset_dict, 'description')

            # Asset Type
            with ui.row().classes(): 
                with ui.column().classes():
                    ui.label("Asset Type").classes('text-lg')
                    asset_type_input = ui.input(label='Asset Type', placeholder='type here',
                                        on_change=lambda f: asset_type_chars_left.set_text(str(len(f.value)) + ' used.')).props('clearable')
                    asset_type_chars_left = ui.label()
                    asset_type_input.bind_value(new_asset_dict, 'asset_type')

            # Attributes
            with ui.row().classes(): 
                with ui.column().classes():
                    ui.label("Do you want to add an attribute to your asset?").classes('text-lg')
                    ui.button(
                        "Add Attribute", 
                                icon="create", 
                                on_click=lambda: add_attribute()
                                )
                    ui.label("Attributes added: ")
                    attributes_display = render_all_attributes(user_confirm, new_asset_dict)

            # Add Buy Costs
            with ui.row().classes(): 
                with ui.column().classes():
                    ui.label("Do you want to add a Buy Cost to your asset?").classes('text-lg')
                    has_buy_costs = ui.switch("Yes")
                    has_buy_costs.props('color="positive"')
                    with ui.column().bind_visibility_from(has_buy_costs, 'value'):
                        # Add Buy Costs
                        ui.label('You can add more than one buy cost to the asset.')
                        new_buy_cost = ui.button(
                            "Add Buy Cost",
                            icon="create",
                            on_click=add_buy_cost
                        )
                        ui.label("Buy Costs added: ").bind_visibility_from(has_buy_costs, 'value')
                        counter_display = render_all_buy_costs()
                        counter_display.bind_visibility_from(has_buy_costs,'value')
                
            # Add Sell Prices
            with ui.row().classes():
                with ui.column().classes():
                    ui.label("Do you want to add a Sell Price to your asset?").classes('text-lg')
                    has_sell_prices = ui.switch("Yes")
                    has_sell_prices.props('color="positive"')
                    # display based on above
                    with ui.column().bind_visibility_from(has_sell_prices, 'value'):
                        ui.label("You can add more than one sell price to the asset.")
                        new_sell_cost = ui.button(
                            "Add Sell Cost",
                            icon="create",
                            on_click=add_sell_price
                        )
                        # TODO: Add way to see already added sell costs
                        # ui.label('Sell Prices Added:')
                        ui.label("Sell Prices added: ").bind_visibility_from(has_sell_prices, 'value')
                        counter_display = render_all_sell_prices()
                        counter_display.bind_visibility_from(has_sell_prices,'value')

            # Add any extra special text to the asset.
            with ui.row().classes():
                with ui.column().classes():
                    ui.label('Enter any special text for the new asset:').classes('text-lg')
                    special = ui.textarea(label='Special Text', placeholder='type here',
                                        on_change=lambda f: special_chars_left.set_text(str(len(f.value)) + ' characters used.')).props('clearable')
                    special.classes('hover:border-solid border-dotted hover:border-4 border-l-4 border-orange-500 rounded')
                    special.bind_value(new_asset_dict, 'special')
                    special_chars_left = ui.label()
            
            # effects
            """
            with ui.column().classes():
                ui.label("Sorry, this feature hasnt been implemented yet!")
                # If loaded_game.effects[] == empty: "Please add effects to the game 
                # before trying to add them to assets."
            """
    
            # Icon selection
            with ui.row().classes():
                with ui.column().classes():
                    ui.label("Select an image you want to use as an icon:").classes('text-lg')

                    async def choose_icon():
                        icon_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
                        for file in icon_files:
                            asset_icon = file
                        new_asset_dict['icon'] = asset_icon
                    
                    ui.button('choose file', on_click=choose_icon)

            # image
            with ui.row().classes():
                with ui.column().classes():
                    ui.label("Select an image you want to associate with the asset:").classes('text-lg')
                    async def choose_image():
                        image_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
                        for file in image_files:
                            asset_image = file
                        new_asset_dict['image'] = asset_image

                    ui.button('choose file', on_click=choose_image)

            # submit
            with ui.row().classes():
                with ui.column().classes():
                    ui.label("Done?")
                    ui.button("Submit", on_click=lambda: create_asset_json(is_default.value))

# Loads the page
@ui.refreshable
def load_page() -> ui.element:
    a = 1+1