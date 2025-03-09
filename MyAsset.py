from dataclasses import dataclass
import json

@dataclass
class MyAsset:
    name: str
    assetType: str
    description: str
    source: str
    category: str
    inGameTypes: list
    buyCosts: dict
    sellPrices: dict
    special: str
    effects: list
    icon: str
    image: str

    def __init__(self, assetDict=None):
        if assetDict is not None:
            for key, value in assetDict.items():
                setattr(self, key, value)

    