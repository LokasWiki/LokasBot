import datetime

# Get yesterday's date
yesterday = datetime.date.today() - datetime.timedelta(days=1)

# Get start time for yesterday
start_time = datetime.datetime.combine(yesterday, datetime.time.min)

# Get last time for yesterday
last_time = datetime.datetime.combine(yesterday, datetime.time.max)

# Format dates for SQL query
start_time_sql = start_time.strftime("%Y%m%d%H%M%S")
last_time_sql = last_time.strftime("%Y%m%d%H%M%S")

# Use start_time_sql and last_time_sql in your SQL query
query = f"SELECT * FROM my_table WHERE date BETWEEN '{start_time_sql}' AND '{last_time_sql}'"

print(query)