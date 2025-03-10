from dataclasses import dataclass
import json

@dataclass
class MySave:
    name: str
    createDate: str
    dateLastSave: str
    description: str
    assetCustoms: bool
    assetCustomsPath: str
    actorCustoms: bool
    actorCustomsPath: str
    eventCustoms: bool
    eventCustomsPath: str
    effectCustoms: bool
    effectCustomsPath: str
    counters: dict
    assets: dict
    actors: dict
    currentEvents: dict
    currentEffects: dict
    logFilePath: str

    def __init__(self, saveDict=None):
        if saveDict is not None:
            for key, value in saveDict.items():
                setattr(self, key, value)
