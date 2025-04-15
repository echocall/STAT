import elements.theme as theme
from elements.message import message
from classes.Enable import Enable
from nicegui import ui

# creating our buddy.
enable = Enable()

async def new_actor_dialog():
    new_actor = {'name':''}

    with ui.dialog() as dialog, ui.card().classes("w-full"):
        ui.label("Create a new Actor")
        # Get name of Actor
        with ui.card_section().classes('w-80 items-actor'):
            name_input = ui.input("Name of the actor?",
                            on_change=lambda e: name_chars_left.set_text(str(len(e.value)) + ' of 50 characters used.'))
            name_input.bind_value(new_actor, 'name')
            # allows user to clear the field
            name_input.props('clearable')

            name_input.validation={"Must have a value": enable.not_null} 

            # Displays the characters.        
            name_chars_left = ui.label()

        with ui.card_actions():
            # The button submits the data in the fields.
            submit = ui.button(
                "Create Counter",
                on_click=lambda: dialog.submit(new_actor)
            )
            
            # This enables or disables the button depending on if the input field has errors or not
            submit.bind_enabled_from(
                name_input, "error", backward=lambda x: not x and name_input.value
            )

            # Cancel out of dialog.
            ui.button("Cancel", on_click=dialog.close)
 
    # Get new_actor
    new_actor = await dialog
    return new_actor