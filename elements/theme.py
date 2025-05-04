from contextlib import contextmanager
from elements.menu import menu
from nicegui import app,ui
import configparser

config = configparser.ConfigParser()
config.read('config.txt')

dark = ui.dark_mode()

@contextmanager
def frame(navigation_title: str):
    selected_game = app.storage.user.get("selected_game", {})
    selected_save = app.storage.user.get("selected_save", {})
    selected_asset = app.storage.user.get("selected_asset", {})

    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {
            font-family: 'Barlow', sans-serif;
            color: #F8B55F;
        }
        a {
            color: inherit;
            text-decoration: none;
        }
    </style>
    ''')

    # Custom page frame to share the same styling and behavior across all pages.
    # Base of this is from the NiceGUI github repo example for modularization

    # colors from: https://colorhunt.co/palette/3d365c7c4585c95792f8b55f
    ui.colors(primary='#771c77', 
              secondary='#C95792', 
              accent='#F8B55F', 
              positive='#41644A',
              warning='#F9CB43',
              negative='#b73333',
              light='#998adb',
              dark='#3D365C',
              dark_page='#23242f ')
    
    with ui.header().classes('items-center justify-center w-full'):
        with ui.row().classes('w-full justify-between'):
            with ui.link(target='/').classes('text-amber-300'):
                ui.label('STAT').classes('font-bold text-xl').props('color="accent"')
            ui.button(icon='keyboard_double_arrow_left', on_click=ui.navigate.back).props('color="secondary"').classes('scale-75')
            ui.button(icon='keyboard_double_arrow_right', on_click=ui.navigate.forward).props('color="secondary"').classes('scale-75')
            ui.label(navigation_title).classes('font-bold text-2xl text-center flex-grow')

            def handle_switch():
                if light_switch.value:
                    print('Enabling Dark Mode') 
                    config['Preferences']['darkMode'] = 'True'
                    # save updated config
                    with open('config.txt', 'w') as configfile:
                        config.write(configfile)
                    dark.enable()
                    ui.notify("Please close the application and reopen it to see this change take effect.",
                              position='top',
                              type='Positive')
                else:
                    print('Enabling Light Mode')
                    config['Preferences']['darkMode'] = 'False'
                    # save updated config
                    with open('config.txt', 'w') as configfile:
                        config.write(configfile)
                    dark.disable()
                    ui.notify("Please close the application and reopen it to see this change take effect.",
                              position='top',
                              type='Positive')

            light_switch = ui.switch("Dark Mode", on_change=handle_switch)
            light_switch.bind_value_from(config['Preferences'].getboolean('darkMode'))

            menu()
    with ui.column().classes('w-full items-stretch justify-center'):
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
        # Selected Asset
        if not selected_asset:
            ui.label("Selected Asset: None")
        else:
            ui.label(f"Selected Asset: {selected_asset['name']}")
