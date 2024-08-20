from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.repositories.pywikibot_page_repository import PywikibotPageRepository
from tasks.sandbox.use_cases.update_page_use_case import UpdatePageUseCase


def main() -> int:
    page_entity = PageEntity(
        title="ويكيبيديا:ملعب",
        text="{{عنوان الملعب}}\n<!-- مرحبا! خذ راحتك في تجربة مهارتك في التنسيق والتحرير أسفل هذا السطر. هذه الصفحة لتجارب التعديل ، سيتم تفريغ هذه الصفحة كل 12 ساعة. -->",
        summary="بوت: إفراغ الصفحة تلقائيا!"
    )

    repository = PywikibotPageRepository()
    use_case = UpdatePageUseCase(repository)
    use_case.execute(page_entity)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
