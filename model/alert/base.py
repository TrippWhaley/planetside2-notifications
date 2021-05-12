from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Alert(ABC):
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data: Dict[str, Any]) -> Optional["Alert"]:
        pass