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
            ui.menu_item('Menu item 2', lambda: ui.notify('Selected item 1').classes('mr-auto'))
            ui.menu_item('Menu item 3 (keep open)',
                         lambda: ui.notify('Selected item 3').classes('mr-auto'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', settings_menu.close)