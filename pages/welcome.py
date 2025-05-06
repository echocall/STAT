import configparser

config = configparser.ConfigParser()
config.read('static/config.txt')

from nicegui import ui

@ui.page('/welcome')
async def content() -> None:
    with ui.element():
        ui.label('Welcome to STAT: the Snazzy Tabletop Assistant Tracker!').classes('font-medium')
        ui.label('The program is meant to be a tool to help you keep track of your progress in whatever table top game you choose!').classes('font-medium break-normal')
        ui.label('With some creative thinking you can model a variety of games and resources.').classes('font-medium break-normal')
        ui.space()
        ui.label('The title of the game in the top left corner will take you back to the homepage.').classes('font-medium break-normal')
        ui.label("You'll be able to see what your currently selected game, save, and asset are in the bottom right corner of the screen. When you click on 'view details' this is what tells STAT what you want to look at.").classes('font-medium break-normal')
        ui.space()
        ui.label('You can return here by clicking on the link under the "Settings" menu, or altering the config.txt file.').classes('font-medium break-normal')
        ui.label('By default STAT will try to find a location to save its files. You can check what location it could reach by looking in config.txt').classes('font-medium break-normal')
        ui.label('This is still a work in progress so we ask that you bear with us for this first release.').classes('font-medium break-normal')        
        ui.space()
        ui.label('View the ReadMe on github for more help.').classes('font-medium break-normal')
        with ui.link(target="https://github.com/echocall/STAT"):
             ui.button("Github")
        with ui.column():
                with ui.row():
                     ui.label("Do you prefer light mode or dark mode?")
                     ui.label("You can change this in the top left corner next to the menus.")

                    
        with ui.column():
            with ui.row():
                ui.label("Do you want to see this welcome next time you log in?").props('font-medium break-normal')
                show_welcome = ui.switch(value=config['Toggles'].getboolean('showwelcome'), on_change=lambda e: set_show_welcome(e.value))

        def set_show_welcome(value):
            config['Toggles']['showwelcome'] = str(value)
            with open('static/config.txt', 'w') as configfile:
                config.write(configfile)
            
        with ui.link(target='/'):
            ui.button("I'm ready to begin!")