from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from model.census.metagame_event import MetagameEvent
from .base import Alert


@dataclass
class FactionConfig:
    name: str
    percent: float
    color: int
    image_url: str


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
        self.faction_tr = round(float(faction_tr), 2)
        self.faction_nc = round(float(faction_nc), 2)
        self.faction_vs = round(float(faction_vs), 2)
        self.metagame_event_name = MetagameEvent().get(metagame_event_id)
        self.metagame_event_state_name = metagame_event_state_name
        self.timestamp = datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional["MetagameEventAlert"]:
        data = data.get("payload")
        if data is not None:
            return MetagameEventAlert(**data)
        return None
    
    # Refactor this into config later, being lazy and writing bad code now
    # Especially these URLs. Really need to be pulled at script init to be sure the images are correct
    def order_factions(self) -> List[FactionConfig]:
        return sorted([
            FactionConfig("Terran Republic", self.faction_tr, 11602713, "https://census.daybreakgames.com/files/ps2/images/static/18.png"), 
            FactionConfig("New Conglomerate", self.faction_nc, 3447003, "https://census.daybreakgames.com/files/ps2/images/static/12.png"), 
            FactionConfig("Vanu Scum", self.faction_vs, 7419530, "https://census.daybreakgames.com/files/ps2/images/static/94.png")
            ], key=lambda x: x.percent, reverse=True) 

    def to_json_string(self):
        ordered_factions: List[FactionConfig] = self.order_factions()
        return  f"""{{
                "embeds": [{{
                    "title": "Alert {self.metagame_event_state_name}",
                    "description": "{self.metagame_event_name}",
                    "color": {3066993 if self.metagame_event_state_name == "started" else ordered_factions[0].color},
                    "timestamp": "{self.timestamp}",
                    "thumbnail": {{
                        "url": "{ordered_factions[0].image_url}"
                    }},
                    "fields": [
                        {{
                        "name": "Faction",
                        "value": "{ordered_factions[0].name}\\n\\n{ordered_factions[1].name}\\n\\n{ordered_factions[2].name}",
                        "inline": true
                        }},
                        {{
                        "name": "Percentage",
                        "value": "{ordered_factions[0].percent}%\\n\\n{ordered_factions[1].percent}%\\n\\n{ordered_factions[2].percent}%",
                        "inline": true
                        }}
                    ]
                }}]
                }}"""
