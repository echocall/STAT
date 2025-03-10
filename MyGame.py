from dataclasses import dataclass
import json

@dataclass
class MyGame:
    name: str
    description: str
    hasCounters: bool
    counters: list
    hasActors: bool
    actorDefaultPath: str
    defaultActors: list
    hasAssets: bool
    assetDefaultPath: str
    defaultAssets: list
    hasEvents: bool
    eventDefaultPath: str
    defaultEvents: list
    hasEffects: bool
    effectDefaultPath: str
    defaultEffects: list
    icon: str
    saveFilesPath: str
    turns: bool
    turnType: str

    def __init__(self, gameDict=None):
        if gameDict is not None:
            for key, value in gameDict.items():
                setattr(self, key, value)
    