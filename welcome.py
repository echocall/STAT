from elements.message import message

from nicegui import ui


def content() -> None:
    message('Welcome to STAT: the Snazzy Tabletop Assistant Tracker.').classes('font-bold')
    ui.label('Use the menu on the top right to navigate.')