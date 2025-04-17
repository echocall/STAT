from nicegui import app, ui
from fastapi import FastAPI, Depends

def menu() -> None:
    # Dynamically determine the target for "View Game File"
    def get_view_game_target():
        selected_game = app.storage.user.get("selected_game", None)
        if selected_game:
            return f"/viewgame/{selected_game['name']}"  # Assuming 'name' is the key for the game name
        return "/selectgames"
    
    with ui.button(icon='menu').classes('scale-75').props('color="secondary"') :
        with ui.menu() as general_menu:
            with ui.link(target='/creategame'):
                ui.menu_item('Create New Game')
            with ui.link(target='/editgame'):
                ui.menu_item('Edit Game File')
            with ui.link(target='/selectgames'):
                ui.menu_item('Load Game File')
            with ui.link(target=get_view_game_target()):
                ui.menu_item('View Game File')
            
            ui.separator()
            ui.menu_item('New Save Start')
            ui.separator()
            with ui.link(target='/loadeddash'):
                ui.menu_item('Current Session Dashboard')
            ui.menu_item('Save Session', lambda: ui.notify('This will call the Save_Session function in the future.'))
            with ui.link(target='/selectsaves'):
                ui.menu_item('Load Session', lambda: ui.notify('This will call the Save_session function in the future.'))
            ui.separator()
            with ui.link(target='/createasset'):
                ui.menu_item('Create an Asset')
            ui.separator()
            ui.menu_item('Close', general_menu.close)

    # Are you sure you want to close?
    with ui.dialog() as confirm_close, ui.card():
        ui.label(f'Are you sure you want to close STAT?')
        ui.label(f'Your changes will not be automatically saved.')
        with ui.row():
            ui.button('Yes', on_click=app.shutdown)
            ui.button('No', on_click=confirm_close.close)

    with ui.button(icon='settings').classes('scale-75').props('color="secondary"'):
        with ui.menu() as settings_menu:
            ui.menu_item('Menu item 1', lambda: ui.notify('Selected item 1'))
            ui.menu_item('Menu item 2', lambda: ui.notify('Selected item 2'))
            ui.menu_item('Menu item 3 (keep open)',
                         lambda: ui.notify('Selected item 3'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', settings_menu.close)
            ui.separator()
            ui.menu_item('Close STAT', on_click=confirm_close.open)

""" Creating a custom menu_item for toggling dark mode on/off.
Based on the example on NiceGUI of acustom ToggleButton."""
class ToggleDark(ui.menu_item):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._state = False
        self.on('click', self.toggle)

    def toggle(self) -> None:
        # Toggling the button state.
        self._state = not self._state
        self.updat()

    def update(self) -> None:
        self.props(f'color={"yellow" if self._state else "blue"}')
        super().update()
    