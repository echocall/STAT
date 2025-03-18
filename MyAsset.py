from dataclasses import dataclass
import json

@dataclass
class MyAsset:
    name: str
    asset_type: str
    description: str
    source: str
    category: str
    in_game_types: list
    buy_costs: dict
    sell_prices: dict
    special: str
    effects: list
    icon: str
    image: str


    def __post__init__ (self, name, asset_type, description, source, category,
                  in_game_types, buy_costs, sell_prices, special,
                  effects, icon, image):
        self.name = name
        self.asset_type = asset_type
        self.description = description
        self.source = source
        self.category = category
        self.in_game_types = in_game_types
        self.buy_costs = buy_costs
        self.sell_prices = sell_prices
        self.special = special
        self.effects = effects
        self.icon = icon
        self.image = image

    def create_from_dict(self, assetDict=None):
        if assetDict is not None:
            for key, value in assetDict.items():
                setattr(self, key, value)

    