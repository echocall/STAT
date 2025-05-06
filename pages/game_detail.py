import elements.theme as theme
from nicegui import app, ui
from handlers.gamehandler import *
from classes.Enable import *
from elements.UserConfirm import *
from elements.new_string_dialog import new_string_dialog
from elements.new_counter_dialog import new_counter_dialog
import traceback

enable = Enable()

@ui.page('/viewgame/')
async def content() -> None:
   # Render the counters.
    @ui.refreshable
    def render_all_counters(user_confirm, edited_game) -> ui.element:
        """Show the user all the counters associated with the game_dict."""
        with ui.row().classes('gap-2') as counter_display_case:
            for counter, value in edited_game['counters'].items():
                with ui.row().classes('items-center gap-2'):
                    ui.label(f'{counter}:').classes('text-sm')
                    ui.label(str(value)).classes('')

                    # Add delete button
                    ui.button(icon='delete', color='red', 
                            on_click=lambda c=counter:  
                           user_confirm.show(f'Are you sure you want to delete {c}?', 
                                        lambda: delete_counter(edited_game, c))).props('flat dense')
        return counter_display_case

    # get the new Counter from New Counter Dialog
    async def add_counter():
        """Add a new counter to the game_dict's default counters."""
        result = await new_counter_dialog() 
        if result:
            if 'counters' not in edited_game:
                edited_game['counters'] = {}
            edited_game['counters'][result[0]] = int(result[1])
            render_all_counters.refresh()
        else:
            ui.notify("""No counters added, dialog cancelled. If you want to add counters use the submit button.""",
                      type='warning',
                      position='top',
                      multi_line=True)
     
    # Delete a counter.
    def delete_counter(edited_game: dict, counter_name: str) -> ui.element:
        """Deletes the counter from the passed in game_dict's counter dictionary."""
        if counter_name in edited_game['counters']:
            del edited_game['counters'][counter_name]
            render_all_counters.refresh()

    # Render the actors.
    @ui.refreshable
    def render_all_actors(user_confirm, edited_game) -> ui.element:
        """Display all the actors in a game's dict and allow user to delete them."""
        with ui.row().classes('gap-2') as actor_display_case:
            for value in edited_game.get('default_actors',[]):
                with ui.row().classes('items-center gap-2'):
                    ui.label(str(value)).classes('text-sm')

                    # Add delete button
                    ui.button(icon='delete', color='red', 
                        on_click=lambda v = value:
                        user_confirm.show(f'Are you sure you want to delete {v}?', 
                                    lambda: delete_actor(edited_game, v))
                                    ).props('flat dense')
        return actor_display_case

    # adding an actor
    async def add_actor():
        """Add an actor to the actor's list of the game_dict referenced on the page."""
        result = await new_string_dialog('Actor')
        if result:
            if 'default_actors' not in edited_game:
                edited_game['default_actors'] = []
            edited_game['default_actors'].append(result['name'])
            render_all_actors.refresh()
        else:
            ui.notify("""Warning: Dialog cancelled. No Actors added.""",
                      type='warning',
                      psoition='top',
                      multi_line=True)

    # Delete an actor.
    def delete_actor(edited_game: dict, actor_name: str) -> ui.element:
        """Deletes the counter from the passed in game_dict's actor list."""
        if actor_name in edited_game['default_actors']:
            target_index = edited_game['default_actors'].index(actor_name)
            del edited_game['default_actors'][target_index]
            render_all_actors.refresh()

    def update_game_wrapper(game_dict):
        """This exists to allow us to not have to worry about the 
        function getting called on page load."""
        update_result = update_game(game_dict)
        
        if update_result['result']:
            ui.notify("Congrats! You've successfully updated the game.",
                      position='top',
                      type='positive',
                      multi_line=True)
            app.storage.user['selected_game'] = edited_game
        else:
            ui.notify("Error: Updating the game has failed. Please check paths in config.txt.",
                      position='top',
                      type='negative',
                      multi_line=True)

    def delete_game_directory_wrapper(game_directory_path):
        result = delete_all(game_directory_path)
        if result:
            ui.notify("Delete success! Go to select_games to see.",
                      position='top',
                      type='negative')
            app.storage.user['selected_game'] = {}
        else:
            ui.notify("Error: Could not delete folder and its contents. Please check paths in config.txt",
                      position='top',
                      type='negative')
                   
    with theme.frame(f'Game Details'):
        edited_game = {}
        selected_game = app.storage.user.get("selected_game", {})
        edited_game = selected_game
        
        user_config = app.storage.user.get("config", {})
        paths = user_config.get("Paths",{})
        root_path = paths.get("osrootpath", "Not Set")
        games_path = paths.get("gamespath", "Not Set")

        format_result = format_str_for_filename_super(selected_game['name'])
        if format_result['result']:
            game_name = format_result['string']
            str_directory_path = root_path + games_path + '//' + game_name
        else:
            ui.notify("Error: Could not format name for building directory path!",
                      position='top',
                      type='negative',
                      multi_line=True)

        user_confirm = UserConfirm()

        with ui.column().classes():
            # Buttons
            with ui.row():
                with ui.link(target='/createasset'):
                    btn_create_asset = ui.button('Create Asset')
                    btn_create_asset.bind_enabled_from(bool(selected_game))
                
                with ui.link(target='/createeffect'):
                    btn_create_event = ui.button('Create Effect')
                    btn_create_event.bind_enabled_from(bool(selected_game))
                
                # TODO: Implement functionality, tooltips, and user confirm
                btn_delete = ui.button('Delete Game Directory', color='red',
                                        on_click=lambda: user_confirm.show(f"""Are you sure you want to delete the game and its files? 
                                                                             This will delete all files associated with the game and the game itself.""", 
                                        lambda: delete_game_directory_wrapper(str_directory_path)))
                with btn_delete:
                    ui.tooltip("This will delete the game folder and all of its contents. You can recover the files from your recycle bin.").classes('bg-red-700 text-white')
                
            # No game selected
            if not selected_game or 'name' not in selected_game:
                with ui.row():
                    ui.icon('warning').classes('text-3xl')
                    ui.label('Warning: No selected game detected.').classes('text-center text-2xl')
                ui.label('Cannot view the details for a game with no game selected.').classes('text-center')
                ui.label('Please select a game from \'View Games\'.').classes('text-center')
                ui.label('Then return here to view the save files.').classes('text-center')
                with ui.link(target = '/selectgames'):
                    ui.button('Find Game File')
            else:
                # Toggle for editing or not
                with ui.row().classes():
                    with ui.column().classes():
                        toggle_edit = ui.switch('Do you want to edit?')
                        toggle_edit.classes('text-base font-bold text-center')
                        toggle_edit.props('color="green"')
                
                # ICON
                with ui.row().classes():
                    with ui.column().classes():
                        if selected_game['icon']:
                            game_icon = ui.image(f'{selected_game['icon']}')
                            ui.label("Current Icon").classes('text-base font-bold text-center')
                            ui.button("Reload Icon", on_click=game_icon.force_reload)
                        else:
                            ui.label("No Icon to display").classes('text-sm text-center')
                    # TODO: Display option to change the Icon's path.

                    async def choose_icon():
                        icon_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
                        for file in icon_files:
                            asset_icon = file
                        edited_game['icon'] = asset_icon
                    
                    pick_icon = ui.button('Choose file', on_click=choose_icon)
                    pick_icon.bind_visibility_from(toggle_edit, 'value')

                # Section for rest of the data
                # with ui.row().classes():
                    # NAME
                with ui.row().classes():
                    with ui.column().classes():
                        # DISPLAY section
                        lbl_game_name = ui.label("Name :").classes('text-base font-bold text-center')
                        game_name = ui.label(f"{selected_game['name']}").classes('text-base font-bold text-center')
                        lbl_game_name.bind_visibility_from(toggle_edit, 
                                                            'value', 
                                                            backward=lambda toggle_edit: not toggle_edit)
                        game_name.bind_visibility_from(toggle_edit, 
                                                        'value', 
                                                        backward=lambda toggle_edit: not toggle_edit)
                        # EDIT section
                        lbl_name_edit = ui.label('Due to the time-constraints please create a new game if you want to change the name.').classes('text-base font-bold break-after-all text-center')

                        # lbl_name_edit.bind_visibility_from(toggle_edit, 'value')
                        # name_edit = ui.input(placeholder=f'{selected_game['name']}',
                        #                            on_change=lambda e: game_name.set_text(e.value))
                        # name_edit.bind_value(edited_game, 'name')
                        # name_edit.validation={"Too short!": enable.is_too_short} 
                        # name_edit.bind_visibility_from(toggle_edit, 'value')

                # DESCRIPTION
                with ui.row().classes():
                    with ui.column().classes():
                        # DISPLAY section
                        lbl_descript = ui.label("Description: ").classes('text-base font-bold text-center')
                        lbl_description = ui.label(f"{selected_game['description']}").classes('break-normal text-sm')
                        lbl_description.bind_visibility_from(toggle_edit, 
                                                                'value', 
                                                                backward=lambda toggle_edit: not toggle_edit)
                            
                        # EDIT section
                        descript_edit=ui.textarea(placeholder=f"{selected_game['description']}")
                        descript_edit.classes('hover:border-solid border-dotted hover:border-4 border-l-4 border-orange-500 rounded w-full')
                        descript_edit.props('clearable')
                        descript_edit.bind_value(edited_game, 'description')
                        descript_edit.bind_visibility_from(toggle_edit, 'value')
            
                # COUNTERS
                with ui.row().classes():
                    with ui.column().classes():
                        ui.label("View Counters?").classes('text-base font-bold text-center')
                        # If there
                        has_counters = ui.switch()
                        if edited_game['counters']:
                            has_counters.set_value(True)
                        else:
                            has_counters.set_value(False)

                        ui.label("Counters: ").bind_visibility_from(has_counters, 'value').classes('text-base font-bold text-center')
                        counter_display = render_all_counters(user_confirm, edited_game)
                        counter_display.bind_visibility_from(has_counters,'value')
                        # Button for adding counters only appears if user wishes to edit.
                        new_counter_btn = ui.button(
                            "Add Counter",
                            icon="create",
                            on_click=add_counter
                        )
                        new_counter_btn.bind_visibility_from(toggle_edit, 'value')

                # View lists of actors of the selected game
                with ui.row().classes():
                    with ui.column().classes():
                        with ui.label("View Default Actors?").classes('text-base font-bold'):
                            ui.tooltip("The default actors can be used as targets/causes for effects later on.")
                        has_actors = ui.switch()
                        # If there
                        if edited_game['default_actors']:
                            has_actors.set_value(True)
                        else:
                            has_actors.set_value(False)

                        ui.label("Default Actors: ").bind_visibility_from(has_actors, 'value').classes('text-base font-bold')
                        actors_display = render_all_actors(user_confirm, edited_game)
                        actors_display.bind_visibility_from(has_actors,'value')

                        create_actors = ui.button(
                            'Add Default Actor', 
                            icon="create", 
                            on_click=add_actor
                        )
                        create_actors.bind_visibility_from(has_actors, 'value')

                """Not viewing assets here except as name. 
                Must go to select_asset -> asset detail to edit an asset."""

                # TODO: 'if you delete a default asset from 'view assets' page, it will delete this here as well.
                # If you wish to move an asset from one game to the other:
                # First, creat a copy of the asset's folder and place it in the new game's folder.
                # Then, in STAT return to the original game, go to 'view assets', then delete the asset that way.

                # TODO: functionality: Add Default Asset() -> Gets Asset file, adds its name to default_assets list
                # TODO: functionality: Add Custom Asset() -> Gets asset file.

                # same as above for effects.

                # Saves_File_Path
                    # Show the path
                    # Warn user they will need to manually move saves to new location

                # TURNS
                with ui.row().classes():
                    with ui.column().classes():
                        ui.label("Turns").classes('text-base font-bold text-center')
                        has_turns = ui.switch()
                        # If there
                        if edited_game['has_turns']:
                            has_turns.set_value(True)
                        else:
                            has_turns.set_value(False)

                    # TURN TYPE
                        # DISPLAY section
                        lbl_turn_type = ui.label("Turn Type: ").classes('text-base font-bold text-center')
                        turn_type = ui.label(f"{selected_game['turn_type']}")
                        turn_type.classes('text-sm')
                        lbl_turn_type.bind_visibility_from(toggle_edit, 
                                                            'value', 
                                                            backward=lambda toggle_edit: not toggle_edit)
                        turn_type.bind_visibility_from(toggle_edit, 
                                                        'value', 
                                                        backward=lambda toggle_edit: not toggle_edit)

                        # EDIT section
                        lbl_type_edit = ui.label("Select how you count turns in your game: ")
                        lbl_type_edit.bind_visibility_from(toggle_edit, 'value')
                        edit_turn_type = ui.radio({'Increasing':'Increasing', 'Decreasing':'Decreasing'},
                                              value=selected_game['turn_type'])
                        edit_turn_type.props('inline left-label')
                        edit_turn_type.classes('text-sm')
                        edit_turn_type.bind_value(
                            edited_game, 
                            'turn_type')
                        edit_turn_type.bind_visibility_from(toggle_edit, 'value')
                        edit_turn_type.bind_visibility_from(toggle_edit, 'value')

                    # START TURN
                        # DISPLAY section
                        lbl_start_turn = ui.label("Start Turn: ").classes('text-base font-bold')
                        start_turn = ui.label(f"{selected_game['start_turn']}")
                        start_turn.classes('text-sm')
                        lbl_start_turn.bind_visibility_from(toggle_edit, 
                                                            'value', 
                                                            backward=lambda toggle_edit: not toggle_edit)
                        start_turn.bind_visibility_from(toggle_edit, 
                                                        'value', 
                                                        backward=lambda toggle_edit: not toggle_edit)
                        
                        # EDIT section
                        lbl_start_edit = ui.label('New Start Turn: ').classes('text-base font-bold')
                        lbl_start_edit.bind_visibility_from(toggle_edit, 'value')

                        start_edit = ui.number(value=selected_game['start_turn'],
                                               on_change=lambda e: edited_game.__setitem__('start_turn', int(e.value) if e.value is not None else 0))
                        start_edit.classes('text-sm')
                        start_edit.props('clearable')
                        start_edit.bind_visibility_from(toggle_edit, 'value')
                
                # IMAGE
                with ui.row().classes():
                    with ui.column().classes():
                        ui.label("Current Image: ").classes('text-base font-bold text-center')
                        game_image = ui.image(selected_game['image'])
                        with ui.button("Reload Image", on_click=game_image.force_reload):
                            ui.tooltip("This attempts to reload the associated image.")
                        ui.label("Image file path: ").classes('text-base font-bold')
                        lbl_image_path = ui.label(selected_game['image']).classes('text-sm text-center')

                        # EDIT
                        # Call the dialog to get new file path
                        async def choose_icon():
                            image_files = await app.native.main_window.create_file_dialog(allow_multiple=True)
                            for file in image_files:
                                asset_image = file
                            edited_game['image'] = asset_image
                        
                        pick_icon = ui.button('Choose file', on_click=choose_icon)
                        pick_icon.bind_visibility_from(toggle_edit, 'value')

                        # display new file path
                        new_file_path = ui.label("The new file path: ").classes('text-base font-bold text-center')
                        new_file_path.bind_visibility_from(toggle_edit, 'value')
                        lbl_new_image_path = ui.label(f'{edited_game['image']}')
                        lbl_new_image_path.bind_visibility_from(toggle_edit, 'value')

                        # display the new image
                        lbl_new_image = ui.label("The new image: ").classes('text-base font-bold text-center')
                        lbl_new_image.bind_visibility_from(toggle_edit, 'value')
                        new_image = ui.image(f'{edited_game['image']}')
                        new_image.bind_visibility_from(toggle_edit, 'value')

                        # reload the new image
                        btn_reload_new = ui.button("Reload New",on_click=new_image.force_reload)
                        btn_reload_new.bind_visibility_from(toggle_edit, 'value')

            ui.button('Submit', on_click=lambda: update_game_wrapper(edited_game))

                
