import elements.theme as theme
from nicegui import app, ui
import pages.select_saves as select_saves
from handlers.gamehandler import *
from elements.alert_dialog import alert_dialog
from helpers.utilities import format_str_for_filename_super

@ui.page('/selectgames')
async def select_games():
    with theme.frame('All Games'):
        # File path for game data
        config = app.storage.user.get("config", {})
        paths = config.get("Paths",{})
        game_paths = paths.get("gamespath", "Not Set")
        root_path = paths.get("osrootpath", "Not Set")

        selected_game = app.storage.user.get("selected_game", {})
        existing_games = app.storage.user.get("existing_games", {})

        if not existing_games:
            # getting the existing games from the file path.
            existing_games = get_games(game_paths, root_path)
            # setting the game objects into the user storage.
            app.storage.user["existing_games"] = existing_games

        ui.label("Select a game to use it as the basis for creating an asset, save, or effect.").classes('text-xl')
        ui.label("Please note that selecting a game will unload your currently selected save and you will lose your changes.")
        ui.label("Make sure to save your data before doing this!")

        # Buttons!!!
        with ui.row():
            btn_detail = ui.button('View Detail', on_click=lambda: game_view_details(selected_game))
            btn_detail.bind_enabled_from(bool(app.storage.user["existing_games"]))
            btn_saves = ui.button('View Saves', on_click=lambda: view_game_saves(selected_game))
            btn_saves.bind_enabled_from(bool(app.storage.user["existing_games"]))
        # Displaying the games.
        game_card_container = ui.row().classes("grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4")
        with game_card_container:
            for game in existing_games.values():
                await render_game_cards(existing_games, game)

# Select a game to load into app.storage.user
def view_game_saves(selected_game):
    if not selected_game or 'name' not in selected_game:
        ui.notify("Please select a game before trying to view it's saves.",
                  position='top',
                  type='warning')
    else:
        ui.navigate.to(f"/selectsaves/")

def game_view_details(selected_game):
    if not selected_game or 'name' not in selected_game:
        ui.notify("Please select a game before trying to view it's details.",
                  position='top',
                  type='warning')
    else:
        ui.navigate.to(f"/viewgame/")

def select_target_game(existing_games: dict, selected_game_name: str):
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
    with ui.card().tight().style('width: 100%; max-width: 250px; aspect-ratio: 4 / 3; max-height: 175px;'):
        with ui.card_section():
            ui.label().bind_text_from(game, 'name', backward=lambda name: f'{name}')
            ui.label().bind_text_from(game, 'description', backward=lambda description: f'{description}')
        with ui.card_actions().classes("w-full justify-end"):
            ui.button('Select', on_click=lambda: select_target_game(existing_games, {game['name']}))
            with ui.button(icon='edit').props('round'):
                ui.tooltip("Edit game.")
            # TODO: Erase game and ALL associated children folders/files
            with ui.button(icon='delete').props('round'):
                ui.tooltip("Delete this game and all files associated with it.")

# Confirm we want to delete the game and its files then call
# TODO: finish
async def confirm_game_delete()-> ui.element:
    # Are you sure you want to delete?
    with ui.dialog() as confirm_delete, ui.card():
                ui.label('Are you sure you want to delete ALL files?')
                with ui.row():
                    ui.button('Yes', on_click=ui.notify("This will delete the game's JSON file."))
                    ui.button('No', on_click=confirm_delete.close)


