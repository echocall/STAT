from contextlib import contextmanager
from elements.menu import menu
import helpers.font_picker as font_picker
import configparser
from pathlib import Path
from nicegui import app,ui

config = configparser.ConfigParser()
config.read('static/config.txt')

# DONT REMOVE THIS.
dark = ui.dark_mode()

@contextmanager
def frame(navigation_title: str):
    selected_game = app.storage.user.get("selected_game", {})
    selected_save = app.storage.user.get("selected_save", {})
    selected_asset = app.storage.user.get("selected_asset", {})

    font_picker.apply_font()

    ui.add_head_html('''
     <style>
        /* Base font size */
        html {
            font-size: 18px;
        }

        /* Medium screens */
        @media (min-width: 768px) {
            html {
                font-size: 20px;
            }
        }

        /* Large screens (desktop monitors) */
        @media (min-width: 1280px) {
            html {
                font-size: 22px;
            }
        }

        /* Extra-large (4K displays etc.) */
        @media (min-width: 1920px) {
            html {
                font-size: 24px;
            }
        }

        a {
            color: inherit;
            text-decoration: none;
        }
                     
        .txt-inherit-accent,
        .q-header,
        .q-footer,
        .menu,
        .title,
        header *,
        footer *,
        .accent-text {
            color: var(--q-accent);
        }
                     
        /* Base tooltip font size */
        .q-tooltip {
            font-size: 0.75rem;
            color: gray;
        }

        /* Medium screens */
        @media (min-width: 768px) {
            .q-tooltip {
                font-size: 0.875rem; 
            }
        }

        /* Large screens */
        @media (min-width: 1280px) {
            .q-tooltip {
                font-size: 1rem; 
            }
        }

        /* Extra-large monitors */
        @media (min-width: 1920px) {
            .q-tooltip {
                font-size: 1.125rem; 
            }
        }
    </style>
    ''')

    # Custom page frame to share the same styling and behavior across all pages.
    # Base of this is from the NiceGUI github repo example for modularization

    # colors from: https://colorhunt.co/palette/3d365c7c4585c95792f8b55f
    ui.colors(primary='#771c77', 
              secondary='#db2b86', 
              accent='#F8B55F', 
              positive='#41644A',
              warning='#F9CB43',
              negative='#b73333',
              light='#998adb',
              dark='#3D365C',
              dark_page='#23242f')
    
    with ui.header().classes('items-center justify-center w-full txt-inherit-accent'):
        with ui.row().classes('w-full justify-between'):
            with ui.link(target='/').classes():
                ui.label('STAT').classes('font-bold text-xl').props('color=accent')
            ui.button(icon='keyboard_double_arrow_left', on_click=ui.navigate.back).props('color=secondary').classes('scale-100')
            ui.button(icon='keyboard_double_arrow_right', on_click=ui.navigate.forward).props('color=secondary').classes('scale-100')
            ui.label(navigation_title).classes('font-bold text-2xl text-center flex-grow')

            def handle_switch():
                if light_switch.value:
                    print('Enabling Dark Mode') 
                    config['Preferences']['darkMode'] = 'True'
                    # save updated config
                    with open('static/config.txt', 'w') as configfile:
                        config.write(configfile)
                    dark.enable()
                    ui.notify("You picked dark mode! Please restart the application to see this change take effect.",
                              position='top',
                              type='Positive')
                else:
                    print('Enabling Light Mode')
                    config['Preferences']['darkMode'] = 'False'
                    # save updated config
                    with open('static/config.txt', 'w') as configfile:
                        config.write(configfile)
                    dark.disable()
                    ui.notify("You picked light mode! Please restart the application to see this change take effect.",
                              position='top',
                              type='Positive')

            light_switch = ui.switch("Dark Mode", on_change=handle_switch)
            light_switch.bind_value_from(config['Preferences'].getboolean('darkMode'))

            menu()
    with ui.row().classes('w-full h-full justify-center items-start'):
        with ui.column().classes('w-full items-stretch'):
            yield
    with ui.footer().props('color=accent'):
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
