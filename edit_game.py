from nicegui import ui
import elements.theme as theme
from elements.message import message
from new_counter_dialog import new_counter_dialog
from classes.MyGame import MyGame
from elements.message import message

def create() -> None:
    @ui.page('/editgame')
    def edit_game():
        with theme.frame('Edit a Game'):
            message("Edit a game!")
