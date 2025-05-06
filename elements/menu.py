from nicegui import app, ui
from fastapi import FastAPI, Depends

def menu() -> None:
    selected_game = app.storage.user.get("selected_game", None)
    selected_save = app.storage.user.get("selected_save", None)

    # Determine the target for "View Game File"
    def get_view_game_target():
        return f"/viewgame/"
    
    # Determine the target for "View Game File"
    def get_view_dashboard_target():
        return f"/loadeddash"
        
    def view_saves():
        return f"/selectsaves/"

    # TODO: deal with no selected_game
    def get_view_save_target():
        if selected_save:
            return f"/viewsave/{selected_save['name']}"
        # ui.notify("Error: No save currently selected!",
        #          position='top',
        #          type='warning')
    
    def get_load_save_target():
        if selected_game:
            return f"'/selectsaves/{selected_game['name']}"
        # if no selected_game
        else:
            # ui.notify("You've got no game! You must have a game selected to view its saves.", type='warning', position='top')
            with ui.dialog() as no_game:
                    ui.label("You've got no game! You must have a game AND a save selected to view the dashboard.").classes('break-all')
                    ui.label("Redirecting to the page to select a game.")
                    ui.button('Close', on_click=no_game.close())
            return ''

    # MAIN MENU
    with ui.button(icon='menu').classes('scale-100 txt-inherit-accent').props('color=secondary'):
        with ui.menu() as general_menu:
            with ui.link(target='/'):
                ui.menu_item('Home')
            ui.separator()

            # GAMES
            with ui.menu_item('Game Menu', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                # Menu Items go under here
                with ui.menu().props('anchor="top end" self="top start" auto-close'):
                    with ui.link(target='/selectgames'):
                        ui.menu_item('View Games')
                    with ui.link(target='/creategame'):
                        ui.menu_item('Create New Game')
                    with ui.link(target=get_view_game_target()):
                        ui.menu_item('View Game File')
                    with ui.link(target='/editgame'):
                        ui.menu_item('Edit Current Game')

            # SAVES
            with ui.menu_item('Save Menu', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                # Menu Items go under here
                with ui.menu().props('anchor="top end" self="top start" auto-close'):
                    with ui.link(target=view_saves()):
                        ui.menu_item('View Saves')
                    # TODO: implement individual view save 
                    # with ui.link(target=get_view_save_target()):
                    ui.menu_item('View Selected')
                    with ui.link(target='/createsave'):
                        ui.menu_item('New Save Start')
                    # with ui.link(target=get_load_save_target()):
                    #    ui.menu_item('Load Save')
                    ui.menu_item('Edit Save')

            # DASHBOARD
            with ui.menu_item('Dashboard', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                with ui.menu().props('anchor="top end" self="top start" auto-close'): 
                    with ui.link(target=get_view_dashboard_target()):
                        ui.menu_item('View Dashboard')
                    ui.menu_item('Save Session', lambda: ui.notify('This will call the Save_Session function in the future.'))
            
            # ASSETS
            with ui.menu_item('Assets Menu', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                with ui.menu().props('anchor="top end" self="top start" auto-close'):  
                    with ui.link(target='/createasset'):
                        ui.menu_item('Create Asset')
                    ui.menu_item('View Asset')
                    with ui.link(target='/editasset'):
                        ui.menu_item('Edit Asset')
                        
            # EFFECTS
            with ui.menu_item('Effects Menu', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                with ui.menu().props('anchor="top end" self="top start" auto-close'):
                    with ui.link(target='/createeffect'):
                        ui.menu_item('Create Effect')
                    ui.menu_item('View Effect')
            ui.separator()
            ui.menu_item('Close', general_menu.close)

    # SETTINGS MENU AREA
    # Are you sure you want to close?
    with ui.dialog() as confirm_close, ui.card():
        ui.label(f'Are you sure you want to close STAT?')
        ui.label(f'Your changes to the current save file will not be automatically saved.')
        with ui.row():
            ui.button('Yes', on_click=app.shutdown)
            ui.button('No', on_click=confirm_close.close)
    # Settings menu
    with ui.button(icon='settings').classes('scale-100').props('color=secondary'):
        with ui.menu() as settings_menu:
            ui.menu_item('Settings', lambda: ui.notify('Under construction! Thank you for your patience.', position='top', type='Warning'))
            ui.menu_item('Preferences', lambda: ui.notify('Under Construction! Thank you for your patience.', position='top', type='Warning'))
            ui.menu_item('Help',
                         lambda: ui.notify('Under construction! Thank you for your patience.', position='top', type='Warning'))
            with ui.link(target='/welcome'):
                ui.menu_item('Welcome Page')
            with ui.menu_item('About', auto_close=False):
                ui.tooltip("""STAT by Pam Pepper. Released under the MIT license. Alpha""")
            ui.separator()
            ui.menu_item('Close', settings_menu.close)
            ui.separator()
            ui.menu_item('Exit STAT', on_click=confirm_close.open)

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
    