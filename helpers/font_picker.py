from handlers.confighandler import config, config_path, write_config
from nicegui import ui

def apply_font():

    font_choice = config['Preferences']['font']

    if font_choice == 'ShantellSans':
        font_family = 'Shantell Sans'
        font_file = 'ShantellSans-Regular.ttf'
        font_url = 'C:/Users/strip/Documents/github/STAT/static/fonts/ShantellSans/ShantellSans-Regular.ttf'
    elif font_choice == 'NotoSerif':
        font_family = 'Noto Serif'
        font_file = 'NotoSerif-Regular.ttf'
        font_url = 'C:/Users/strip/Documents/github/STAT/static/fonts/NotoSerif/NotoSerif-Regular.ttf'
    else:
        font_family = "sans-serif"
        font_file = ''

    ui.add_head_html(f'''
    <style>
        @font-face {{
            font-family: '{font_family}';
            src: url('{font_url}') format('truetype');
            font-weight: normal;
            font-style: normal;
        }}

        body {{
            font-family: '{font_family}', sans-serif;
        }}
    </style>
    ''')