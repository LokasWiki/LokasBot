import os

from sqlalchemy import create_engine

home_path = os.path.expanduser("~")
# todo : merge it in one database
maintenance_database_path = os.path.join(home_path, "maintenance.db")
webcite_database_path = os.path.join(home_path, "webcite.db")
statistics_database_path = os.path.join(home_path, "statistics.db")

maintenance_engine = create_engine(f"sqlite+pysqlite:////{maintenance_database_path}", echo=False)

webcite_engine = create_engine(f"sqlite+pysqlite:////{webcite_database_path}", echo=False)

statistics_engine = create_engine(f"sqlite+pysqlite:////{statistics_database_path}", echo=False)

