from typing import Any, Dict
from .base import Census

class MetagameEvent(Census):
    
    def __init__(self):
        self.data = { event.get("metagame_event_id"):event.get("name").get("en") for event in self._get("metagame_event", limit=1000) }