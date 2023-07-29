from tasks.statistics.module import UpdatePage, ArticleTables

# Set the parameters for the update
query = """SELECT
    afl_filter_id,
    SUM(CASE WHEN DATE(afl_timestamp) = CURDATE() - INTERVAL 6 DAY THEN 1 ELSE 0 END) AS hit_in_day_1,
    SUM(CASE WHEN DATE(afl_timestamp) = CURDATE() - INTERVAL 5 DAY THEN 1 ELSE 0 END) AS hit_in_day_2,
    SUM(CASE WHEN DATE(afl_timestamp) = CURDATE() - INTERVAL 4 DAY THEN 1 ELSE 0 END) AS hit_in_day_3,
    SUM(CASE WHEN DATE(afl_timestamp) = CURDATE() - INTERVAL 3 DAY THEN 1 ELSE 0 END) AS hit_in_day_4,
    SUM(CASE WHEN DATE(afl_timestamp) = CURDATE() - INTERVAL 2 DAY THEN 1 ELSE 0 END) AS hit_in_day_5,
    SUM(CASE WHEN DATE(afl_timestamp) = CURDATE() - INTERVAL 1 DAY THEN 1 ELSE 0 END) AS hit_in_day_6,
    SUM(CASE WHEN DATE(afl_timestamp) = CURDATE() THEN 1 ELSE 0 END) AS hit_in_day_7,
    abuse_filter.af_public_comments,
    abuse_filter.af_hidden
FROM
    abuse_filter_log 
INNER JOIN
    abuse_filter ON abuse_filter.af_id = abuse_filter_log.afl_filter_id
WHERE
    afl_timestamp >= NOW() - INTERVAL 1 WEEK
    AND abuse_filter.af_enabled = 1
    AND abuse_filter.af_deleted = 0
GROUP BY
    afl_filter_id, abuse_filter.af_public_comments
ORDER BY
    afl_filter_id;
"""
file_path = 'stub/filters_blow_in_the_last_week.txt'
page_name = "مستخدم:LokasBot/ضربات المرشحات في آخر أسبوع"


def afl_filter_id(row, result, index):
    id = str(row['afl_filter_id'])
    return "[[Special:AbuseFilter/" + id + "|" + id + "]]"


def afl_public_comments(row, result, index):
    af_public_comments = str(row['af_public_comments'], 'utf-8')
    return af_public_comments


def is_hidden(row, result, index):
    af_hidden = str(row['af_hidden'])
    template_of_hidden_status = af_hidden == "1" and "نعم" or "لا"
    return "{{" + template_of_hidden_status + "}}"


def day_1(row, result, index):
    number_of_hits = str(row['hit_in_day_1'])
    return number_of_hits


def day_2(row, result, index):
    return str(row['hit_in_day_2'])


def day_3(row, result, index):
    return str(row['hit_in_day_3'])


def day_4(row, result, index):
    return str(row['hit_in_day_4'])


def day_5(row, result, index):
    return str(row['hit_in_day_5'])


def day_6(row, result, index):
    return str(row['hit_in_day_6'])


def day_7(row, result, index):
    return str(row['hit_in_day_7'])


def user_registration(row, result, index):
    last_edit_date = str(row['last_edit_date'], 'utf-8')
    return "{{نسخ:#time:j F Y|" + last_edit_date + "}}"


columns = [
    ("#", None, afl_filter_id),
    ("الوصف", None, afl_public_comments),
    ("مخفي", None, is_hidden),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-0 days}}}}", None, day_7),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-1 days}}}}", None, day_6),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-2 days}}}}", None, day_5),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-3 days}}}}", None, day_4),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-4 days}}}}", None, day_3),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-5 days}}}}", None, day_2),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-6 days}}}}", None, day_1),

]


def main(*args: str) -> int:
    # Create an instance of the ArticleTables class
    tables = ArticleTables()
    tables.add_table("main_table", columns)

    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables)
    updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
