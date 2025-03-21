from message import message

from nicegui import ui


def content() -> None:
    ui.label('Do you want to add a new game to STAT, or work with a preexisting game?')
    with ui.link(target='/newgame'):
        ui.button('New Game', on_click=lambda: ui.colors(primary='#777'))
    ui.button('Select Game', on_click=lambda: ui.colors(primary='#555'))