from nicegui import ui

def menu() -> None:
    with ui.link(target='/'):
        ui.icon('home')
    ui.link('A', '/a').classes(replace='text-white')
    with ui.button(icon='help').classes('scale-75'):
        with ui.menu() as help_menu:
            ui.menu_item('Help Topic 1', lambda: ui.notify('Selected help item 1').classes('mr-auto'))
            ui.menu_item('Help Topic 2', lambda: ui.notify('Selected help item 2').classes('mr-auto'))
            ui.menu_item('Help Topic 3 (keep open)',
                         lambda: ui.notify('Selected help item 3').classes('mr-auto'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', help_menu.close)

    with ui.button(icon='settings').classes('scale-75'):
        with ui.menu() as settings_menu:
            ui.menu_item('Menu item 1', lambda: ui.notify('Selected item 1').classes('mr-auto'))
            ui.menu_item('Menu item 2', lambda: ui.notify('Selected item 2').classes('mr-auto'))
            ui.menu_item('Menu item 3 (keep open)',
                         lambda: ui.notify('Selected item 3').classes('mr-auto'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', settings_menu.close)

    with ui.button(icon='menu').classes('scale-75'):
        with ui.menu() as general_menu:
            ui.menu_item('Load Game', lambda: ui.notify('This open the Load Game screen in the future.').classes('mr-auto'))
            ui.separator()
            ui.menu_item('Load Save', lambda: ui.notify('This load the Load Save screen in the future.').classes('mr-auto'))
            ui.separator()
            with ui.link(target='/loadeddash'):
                ui.menu_item('Session Dash')
            ui.menu_item('Save Session', lambda: ui.notify('This will call the Save_Session function in the future.').classes('mr-auto'))
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
    