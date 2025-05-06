from nicegui import ui
import configparser


def light_switch() -> None:
    config = configparser.ConfigParser()
    config.read('static/config.txt')

    dark = ui.dark_mode()

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
            with open('static/config.txt', 'w') as configfile:
                config.write(config.txt)
            dark.enable()
            ui.notify("Please close the application and reopen it to see this change take effect.",
                        position='top',
                        type='Positive')
        else:
            print('Enabling Light Mode')
            config['Preferences']['darkMode'] = 'False'
            # save updated config
            with open('static/config.txt', 'w') as configfile:
                config.write(config.txt)
            dark.disable()
            ui.notify("Please close the application and reopen it to see this change take effect.",
                        position='top',
                        type='Positive')
