import datetime

from tasks.check_usernames.core.factory.factory import DatabaseFactory
from tasks.check_usernames.core.models.user import User

# Get yesterday's date
yesterday = datetime.date.today() - datetime.timedelta(days=1)

# Get start time for yesterday
start_time = datetime.datetime.combine(yesterday, datetime.time.min)

# Get last time for yesterday
last_time = datetime.datetime.combine(yesterday, datetime.time.max)

# Format dates for SQL query
start_time_sql = start_time.strftime("%Y%m%d%H%M%S")
# start_time_sql = 20221207000000
last_time_sql = last_time.strftime("%Y%m%d%H%M%S")
# last_time_sql = 20230322235959


factory = DatabaseFactory()

mysql_repository = factory.create_mysql_repository()

query = """ select log_title as "q_log_title",log_id as "q_log_id"
            from logging
            where log_type in ("newusers")
            and log_timestamp BETWEEN {} AND {}
            and log_title not in (
              select page.page_title from categorylinks
              inner join page on page.page_id = categorylinks.cl_from
              where cl_to like "أسماء_مستخدمين_مخالفة_مرشحة_للمنع"
              and cl_type in ("page")
            )
            and log_title not in (
                select replace(user.user_name," ","_") as "user_name_temp" from ipblocks
                inner join user on ipblocks.ipb_user = user.user_id
            )
            """.format(start_time_sql, last_time_sql)

users_models = []
raw_users = mysql_repository.selectAllUsers(query=query)

for row in raw_users:
    users_models.append(
        User(
            id=row["q_log_id"],
            user_name=str(row["q_log_title"], 'utf-8'),
            created_at=datetime.datetime.now()
        )
    )

sqlite_repository = factory.create_sqlite_memory_repository()
sqlite_repository.createUserTable()
sqlite_repository.deleteAllUsers()
sqlite_repository.saveUsers(users_models)
