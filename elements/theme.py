from contextlib import contextmanager
from elements.menu import menu
from nicegui import ui

@contextmanager
def frame(navigation_title: str):
    """Custom page frame to share the same styling and behavior across all pages.
    Base of this is from the NiceGUI github repo example for modularization"""
    # Why tho color palette from fastman27
    ui.colors(primary='#262f50 ', secondary='#d5c7ba', accent='#686157', positive='#cdbb8b')
    with ui.header():
        ui.label('STAT').classes('font-bold')
        ui.space()
        ui.label(navigation_title).classes('font-bold')
        ui.space()
        with ui.row():
            menu()
    with ui.column().classes('w-full items-center'):
        yield
    with ui.footer().props(f' color=#d5c7ba'):
        ui.label('STAT').classes('font-bold')
    # with ui.label.color('#688157'):
    #    yield