import os

from tasks.copypatrol.config.config_loader import ConfigLoader
from tasks.copypatrol.data.database import Database
from tasks.copypatrol.data.mysql_copyright_repository import MySQLCopyrightRepository
from tasks.copypatrol.domain.use_cases.get_open_cases import GetOpenCases
from tasks.copypatrol.presentation.wiki_page_updater import WikiPageUpdater


def main():
    home_path = os.path.expanduser("~")
    config_path = os.path.join(home_path, 'config.ini')

    config_loader = ConfigLoader(config_path)
    db_config = config_loader.get_db_config()

    db = Database(db_config)
    try:
        # Repository layer
        repository = MySQLCopyrightRepository(db)

        # Use Case layer
        get_open_cases = GetOpenCases(repository)
        open_cases_count = get_open_cases.execute(lang='ar', project='wikipedia')

        # Presentation layer
        wiki_updater = WikiPageUpdater(site='ar', page_name="قالب:إحصاءات أداء كشف خرق حقوق النشر")
        wiki_updater.update_page(open_cases_count)
    finally:
        db.close()


if __name__ == "__main__":
    main()
