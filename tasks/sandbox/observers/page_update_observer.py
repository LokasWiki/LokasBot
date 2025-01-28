from abc import ABC, abstractmethod
from datetime import datetime
from tasks.sandbox.entities.page_entity import PageEntity


class PageUpdateObserver(ABC):
    @abstractmethod
    def update(self, page: PageEntity) -> None:
        """Called when a page is updated"""
        pass


class ConsoleLogger(PageUpdateObserver):
    def update(self, page: PageEntity) -> None:
        """Log page updates to console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Updated page: {page.title}")
        print(f"Summary: {page.summary}")


class FileLogger(PageUpdateObserver):
    def __init__(self, log_file: str = "page_updates.log"):
        self.log_file = log_file

    def update(self, page: PageEntity) -> None:
        """Log page updates to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Updated page: {page.title}\n")
            f.write(f"Summary: {page.summary}\n\n") 