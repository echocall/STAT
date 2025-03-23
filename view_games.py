from message import message
import theme
from pathlib import PurePath, Path
from nicegui import ui

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

            rows = [
                {'name': 'Test', 'description':'A game for testing purposes.'},
                {'name': 'Delve', 'description':'A game about digging too deep.'}
            ]

            with ui.row():
                ui.table(columns=columns, rows=rows, row_key='name')
                with ui.card().tight():
                    with ui.card_section():
                        ui.label('Test')
                        ui.label('A game for testing purposes.')
                        ui.button('Select Game', on_click=lambda: ui.notify('This will load the game.'))

                with ui.card().tight():
                    with ui.card_section():
                        ui.label('Delve')
                        ui.label('A game about digging deep.')
                        ui.button('Select Game', on_click=lambda: ui.notify('This will load the game.'))
                