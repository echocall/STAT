import elements.theme as theme
from nicegui import app, ui
import pages.select_saves as select_saves
from handlers.gamehandler import *
from elements.alert_dialog import alert_dialog
from helpers.utilities import format_str_for_filename_super
from elements.UserConfirm import *

@ui.page('/selectgames')
async def select_games():

    # Select a game to load into app.storage.user
    def view_game_saves(selected_game):
        """Take user to view the saves associated with the game unless user has not selected a game."""
        if not selected_game or 'name' not in selected_game:
            ui.notify("Please select a game before trying to view it's saves.",
                    position='top',
                    type='warning')
        else:
            ui.navigate.to(f"/selectsaves/")

    def game_view_details(selected_game):
        """Take user to view the details of a game unless user has not selected a game."""
        if not selected_game or 'name' not in selected_game:
            ui.notify("Please select a game before trying to view it's details.",
                    position='top',
                    type='warning')
        else:
            ui.navigate.to(f"/viewgame/")

    def select_target_game(existing_games: dict, selected_game_name: str):
        """Load the selected game into storage and refresh the page."""
        for name in selected_game_name:
            # getting the name to be correct.
            file_name = format_str_for_filename_super(name)['string']
            selected_game = {}

            # trying to get the specified game
            try:
                selected_game = existing_games[file_name]
                app.storage.user['is_game_loaded']  = True
            except:
                alert_dialog("Problem with loading the game.",
                            "Please check the game file exists.")
            finally:
                app.storage.user['selected_game'] = selected_game
                app.storage.user['selected_save'] = {}
                ui.notify(f"Success! You selected {name}.", type='positive', position='top')
                ui.navigate.reload()

    # Render the cards displaying the existing games.
    async def render_game_cards(existing_games: dict, game: dict)-> ui.element:
        """Render the cards displaying each game STAT found a JSON for."""
        with ui.card().classes(
            'w-full max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl p-2 '
            'flex flex-col justify-between h-full'
        ):
            with ui.row().classes('w-full justify-between items-start'):
                ui.label().bind_text_from(game, 'name', backward=lambda name: f'{name}').classes('text-lg font-bold mb-0')

            # Show first 25 characters of description with ellipsis if longer
            desc = game.get('description') or ''
            short_desc = (desc[:50] + '...') if len(desc) > 50 else desc
            ui.label(short_desc).classes('text-sm text-gray-300 mt-0')

            # Spacer to push buttons to the bottom
            ui.element('div').classes('flex-grow')

            # Button row anchored bottom-right
            with ui.row().classes('w-full justify-end'):
                with ui.button_group().classes('gap-2'):
                    ui.button('Select', on_click=lambda: select_target_game(existing_games, {game['name']})) \
                        .classes('text-sm px-3 py-1 sm:text-xs sm:px-2 sm:py-1')

    with theme.frame('All Games'):
        # File path for game data
        user_config = app.storage.user.get("config", {})
        paths = user_config.get("Paths",{})
        root_path = paths.get("osrootpath", "Not Set")
        games_path = paths.get("gamespath", "Not Set")
        user_confirm = UserConfirm()

        
        selected_game = app.storage.user.get("selected_game", {})
        existing_games = app.storage.user.get("existing_games", {})

        # Get the games_directory_path
        try:
            str_games_directory_path = root_path + games_path
            # getting the existing games from the file path.
            get_games_result = get_games(str_games_directory_path)
            if get_games_result['result']:
                existing_games = get_games_result['games']
                # setting the game objects into the user storage.
                app.storage.user["existing_games"] = existing_games
            else:
                ui.notify("Error getting existing games!", position='top', type='negative')
        except:
            ui.notify("""Error! Unable to retrieve the games. Please check the path loctions in config.py""",
                      position='top',
                      type='negative',
                      multi_line=True)

    with ui.row():
        with ui.column().classes('items-center w-full gap-4 pt-3 max-w-5xl'):
            ui.label("Select a game to get started!").classes('text-xl text-center accent-text')
            ui.label("Once you selecte a save it will update the 'Selected Game' in the bottom left of your screen and you may seen yoru screen flash.")
            ui.label("Please note that selecting a game will unload your currently selected save.")
            ui.label("Make sure to save your data before doing this!")

        # Buttons!!!
        with ui.row().classes('w-full justify-center items-start gap-8'):
            btn_create = ui.button('Create Game', on_click=lambda: ui.navigate.to("/creategame"))
            btn_detail = ui.button('View Detail', on_click=lambda: game_view_details(selected_game))
            btn_detail.bind_enabled_from(bool(app.storage.user["existing_games"]))
            btn_saves = ui.button('View Saves', on_click=lambda: view_game_saves(selected_game))
            btn_saves.bind_enabled_from(bool(app.storage.user["existing_games"]))
        # Displaying the games.
        game_card_container = ui.row().classes("grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4")
        with game_card_container:
            for game in existing_games.values():
                await render_game_cards(existing_games, game)

