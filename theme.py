from contextlib import contextmanager

from menu import menu

from nicegui import ui


@contextmanager
def frame(navigation_title: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    # Frightful Freight
    ui.colors(primary='#262f50', secondary='#994f50', accent='#ce944e', positive='#cdbb8b')
    with ui.header():
        ui.label('STAT').classes('font-bold')
        ui.space()
        ui.label(navigation_title)
        ui.space()
        with ui.row():
            menu()
    with ui.column().classes('absolute-center items-center'):
        yield
