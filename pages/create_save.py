import elements.theme as theme
from classes.Enable import *
from handlers.savehandler import *
from nicegui import app,ui
import traceback

enable = Enable()

@ui.page('/createsave')
def create_save():
    # File path for game data
    user_config = app.storage.user.get("config", {})
    paths = user_config.get("Paths",{})
    root_path = paths.get("osrootpath", "Not Set")
    games_path = paths.get("gamespath", "Not Set")
    saves_path = paths.get("savespath", "Not Set")
    template_paths = paths.get("templatefilepath", "Not Set")
    selected_game = app.storage.user.get('selected_game', {})

    str_games_path = root_path + games_path



    new_save_dict = {'name': '','base_game': '', 'create_date':'', 
                     'date_last_save': '','description': '', 
                     'asset_customs': False,'actor_customs': False,
                     'event_customs': False, 'effect_customs': False,
                     'counters':{}, 'assets': {}, 'actors':[],
                     'current_events':{}, 'current_effects': {},
                     'current_turn': -1, 'log_file_path': ''
                     }

    async def create_save_json():
        matches_template = False
        save_name_result = {}
        create_save_result = False
        game_file_name = ''
        try:
            # Convert game name to file friendly format
            game_name_result = format_str_for_filename_super(selected_game['name'])
            if game_name_result['result']:
                game_file_name = game_name_result['string']

                # Make str_save_directory_path here
                str_save_directory_path = str_games_path + '\\' +  game_file_name +  saves_path

                save_name_result = format_str_for_filename_super(new_save_dict['name'])
                if save_name_result['result']:
                    # Check for duplicates
                    save_name_check = get_new_save_name(str_save_directory_path, new_save_dict['name'])

                    if "_Placeholder" in save_name_check['name']:
                        ui.notify(f"""Notice! An asset by the same name already exists. 
                                Could not save asset.""",
                                    type='warning',
                                    position='top',
                                    multi_line=True)

                    # Get the starting information from the game
                    new_save_dict['base_game'] = selected_game['name']
                    new_save_dict['counters'] = selected_game['counters']
                    new_save_dict['actors'] = selected_game['default_actors']
                    new_save_dict['current_turn'] = selected_game['start_turn']
                    try:
                        create_save_result = new_save_gui(selected_game['name'], new_save_dict)
                        if create_save_result['result']:
                            ui.notify("Save created! You can now use to the dashboard.",
                                    position='top',
                                    type='positive')
                            # Pull the newly created save out of the file and use that.
                            app.storage.user['selected_save'] = create_save_result['dict']
                            # refresh screen to see the change
                            ui.navigate.reload()
                            
                        else:
                            ui.notify(f"""Save file could not be created. Please check file permissions. 
                                Check the log file in folder where the asset would be created for more details.""",
                                    type='negative',
                                    position="top",)
                            raise Exception(f"""Save file could not be created. 
                                Check the log file in folder where the asset would be created for more details.""")
                    except Exception as e:
                            print(traceback.format_exc())
                            ui.notify("Error: Failed to save save file. Please ensure file paths in config.txt are correct and STAT has write permission to the folders.",
                                    position='top',
                                    type='negative',
                                    multi_line=True)
                # unable to format save name
                else:
                    ui.notify(f"""Warning: the new save file's name could not be converted into a file-friendly format!
                            Please try a different name.""",
                            position='top',
                            type='warning',
                            multi_line=True)
            # unable to format game name
            else:
                ui.notify(f"""Warning: the new game's name could not be converted into a file-friendly format!
                        How in the codebase did you manage THAT?""",
                        position='top',
                        type='warning',
                        multi_line=True)
            

        except FileNotFoundError as e:
            print(traceback.format_exc())
            ui.notify("Error: Could not save. STAT cound not find the file. Please check the file paths in config.txt are correct.",
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
            ui.notify("Error: Could not save. An unexpected error has occured. Please check application logs for more information.",
                      position='top',
                      type='negative',
                      multi_line=True)

    async def handle_create_save():
        await create_save_json()

    with theme.frame('Create New Save'):
        with ui.column().classes("flex content-center w-100"):
            with ui.column().classes('justify-center items-center w-full mt-4'):
                # Checking if a selected game is loaded.
                if not selected_game or 'name' not in selected_game:
                    with ui.row():
                        ui.icon('warning').classes('text-3xl')
                        ui.label('Warning: No selected game detected.').classes('text-2xl')
                    ui.label('Cannot create a save file with no game selected.')
                    ui.label('Please select a game from \'Select Games\' first.')
                    with ui.link(target = '/selectgames'):
                        ui.button('Find Game File')
                # Actually creating the save.
                else:
                    ui.label("All we need from you is the name of the save and a description.").classes('h-5')
                    ui.label("We'll handle the rest!")
                    ui.label("The form will clear itself after a successful save file creation, make sure to check selected_save in the bottom left corner!")
                    with ui.column().classes('items-start'):
                        name_input = ui.input(label='Save Name: ', placeholder='50 character limit',
                                        on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                        # allows user to clear the field
                        name_input.props('clearable')
                        name_input.bind_value(new_save_dict, 'name')
                        # This handles the validation of the field.
                        name_input.validation={"Too short!": enable.is_too_short} 
                        # Displays the characters.        
                        name_chars_left = ui.label()
                
                    # Description of Save    
                    with ui.row().classes('justify-center items-center w-full mt-4'):
                        with ui.column():
                            description = ui.input(label='Save Description', placeholder='500 character limit',
                                            on_change=lambda f: desc_chars_left.set_text(str(len(f.value)) + ' of 500 characters used.'))
                            description.props('clearable')
                            
                            description.bind_value(new_save_dict, 'description')
                            # this handles the validation of the field.
                            description.validation={"Too long!": lambda b: enable.is_too_long_variable(b, 500)}
                            with ui.row():
                                desc_chars_left = ui.label()

                    # Handle the rest behind the scenes

                    # Submit button.
                    with ui.row().classes('justify-center items-center w-full mt-4'):
                        # The button submits the dialog providing the text entered
                        submit = ui.button(
                            "Create Save",
                            icon='create',
                            on_click=handle_create_save,
                        )
                        # This enables or disables the button depending on if the input field has errors or not
                        submit.bind_enabled_from(
                            name_input, "error", backward=lambda x: not x and name_input.value
                        )

                        # Disable the button by default until validation is done.
                        submit.disable()
                        


            