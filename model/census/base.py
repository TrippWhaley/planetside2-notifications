from abc import ABC
import json
from typing import Any, Dict, List
import requests

class Census(ABC):
    """
    Docs
    """
    version: str = "ps2:v2"
    data: Dict[str, str]

    def _get(self, model: str, limit: int = 100) -> List[Any]:
        
        return json.loads(requests.get(f"http://census.daybreakgames.com/json/get/{self.version}/{model}/?c:limit={limit}").text).get(f"{model}_list")

    
    def get(self, key: str = None) -> Any:
        if key is None:
            return self.data
        return self.data.get(key)