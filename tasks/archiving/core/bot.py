import pywikibot
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Callable
from tasks.archiving.config import USER_CONFIG, TEMPLATE_NAME_KEY


# Define the Job interface
class Job(ABC):
    @abstractmethod
    def perform(self, item):
        """
        Perform an action on the given item.
        :param item: The item to process, e.g., a page or a file
        """
        pass


# Implement concrete strategies for different jobs
class ActionJob(Job):
    def perform(self, page):
        # Implement specific action here
        print(f"Performing action on page: {page.title()}")
        logging.info(f"Performing action on page: {page.title()}")



# Define a HookManager for dynamic hooks
class HookManager:
    def __init__(self):
        self.hooks: Dict[str, List[Callable]] = {
            'before': [],
            # 'main': [],
            'after': []
        }

    def add_hook(self, point: str, hook: Callable):
        if point in self.hooks:
            self.hooks[point].append(hook)

    def remove_hook(self, point: str, hook: Callable):
        if point in self.hooks:
            self.hooks[point].remove(hook)

    def run_hooks(self, point: str, item):
        if point in self.hooks:
            for hook in self.hooks[point]:
                hook(item)


# Define the CompositeJob class to handle multiple jobs
class CompositeJob(Job):
    def __init__(self, hook_manager: HookManager):
        self.jobs: List[Job] = []
        self.hook_manager = hook_manager

    def add_job(self, job: Job):
        self.jobs.append(job)

    def perform(self, item):
        # Run before hooks
        self.hook_manager.run_hooks('before', item)

        # Execute main jobs
        for job in self.jobs:
            job.perform(item)

        # Run after hooks
        self.hook_manager.run_hooks('after', item)


# Define the abstract Processor class
class Processor(ABC):
    def __init__(self, job: Job):
        self.job = job  # Dependency injection of Job strategy

    @abstractmethod
    def get_items(self):
        """
        Retrieve the items to be processed.
        :return: A list of items to process
        """
        pass

    def process_items(self):
        items = self.get_items()
        for item in items:
            self.job.perform(item)  # Delegate action to the injected Job strategy


# Example hook functions
def before_hook(item):
    print(f"Before processing item: {item.title()}")


def after_hook(item):
    print(f"After processing item: {item.title()}")

