from elements.message import message

from nicegui import ui

@ui.page('/welcome')
def content() -> None:
    message('Welcome to STAT: the Snazzy Tabletop Assistant Tracker.').classes('font-bold')
    ui.label('Prototype 2 Presentation')
    ui.label('By Pam Pepper')
    
    with ui.link(target='/'):
        ui.icon('home').classes('scale-200').props('color="white"')