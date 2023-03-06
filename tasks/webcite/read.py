import sys

from core.utils.sqlite import create_database_table, webcite_db_name, save_pages_to_db
from tasks.webcite.module import get_pages


def main(*args: str) -> int:
    try:
        thread_number = 1
        time_before_start = int(sys.argv[1])

        if time_before_start == 2540:
            thread_number = 3
        elif time_before_start == 500:
            thread_number = 2

        pages = get_pages(time_before_start)
        conn, cursor = create_database_table(webcite_db_name)
        save_pages_to_db(pages, conn, cursor, thread_number=thread_number)
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
