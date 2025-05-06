from handlers.confighandler import config, write_config
import elements.theme as theme
from nicegui import ui

@ui.page('/welcome')
async def content() -> None:
    with theme.frame('Welcome'):
        with ui.column().classes('items-center w-full gap-4 p-6 max-w-5xl'):
            ui.label('Welcome to STAT: the Snazzy Tabletop Assistant Tracker!').classes('text-2xl font-bold accent-text text-center')
            ui.label('The program is meant to be a tool to help you keep track of your progress in whatever tabletop game you choose!').classes('font-medium text-center')
            ui.label('With some creative thinking you can model a variety of games and resources.').classes('font-medium text-center')

            ui.separator()

            with ui.row().classes('w-full justify-center items-start gap-8'):
                with ui.column().classes('gap-2 w-full'):
                    ui.label('The title of the game in the top left corner will take you back to the homepage.').classes('font-medium')
                    ui.label("You’ll be able to see your selected game, save, and asset in the bottom right.").classes('font-medium')
                    ui.label("Clicking 'view details' shows what you're focused on.").classes('font-medium')

                with ui.column().classes('gap-2 w-full'):
                    ui.label('Return here via the "Settings" menu or `config.txt`.').classes('font-medium')
                    ui.label('STAT tries to find a default save location — check `config.txt`.').classes('font-medium')
                    ui.label('This is a work in progress — thanks for your patience!').classes('font-medium')

            ui.separator()

            ui.label('View the ReadMe on GitHub for more help.').classes('font-medium')
            with ui.link(target="https://github.com/echocall/STAT"):
                ui.button("GitHub")

            ui.separator()

            with ui.row().classes('w-full justify-center items-start gap-8'):
                with ui.column().classes('gap-2 w-full'):
                    ui.label("Do you prefer light mode or dark mode?").classes('font-medium')
                    ui.label("You can change this in the top left corner next to the menus.").classes('font-medium')

                with ui.column().classes('gap-2 w-full'):
                    ui.label("Show this welcome page next time?").classes('font-medium')
                    show_welcome = ui.switch(value=config['Toggles'].getboolean('showwelcome'),
                                             on_change=lambda e: set_show_welcome(e.value))

            ui.space()
            with ui.link(target='/'):
                ui.button("I'm ready to begin!").classes('text-lg')

    def set_show_welcome(value):
        config['Toggles']['showwelcome'] = str(value)
        write_config()
