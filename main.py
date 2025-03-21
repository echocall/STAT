#!/usr/bin/env python3
import api_router_example
import class_example
import function_example
import home_page
import new_game
import theme

from nicegui import app, ui


# Example 1: use a custom page decorator directly and putting the content creation into a separate function
@ui.page('/')
def index_page() -> None:
    with theme.frame('Homepage'):
        home_page.content()

new_game.create()

function_example.create()


ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', window_size=(800, 500), fullscreen=False)