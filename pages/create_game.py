import elements.theme as theme
from classes.Enable import *
from elements.new_counter_dialog import new_counter_dialog
from elements.new_string_dialog import new_string_dialog
from handlers.gamehandler import *
from elements.UserConfirm import *
from nicegui import app,ui
import traceback
from handlers.confighandler import config, config_path, load_config, create_default_config

enable = Enable()

@ui.page('/creategame')
async def create_game():
    # File path for game data
    user_config = app.storage.user.get("config", {})
    paths = user_config.get("Paths",{})
    root_path = paths.get("osrootpath", "Not Set")
    games_path = paths.get("gamespath", "Not Set")

    str_games_path = root_path + games_path

    new_game_dict = {'name': '','description':'', 'has_counters': False,
                'counters': {}, 'has_actors': False, 'default_actors':["Player"], 
                'has_assets': False, 'default_assets':[],
                'has_events': False, 'default_events':[],
                'has_effects': False, 'default_effects':[],
                'icon':'', 'has_turns':False,
                'turn_type':'', 'start_turn':0, 'image':''
                }

    # Render the counters.
    @ui.refreshable
    def render_all_counters(user_confirm, new_game_dict) -> ui.element:
        with ui.row().classes('gap-2') as counter_display_case:
            for counter, value in new_game_dict['counters'].items():
                with ui.row().classes('items-center gap-2'):
                    ui.label(f'{counter}:').classes('text-sm font-medium')
                    ui.label(str(value)).classes('text-sm')

                    # Add delete button
                    ui.button(icon='delete', color='red', 
                            on_click=lambda c=counter:  
                           user_confirm.show(f'Are you sure you want to delete {c}?', 
                                        lambda: delete_counter(new_game_dict, c))).props('flat dense')
        return counter_display_case

    # get the new Counter from New Counter Dialog
    async def add_counter():
        result = await new_counter_dialog() 
        if result:
            if 'counters' not in new_game_dict:
                new_game_dict['counters'] = {}
            new_game_dict['counters'][result[0]] = int(result[1])
            render_all_counters.refresh()
        else:
            ui.notify("""No counters added, dialog cancelled. If you want to add counters use the submit button.""",
                      type='warning',
                      position='top',
                      multi_line=True)
     
    # Delete a counter.
    def delete_counter(new_game_dict: dict, counter_name: str) -> ui.element:
        """Deletes the counter from the passed in game_dict's counter dictionary."""
        if counter_name in new_game_dict['counters']:
            del new_game_dict['counters'][counter_name]
            render_all_counters.refresh()


    # Render the actors.
    @ui.refreshable
    def render_all_actors(user_confirm, new_game_dict) -> ui.element:
        with ui.row().classes('gap-2') as actor_display_case:
            for value in new_game_dict.get('default_actors',[]):
                with ui.row().classes('items-center gap-2'):
                    ui.label(str(value)).classes('text-sm font-medium')

                    # Add delete button
                    ui.button(icon='delete', color='red', 
                        on_click=lambda v = value:
                        user_confirm.show(f'Are you sure you want to delete {v}?', 
                                    lambda: delete_actor(new_game_dict, v))
                                    ).props('flat dense')
        return actor_display_case

    # adding an actor
    async def add_actor():
        result = await new_string_dialog('Actor')
        if result:
            if 'default_actors' not in new_game_dict:
                new_game_dict['default_actors'] = []
            new_game_dict['default_actors'].append(result['name'])
            render_all_actors.refresh()
        else:
            ui.notify("""Warning: Dialog cancelled. No Actors added.""",
                      type='warning',
                      psoition='top',
                      multi_line=True)

    # Delete an actor.
    def delete_actor(new_game_dict: dict, actor_name: str) -> ui.element:
        """Deletes the counter from the passed in game_dict's actor list."""
        if actor_name in new_game_dict['default_actors']:
            target_index = new_game_dict['default_actors'].index(actor_name)
            del new_game_dict['default_actors'][target_index]
            render_all_actors.refresh()

    async def create_game_json():
        """Checks that the name hasn't been used for a game already. 
        Sends the name of the config file, the new_game_dict,
          and the game_name_result['file'] to new_game_gui in gamehandler."""
        matches_template = False
        game_name_result = {}
        create_game_result = False
        
        # Creating the game
        try:
            # Ensure the game matches the template
            matches_template = check_game_template_bool(new_game_dict)
            if matches_template['result']:
                # Check if a game with that name already exists
                new_game_name = new_game_dict['name']

                game_name_result = get_new_game_name(new_game_name, str_games_path)
                if not "_Placeholder" in game_name_result['name']:
                    try:
                        create_game_result = new_game_gui( new_game_dict, game_name_result['file'])
                        if create_game_result['result']:
                            app.storage.user['selected_game'] = create_game_result['dict']
                            ui.notify(f"""Success! You've created the game {new_game_dict['name']}!
                                    You can view it on the select games screen.""",
                                        multi_line = True,
                                        type='positive',
                                        position='top')
                            
                            ui.navigate.reload()
                            
                        else:
                            ui.notify(f"""File Write Failed: {create_game_result['string']} """,
                                        type='negative',
                                        position='top',
                                        multi_line = True,)
                    except Exception as e:
                        print(traceback.format_exc())
                        ui.notify(f"""Game file could not be created.
                                        Please check file permissions.
                                        {create_game_result['string']}""",
                                        type='negative',
                                        position='top',
                                        multi_line = True)
                else:
                    ui.notify(f"""Notice! A game of that name already exists. Please pick a new name.""",
                              type='warning',
                              position='top',
                              multi_line = True)
                
            # Template Mismatch
            else:
                ui.notify("""Error! The new game dictionary does not match the expected game template.
                          Please check the template jsons and try again.""", 
                          type='negative',
                          position="top",
                          multi_line = True,
                          )

        except FileNotFoundError as e:
            print(traceback.format_exc())
            ui.notify("Error: File not found. Unable to find location.",
                      position='top',
                      type='negative',
                      multi_line=True)

        except PermissionError as e:
            print(traceback.format_exc())
            ui.notify(f"""Error: STAT does not have permission to write there. 
                      Please verify the filepaths in config.tx and that STAT has permission to write there.""",
                      position='top',
                      type='negative',
                      multi_line=True)

        except Exception as e:
            print(traceback.format_exc())
            ui.notify(f"""Error: An unexpected error has occured. 
                      Please check the traceback for more information.""",
                      position='top',
                      type='negative',
                      multi_line=True)

    with theme.frame('Create a Game'):
        with ui.column().classes("full-flex content-center w-full md:w-1/2"):
            ui.label("Welcome to creating a game!")
            ui.label("""Upon successful completion the forms should empty themselves 
                    and you should see 'selected game' in the bottom left update with name of the new game.""")
            
            user_confirm = UserConfirm()
            
            # Name of the Game
            with ui.row().classes('items-center justify-start space-x-4'):
                with ui.column().classes('items-start'):
                    ui.label("Game Name: ").classes('font-bold')
                    name_input = ui.input(placeholder='50 character limit',
                                    on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                    # allows user to clear the field
                    name_input.props('clearable')
                    name_input.bind_value(new_game_dict, 'name')
                    # This handles the validation of the field.
                    name_input.validation={"Too short!": enable.is_too_short} 
                    # Displays the characters.        
                    name_chars_left = ui.label()

            # Description of Game    
            with ui.row().classes('items-center justify-start space-x-4'):
                with ui.column().classes('items-start'):
                    ui.label('Game Description:').classes('font-bold')
                    description = ui.textarea(placeholder='Type description here.',
                                    on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' characters used.'))
                    description.classes('hover:border-solid border-dotted hover:border-4 border-l-4 border-orange-500 rounded')
                    description.props('clearable')
                    description.bind_value(new_game_dict, 'description')
                    desc_chars_left = ui.label()
                
            # Creating counters
            with ui.row().classes('items-center justify-start space-x-4'):
                # Create counters
                    with ui.column().classes('items-start'):
                        ui.label('Do you want to add counters to your game?').classes('font-bold')
                        has_counters = ui.switch()
                        has_counters.bind_value(new_game_dict, 'has_counters')

                        new_counter_btn = ui.button(
                            "Add Counter",
                            icon="create",
                            on_click=add_counter
                        )
                        new_counter_btn.bind_visibility_from(has_counters, 'value')
                        ui.label("Counters added: ").bind_visibility_from(has_counters, 'value')
                        counter_display = render_all_counters(user_confirm, new_game_dict)
                        counter_display.bind_visibility_from(has_counters,'value')
             
            # Creating Actors
            with ui.row().classes('items-center justify-start space-x-4'):
                with ui.column().classes('items-start'):
                    ui.label('Do you want to add Actors now?').classes('font-bold')
                    ui.label('By default \"Player\" is added as an actor.')
                    has_actors = ui.switch()
                    has_actors.on('click', has_actors.set_value(has_actors.value))
                    has_actors.bind_value(new_game_dict, 'has_actors')

                    create_actors = ui.button(
                        'Add Actor', 
                        icon="create", 
                        on_click=add_actor
                    )
                    create_actors.bind_visibility_from(has_actors, 'value')
                    ui.label("Actors added: ").bind_visibility_from(has_actors, 'value')
                    actors_display = render_all_actors(user_confirm, new_game_dict)
                    actors_display.bind_visibility_from(has_actors,'value')

            
            # Creating Assets moved to its own form.

            # Creating Effects moved to its own form.
            

            # Initializing Turns
            with ui.row().classes('items-center justify-start space-x-4'):
                with ui.column():
                    ui.label("Does your game have turns or rounds?").classes('font-bold')
                    has_turns = ui.switch()
                    has_turns.on('click',has_turns.set_value(has_turns.value))
                    has_turns.bind_value(new_game_dict, 'has_turns')
                    # These should be invisible unless has_turns == True.
                    with ui.column().bind_visibility_from(has_turns,'value'):
                        ui.label("Do the turns increase or decrease as you play?")
                        turn_type = ui.radio({'Increasing':'Increasing', 'Decreasing':'Decreasing'}).props('inline left-label')
                        ui.label("What turn or round number does your game start on?")
                        turn_type.bind_value(
                            new_game_dict, 
                            'turn_type')
                        start_turn = ui.number("Enter a whole number.",
                                               on_change=lambda e: new_game_dict.__setitem__('start_turn', int(e.value) if e.value is not None else 0))
                        

            # Submit button.
            with ui.row():
                # The button submits the dialog providing the text entered
                submit = ui.button(
                    "Create Game",
                    icon='create',
                    on_click=lambda: create_game_json()
                )
                # This enables or disables the button depending on if the input field has errors or not
                submit.bind_enabled_from(
                    name_input, "error", backward=lambda x: not x and name_input.value
                )

                # Disable the button by default until validation is done.
                submit.disable()

