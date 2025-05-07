import elements.theme as theme
from nicegui import app,ui
from handlers.confighandler import config, write_config
import traceback

@ui.page('/userpreferences')
async def userprefrences():
    def handle_font_toggle(e):
        """Handles writing user preference for the font to the config.txt file."""
        new_font = 'NotoSerif' if e.value else 'ShantellSans'
        config['Preferences']['font'] = new_font
        write_config()
        ui.notify(f'Font set to {new_font}. Restart the app to apply changes.', type='info')

    # Actual Page starts here.
    with theme.frame('Preferences'):
        # Default value from config
        default_font = config['Preferences']['font']
        font_switch = ui.switch('Use Noto Serif font or ShantellSans?', on_change=handle_font_toggle).props('left-label')
        font_switch.value = (default_font == 'NotoSerif')

