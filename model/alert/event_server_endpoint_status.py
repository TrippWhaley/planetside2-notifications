from typing import Any, Dict, Optional
from .base import Alert


class EventServerEndpointStatus(Alert):
    def __init__(self, detail: str, online: str, service: str, type: str, **kwargs):
        self.detail = detail
        self.online = "online" if online == "true" else "offline"
        self.service = service
        self.type = type

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional["EventServerEndpointStatus"]:
        if data.get("detail") is not None:
            return EventServerEndpointStatus(**data)
        return None

    def _get_world(self):
        s = self.detail
        return s[s.find("_") + 1 : s.rfind("_")]

    def to_string(self):
        return f"Event Server Endpoint: {self.online} for {self._get_world()}"
