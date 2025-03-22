from nicegui import ui


def menu() -> None:
    with ui.link(target='/'):
        ui.icon('home')
    ui.link('A', '/a').classes(replace='text-white')
    with ui.row().classes('w-full items-center'):
            result = ui.label().classes('mr-auto')
            with ui.button(icon='help'):
                 with ui.menu() as help_menu:
                    ui.menu_item('Help Topic 1', lambda: result.set_text('Selected help item 1'))
                    ui.menu_item('Help Topic 2', lambda: result.set_text('Selected help item 2'))
                    ui.menu_item('Help Topic 3 (keep open)',
                         lambda: result.set_text('Selected help item 3'), auto_close=False)
                    ui.separator()
                    ui.menu_item('Close', help_menu.close)
    with ui.row().classes('w-full items-center'):
            result = ui.label().classes('mr-auto')
            with ui.button(icon='settings'):
                 with ui.menu() as settings_menu:
                    ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                    ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                    ui.menu_item('Menu item 3 (keep open)',
                         lambda: result.set_text('Selected item 3'), auto_close=False)
                    ui.separator()
                    ui.menu_item('Close', settings_menu.close)