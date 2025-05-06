import elements.theme as theme
from nicegui import app,ui
import configparser
import traceback

@ui.page('/preferences')
async def prefrences():
    def handle_font_toggle(e):
        """Handles writing user preference for the font to the config.txt file."""
        config = configparser.ConfigParser()
        config.read('static/config.txt')
        new_font = 'NotoSerif' if e.value else 'ShantellSans'
        config['Preferences']['font'] = new_font
        with open('static/config.txt', 'w') as f:
            config.write(f)
        ui.notify(f'Font set to {new_font}. Restart the app to apply changes.', type='info')

    # Actual Page starts here.
    with theme.frame('Preferences'):
        # Default value from config
        config = configparser.ConfigParser()
        config.read('static/config.txt')
        default_font = config['Preferences'].get('font', 'ShantellSans')
        font_switch = ui.switch('Use Noto Serif font', on_change=handle_font_toggle)
        font_switch.value = (default_font == 'NotoSerif')