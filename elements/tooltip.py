from nicegui import ui


class blue_tooltip(ui.label):

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.classes('bg-blue')