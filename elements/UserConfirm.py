class UserConfimr:
    # from: https://smhk.net/note/2023/09/nicegui-show-a-confirmation-popup/
    def __init__(self, *args, **kwargs):
        # Default text to display in the popup.
        self.popup_text = "Are you sure?"

        async def show_popup(_popup_text: str, func):
            """Call this function to trigger the popup.

            The functon `func` is only called if "Yes" is clicked in the dialog.
            """
            self.popup_text = _popup_text
            result = await popup_dialog
            if result == "Yes":
                func()

        # Define a single yes/no dialog that gets re-used for all the popups.
        with ui.dialog() as popup_dialog, ui.card():
            # Bind the text for the question, so that when `self.popup_text`
            # gets updated by `show_popup`, the text in the dialog also gets
            # updated.
            ui.label().bind_text_from(self, "popup_text")
            with ui.row():
                ui.button("Yes", on_click=lambda: popup_dialog.submit("Yes"))
                ui.button("No", on_click=lambda: popup_dialog.submit("No"))

        # Create a simple menu with some buttons, which call `show_popup` when
        # clicked and change the text for the question. The passed in `func`
        # is only executed by `show_popup` if the "Yes" button is pressed.
        with ui.button(icon="menu"):
            with ui.menu() as menu:
                ui.menu_item(
                    "Destroy widget",
                    lambda: show_popup(
                        "Do you really want to destroy the widget?",
                        self._action_widget_destroy
                    ),
                )
                ui.menu_item(
                    "Reset to defaults",
                    lambda: show_popup(
                        "Are you sure you want to reset to defaults?",
                        self._action_config_reset,
                    ),
                )

    def _action_widget_destroy(self):
        """Action: destroy the widget."""

    def _action_config_reset(self):
        """Action: reset to defaults."""