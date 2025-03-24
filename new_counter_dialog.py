import elements.theme as theme
from elements.message import message
from classes.Enable import Enable
from nicegui import ui
from classes.Counter import Counter

new_counter = {'name': 'value'}
# creating our buddy.
enable = Enable()

async def new_counter_dialog():
    with ui.dialog() as dialog, ui.card().classes("w-full"):
        ui.label("Create a new Counter")
        with ui.card_section().classes('w-80 items-stretch'):
            name_input = ui.input("Name of the Counter?",
                            on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
            # allows user to clear the field
            name_input.props('clearable')
            # This handles the validation of the field.
            name_input.validation={"Must have a value": enable.not_null} 
            # Displays the characters.        
            name_chars_left = ui.label()

        # getting the number.
        with ui.card_section().classes('w-80 items-stretch'):
            value_input = ui.number("Starting value of the counter?")
            # This handles the validation of the field. Checking for not null.
            value_input.validation={"Must have a value.": enable.not_null} 
        new_counter ={}
        new_counter[name_input] = value_input
        with ui.card_actions():
            # The button submits the data in the fields.
            submit = ui.button(
                "Create Counter",
                on_click=lambda: dialog.submit(new_counter),
            )
            
            # This enables or disables the button depending on if the input field has errors or not
            submit.bind_enabled_from(
                name_input, "error", backward=lambda x: not x and name_input.value
            )

            # Disable the button by default until validation is done.
            submit.disable()

            # Cancel out of dialog.
            ui.button("Cancel", on_click=dialog.close)
 
    # Get new_counter
    counter = await dialog

    ui.notify(counter)
    # creating a new counter as a dict