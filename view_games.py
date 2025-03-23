from message import message
import theme
from pathlib import PurePath, Path
from nicegui import ui

""" TODO: Load in all games from the game file and create cards.
Find the # of saves for each game and display that as well.
Suffer the sins of my hubris.
TODO: make it pull pathing from config.txt and also write selection to the session data holder."""

def create() -> None:
    @ui.page('/viewgames')
    def view_games():
        with theme.frame('- View Games -'):
            games = [
                {'name': 'Test', 'description':'A game for testing purposes.', 'saves': 1},
                {'name': 'Delve', 'description':'A game about digging too deep.', 'saves': 0}
            ]

            game_card_container = ui.row().classes("full flex items-center")
            with game_card_container:
                for game in games:
                    with ui.card().tight():
                        with ui.card_section():
                            ui.label().bind_text_from(game, 'name', backward=lambda name: f'Name: {name}')
                            ui.label().bind_text_from(game, 'description', backward=lambda description: f'{description}')
                            ui.label().bind_text_from(game, 'saves', backward=lambda saves:f'# of save files: {saves}')
                        with ui.card_actions().classes("w-full justify-end"):
                            ui.button('Select Game', on_click=lambda: ui.notify('This will load the game.'))


                