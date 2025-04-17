import elements.theme as theme
from nicegui import app, ui

async def prompt_select_save():
    """Prompt the user to select a save if none is selected."""
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("No save selected! Please choose a save.").classes("h3")
            ui.button("Choose File", on_click=lambda: dialog.submit())
    files = await dialog
    if files:
        # Store the selected save in app.storage.user
        app.storage.user["selected_save"] = files[0]  # Assuming single file selection
        ui.notify(f"Game '{files[0]}' selected!")
        return files[0]
    else:
        ui.notify("No save selected. Please try again.")
        return None