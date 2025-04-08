from nicegui import ui

def add_chip():
    with chips:
        ui.chip(label_input.value, icon='label', color='silver')
    label_input.value = ''

label_input = ui.input('Add label').on('keydown.enter', add_chip)
with label_input.add_slot('append'):
    ui.button(icon='add', on_click=add_chip).props('round dense flat')

with ui.row().classes('gap-0') as chips:
    ui.chip('Label 1', icon='label', color='silver', removable=True)

ui.button('Restore removed chips', icon='unarchive',
          on_click=lambda: [chip.set_value(True) for chip in chips]) \
    .props('flat')

ui.run()
