from nicegui import ui
import elements.theme as theme
from elements.message import message
from classes.Enable import *
from new_counter_dialog import new_counter_dialog
from classes.MyGame import MyGame
from elements.message import message
from typing import Annotated, Awaitable

enable = Enable()

@ui.page('/editgame')
async def edit_game():
    with theme.frame('Edit a Game'):
        loaded_game = {
            'name':'Test',
            'description':'This is the test game for basic STAT testing',
            'has_counters':True,
            'counters':{'Gold': 10, "Silver": 25, "Copper": 100, "Health": 100, "1st Level Spell Slot": 3},
            'has_actors':False,
            'actor_default_path':"",
            'default_actors':[],
            'has_assets':True,
            'asset_default_path':"statassets\\datapacks\\test\\default\\assets",
            'default_assets':["Barracks","Spell Strike","Monkey"],
            'has_events':False,
            'event_default_path':"",
            'default_events':[],
            'has_effects': False,
            'effect_default_path':"",
            'default_effects':[],
            'icon':"",
            'save_files_path':"statassets\\saves\\test",
            'has_turns': True,
            'turn_type': "Increasing",
            'start_turn': 0
        }
        message("Edit the details of the game:")
        # edit loaded game or new game?
        # give user list of games to pick to edit.
        # when user selects game, fetch from JSON file and load in.
        # update screen to show pages.

        
        with ui.column().props('flex'):
            # Name of the Game
            with ui.row():
                    # get the name of the game.
                ui.label("Enter a name for the game. The name should be unique.")
                game_name_edit = ui.input(label='Game Name', placeholder='Required field',
                                        on_change=lambda : name_chars_left.set_text(str(len(game_name_edit.value)) + ' of 50 characters used.'))
                game_name_edit.props('clearable')
                game_name_edit.bind_value(loaded_game, 'name')
                print(game_name_edit.value)
                # allows user to clear the field
                # This handles the validation of the field.
                # name_input.validation={"Too short!": lambda name_value: enable.is_too_short_variable(name_value,1)} 
                # Displays the characters.        
                name_chars_left = ui.label()
            
            # Description of the Game
            with ui.row():
                # input description for the game.
                ui.label('Enter a description for the new game:')
                description = ui.textarea(label='Game Description', placeholder='500 character limit',
                                on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.'))
                description.props('clearable')
                description.bind_value(loaded_game, 'description')
                # this handles the validation of the field.
                description.validation={"Too long!": lambda descript_value: enable.is_too_long_variable(descript_value, 500)}
                desc_chars_left = ui.label()

            # Counter cards
            with ui.row():
                ui.label('Select a counter to update:')
                counters = loaded_game['counters']
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
            
            # Has Actors
            with ui.row():
                ui.label("Are there Actors?")
                has_actors_switch = ui.switch()
                game_name_edit.bind_value(loaded_game, 'has_actors')
                with ui.column():
                    default_actors = loaded_game['default_actors']
                    for actor in default_actors:
                        with ui.list().props('dense separator'):
                            ui.item(actor)
                            # TODO: this should pop up an 'edit actor' dialog box.
                            ui.icon('Edit')
                            # TODO: this should pop up a 'are you sure you want to delete?
                            ui.icon('Delete')
                with ui.column():
                    edit_actors = ui.button('Edit Actors', 
                                            on_click=lambda: ui.notify('You clicked edit actors! In the future this will pop up a dialog box.'))
                    edit_actors.bind_visibility(has_actors_switch, 'value')


        ui.button('Print Game', on_click=lambda: ui.notify(loaded_game))
