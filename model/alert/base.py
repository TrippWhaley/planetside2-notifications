from abc import ABC, abstractmethod
import requests
from typing import Any, Dict, Optional


class Alert(ABC):
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def to_json_string(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data: Dict[str, Any]) -> Optional["Alert"]:
        pass

    def send_discord(self, discord_webhook: str) -> None:
        headers = {'Content-type': 'application/json'}
        return requests.post(url=discord_webhook, data=self.to_json_string(), headers=headers)
