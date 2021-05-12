from typing import Any, Dict
from .base import Census

class World(Census):
    
    def __init__(self):
        self.data = { world.get("name").get("en"):world.get("world_id") for world in self._get("world") }