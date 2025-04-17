from contextlib import contextmanager
from elements.menu import menu
from nicegui import app,ui

@contextmanager
def frame(navigation_title: str):
    loaded_game = app.storage.user.get("loaded_game", {})
    loaded_save = app.storage.user.get("loaded_save", {})
    selected_game = app.storage.user.get("selected_game", {})
    selected_save = app.storage.user.get("selected_save", {})
    """Custom page frame to share the same styling and behavior across all pages.
    Base of this is from the NiceGUI github repo example for modularization"""
    # 'Frightful Freight' color palette from SeesawSiya
    ui.colors(primary='#262f50', 
              secondary='#ce944e', 
              accent='#994f50', 
              positive='#cdbb8b',
              light='#C15F7C',
              dark='#9C4A52')
    with ui.header().classes('items-center justify-center w-full'):
        with ui.link(target='/'):
            ui.label('STAT').classes('font-bold text-lg')
        ui.label(navigation_title).classes('font-bold text-2xl text-center flex-grow')
        with ui.row():
            menu()
    with ui.column().classes('items-center justify-center w-full'):
        yield
    with ui.footer().props(f' color=#d5c7ba'):
        # Selected Game
        if not selected_game:
            ui.label("Selected Game: None")
        else:
            ui.label(f"Selected Game: {selected_game['name']}")
        # Selected Save
        if not selected_save:
            ui.label("Selected Save: None")
        else:
            ui.label(f"Selected Save: {selected_save['name']}")

    # with ui.label.color('#688157'):
    #    yield