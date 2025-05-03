import elements.theme as theme
from classes.Enable import *
from handlers.savehandler import *
from nicegui import app,ui
import traceback

enable = Enable()

@ui.page('/createsave')
def create_save():
    # File path for game data
    config = app.storage.user.get("config", {})
    paths = config.get("Paths",{})
    game_paths = paths.get("gamespath", "Not Set")
    template_paths = paths.get("templatefilepath", "Not Set")
    save_paths = paths.get("savespath", "Not Set")
    datapack_paths = paths.get("datapackspath", "Not Set")
    selected_game = app.storage.user.get('selected_game', {})

    new_save_dict = {'name': '','base_game': '', 'create_date':'', 
                     'date_last_save': '','description': '', 
                     'asset_customs': False, 'asset_customs_path':'',
                     'actor_customs': False, 'actor_customs_path':'',
                     'event_customs': False, 'event_customs_path':'',
                     'effect_customs': False, 'effect_customs_path':'',
                     'counters':{}, 'assets': {}, 'actors':[],
                     'current_events':{}, 'current_effects': {},
                     'current_turn': -1, 'log_file_path': ''
                     }

    async def create_save_json():
        matches_template = False;
        save_name = {}
        create_save_result = False;
    
        try:
            # Ensure the game matches the template
            matches_template = check_template_bool(new_save_dict, template_paths)
            if matches_template:
                # Check if a game with that name already exists
                new_save_name = new_save_dict['name']

                save_name = get_new_save_name(new_save_name, save_paths)
                if "_Placeholder" in save_name['name']:
                    with ui.dialog() as name_existed, ui.card():
                        ui.label("Notice!").classes('h3')
                        ui.label("A game by the same name already exists.")
                        ui.label(f"Your game will be saved as: {save_name['name']}")
                        ui.button('Close', on_click=name_existed.close)
            
                # Get the starting information from the game
                new_save_dict['base_game'] = selected_game['name']
                new_save_dict['counters'] = selected_game['counters']
                new_save_dict['actors'] = selected_game['default_actors']
                new_save_dict['current_turn'] = selected_game['start_turn']

                try:
                    create_save_result = new_save_gui(datapack_paths, save_paths, new_save_dict, save_name['file'])
                    if create_save_result['result']:
                        with ui.dialog() as game_created, ui.card():
                            ui.label("Success!").classes('h3')
                            ui.label("Game file created successfully.")
                            ui.label("You will now be taken to the screen for your game's details.")
                            ui.button('Close', on_click=game_created.close)
                        # Navigate to the game view
                        # Make sure to get the dictionary back from create_game_result as it handles multiple fields
                        app.storage.user['selected_save'] = create_save_result['dict']
                        
                    else:
                        ui.notify("Game file could not be created. Please check file permissions.",
                                  type='negative',
                                  position="top",)
                        raise Exception("Game file could not be created. Please check file permissions.")
                except Exception as e:
                        print(traceback.format_exc())
                        with ui.dialog() as save_error, ui.card():
                            ui.label("Error!").classes('h3')
                            ui.label("Failed to save the game file.")
                            ui.label(f"Details: {str(e)}")
                            ui.label("Please ensure the application has write permissions to the target directory.")
                            ui.button('Close', on_click=save_error.close)
            else:
                # Template mismatch
                with ui.dialog() as template_error, ui.card():
                    ui.label("Error!").classes('h3')
                    ui.label("The new game dictionary does not match the expected game template.")
                    ui.label("Unable to save the game.")
                    ui.button('Close', on_click=template_error.close)

        except FileNotFoundError as e:
            print(traceback.format_exc())
            with ui.dialog() as file_error, ui.card():
                ui.label("Error!").classes('h3')
                ui.label("File not found.")
                ui.label(f"Details: {str(e)}")
                ui.label("Please ensure the specified file paths are correct.")
                ui.button('Close', on_click=file_error.close)
        except PermissionError as e:
            print(traceback.format_exc())
            with ui.dialog() as permission_error, ui.card():
                ui.label("Error!").classes('h3')
                ui.label("Permission denied.")
                ui.label(f"Details: {str(e)}")
                ui.label("Please ensure the application has the necessary permissions.")
                ui.button('Close', on_click=permission_error.close)
        except Exception as e:
            print(traceback.format_exc())
            with ui.dialog() as general_error, ui.card():
                ui.label("Error!").classes('h3')
                ui.label("An unexpected error occurred.")
                ui.label(f"Details: {str(e)}")
                ui.label("Please check the application logs for more information.")
                ui.button('Close', on_click=general_error.close)

    async def handle_create_save():
        await create_save_json()
        ui.navigate.to(f"/loadeddash/")

    with theme.frame('Create New Save'):
        with ui.column().classes("flex content-center w-100"):
        # Name of the Save
            with ui.column().classes('justify-center items-center w-full mt-4'):
                if not selected_game or 'name' not in selected_game:
                    with ui.row():
                        ui.icon('warning').classes('text-3xl')
                        ui.label('Warning: No selected game detected.').classes('text-2xl')
                    ui.label('Cannot create a save file with no game selected.')
                    ui.label('Please select a game from \'Select Games\' first.')
                    with ui.link(target = '/selectgames'):
                        ui.button('Find Game File')
                else:
                    ui.label("All we need from you is the name of the save and a description. ").classes('h-5')
                    ui.label("We'll handle the rest!")
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
                        


            