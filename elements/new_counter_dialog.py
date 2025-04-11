import elements.theme as theme
from elements.message import message
from classes.Enable import Enable
from nicegui import ui
from classes.Counter import Counter

# creating our buddy.
enable = Enable()

async def new_counter_dialog():
    def submit_values(new_counter: dict) -> dict:
        counter = {}
        counter[new_counter['name']] = new_counter['value']
        return counter

    new_counter = {'name':'', 'value':0}

    with ui.dialog() as dialog, ui.card().classes("w-full"):
        ui.label("Create a new Counter")
        # Get name of counter
        with ui.card_section().classes('w-80 items-stretch'):
            name_input = ui.input("Name of the counter?",
                            on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
            name_input.bind_value(new_counter, 'name')
            # allows user to clear the field
            name_input.props('clearable')

            # This handles the validation of the field.
            # name_input.validation={"Must have a value": enable.not_null} 

            # Displays the characters.        
            name_chars_left = ui.label()

        # getting the number.
        with ui.card_section().classes('w-80 items-stretch'):
            value_input = ui.number("Starting value of the counter?", value=0, precision=0)
            # This handles the validation of the field. Checking for not null.
            # value_input.validation={"Must have a value.": enable.not_null}
            value_input.bind_value(new_counter, 'value')

        with ui.card_actions():
            # The button submits the data in the fields.
            submit = ui.button(
                "Create Counter",
                on_click=lambda: dialog.submit([new_counter['name'], new_counter['value']])
            )
            
            # This enables or disables the button depending on if the input field has errors or not
            submit.bind_enabled_from(
                name_input, "error", backward=lambda x: not x and name_input.value
            )

            # Cancel out of dialog.
            ui.button("Cancel", on_click=dialog.close)
 
    # Get new_counter
    counter = await dialog
    return counter