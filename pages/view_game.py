from elements.message import message
import elements.theme as theme
from fastapi import FastAPI, Depends
from nicegui import app, ui
from classes.MyGame import MyGame
import pages.select_saves as select_saves
from handlers.gamehandler import *

@ui.page('/selectgames')
async def seleect_games():
    with theme.frame('Select Games'):
        ui.label("TODO: Fill this in. :) :) :)")
        # View the details of the game
        # View list of assets of the game
        # view list of effects of the game