from dataclasses import dataclass
import json

@dataclass
class Counter:
    name: str
    value: int