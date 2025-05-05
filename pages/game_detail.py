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

    async def choose_icon_file() -> str:
            """For bringing up a file picker to select an image."""
            files = await app.native.main_window.create_file_dialog(allow_multiple=False)
            for file in files:
                edited_game['icon'] = file

    async def choose_image_file() -> str:
        """For bringing up a file picker to select an image."""
        files = await app.native.main_window.create_file_dialog(allow_multiple=False)
        for file in files:
            edited_game['image'] = file

   # Render the counters.
    @ui.refreshable
    def render_all_counters(user_confirm, edited_game) -> ui.element:
        """Show the user all the counters associated with the game_dict."""
        with ui.row().classes('gap-2') as counter_display_case:
            for counter, value in edited_game['counters'].items():
                with ui.row().classes('items-center gap-2'):
                    ui.label(f'{counter}:').classes('font-bold')
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
                    ui.label(str(value)).classes('text-sm font-bold')

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


    with theme.frame(f'Game Details'):
        edited_game = {}
        selected_game = app.storage.user.get("selected_game", {})
        edited_game = selected_game

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
                with ui.link(target='/selectgames'):
                    btn_create_event = ui.button('Delete Game')
                    btn_create_event.bind_enabled_from(bool(selected_game))
                
            # No game selected
            if not selected_game or 'name' not in selected_game:
                with ui.row():
                    ui.icon('warning').classes('text-3xl')
                    ui.label('Warning: No selected game detected.').classes('text-2xl')
                ui.label('Cannot view the details for a game with no game selected.')
                ui.label('Please select a game from \'View Games\'.')
                ui.label('Then return here to view the save files.')
                with ui.link(target = '/selectgames'):
                    ui.button('Find Game File')
            else:
                # Toggle for editing or not
                with ui.row().classes():
                    with ui.column().classes():
                        toggle_edit = ui.switch('Do you want to edit?')
                        toggle_edit.classes('font-bold')
                        toggle_edit.props('color="green"')
                
                # ICON
                with ui.row().classes():
                    with ui.column().classes():
                        if selected_game['icon']:
                            game_icon = ui.image(f'{selected_game['icon']}')
                            ui.label("The icon for your game.").classes('font-bold')
                            ui.button("Reload Icon", on_click=game_icon.force_reload)
                        else:
                            ui.label("No Icon to display").classes('font-bold')
                    # TODO: Display option to change the Icon's path.

                # Section for rest of the data
                # with ui.row().classes():
                    # NAME
                with ui.row().classes():
                    with ui.column().classes():
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
                with ui.row().classes():
                    with ui.column().classes():
                        # DISPLAY section
                        lbl_descript = ui.label("Description: ").classes('font-bold')
                        lbl_description = ui.label(f"{selected_game['description']}").classes('break-normal')
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
                        ui.label("View Counters?").classes('font-bold')
                        # If there
                        has_counters = ui.switch()
                        if edited_game['counters']:
                            has_counters.set_value(True)
                        else:
                            has_counters.set_value(False)

                        ui.label("Counters: ").bind_visibility_from(has_counters, 'value')
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
                        with ui.label("View Default Actors?"):
                            ui.tooltip("The default actors can be used as targets/causes for effects later on.")
                        has_actors = ui.switch()
                        # If there
                        if edited_game['default_actors']:
                            has_actors.set_value(True)
                        else:
                            has_actors.set_value(False)

                        ui.label("Default Actors: ").bind_visibility_from(has_actors, 'value')
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
                    # Default turn
                    # Turn Type
                
                # IMAGE
                with ui.row().classes():
                    with ui.column().classes():
                        game_image = ui.image(f'{selected_game['image']}')
                        with ui.button("Reload Image", on_click=game_image.force_reload):
                            ui.tooltip("This attempts to reload the associated image.")
                        ui.label("Image file path").classes('font-bold')
                        lbl_image_path = ui.label(f'{selected_game['image']}')

                        # EDIT
                        # Call the dialog to get new file path
                        btn_find_image = ui.button("Find New Image").on_click(lambda: choose_image_file)
                        btn_find_image.bind_visibility_from(toggle_edit, 'value')
                        # display new file path
                        lbl_new_image_path = ui.label(f'{edited_game['image']}').classes('font-bold')
                        lbl_new_image_path.bind_visibility_from(toggle_edit, 'value')
                        # display the new image
                        new_image = ui.image(f'{edited_game['image']}')
                        new_image.bind_visibility_from(toggle_edit, 'value')
                        # reload the new image
                        btn_reload_new = ui.button("Reload New",on_click=new_image.force_reload)
                        btn_reload_new.bind_visibility_from(toggle_edit, 'value')

                # Submit button

                
