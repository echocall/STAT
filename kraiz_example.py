from nicegui import ui
async def new_table_dialog(db: AsyncSession, user: UserResponse, callback):
    with ui.dialog() as dialog, ui.card().classes("w-full"):
        ui.label("Create a New Table").classes("text-h3")
        with ui.card_section().classes("w-full"):
            ui.label("Just give us a name and we'll take care of the rest.")
            name_input = ui.input("Name of your Table?").classes("w-full")
            name_input.validation = {
                "You need at least 5 characters in the name...": lambda x: len(x) >= 5
            }

        with ui.card_actions().classes("w-full justify-end"):
            # The button submits the dialog providing the text entered
            submit = ui.button(
                "Let's Go!",
                on_click=lambda: dialog.submit(name_input.value),
            ).classes("w-1/4")
            # This enables or disables the button depending on if the input field has errors or not
            submit.bind_enabled_from(
                name_input, "error", backward=lambda x: not x and name_input.value
            )
            # Its disabled by default since the validation rules only run when the text changes
            submit.disable()

            ui.button("Maybe Later", color="dark", on_click=dialog.close).classes(
                "w-1/4"
            )
    # when the dialog.submit(...) is called, here's where the value comes out.
    display_name = await dialog
    new_table = await TableTop.create(db=db, created_by=user, display_name=display_name)
    await asyncio.sleep(0.5)
    callback()
    return new_table