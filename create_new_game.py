import elements.theme as theme
from classes.Enable import *
from elements.message import message
from new_counter_dialog import new_counter_dialog
from classes.MyGame import MyGame
from elements.message import message
from nicegui import ui

enable = Enable()

def create() -> None:
    @ui.page('/creategame')
    def new_game():
        with theme.frame('Create a Game'):
            message('Create a Game')
            with ui.card().classes("flex"):
                with ui.card_section().classes('w-80 items-stretch items-center'):
                    # get the name of the game.
                    ui.label("Enter a name for the game. The name should be unique.").classes()
                    name_input = ui.input(label='Game Name', placeholder='50 character limit',
                                    on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                    # allows user to clear the field
                    name_input.props('clearable')
                    # This handles the validation of the field.
                    name_input.validation={"Too short!": enable.is_too_short} 
                    # Displays the characters.        
                    name_chars_left = ui.label()
                    
                with ui.card_section().classes('w-80 items-stretch'):
                    # input description for the game.
                    ui.label('Enter a description for the new game:').classes()
                    description = ui.input(label='Game Description', placeholder='500 character limit',
                                    on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.')).props('clearable')
                    # this handles the validation of the field.
                    description.validation={"Too long!": lambda b: enable.is_too_long_variable(b, 500)}
                    desc_chars_left = ui.label()
                    
                # Creating counters
                with ui.card_section().classes('w-80 items-stretch'):
                    # Create counters
                    ui.label('Do you want to add counters to your game?')
                    has_counters = ui.switch()

                    new_counter = ui.button(
                        "Add Counter",
                        icon="create",
                    )
                    new_counter.bind_visibility_from(has_counters, 'value')
                    new_counter.on(
                        "click",
                        lambda: new_counter_dialog(),
                    )
                    
                # Creating actors
                with ui.card_section().classes('w-80 items-stretch'):
                    ui.label('Do you want to add Actors now?')
                    has_actors = ui.switch()
                    has_actors.on('click', has_actors.set_value(has_actors.value))
                    # The button will pull up a different dialog box for creating an event
                    create_actors = ui.button('Create Actors', 
                                            on_click=lambda: ui.notify('You clicked Create Actors!'))
                    create_actors.bind_visibility_from(has_actors, 'value')

                # Creating Assets
                with ui.card_section().classes('w-80 items-stretch'):
                    ui.label('Do you want to add Assets now?')
                    has_assets = ui.switch()
                    has_assets.on('click', has_assets.set_value(has_assets.value))
                    # Button to called the dialog for creating an asset.
                    create_assets = ui.button('Create Assets', 
                                            on_click=lambda: ui.notify('You clicked Create Assets!'))
                    create_assets.bind_visibility_from(has_assets, 'value')

                # Creating Effects
                with ui.card_section().classes('w-80 items-stretch'):
                    ui.label('Do you want to add Effects now?')
                    has_effects = ui.switch()
                    has_effects.on('click', has_effects.set_value(has_effects.value))
                    # The button will pull up a different dialog box for creating an effect.
                    create_effects = ui.button('Create Effect', 
                                            on_click=lambda: ui.notify('You clicked Create Effects!'))
                    create_effects.bind_visibility_from(has_effects, 'value')

                # Creating Events
                with ui.card_section().classes('w-80 items-stretch'):
                    ui.label('Do you want to add Events now?')
                    has_events = ui.switch()
                    has_events.on('click', has_events.set_value(has_events.value))
                    # The button will pull up a different dialog box for creating an event.
                    create_events = ui.button('Create Events', 
                                            on_click=lambda: ui.notify('You clicked Create Events!'))
                    create_events.bind_visibility_from(has_events, 'value')

                # Initializing Turns
                with ui.card_section().classes('w-80 items-stretch'):
                    has_turns = ui.switch("Does your game have turns or rounds?")
                    has_turns.on('click',has_turns.set_value(has_turns.value))
                    # These should be invisible unless has_turns == True.
                    with ui.column().bind_visibility_from(has_turns,'value'):
                        ui.label("Do they increase or decrease as you play?")
                        turn_type = ui.radio({1: 'Increasing', 2: 'Decreasing'}).props('inline')
                        ui.label("What turn or round number does your game start on?")
                        start_turn = ui.number("Enter a whole number.")

                with ui.card_actions():
                    # The button submits the dialog providing the text entered
                    submit = ui.button(
                        "Create Game",
                        on_click=lambda:  ui.notify("You clicked submit!"),
                    )
                    # This enables or disables the button depending on if the input field has errors or not
                    submit.bind_enabled_from(
                        name_input, "error", backward=lambda x: not x and name_input.value
                    )

                    # Disable the button by default until validation is done.
                    submit.disable()

                    # Cancel out of dialog.
                    # ui.button("Cancel", on_click=dialog.close)

        # when the dialog.submit(...) is called, here's where the value comes out.
        game = 'TODO: Fix this'
        
        message(game)
        return game
