from nicegui import ui

def alert_dialog(error: str, message: str):
    with ui.dialog() as alert:
        ui.icon('warning').classes().style('background-color: yellow; ' \
        'color: black; border-radius: 50%; padding: 8px;')
        ui.label("Warning!").classes('h-3')
        ui.label(error)
        ui.label(message)
        ui.button("Close",on_click=alert.close)