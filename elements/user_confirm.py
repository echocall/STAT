from nicegui import ui

with ui.dialog() as user_confirm, ui.card():
    ui.label('Are you sure?')
    with ui.row():
        ui.button('Yes', on_click=lambda: user_confirm.submit('Yes'))
        ui.button('No', on_click=lambda: user_confirm.submit('No'))

