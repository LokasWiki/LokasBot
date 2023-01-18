from module import UpdatePage, ArticleTables, index

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
WHERE ug_group = "sysop"
ORDER BY user_name ASC , delete_count DESC, restore_count DESC, revision_count DESC, event_count DESC, protect_count DESC, unprotect_count DESC, modify_count DESC, block_count DESC, unblock_count DESC, reblock_count DESC, rights_count DESC;"""

file_path = 'stub/administrators_activity.txt'
page_name = "ويكيبيديا:إحصاءات/نشاط الإداريين"

# Create an instance of the ArticleTables class
tables = ArticleTables()


def start_table(word):
    start = """<div class="NavFrame collapsed" style="text-align:right">
  <div class="NavHead" style="font-size: 10pt;">&nbsp; WORD </div>
    <div class="NavContent">
<div style="text-align: right;">"""
    return "\n\n" + start.replace("WORD", word) + "\n\n"


def end_table():
    end = """الإحصاءات الكاملة متوفرة في [[{{FULLPAGENAME}}#الإحصاءات الكاملة|الأسفل]].
</div>
</div>
</div>"""
    return "\n\n" + end + "\n\n"



def start_main_table(word):
    start = """== WORD =="""
    return "\n\n" + start.replace("WORD", word) + "\n\n"


def end_main_table():
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


tables.add_table("delete_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "delete_count"), ],
                 start_table("حذف"), end_table())
tables.add_table("restore_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "restore_count"), ],
                 start_table("استرجاع"), end_table())
tables.add_table("revision_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "revision_count"), ],
                 start_table("إخفاء نسخة"), end_table())
tables.add_table("event_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "event_count"), ],
                 start_table("  حذف النسخة المُعدله"), end_table())
tables.add_table("protect_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "protect_count"), ],
                 start_table("حماية"), end_table())
tables.add_table("unprotect_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "unprotect_count"), ],
                 start_table("  إزالة الحماية"), end_table())
tables.add_table("modify_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "modify_count"), ],
                 start_table("تغيير الحماية"), end_table())
tables.add_table("block_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "block_count"), ],
                 start_table("  منع "), end_table())
tables.add_table("unblock_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "unblock_count"), ],
                 start_table("    رفع المنع"), end_table())
tables.add_table("reblock_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "reblock_count"), ],
                 start_table("  تغيير مدة المنع"), end_table())
tables.add_table("rights_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "rights_count"), ],
                 start_table("  تغيير صلاحيات"), end_table())

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
    ("المحموع", None, total),

]

tables.add_table("main_table", columns,start_main_table("الإحصاءات الكاملة"),end_main_table())

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables)
updater.update()
