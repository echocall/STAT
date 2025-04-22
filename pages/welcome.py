from elements.message import message

from nicegui import ui

@ui.page('/welcome')
async def content() -> None:
    message('Welcome to STAT: the Snazzy Tabletop Assistant Tracker.').classes('font-bold')
    ui.label('Presentation')
    ui.label('By Pam Pepper')
    # TODO: Set this up for setting some of the options in Config for the first time
    
    with ui.link(target='/'):
        ui.icon('home').classes('scale-200').props('color="white"')