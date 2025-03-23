from nicegui import ui
from CategoryLabel import CategoryLabel

# Call after for category in sorted_assets:
# pass in category and sorted_assets, return asset_contianer.
class AssetContainer(ui.row):
    def __init__(self) -> None:
        super().__init__(self)
        self.classes("full flex items-left")
