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


class LoggingJob(Job):
    def perform(self, page):
        # Log the page title or other information
        print(f"Logging information for page: {page.title()}")
        logging.info(f"Logging information for page: {page.title()}")


# Define a HookManager for dynamic hooks
class HookManager:
    def __init__(self):
        self.hooks: Dict[str, List[Callable]] = {
            'before': [],
            'main': [],
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


# Concrete implementation for WikiPage processing
class WikiPageProcessor(Processor):
    def __init__(self, job: Job):
        super().__init__(job)
        self.site = pywikibot.Site('ar', 'wikipedia')
        self.template_name = USER_CONFIG.get(TEMPLATE_NAME_KEY)
        self.template_page = pywikibot.Page(self.site, self.template_name)

    def get_items(self):
        pages = self.template_page.embeddedin()
        filtered_pages = [
            page for page in pages
            if page.depth == 0 and not ('edit' in page.protection() and 'sysop' in page.protection()['edit'])
        ]
        return filtered_pages


# Example hook functions
def before_hook(item):
    print(f"Before processing item: {item.title()}")


def after_hook(item):
    print(f"After processing item: {item.title()}")


# Usage
# Create the HookManager
hook_manager = HookManager()
hook_manager.add_hook('before', before_hook)
hook_manager.add_hook('after', after_hook)

# Create and configure the composite job
composite_job = CompositeJob(hook_manager=hook_manager)
composite_job.add_job(ActionJob())
composite_job.add_job(LoggingJob())

# Create the processor with the composite job
processor = WikiPageProcessor(job=composite_job)
processor.process_items()
