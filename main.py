#!/usr/bin/env python3
import api_router_example
import function_example
import home_page
import new_game
import theme
import view_games
import game_loaded
import loaded_save_dash
from fastapi import Depends 
from nicegui import app, ui


# Example 1: use a custom page decorator directly and putting the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        home_page.content()

new_game.create()

view_games.create()

game_loaded.create()

function_example.create()

loaded_save_dash.create()


ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', dark = 'None', window_size=(800, 500), fullscreen=False)