# macOS packaging support
from multiprocessing import freeze_support  
freeze_support() 
from handlers.confighandler import set_paths, write_config, config, config_path

from typing import Annotated
import pages.home_page as home_page
import pages.select_games as select_games
import pages.select_saves as select_saves
import pages.create_game as create_game
import pages.create_asset as create_asset
import pages.create_save as create_save
import pages.create_effect as create_effect
import pages.loaded_save_dashboard as loaded_save_dashboard
import pages.game_detail as game_detail
import pages.edit_asset as edit_asset
import pages.welcome as welcome
from handlers.confighandler import set_paths, write_config, create_default_config

from nicegui import ui, app

from pages import *
import elements.theme as theme
from helpers.utilities import *

# Run this only if config doesn't exist or needs first-time setup
if not config_path.exists() or config['Toggles'].getboolean('firstsetup'):
    create_default_config()
    config['Toggles']['firstsetup'] = 'False'
    write_config()


if config['Toggles'].getboolean('firstsetup'):
    # Initialize config on startup
    set_paths()
    write_config()
    config['Toggles']['showwelcome'] = 'False'

@ui.page('/')
async def index_page() -> None:
    # Show Welcome or Home Page
    if config['Toggles'].getboolean('showwelcome'):
        config['Toggles']['showwelcome'] = 'False'
        write_config()

        with theme.frame('Welcome'):
            await welcome.content()
    else:
        with theme.frame('Home Page'):
            await home_page.content()
   
   # Dark mode
    dark_mode_on = config['Preferences'].getboolean('darkmode')

ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', fullscreen=False,
        storage_secret='teehee a secret for me', dark=config['Preferences'].getboolean('darkmode'))