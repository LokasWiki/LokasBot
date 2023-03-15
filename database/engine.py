import os

from sqlalchemy import create_engine

home_path = os.path.expanduser("~")
# todo : merge it in one database
maintenance_database_path = os.path.join(home_path, "maintenance.db")
webcite_database_path = os.path.join(home_path, "webcite.db")

maintenance_engine = create_engine(f"sqlite+pysqlite:////{database_path}", echo=False)

webcite_engine = create_engine(f"sqlite+pysqlite:////{database_path}", echo=False)

