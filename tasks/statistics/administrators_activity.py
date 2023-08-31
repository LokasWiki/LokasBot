from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT user_name,

           (select count(*) from logging
                    inner join actor on actor_id = log_actor
                    where actor_user = user_id and log_type = "delete"  and log_action not in ("delete_redir","restore") ) as "delete_count",
           (select count(*) from logging
                    inner join actor on actor_id = log_actor
                    where actor_user = user_id and log_type = "delete" and log_action = "restore" ) as "restore_count",

           (select count(*) from logging
                    inner join actor on actor_id = log_actor
                    where actor_user = user_id and log_type = "delete" and log_action = "revision" ) as "revision_count",
           (select count(*) from logging
                    inner join actor on actor_id = log_actor
                    where actor_user = user_id and log_type = "delete" and log_action = "event"  ) as "event_count",
           (select count(*) from logging
                    inner join actor on actor_id = log_actor
                    where actor_user = user_id and log_type = "protect" and log_action in("modify","protect")) as "protect_count",
       (select count(*) from logging
                                 inner join actor on actor_id = log_actor
        where actor_user = user_id and log_type = "protect" and log_action = "unprotect") as "unprotect_count",
       (select count(*) from logging
                                 inner join actor on actor_id = log_actor
        where actor_user = user_id and log_type = "protect" and log_action = "modify") as "modify_count",
       (select count(*) from logging
                                 inner join actor on actor_id = log_actor
        where actor_user = user_id and log_type = "block" ) as "block_count",
       (select count(*) from logging
                                 inner join actor on actor_id = log_actor
        where actor_user = user_id and log_type = "block" and log_action = "unblock") as "unblock_count",
       (select count(*) from logging
                                 inner join actor on actor_id = log_actor
        where actor_user = user_id and log_type = "block" and log_action = "reblock") as "reblock_count",
       (select count(*) from logging
                                 inner join actor on actor_id = log_actor
        where actor_user = user_id and log_type = "rights" ) as "rights_count"
FROM user
         JOIN user_groups ON user_id = ug_user
WHERE ug_group = "sysop" and user_name not in ("مرشح الإساءة")
ORDER BY user_name ASC , delete_count DESC, restore_count DESC, revision_count DESC, event_count DESC, protect_count DESC, unprotect_count DESC, modify_count DESC, block_count DESC, unblock_count DESC, reblock_count DESC, rights_count DESC;"""

file_path = 'stub/administrators_activity.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/نشاط الإداريين"


def start_table(result):
    start = """<div class="NavFrame collapsed" style="text-align:right">
  <div class="NavHead" style="font-size: 10pt;">&nbsp; TABLE_NAME </div>
    <div class="NavContent">
<div style="text-align: right;">"""
    return "\n\n" + start + "\n\n"


def end_table(result):
    end = """الإحصاءات الكاملة متوفرة في [[{{FULLPAGENAME}}#الإحصاءات الكاملة|الأسفل]].
</div>
</div>
</div>"""
    return "\n\n" + end + "\n\n"


def start_main_table(result):
    start = """== TABLE_NAME =="""
    return "\n\n" + start + "\n\n"


def end_main_table(result):
    end = """ """
    return "\n\n" + end + "\n\n"


def username(row, result, index):
    username = str(row['user_name'], 'utf-8')
    name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + username + "|" + name + "]]"


def total(row, result, index):
    number = 0
    user_name = str(row['user_name'], 'utf-8')
    del row['user_name']
    number = sum(row.values())
    # to avoid raising any errors
    return number


def end_row_in_main(result):
    total = {'delete_count': 0, 'restore_count': 0, 'revision_count': 0, 'event_count': 0, 'protect_count': 0,
             'unprotect_count': 0,
             'modify_count': 0, 'block_count': 0, 'unblock_count': 0, 'reblock_count': 0, 'rights_count': 0}
    for row in result:
        for key in total:
            total[key] += row[key]

    text = f"""\n|- class="sortbottom"
    ! colspan="2" | المجموع
    ! style="text-align:left;" | {total['delete_count']}
    ! style="text-align:left;" | {total['restore_count']}
    ! style="text-align:left;" | {total['revision_count']}
    ! style="text-align:left;" | {total['protect_count']}
    ! style="text-align:left;" | {total['unprotect_count']}
    ! style="text-align:left;" | {total['modify_count']}
    ! style="text-align:left;" | {total['block_count']}
    ! style="text-align:left;" | {total['unblock_count']}
    ! style="text-align:left;" | {total['reblock_count']}
    ! style="text-align:left;" | {total['rights_count']}
    ! style="text-align:left;" | {sum(total.values())}
    \n"""
    return text


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("حذف", "delete_count"),
    ("استرجاع", "restore_count"),
    ("إخفاء نسخة", "revision_count"),
    ("حماية", "protect_count"),
    ("إزالة الحماية", "unprotect_count"),
    ("تغيير الحماية", "modify_count"),
    ("المنع", "block_count"),
    ("رفع المنع", "unblock_count"),
    ("تغيير مدة المنع", "reblock_count"),
    ("تغيير صلاحيات", "rights_count"),
    ("المجموع", None, total),

]


def main(*args: str) -> int:
    # Create an instance of the ArticleTables class
    tables = ArticleTables()

    tables.add_table("حذف",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "delete_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column='delete_count')
    tables.add_table("استرجاع",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "restore_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="restore_count")
    tables.add_table("إخفاء نسخة",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "revision_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="revision_count")
    tables.add_table("  حذف النسخة المُعدله",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "event_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="event_count")
    tables.add_table("حماية",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "protect_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="protect_count")
    tables.add_table("  إزالة الحماية",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "unprotect_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="unprotect_count")
    tables.add_table("تغيير الحماية",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "modify_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="modify_count")
    tables.add_table("  منع ",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "block_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="block_count")
    tables.add_table("    رفع المنع",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "unblock_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="unblock_count")
    tables.add_table("  تغيير مدة المنع",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "reblock_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="reblock_count")
    tables.add_table("  تغيير صلاحيات",
                     [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "rights_count"), ],
                     header_text=start_table, footer_text=end_table, sort_column="rights_count")

    tables.add_table("الإحصاءات الكاملة", columns, header_text=start_main_table, footer_text=end_main_table,
                     end_row_text=end_row_in_main)

    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables)
    updater.update()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
