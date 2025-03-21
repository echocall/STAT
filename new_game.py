import theme
from message import message

from nicegui import ui


def create() -> None:
    @ui.page('/newgame')
    def new_game():
        with theme.frame('- Create a Game -'):
            message('Create a Game')
            # Input name for the game.
            with ui.row():
                ui.label('Enter a name for the new game: ')
                ui.input(label='Game Name', placeholder='50 character limit',
                            on_change=lambda e: result.set_text(len(e) + ' of 50 characters used.'),
                            validation={'Input too long, limit is 50 characters.': lambda value: len(e) > 50,
                                        'Input too short, you need at least one character.': lambda value: len(value) < 1}
                            ).props('clearable')
                result = ui.label()
            # input description for the game.
            ui.label('Enter a description for the new game:')
            description = ui.input(label='Game Description', placeholder='500 character limit',
                            on_change=lambda e: description_result.set_text(e.value + ' of 500 characters used.')).props('clearable')
            description = validation={'Input too long, limit is 500 characters.': lambda value: len(value) > 500}
            description_result = ui.label()
            # Do you want to add counters to the game?
            with ui.row():
                ui.label('Add a counter?')
                ui.button
