# macOS packaging support
from multiprocessing import freeze_support  
freeze_support() 
from handlers.confighandler import config_path, config, create_default_config, set_paths, write_config, load_config
from helpers.logging import log_startup_event
from typing import Annotated
import pages.home_page as home_page
import pages.select_games as select_games
import pages.select_saves as select_saves
import pages.select_assets as select_assets
import pages.create_game as create_game
import pages.create_asset as create_asset
import pages.create_save as create_save
import pages.create_effect as create_effect
import pages.loaded_save_dashboard as loaded_save_dashboard
import pages.game_detail as game_detail
import pages.edit_asset as edit_asset
import pages.welcome as welcome

from nicegui import ui, app

from pages import *
import elements.theme as theme
from helpers.utilities import *



@ui.page('/')
async def index_page() -> None:
    #For converting config into dict
    config_data = load_config(config_path)

    structured_data = {}
    
    # Create organized nested structure for config.
    for key in config_data:
        structured_data[key] = config_data[key]

    # Store as nested dictionary
    app.storage.user["config"] = structured_data
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

ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', fullscreen=False, reload=False,
        storage_secret='teehee a secret for me', dark=config['Preferences'].getboolean('darkmode', fallback=False))