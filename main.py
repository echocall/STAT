#!/usr/bin/env python3

import function_example
import home_page
import create_new_game
import create_new_asset
import elements.theme as theme
import view_games
import view_saves
import loaded_save_dashboard

from fastapi import Depends 
from nicegui import ui

# Example 1: use a custom page decorator directly and putting the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        home_page.content()

create_new_game.create()

create_new_asset.create()

view_games.create()

view_saves.create()

function_example.create()

loaded_save_dashboard.create()


ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', window_size=(800, 500), fullscreen=False)