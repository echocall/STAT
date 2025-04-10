import elements.theme as theme
from elements.message import message
from classes.Enable import Enable
from nicegui import ui

enable = Enable()

new_dict_entry = {}

# TODO: replace old Enable() class with newer version.
# TODO: Learn how to pass stuff in properly.

# pass in the name_of_type of w/e it is that this is being written to.
# example: Counter, Buy Cost, Sell Price, etc.
# then pass in the object template to be validated
# Then validate with SchemaValidator or FastAPI's validator
async def new_dict_entry(dict_name: str):
    with ui.dialog() as dialog, ui.card().classes("w-full"):
        ui.label("Create a new " + dict_name)
        with ui.card_section().classes('w-80 items-stretch'):
            name_input = ui.input("Name of the " + dict_name,
                            on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
            # allows user to clear the field
            name_input.props('clearable')
            # This handles the validation of the field.
            name_input.validation={"Too short!": enable.is_too_short} 
            # Displays the characters.        
            name_chars_left = ui.label()

        # getting the number.
        with ui.card_section().classes('w-80 items-stretch'):
            value_input = ui.number("Starting value of the " + dict_name + "?")
            # This handles the validation of the field. Checking for not null.
            value_input.validation={"Must have a value.": enable.not_null} 

        with ui.card_actions():
            # The button submits the data in the fields.
            submit = ui.button(
                "Create " + dict_name,
                on_click=lambda: dialog.submit(),
            )
            # This enables or disables the button depending on if the input field has errors or not
            submit.bind_enabled_from(enable, "no_errors")

            # Disable the button by default until validation is done.
            submit.disable()

            # Cancel out of dialog.
            ui.button("Cancel", on_click=dialog.close)
 
    # Get value
    result = await dialog
    print(result)
    # creating a new counter as a dict
    #
    new_dict_entry[result.name_input] = result.value_input

    print(new_dict_entry)