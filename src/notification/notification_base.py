from abc import ABC, abstractmethod
from typing import Dict
from src.core.checker import Recipient


class NotificationBase(ABC):
    @abstractmethod
    def render_content(self, name: str, template_file: str, extra_info: Dict) -> str:
        pass

    @abstractmethod
    async def send(self, recipient: Recipient, content: str, days_until: int, age: int):
        pass
