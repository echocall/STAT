import elements.theme as theme
from nicegui import app, ui
import pages.select_saves as select_saves
from handlers.gamehandler import *
from elements.alert_dialog import alert_dialog

@ui.page('/selectgames')
async def select_games():
    with theme.frame('Select Games'):
        # File path for game data
        config = app.storage.user.get("config", {})
        paths = config.get("Paths",{})
        game_paths = paths.get("gamespath", "Not Set")

        existing_games = {}

        # getting the existing games from the file path.
        existing_games = get_games(game_paths)

        # setting the game objects into the user storage.
        app.storage.user["existing_games"] = existing_games

        # Displaying the games.
        game_card_container = ui.row().classes("grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4")
        with game_card_container:
            for game in existing_games.values():
                await render_game_cards(existing_games, game)

# Select a game to load into app.storage.user
def view_game_saves(existing_games: dict, selected_game_name: str):
    for name in selected_game_name:
        selected_game = {}
        try:
            selected_game = existing_games[name]
            app.storage.user['is_game_loaded']  = True
        except:
            alert_dialog("Problem with loading the game.",
                         "Please check the game file exists.")
        finally:
            app.storage.user['selected_game'] = selected_game
            ui.navigate.to(f"/selectsaves/{name}")

def game_view_details(existing_games: dict, selected_game_name: str):
    for name in selected_game_name:
        selected_game = {}
        try:
            selected_game = existing_games[name]
            app.storage.user['is_game_selected']  = True
        except:
            alert_dialog("Problem with selecting the game.",
                         "Please check the game file exists.")
        finally:
            app.storage.user['selected_game'] = selected_game
            ui.navigate.to(f"/viewgame/{name}")


# Render the cards displaying the existing games.
async def render_game_cards(existing_games: dict, game: dict)-> ui.element:
    with ui.card().tight().style('aspect-ratio: 4 / 3;'):
        with ui.card_section():
            ui.label().bind_text_from(game, 'name', backward=lambda name: f'{name}')
            ui.label().bind_text_from(game, 'description', backward=lambda description: f'{description}')
        with ui.card_actions().classes("w-full justify-end"):
            ui.button('View Details', on_click=lambda: game_view_details(existing_games, {game['name']}))
            ui.button('View Saves', on_click=lambda: view_game_saves(existing_games, {game['name']}))
            with ui.button(icon='edit').props('round'):
                ui.tooltip("Edit game.")
            with ui.button(icon='delete', on_click=ui.notify("TODO: Call confirm delete dialog to erase all files")).props('round'):
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
