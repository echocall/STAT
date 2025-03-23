from contextlib import contextmanager
from menu import menu
from nicegui import ui

@contextmanager
def frame(navigation_title: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    # Instead of a Head
    ui.colors(primary='#b7bfb0 ', secondary='#d5c7ba', accent='#686157', positive='#cdbb8b')
    with ui.header():
        ui.label('STAT').classes('font-bold')
        ui.space()
        ui.label(navigation_title).classes('font-bold')
        ui.space()
        with ui.row():
            menu()
    with ui.column().classes('absolute-center items-center'):
        yield
    with ui.label.color('#688157'):
        yield