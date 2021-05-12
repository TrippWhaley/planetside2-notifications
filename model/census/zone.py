from typing import Any, Dict
from .base import Census

class Zone(Census):

    def __init__(self) -> None:
        self.data = { zone.get("zone_id"):zone.get("code") for zone in self._get("zone") }
