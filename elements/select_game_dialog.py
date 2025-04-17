import elements.theme as theme
from nicegui import app, ui
from handlers.gamehandler import *

async def prompt_select_game():
    """Prompt the user to select a game if none is selected."""
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("No game selected! Please choose a game.").classes("h3")
            ui.button("Choose File", on_click=lambda: dialog.submit())
    files = await dialog
    if files:
        # Store the selected game in app.storage.user
        app.storage.user["selected_game"] = files[0]  # Assuming single file selection
        ui.notify(f"Game '{files[0]}' selected!")
        return files[0]
    else:
        ui.notify("No game selected. Please try again.")
        return None