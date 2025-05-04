#!/usr/bin/env python3
from typing import Annotated
import pages.home_page as home_page
import pages.select_games as select_games
import pages.select_saves as select_saves
import pages.create_game as create_game
import pages.create_asset as create_asset
import pages.create_save as create_save
import pages.create_effect as create_effect
import pages.loaded_save_dashboard as loaded_save_dashboard
import pages.edit_game as edit_game
import pages.game_detail as game_detail
import pages.edit_asset as edit_asset
import pages.welcome as welcome

from pages import *
import elements.theme as theme
from helpers.utilities import *
import configparser

from fastapi import Depends 
from nicegui import ui, app

# Load configuration
config = configparser.ConfigParser()
config.read('config.txt')

@ui.page('/')
async def index_page() -> None:
    # Show Welcome or Home Page
    if config['Toggles'].getboolean('showwelcome'):
        config['Toggles']['showwelcome'] = 'False'
        # save updated config
        with open('config.txt', 'w') as configfile:
            config.write(configfile)
        with theme.frame('Welcome'):
            await welcome.content()
    else:
        with theme.frame('Home Page'):
            await home_page.content()
   
    # Dark mode
    if config['Preferences'].getboolean('darkMode'):
        dark_mode_on = True
    else:
        dark_mode_on = False

ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', window_size=(1200, 800), 
       fullscreen=False, storage_secret='teehee a secret for me', dark=config['Preferences'].getboolean('darkMode'))