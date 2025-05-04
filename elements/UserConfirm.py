# based on: https://smhk.net/note/2023/09/nicegui-show-a-confirmation-popup/
from nicegui import ui
class UserConfirm:
    def __init__(self):
        # default text
        self.popup_text = "Are you sure?"
        self._popup_dialog = None

        # Create a dialog and bind label to self.popup_text
        with ui.dialog() as self._popup_dialog, ui.card():
            self._label = ui.label(self.popup_text)
            self._label.bind_text_from(self, 'popup_text')

            with ui.row():
                ui.button("Yes", on_click=lambda: self._popup_dialog.submit("Yes"))
                ui.button("No", on_click=lambda: self._popup_dialog.submit("No"))

    async def show(self, message: str, on_confirm: callable):
        """Show the confirmation popup with a custom message.
        Calls `on_confirm()` if user clicks Yes."""
        self.popup_text = message
        result = await self._popup_dialog
        if result == "Yes":
            on_confirm()

