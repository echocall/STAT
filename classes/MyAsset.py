from dataclasses import dataclass
import json

@dataclass
class MyAsset:
    name: str
    category: str
    description: str
    source: str
    asset_type: str
    attributes: list
    buy_costs: dict
    sell_prices: dict
    special: str
    effects: list
    icon: str
    image: str


    def __post__init__ (self, name, category, description, source, asset_type,
                  attributes, buy_costs, sell_prices, special,
                  effects, icon, image):
        self.name = name
        self.category = category
        self.description = description
        self.source = source
        self.asset_type = asset_type
        self.attributes = attributes
        self.buy_costs = buy_costs
        self.sell_prices = sell_prices
        self.special = special
        self.effects = effects
        self.icon = icon
        self.image = image

    def __str__(self):
        return self.name 

    def create_from_dict(self, assetDict=None):
        if assetDict is not None:
            for key, value in assetDict.items():
                setattr(self, key, value)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    # 

    # set attributes
    def set_attributes(self, attributesList=None):
        if attributesList is not None:
            self.attributes = attributesList

    # set buy_costs
    def set_buy_costs(self, buy_costsDict=None):
        if buy_costsDict is not None:
            self.buy_costs = buy_costsDict

    # set sell_prices
    def set_sell_prices(self, sell_pricesDict=None):
        if sell_pricesDict is not None:
            self.buy_costs = sell_pricesDict

    # to_JSON
    def to_JSON(self):
        return json.dumps(self,  indent=4)