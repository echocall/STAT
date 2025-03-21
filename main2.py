from nicegui import app, ui

app.native.window_args['resizable'] = True
app.native.start_args['debug'] = True
app.native.settings['ALLOW_DOWNLOADS'] = False

dark = ui.dark_mode()
ui.add_css(''' .align{ align ="right"}        
}''')

with ui.row():
    # ui.icon('visibility', on_click=lambda: switch.bind_value(dark))
    ui.icon('question_mark')
    ui.icon('settings')



ui.switch('Dark mode').bind_value(dark)
ui.label('app running in native mode')
ui.button('New Game', on_click=lambda: app.native.main_window.resize(1000,700))
ui.button('Select Game', on_click=lambda: ui.colors(primary='#555'))

ui.run(native=True, title='Snazzy Tabletop Assistant Tracker', window_size=(600, 800), fullscreen=False)


    