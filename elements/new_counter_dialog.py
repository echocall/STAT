import elements.theme as theme
from classes.Enable import Enable
import traceback
from nicegui import ui

# creating our buddy.
enable = Enable()

async def new_counter_dialog():
    new_counter = {'name':'', 'value':0}
    try:
        with ui.dialog() as dialog, ui.card().classes("w-full"):
            ui.label("Create a new Counter").classes('h3')
            # Get name of counter
            with ui.card_section().classes('w-80 items-stretch'):
                name_input = ui.input("Name of the counter?",
                                on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
                name_input.bind_value(new_counter, 'name')
                # Allows user to clear the field
                name_input.props('clearable')
                # This handles the validation of the field.
                name_input.validation={"Must have a value": enable.not_null} 
                # Displays the characters.        
                name_chars_left = ui.label()

            # getting the number.
            with ui.card_section().classes('w-80 items-stretch'):
                value_input = ui.number("Starting value of the counter?", value=0, precision=0)
                # This handles the validation of the field. Checking for not null.
                value_input.validation={"Must have a value.": enable.not_null}
                value_input.bind_value(new_counter, 'value')

            with ui.card_actions():
                submit = ui.button(
                    "Create Counter",
                    on_click=lambda: dialog.submit([new_counter['name'], new_counter['value']])
                )
                
                # This enables or disables the button depending on if the input field has errors or not
                submit.bind_enabled_from(
                    name_input, "error", backward=lambda x: not x and name_input.value
                )
                # Gives us something we can check against for better closing.
                ui.button("Cancel", on_click=lambda: dialog.submit(None))  

        # gracefully handling cancelling
        result = await dialog
        if result is None:
            print("Dialog was cancelled.")
            return None  
        return result

    except Exception:
        print(traceback.format_exc())
        return None
