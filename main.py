#!/usr/bin/env python3
from typing import Annotated
import configparser
import home_page
import elements.theme as theme

from fastapi import Depends 
from nicegui import ui, app

# load file paths from config.txt
# Reworked from utilities -> stat_initializer
def load_config(config_file: str):
    # Reading from config file
    configParser = configparser.ConfigParser()
    configFilePath = config_file
    configParser.sections()
    configParser.read(configFilePath)

    config_dict = {}
    # We want to preserve the sections for organization later
    for Section in configParser.sections():
        temp_dict = {}
        # Create a temporary diction that gets added to the Sectiond ictionary
        for key, value in configParser[Section].items():
            temp_dict.update({key:value})
        config_dict[Section] = temp_dict

    # Return the organized dictionary
    return config_dict

@ui.page('/')
async def index_page() -> None:

    config_data = load_config('config.txt')
    structured_data = {}
    
    for section in config_data:
        structured_data[section] = config_data[section]
    # Store as nested dictionary
    app.storage.user["config"] = structured_data

    with theme.frame('Home Page'):
        await home_page.content()

ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', window_size=(800, 500), fullscreen=False)