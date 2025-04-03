from nicegui import ui
from fastapi import FastAPI, Depends

def menu() -> None:
    with ui.link(target='/'):
        ui.icon('home').classes('scale-200').props('color="white"')
    # ui.link('A', '/a').classes(replace='text-white')

    with ui.button(icon='menu').classes('scale-75').props('color="secondary"') :
        with ui.menu() as general_menu:
            with ui.link(target='/creategame'):
                ui.menu_item('Create New Game')
            with ui.link(target='/editgame'):
                ui.menu_item('Edit Game File')
            with ui.link(target='/viewgames'):
                ui.menu_item('Load Game File')
            ui.separator()
            ui.menu_item('New Save Start')
            ui.separator()
            with ui.link(target='/loadeddash'):
                ui.menu_item('Current Session Dashboard')
            ui.menu_item('Save Session', lambda: ui.notify('This will call the Save_Session function in the future.'))
            with ui.link(target='/viewsaves'):
                ui.menu_item('Load Session', lambda: ui.notify('This will call the Save_session function in the future.'))
            ui.separator()
            with ui.link(target='/createasset'):
                ui.menu_item('Create an Asset')
            ui.separator()
            ui.menu_item('Close', general_menu.close)


    with ui.button(icon='help').classes('scale-75').props('color="secondary"') as help_menu_btn:
        with ui.menu() as help_menu:
            game_help = ui.menu_item('Game Help', auto_close=False)
            with ui.menu() as game_help:
                ui.menu_item('What is a Game?', lambda: ui.notify('In the context of STAT'
                ' a game is a file that contians the default information for a playtime of that game.'), auto_close=False)
                ui.menu_item("What is a counter?", lambda: ui.notify('A counter is meant to keep track of any resource where you just need to keep track of the Name and Amount you have.'
                ' This could be health,  money, points for victory, spell slots you expend by using spells, or other uses.'), auto_close=False)
                ui.menu_item('Close game menu', game_help.close)    
            asset_help = ui.menu_item('Help Topic 2', lambda: ui.notify('Selected help item 2'))
            with ui.menu() as asset_help:
                ui.menu_item('What is an Asset?', lambda: ui.notify('An asset is anything you want to track the amount you have'
                ' as well as any possible changes to your counters upon gaining, using, or selling the item.'))
            ui.menu_item('Help item 3 (keep open)',
                         lambda: ui.notify('Selected item 3'), auto_close=False)
            ui.menu_item('Close', help_menu.close)

    with ui.button(icon='settings').classes('scale-75').props('color="secondary"'):
        with ui.menu() as settings_menu:
            ui.menu_item('Menu item 1', lambda: ui.notify('Selected item 1'))
            ui.menu_item('Menu item 2', lambda: ui.notify('Selected item 2'))
            ui.menu_item('Menu item 3 (keep open)',
                         lambda: ui.notify('Selected item 3'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', settings_menu.close)


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
    