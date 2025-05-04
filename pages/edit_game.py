from nicegui import app, ui
import elements.theme as theme
from classes.Enable import *
from elements.new_counter_dialog import new_counter_dialog

enable = Enable()

@ui.page('/editgame')
async def edit_game():
    with theme.frame('Edit Game'):
        selected_game = app.storage.user.get("selected_game", {})

        with ui.column().classes("flex content-center"):
            # If no selected_game, open up prompt to select one
            if not selected_game or 'name' not in selected_game:
                with ui.row():
                    ui.icon('warning').classes('text-3xl')
                    ui.label('Warning: No selected game detected.').classes('text-2xl')
                ui.label('Cannot edit a game with no game selected.')
                ui.label('Please select a game from \'Select Games\'.')
                with ui.link(target = '/selectgames'):
                    ui.button('Find Game File')
            else:
                # Name
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        name_input = ui.input(label='Game Name: ', placeholder='50 character limit',
                                        on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                        # allows user to clear the field
                        name_input.props('clearable')
                        name_input.bind_value(selected_game, 'name')
                        # This handles the validation of the field.
                        name_input.validation={"Too short!": enable.is_too_short} 
                        # Displays the characters.        
                        name_chars_left = ui.label()

                # Description
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        description = ui.textarea(label='Game Description', placeholder='Type description here.',
                                        on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' characters used.'))
                        description.props('clearable')
                        description.bind_value(selected_game, 'description')
                        # this handles the validation of the field.
                        desc_chars_left = ui.label()

                # Counters
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        ui.label('Select a counter to update:')
                        counters = selected_game['counters']
                        counter_card_container = ui.row().classes("full flex items-center")
                        with counter_card_container:
                            for counter in counters:
                                with ui.card():
                                    with ui.card_section():
                                        with ui.row():
                                            ui.label("Name: ")
                                            ui.label(counter)
                                        with ui.row():
                                            ui.label("Default Value:")
                                            ui.label().bind_text_from(counters, counter)
                                    with ui.card_actions().classes("w-full justify-end"):
                                        ui.button('Select Counter', on_click=lambda: ui.notify('This will launch a counter dialog in the future'))
            
                # Actors
                with ui.row().classes('items-center justify-start space-x-4'):
                    with ui.column().classes('items-start'):
                        # Has Actors
                            ui.label("The Actors")
                            has_actors_switch = ui.switch()
                            has_actors_switch.bind_value(selected_game, 'has_actors')
                            default_actors = selected_game['default_actors']
                            for actor in default_actors:
                                with ui.list().props('separator'):
                                    ui.item(actor)
                                    # TODO: this should tell them to go to Edit Asset to edit the asset
                                    ui.icon('Edit')
                                    # TODO: this should pop up a 'are you sure you want to delete?
                                    ui.icon('Delete')
                            edit_actors = ui.button('Edit Actors', 
                                                    on_click=lambda: ui.notify('You clicked edit actors! In the future this will pop up a dialog box.'))
                            edit_actors.bind_visibility(has_actors_switch, 'value')


                ui.button('Print Game', on_click=lambda: ui.notify(selected_game, type='positive', position='top'))
