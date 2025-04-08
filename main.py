#!/usr/bin/env python3
from typing import Annotated
import configparser
import pages.home_page as home_page
import pages.view_games as view_games
import pages.view_saves as view_saves
import pages.create_new_game as create_new_game
import pages.create_new_asset as create_new_asset
import pages.loaded_save_dashboard as loaded_save_dashboard
import pages.edit_game as edit_game

from pages import *
import elements.theme as theme
from helpers.utilities import *

from fastapi import Depends 
from nicegui import ui, app

@ui.page('/')
async def index_page() -> None:
    with theme.frame('Home Page'):
        await home_page.content()

ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', window_size=(1200, 800), 
       fullscreen=False, storage_secret='teehee a secret for me')