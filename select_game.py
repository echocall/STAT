from message import message
from nicegui import ui
from handlers.gamehandler import get_games_names
from classes.StatInstance import *
from helpers.utilities import stat_initialize
from classes.MyGame import *

# Initialzie the class instance.
currentStat = MyStat(".\config.txt")
print(currentStat.is_game_loaded)
print(currentStat.game_loaded_name)

filePaths = stat_initialize(currentStat.config_file)
print(filePaths)

def fetch_games():
    available_games = get_games_names()

def content() -> None:
    ui.label('Shall I load the games for you?')
    get_games = ui.button(
    "Fetch Games",
    icon="",
    )
    get_games.on("click",
                lambda: new_game_dialog())
    ui.button('Select Game', on_click=lambda: ui.colors(primary='#555'))