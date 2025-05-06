from nicegui import ui
from handlers.confighandler import config, config_path, write_config


def light_switch() -> None:
    dark = ui.dark_mode()
    config['Preferences']['darkmode'] = str(not dark)
    write_config()
    ui.notify(f"Switched to {'Dark' if not dark else 'Light'} mode", color='primary')

    # ui.switch()
    # ui.switch('Dark mode').bind_value(dark)
    
    switch = ui.switch("Dark Mode", on_change=handle_switch)
    switch.bind_value_from(config['Preferences'].getboolean('darkMode'))
    switch.is_ignoring_events(True)

    # Old way of handling it
    def handle_switch():
        if switch.value:
            print('Enabling Dark Mode') 
            config['Preferences']['darkMode'] = 'True'
            # save updated config
            write_config()
            dark.enable()
            ui.notify("Please close the application and reopen it to see this change take effect.",
                        position='top',
                        type='Positive')
        else:
            print('Enabling Light Mode')
            config['Preferences']['darkMode'] = 'False'
            # save updated config
            write_config()
            dark.disable()
            ui.notify("Please close the application and reopen it to see this change take effect.",
                        position='top',
                        type='Positive')
