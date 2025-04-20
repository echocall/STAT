import elements.theme as theme
from classes.Enable import Enable
from nicegui import app, ui
from elements.target_counter_dialog import target_counter_dialog
from elements.select_game_dialog import prompt_select_game


# creating our buddy.
enable = Enable()

@ui.page('/createeffect')
async def create_effect():
    selected_game = app.storage.user.get("selected_game", {})

    new_effect = {'name':'', 'targets':'',
                   'sources':'', 'turn_duration':0,
                   'counters_affected':{}, 'source_game':''}
    
    affects_counters_bln = False

    # get the new Counter from New Counter Dialog
    async def add_counter():
        result = await target_counter_dialog() 
        if 'counters_affected' not in new_effect:
            new_effect['counters_affected'] = {}
        new_effect['counters_affected'][result[0]] = result[1]

    with theme.frame('Create Effect'):
        ui.label("Create a new Effect").classes('h3')
        if not selected_game or 'name' not in selected_game:
            with ui.row():
                ui.icon('warning').classes('text-3xl')
                ui.label('Warning: No selected game detected.').classes('text-2xl')
            ui.label('Cannot create asset with no game selected.')
            ui.label('Please select a game from \'Select Games\'.')
            with ui.link(target = '/selectgames'):
                ui.button('Find Game File')
        else:
            # Get name of Effect
            with ui.card_section().classes('w-80 items-stretch'):
                name_input = ui.input("Name of the effect?",
                                on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                name_input.bind_value(new_effect, 'name')
                # allows user to clear the field
                name_input.props('clearable')
                name_input.validation={"Must have a value": enable.not_null} 
                # Displays the characters.        
                name_chars_left = ui.label()

            # Effect Source
            with ui.card_section().classes('w-80 items-stretch'):
                ui.label("Acceptable source types for the effect?")
                effect_sources = ui.radio({1: 'Assets', 2: 'Actors', 3:'Other', 5: 'All'}, value=1).props('inline')
                effect_sources.bind_value(new_effect,'sources')

            # Get Source Game Name
            with ui.card_section().classes('w-80 items-stretch'):
                source_game_name = ui.input("Source Game?")
                source_game_name.bind_value(new_effect, 'name')
                # allows user to clear the field
                source_game_name.props('clearable')
                source_game_name.validation={"Must have a value": enable.not_null} 

            # Get Targets of the Effect
            with ui.card_section().classes('w-80 items-stretch'):
                ui.label("Acceptable target types for the effect?")
                effect_targets = ui.radio({1: 'Assets', 2: 'Actors', 3: 'Counters', 4:'Other', 5: 'All'}, value=1).props('inline')
                effect_targets.bind_value(new_effect,'targets')

            # Get Turn Duration Count
            with ui.card_section().classes('w-80 items-stretch'):
                turn_duration = ui.number(label="Turn duration? Leave 0 if none, -1 if infinity.", value=0, min=-1, precision=-1)
                turn_duration.bind_value(new_effect,'turn_duration')

            # Get Counters Affected
            with ui.card_section().classes('w-80 items-stretch'):
                affects_counters = ui.switch()
                affects_counters.bind_value(affects_counters_bln)

                new_counter = ui.button(
                    "Add Counter",
                    icon="create",
                    on_click=add_counter
                )
                new_counter.bind_visibility_from(affects_counters, 'value')

            btn_show_counters = ui.button()

            # Submitting the form.
            with ui.card_actions():
                submit = ui.button(
                    "Create Effect",
                    on_click=lambda: create_effect.submit(new_effect)
                )
                
                # This enables or disables the button depending on if the input field has errors or not
                submit.bind_enabled_from(
                    name_input, "error", backward=lambda x: not x and name_input.value
                )
    
