import elements.theme as theme
from nicegui import app, ui
from handlers.gamehandler import *
from elements.select_game_dialog import prompt_select_game
from classes.Enable import *

enable = Enable()

@ui.page('/viewgame/{game_name}')
async def game_detail():
    with theme.frame(f'Game Details'):
        edited_game = {}
        selected_game = app.storage.user.get("selected_game", {})
        edited_game = selected_game

        with ui.column().classes("flex content-center w-100"):
            with ui.row():
                with ui.link(target='/selectgames'):
                    btn_select = ui.button('Select Game')  
                
                with ui.link(target='/createasset'):
                    btn_create_asset = ui.button('Create Asset')
                    btn_create_asset.bind_enabled_from(bool(selected_game))
                
                with ui.link(target='/createeffect'):
                    btn_create_event = ui.button('Create Effect')
                    btn_create_event.bind_enabled_from(bool(selected_game))

            # If no game is selected, prompt the user to select one
            if not selected_game or 'name' not in selected_game:
                with ui.row():
                    ui.icon('warning').classes('text-3xl')
                    ui.label('Warning: No selected game detected.').classes('text-2xl')
                ui.label('Cannot create asset with no game selected.')
                ui.label('Please select a game from \'Select Games\'.')
                with ui.link(target = '/selectgames'):
                    ui.button('Find Game File')
            else:
                # Toggle for editing or not
                with ui.row().classes('items-center justify-start space-x-4'):
                    toggle_edit = ui.switch('Do you want to edit?').props('color="green"')
                
                    # IMAGE
                    with ui.column().classes('items-start'):
                        # DISPLAY
                        game_image = ui.image(f'{selected_game['image_file_path']}')
                        with ui.button("Reload Image", on_click=game_image.force_reload):
                            ui.tooltip("This attempts to reload the associated image.")
                        ui.label("Image file path").classes('font-bold')
                        lbl_image_path = ui.label(f'{selected_game['image_file_path']}')

                        # EDIT
                        # Call the dialog to get new file path
                        btn_find_image = ui.button("Find New Image").on_click(lambda: choose_file)
                        btn_find_image.bind_visibility_from(toggle_edit, 'value')
                        # display new file path
                        lbl_new_image_path = ui.label(f'{edited_game['image_file_path']}').classes('font-bold')
                        lbl_new_image_path.bind_visibility_from(toggle_edit, 'value')
                        # display the new image
                        new_image = ui.image(f'{edited_game['image_file_path']}')
                        new_image.bind_visibility_from(toggle_edit, 'value')
                        # reload the new image
                        btn_reload_new = ui.button("Reload New",on_click=new_image.force_reload)
                        btn_reload_new.bind_visibility_from(toggle_edit, 'value')

                    # ICON
                    with ui.column().classes('items-start'):
                        game_icon = ui.image(f'{selected_game['icon']}')
                        ui.button("Reload Icon", on_click=game_icon.force_reload)
                            

                # Section for rest of the data
                with ui.row().classes('items-center justify-start space-x-4'):
                    # NAME
                    with ui.column().classes('items-start'):
                        # DISPLAY section
                        lbl_game_name = ui.label("Current Name :").classes('font-bold')
                        game_name = ui.label(f"{selected_game['name']}")
                        lbl_game_name.bind_visibility_from(toggle_edit, 
                                                            'value', 
                                                            backward=lambda toggle_edit: not toggle_edit)
                        game_name.bind_visibility_from(toggle_edit, 
                                                        'value', 
                                                        backward=lambda toggle_edit: not toggle_edit)
                        # EDIT section
                        lbl_name_edit = ui.label('New Name: ').classes('font-bold')
                        lbl_name_edit.bind_visibility_from(toggle_edit, 'value')
                        name_edit = ui.input(placeholder=f'{selected_game['name']}',
                                                    on_change=lambda e: game_name.set_text(e.value))
                        name_edit.props('clearable')
                        name_edit.bind_value(edited_game, 'name')
                        name_edit.validation={"Too short!": enable.is_too_short} 
                        name_edit.bind_visibility_from(toggle_edit, 'value')

                    # DESCRIPTION
                    with ui.column().classes('items-start'):
                        # DISPLAY section
                        lbl_descript = ui.label("Description: ").classes('font-bold')
                        lbl_description = ui.label(f"{selected_game['description']}").classes('break-normal')
                        lbl_description.bind_visibility_from(toggle_edit, 
                                                                'value', 
                                                                backward=lambda toggle_edit: not toggle_edit)
                            
                        # EDIT section
                        descript_edit=ui.textarea(placeholder=f"{selected_game['description']}")
                        descript_edit.props('clearable')
                        descript_edit.bind_value(edited_game, 'description')
                        descript_edit.bind_visibility_from(toggle_edit, 'value')
                
                    # Counters in editable format
                    with ui.column().classes('items-start'):
                        lbl_counters = ui.label("Default Counters:").classes('font-bold')
                # View lists of actors of the selected game
                    # Show the filepath

                # View list of assets of the selected game
                    # Split lists into default assets and custom assets
                    # TODO: do custom assets AFTER file layout rework
                    # show the filepath

                # view list of effects of the selected game

                # Show the icon path

                # Saves_File_Path
                    # Show the path
                    # Warn user they will need to manually move saves to new location

                # TURNS
                    # Default turn
                    # Turn Type
                
                # Image File Path

                # Submit button
                
    async def choose_file() -> str:
        files = await app.native.main_window.create_file_dialog(allow_multiple=True)
        for file in files:
            edited_game['image'] = file