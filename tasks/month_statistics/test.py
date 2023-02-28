import datetime

# Get the current date
now = datetime.datetime.now()

# Calculate the first day of the previous month
first_day_of_month = datetime.date(now.year, now.month, 1)
previous_month = first_day_of_month - datetime.timedelta(days=1)
previous_month_first_day = datetime.date(previous_month.year, previous_month.month, 1)

# Calculate the last day of the previous month
last_day_of_previous_month = previous_month_first_day - datetime.timedelta(days=1)

# Format the start and end times for the previous month in the format "%Y%m%d%H%M%S"
previous_month_start_time = previous_month_first_day.strftime("%Y%m%d") + '000000'
previous_month_end_time = last_day_of_previous_month.strftime("%Y%m%d") + '235959'

# Use these values in your SQL query
sql_query = f"SELECT * FROM my_table WHERE date BETWEEN '{previous_month_start_time}' AND '{previous_month_end_time}'"

print(sql_query)