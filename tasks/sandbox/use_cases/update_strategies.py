from abc import ABC, abstractmethod
from tasks.sandbox.entities.page_entity import PageEntity


class UpdateStrategy(ABC):
    @abstractmethod
    def prepare_content(self, current_content: str, new_content: str) -> str:
        """Prepare the content according to the strategy"""
        pass


class ReplaceContentStrategy(UpdateStrategy):
    def prepare_content(self, current_content: str, new_content: str) -> str:
        """Simply replace the entire content"""
        return new_content


class AppendContentStrategy(UpdateStrategy):
    def prepare_content(self, current_content: str, new_content: str) -> str:
        """Append new content to existing content"""
        return f"{current_content}\n{new_content}"


class PrependContentStrategy(UpdateStrategy):
    def prepare_content(self, current_content: str, new_content: str) -> str:
        """Add new content before existing content"""
        return f"{new_content}\n{current_content}" 