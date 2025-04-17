import elements.theme as theme
from fastapi import FastAPI, Depends
from nicegui import app, ui
from handlers.gamehandler import *

@ui.page('/viewgame/{game_name}')
async def seleect_games():
    with theme.frame('Select Games'):
        ui.label("TODO: Fill this in. :) :) :)")
        # View the details of the selected game
        # View list of assets of the selected game
        # view list of effects of the selected game