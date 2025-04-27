from nicegui import ui


class explanation(ui.tooltip):

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.classes('bg-stone-600')