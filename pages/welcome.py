from elements.message import message
import configparser

config = configparser.ConfigParser()
config.read('config.txt')

from nicegui import ui

@ui.page('/welcome')
async def content() -> None:
    with ui.element():
        ui.label('Welcome to STAT: the Snazzy Tabletop Assistant Tracker!').classes('font-bold')
        ui.label('The program is meant to be a tool to help you keep track of your progress in whatever table top game you choose!').classes('break-normal')
        ui.label('With some creative thinking you can model a variety of games and resources.').classes('break-normal')
        # TODO: Set this up for setting some of the options in Config for the first time
        
        with ui.row():
            ui.label("Do you want to see this welcome next time you log in?")
            show_welcome = ui.switch(value=config['Toggles'].getboolean('showwelcome'), on_change=lambda e: set_show_welcome(e.value))

        def set_show_welcome(value):
            config['Toggles']['showwelcome'] = str(value)
            with open('config.txt', 'w') as configfile:
                config.write(configfile)
            