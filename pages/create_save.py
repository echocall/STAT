import elements.theme as theme
from classes.Enable import *
from handlers.gamehandler import *
from nicegui import app,ui
import traceback

enable = Enable()

@ui.page('/creategame')
def create_game():
        with theme.frame('Create New Save'):
            with ui.column().classes("flex content-center w-100"):
                a = 1+1