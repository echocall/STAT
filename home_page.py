from message import message
from new_game_dialog import new_game_dialog

from nicegui import ui



def content() -> None:
    new_game = ui.button(
    "Create New Game",
    icon="create",
    )
    
    ui.label('Do you want to add a new game to STAT, or work with a preexisting game?')
    new_game.on("click",
                lambda: new_game_dialog())
    ui.button('Select Game', on_click=lambda: ui.colors(primary='#555'))