import theme
from message import message
from classes.enable import Enable
from nicegui import ui


counter = {'name': 'value'}

async def new_counter_dialog():
    with ui.dialog() as dialog, ui.card():
        ui.label("Create a new Counter")
        with ui.card_section().classes:
            name_input = ui.input("Name of the Counter?")
            name_input.validation = {
                "Must have at least one character in the name.": lambda x: len(x) >= 1
            }
            name_input.bind_vale(globals(), 'counter')
            name_input.bind_key(name_input)
        with ui.card_section():
            value_input = ui.number("Starting value of the counter?")
            value_input.validation={
                "Box cannot be empty": lambda y: y.value != None
            }
            value_input.bind_vale(globals(), 'counter')
            value_input.bind_key(value_input)

        with ui.card_actions():
            # The button submits the data in the fields.
            submit = ui.button(
                "Create Counter",
                on_click=lambda: dialog.submit(name_input.value, value_input.value),
            )
            # This enables or disables the button depending on if the input field has errors or not
            submit.bind_enabled_from(
                name_input, "error", backward=lambda x: not x and name_input.value,
            )
            # Its disabled by default since the validation rules only run when the text changes
            submit.disable()

            # Cancel out of dialog.
            ui.button("Cancel", on_click=dialog.close)
 
    # Get value
    counter = await dialog
    callback()
    return counter