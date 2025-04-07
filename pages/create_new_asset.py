import elements.theme as theme
from elements.message import message
from classes.Enable import Enable
from classes.MyAsset import MyAsset
from create_new_dict_entry_dialog import new_dict_entry_dialog
from new_counter_dialog import new_counter_dialog
from nicegui import ui

# TODO: Fix returns & passing info in.
# TODO: don't call during the creation of a new game, wait until game has been created?
# COULD pass in the value in the game.name, or have a list of game names passed in in other call cases... hm...
enable = Enable()
@ui.page('/createasset')
def new_asset():
    with theme.frame('Create an Asset'), ui.card().classes("w-full"):
        
        message('Create an Asset')
        # Input name for the asset.
        with ui.card_section().classes('w-80 items-stretch'):
            ui.label('Enter a name for the new asset: ')
            name_input = ui.input(label='Asset Name', placeholder='50 character limit',
                        on_change=lambda e: name_chars_left.set_text(len(e) + ' of 50 characters used.'))
            name_input.props('clearable')
            name_input.validation={"Too short!": enable.is_too_short} 
            name_chars_left = ui.label()

        with ui.card_section().classes('w-80 items-stretch'):
            ui.label('Enter a category for the new asset: ')
            category_input = ui.input(label='Category', placeholder='50 character limit',
                        on_change=lambda e: category_chars_left.set_text(len(e) + ' of 50 characters used.'))
            category_input.props('clearable')
            category_input.validation={"Too short!": enable.is_too_short} 
            category_chars_left = ui.label()

        # Input description for the asset.
        with ui.card_section().classes('w-80 items-stretch'):
            ui.label('Enter a description for the new asset:').classes()
            description = ui.input(label='Asset Description', placeholder='500 character limit',
                            on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.')).props('clearable')
            # this handles the validation of the field.
            description.validation={"Too long!": lambda b: enable.is_too_long_variable(b, 500)}
            desc_chars_left = ui.label()
        
        # Name the source asset
        with ui.card_section().classes('w-80 items-stretch'):
            ui.label('Enter the source game for the asset: ')
            # TODO: Grab the game name from list of games.


        # Create Buy Costs
        ui.label("Do you want to add a Buy Cost to your asset?")
        has_buy_costs = ui.switch()
        # Add Buy Costs
        with ui.card_section().classes('w-80 items-stretch').bind_visibility_from(has_buy_costs, 'value'):
            ui.label('You can add more than one buy cost to the asset.')
            new_buy_cost = ui.button(
                "Add Buy Cost",
                icon="create",
            )
            new_buy_cost.on(
                "click",
                lambda: new_dict_entry_dialog('Buy Cost'),
            )

        # Add Sell Prices
        ui.label("Do you want to add a Sell Price to your asset?")
        has_sell_costs = ui.switch()
        with ui.card_section().classes('w-80 items.stretch').bind_visibility_from(has_sell_costs,'value'):
            ui.label("You can add more than one sell price to the asset.")
            new_sell_cost = ui.button(
                "Add Sell Cost",
                icon="create",
            )
            # Pull up the new_dict_entry_dialog to set new sell price.
            new_sell_cost.on(
                "click",
                lambda: new_dict_entry_dialog('Sell Price'),
            )

        # Add any extra special text to the asset.
        with ui.card_section().classes('w-80 items-stretch'):
            ui.label('Enter any special text for the new asset:').classes()
            special = ui.input(label='Special Text', placeholder='500 character limit',
                                on_change=lambda f: special_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.')).props('clearable')
            # this handles the validation of the field.
            special.validation={"Too long!": lambda b: enable.is_too_long_variable(b, 500)}
            special_chars_left = ui.label()
        
        # effects
        with ui.card_section().classes('w-80 items-stretch'):
            ui.label("Sorry, this feature hasnt been implemented yet!")
            # If loaded_game.effects[] == empty: "Please add effects to the game 
            # before trying to add them to assets."
    
    # icon

    # image

