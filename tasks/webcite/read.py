import sys
from tasks.webcite.module import create_database_table, get_pages, save_pages_to_db


def main(*args: str) -> int:
    try:
        time_before_start = int(sys.argv[1])
        pages = get_pages(time_before_start)
        conn, cursor = create_database_table()
        save_pages_to_db(pages, conn, cursor)
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
