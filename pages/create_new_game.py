import elements.theme as theme
from classes.Enable import *
from elements.new_counter_dialog import new_counter_dialog
from elements.new_actor_dialog import new_actor_dialog
from handlers.gamehandler import *
from nicegui import app,ui
import traceback

enable = Enable()

@ui.page('/creategame')
async def create_game():
    # File path for game data
    config = app.storage.user.get("config", {})
    paths = config.get("Paths",{})
    root_path = paths.get("osrootpath", "Not Set")
    games_path = paths.get("gamespath", "Not Set")
    template_paths = paths.get("templatefilepath", "Not Set")

    str_games_path = root_path + games_path

    new_game_dict = {'name': '','description':'', 'has_counters': False,
                'counters': {}, 'has_actors': False, 'default_actors':["Player"], 
                'has_assets': False, 'default_assets':[],
                'has_events': False, 'default_events':[],
                'has_effects': False, 'default_effects':[],
                'icon':'', 'has_turns':False,
                'turn_type':'', 'start_turn':0
                }

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
        

    async def add_actor():
        result = await new_actor_dialog()
        if result:
            if 'actors' not in new_game_dict:
                new_game_dict['actors'] = []
            new_game_dict['actors'].append(result['name'])
            render_all_actors.refresh()
        else:
            ui.notify("""Warning: Dialog cancelled. No Actors added.""",
                      type='warning',
                      psoition='top',
                      multi_line=True)
    



    async def create_game_json():
        matches_template = False
        game_name_result = {}
        create_game_result = False
        # Creating the game
        try:
            # Ensure the game matches the template
            matches_template = check_template_bool(new_game_dict, template_paths)
            if matches_template:
                # Check if a game with that name already exists
                new_game_name = new_game_dict['name']

                game_name_result = get_new_game_name(new_game_name, str_games_path)
                if not "_Placeholder" in game_name_result['name']:
                    try:
                        create_game_result = new_game_gui('config.txt', new_game_dict, game_name_result['file'])
                        if create_game_result['result']:
                            app.storage.user['selected_game'] = create_game_result['dict']
                            ui.notify(f"""Success! You've created the game {new_game_dict['name']}!
                                    You can view it on the select games screen.""",
                                        multi_line = True,
                                        type='positive',
                                        position='top')
                            
                            ui.navigate.reload()
                            
                        else:
                            ui.notify(f"""Game file could not be created. Please check file permissions.
                                        More information can be found in the debug log in the folder where STAT was trying to create the game.""",
                                        type='negative',
                                        position='top',
                                        multi_line = True,)
                    except Exception as e:
                            ui.notify(f"""Game file could not be created.
                                        Please check file permissions.
                                        More information can be found in the debug log in the folder where STAT was trying to create the game.""",
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
            print(traceback.format_exc())
            with ui.dialog() as general_error, ui.card():
                ui.label("Error!").classes('h3')
                ui.label("An unexpected error occurred.")
                ui.label(f"Details: {str(e)}")
                ui.label("Please check the application logs for more information.")
                ui.button('Close', on_click=general_error.close)
            general_error.open


    with theme.frame('Create a Game'):
        with ui.column().classes("full-flex content-center w-full md:w-1/2"):
            ui.label("Welcome to creating a game!")
            ui.label("""Upon successful completion the forms should empty themselves 
                    and you should see 'selected game' in the bottom left update with name of the new game.""")
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
                        # TODO: give user way to view counters added
                        ui.label("Counters added: ").bind_visibility_from(has_counters, 'value')
                        counter_display = render_all_counters(new_game_dict)
             
            # Creating Actors
            with ui.row().classes('items-center justify-start space-x-4'):
                with ui.column().classes('items-start'):
                    ui.label('Do you want to add Actors now?').classes('font-bold')
                    ui.label('By default \"Player\" is added as an actor.')
                    has_actors = ui.switch()
                    has_actors.on('click', has_actors.set_value(has_actors.value))
                    has_actors.bind_value(new_game_dict, 'has_actors')
                    # The button will pull up a different dialog box for creating an event
                    create_actors = ui.button('Create Actors',
                                            icon="create",
                                            on_click=add_actor)
                    create_actors.bind_visibility_from(has_actors, 'value')
                    ui.label("Actors added: ").bind_visibility_from(has_actors, 'value')
                    actors_display = render_all_actors(new_game_dict)

            # Creating Assets
            with ui.row().classes('items-center justify-start space-x-4'):
                with ui.column().classes('items-start'):
                    ui.label('Assets').classes('font-bold')

            # Creating Effects
            with ui.row().classes('items-center justify-start space-x-4'):
                with ui.column().classes('items-start'):
                    ui.label('Effects').classes('font-bold')
                    ui.label('You will add these later.')

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
                        start_turn = ui.number("Enter a whole number.")
                        turn_type.bind_value(
                            new_game_dict, 
                            'turn_type')
                        start_turn.bind_value(new_game_dict, 'start_turn')

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

# Render the counters.
@ui.refreshable
def render_all_counters(new_game_dict) -> ui.element:
    with ui.row().classes('gap-2') as counter_display_case:
        for counter, value in new_game_dict['counters'].items():
            with ui.row().classes('items-center gap-2'):
                ui.label(f'{counter}:').classes('text-sm font-medium')
                ui.label(str(value)).classes('text-sm')

                 # Add delete button
                ui.button(icon='delete', color='red', on_click=lambda c=counter: delete_counter(new_game_dict, c)).props('flat dense')
    return counter_display_case

# Render the actors.
@ui.refreshable
def render_all_actors(new_game_dict: dict) -> ui.element:
    with ui.row().classes('gap-2') as actor_display_case:
        for value in new_game_dict['default_actors']:
                ui.label(value).classes('text-sm font-medium')
    return actor_display_case

async def confirm_delete():
    try:
        with ui.dialog("Are you sure you want to delete?") as dialog:
            ui.label("Warning!").classes('h3')
            ui.label("Are you sure you want to delete this?")
            submit = ui.button(
                        "Create Counter",
                        on_click=lambda: dialog.submit()
                    )
            ui.button("Cancel", on_click=lambda: dialog.submit(None))

        # gracefully handling cancelling
        result = await dialog
        if result is None:
            print("Dialog was cancelled.")
            return None  
        return result

    except Exception:
        print(traceback.format_exc())
        return None

# Delete a counter.
def delete_counter(new_game_dict: dict, counter_name: str) -> ui.element:
    if counter_name in new_game_dict['counters']:
        del new_game_dict['counters'][counter_name]
        render_all_counters.refresh()