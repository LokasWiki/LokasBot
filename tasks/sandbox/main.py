from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.repositories.repository_factory import RepositoryFactory, RepositoryType
from tasks.sandbox.use_cases.update_page_use_case import UpdatePageUseCase
from tasks.sandbox.observers.page_update_observer import ConsoleLogger, FileLogger
from tasks.sandbox.use_cases.update_strategies import ReplaceContentStrategy


def main() -> int:
    # Create repository using factory
    repository = RepositoryFactory.create_repository(RepositoryType.PYWIKIBOT)
    
    # Create use case and add observers
    use_case = UpdatePageUseCase(repository)
    use_case.add_observer(ConsoleLogger())
    use_case.add_observer(FileLogger("sandbox_updates.log"))
    
    # Set update strategy
    use_case.set_strategy(ReplaceContentStrategy())

    # Define the page to update with new content
    page_entity = PageEntity(
        title="ويكيبيديا:ملعب",
        text="{{عنوان الملعب}}\n<!-- مرحبا! خذ راحتك في تجربة مهارتك في التنسيق والتحرير أسفل هذا السطر. هذه الصفحة لتجارب التعديل ، سيتم تفريغ هذه الصفحة كل 12 ساعة. -->",
        summary="بوت: إفراغ الصفحة تلقائيا!"
    )

    # Execute the use case to update the page
    use_case.execute(page_entity)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
