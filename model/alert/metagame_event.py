from datetime import datetime
from typing import Any, Dict, Optional

from model.census.metagame_event import MetagameEvent
from .base import Alert


class MetagameEventAlert(Alert):
    def __init__(
        self,
        faction_tr: str,
        faction_nc: str,
        faction_vs: str,
        metagame_event_id: str,
        metagame_event_state_name: str,
        timestamp: str,
        **kwargs,
    ):
        self.faction_tr = faction_tr
        self.faction_nc = faction_nc
        self.faction_vs = faction_vs
        self.metagame_event_name = MetagameEvent().get(metagame_event_id)
        self.metagame_event_state_name = metagame_event_state_name
        self.timestamp = datetime.fromtimestamp(int(timestamp)).strftime("%H:%M:%S")

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional["MetagameEventAlert"]:
        data = data.get("payload")
        if data is not None:
            return MetagameEventAlert(**data)
        return None

    def to_string(self):
        return f"""
  ALERT:
  Terran Republic: {self.faction_tr}
  New Conglomerate: {self.faction_nc}
  Vanu Scum: {self.faction_vs}
  {self.metagame_event_name}
  {self.metagame_event_state_name} at UTC {self.timestamp}
            """
