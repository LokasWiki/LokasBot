import os

from sqlalchemy import create_engine

home_path = os.path.expanduser("~")
database_path = os.path.join(home_path, "requests.db")

engine = create_engine(f"sqlite+pysqlite:////{database_path}",echo=False)
