from classes.Enable import Enable
import traceback
from nicegui import ui

# creating our buddy.
enable = Enable()

async def new_string_dialog(string_name):
    new_string = {'name':''}
    try:
        with ui.dialog() as dialog, ui.card().classes("w-full"):
            ui.label(f"Create a new {string_name}").classes('h3')
            # Get name of counter
            with ui.card_section().classes('w-100 items-stretch'):
                string_input = ui.input(f"Name of the {string_name}?",
                                on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' characters used.'))
                string_input.bind_value(new_string, 'name')
                # allows user to clear the field
                string_input.props('clearable')
                # This handles the validation of the field.
                string_input.validation={"Must have a value": enable.not_null} 
                # Displays the characters.        
                name_chars_left = ui.label()

            with ui.card_actions():
                # The button submits the data in the fields.
                submit = ui.button(
                    f"Create {string_name}",
                    on_click=lambda: dialog.submit(new_string)
                )
                
                # This enables or disables the button depending on if the input field has errors or not
                submit.bind_enabled_from(
                    string_input, "error", backward=lambda x: not x and string_input.value
                )

                # Cancel out of dialog.
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