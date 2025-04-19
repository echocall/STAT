from classes.Enable import Enable
from nicegui import app, ui

# creating our buddy.
enable = Enable()

async def target_counter_dialog(purpose: str):
    target_counter = {'name':'', 'value':0}

    # populates self from the counters 
    # associated with the currently selected game
    selected_game = app.storage.user.get("selected_game", {})
    
    # get the counters as a dictionary of name: value pair
    counters = selected_game['counters']
    # list of keys
    counter_names = list(counters.keys())
    
    def is_valid():
        return counter_name_select.value and not counter_name_select.error and value_input.value is not None

    with ui.dialog() as dialog, ui.card().classes("w-full"):
        ui.label(f"{purpose}").classes('h-3')
        ui.label("Select Counter to be added").classes('h-4')
        with ui.column().classes('items-stretch'):
        # Get name of counter
            with ui.card_section().classes():
                counter_name_select = ui.select(options=counter_names, with_input=True)
                counter_name_select.bind_value(target_counter, 'name')
                # This handles the validation of the field.
                counter_name_select.validation={"Must have a value": enable.not_null} 

            # getting the number.
            with ui.card_section().classes():
                ui.label("Enter the appropriate value.").classes('h-4')
                value_input = ui.number("Value: ", value=0, precision=0)
                # This handles the validation of the field. Checking for not null.
                value_input.validation={"Must have a value.": enable.not_null}
                value_input.bind_value(target_counter, 'value')

            with ui.card_actions():
                # The button submits the data in the fields.
                submit = ui.button(
                    "Add Counter",
                    on_click=lambda: dialog.submit(target_counter)
                )
                # Testing new enabling
                submit.bind_enabled_from(counter_name_select, "value", backward=lambda _: is_valid())
                submit.bind_enabled_from(value_input, "value", backward=lambda _: is_valid())  

                # Cancel out of dialog.
                ui.button("Cancel", on_click=dialog.close)
 
    # Get the result
    counter = await dialog
    return counter