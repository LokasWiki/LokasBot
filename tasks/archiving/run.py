import pywikibot

from tasks.archiving.config import USER_CONFIG, TEMPLATE_NAME_KEY
from tasks.archiving.core.bot import HookManager, CompositeJob, ActionJob, Processor, Job


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


# Create the HookManager
hook_manager = HookManager()
# hook_manager.add_hook('before', before_hook)
# hook_manager.add_hook('after', after_hook)

# Create and configure the composite job
composite_job = CompositeJob(hook_manager=hook_manager)
composite_job.add_job(ActionJob())

# Create the processor with the composite job
processor = WikiPageProcessor(job=composite_job)
processor.process_items()
