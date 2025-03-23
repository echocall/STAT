from nicegui import ui

# Class to nicely format category labels
class CategoryLabel(ui.label):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.classes('text-h5 text-orange-500')