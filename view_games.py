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
            columns = [
                {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True,
                'align': 'left' },
                {'name': 'description', 'label':'Descrpition', 'field': 'description',
                'sortable': True} 
            ]

            games = [
                {'name': 'Test', 'description':'A game for testing purposes.', 'saves': 5},
                {'name': 'Delve', 'description':'A game about digging too deep.', 'saves': 0}
            ]

            game_card_container = ui.row().classes("full flex items-center")
            with game_card_container:
                for each in games:
                    with ui.card().tight():
                        with ui.card_section():
                            ui.label().bind_text_from(each, 'name', backward=lambda name: f'Name: {name}')
                            ui.label().bind_text_from(each, 'description', backward=lambda description: f'Description: {description}')
                            ui.label().bind_text_from(each, 'saves', backward=lambda saves:f'# of save files: {saves}')
                        with ui.card_actions().classes("w-full justify-end"):
                            ui.button('Select Game', on_click=lambda: ui.notify('This will load the game.'))


                