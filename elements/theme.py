from contextlib import contextmanager
from elements.menu import menu
from nicegui import ui

@contextmanager
def frame(navigation_title: str):
    """Custom page frame to share the same styling and behavior across all pages.
    Base of this is from the NiceGUI github repo example for modularization"""
    # 'Frightful Freight' color palette from SeesawSiya
    ui.colors(primary='#262f50', 
              secondary='#ce944e', 
              accent='#994f50', 
              positive='#cdbb8b',
              light='#C15F7C',
              dark='#9C4A52')
    with ui.header().classes('items-center justify-center w-screen'):
        with ui.link(target='/'):
            ui.label('STAT').classes('font-bold text-lg')
        ui.space()
        ui.label(navigation_title).classes('font-bold text-2xl')
        ui.space()
        with ui.row():
            menu()
    with ui.column().classes('items-center justify-center w-screen'):
        yield
    with ui.footer().props(f' color=#d5c7ba'):
        ui.label('STAT').classes('font-bold')
    # with ui.label.color('#688157'):
    #    yield