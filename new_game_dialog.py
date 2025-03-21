import theme
from message import message

from nicegui import ui

async def new_game_dialog():

    game = {'name': '', 'description':'', 
            'has_counters': False, 'counters': {},
            'has_actors': False, 'actor_default_path': '', 'default_actors':[],
            'has_assets': False, 'asset_default_path': '', 'default_assets':[],
            'has_events': False, 'event_default_path': '', 'default_events': [],
            'has_effects': False, 'effect_default_path': '', 'default_effects':[],
            'icon':'', 'save_files_path': '', 
            'has_turns': False, 'turn_type': '', 'start_turn': 0}
    
    with ui.dialog() as dialog, ui.card().classes():
        ui.label("Create a New Game").classes()
        with ui.card_section().classes():
            # get the name of the game.
            ui.label("Enter a name for the game. The name should be unique.")
            name_input = ui.input(label='Game Name', placeholder='50 character limit',
                            on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.')).props('clearable')
            # This handles the validation of the field.
            name_input.validation={'Input too long, limit is 50 characters.': lambda x: len(x) <= 50,
                                        'Input too short, you need at least five characters.': lambda y: len(y) >= 5} 
            # Binds to the field in the dictionary.             
            name_chars_left = ui.label()

            # input description for the game.
            ui.label('Enter a description for the new game:')
            description = ui.input(label='Game Description', placeholder='500 character limit',
                            on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.')).props('clearable')
            # this handles the validation of the field.
            description.validation={'Input too long, limit is 500 characters.': lambda z: len(z) <= 500}
            desc_chars_left = ui.label()

        with ui.card_actions().classes():
            # The button submits the dialog providing the text entered
            submit = ui.button(
                "Create Game",
                on_click=lambda:  dialog.submit(game),
            ).classes()
            # This enables or disables the button depending on if the input field has errors or not
            submit.bind_enabled_from(
                name_input, "error", backward=lambda x: not x and name_input.value
            )
            name_input.bind_value_from(game, 'name', name_input.value)
            description.bind_value_from(game, 'description', description.value)
            # Its disabled by default since the validation rules only run when the text changes
            submit.disable()

    # when the dialog.submit(...) is called, here's where the value comes out.
    game = await dialog
    print(game)
    message(game['description'])
    return game
