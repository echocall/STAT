from dataclasses import dataclass
import json

@dataclass
class MyAsset:
    name: str
    category: str
    description: str
    source: str
    type: str
    attributes: list
    buy_costs: dict
    sell_prices: dict
    special: str
    effects: list
    icon: str
    image: str


    def __post__init__ (self, name, category, description, source, type,
                  attributes, buy_costs, sell_prices, special,
                  effects, icon, image):
        self.name = name
        self.category = category
        self.description = description
        self.source = source
        self.type = type
        self.attributes = attributes
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

    