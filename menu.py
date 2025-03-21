from nicegui import ui


def menu() -> None:
    ui.icon('question_mark')
    ui.icon('settings')
    with ui.link(target='/'):
        ui.icon('home')
    ui.link('B', '/b').classes(replace='text-white')
    ui.link('C', '/c').classes(replace='text-white')