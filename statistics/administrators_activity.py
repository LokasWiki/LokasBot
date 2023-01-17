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


def username(row, result, index):
    username = str(row['user_name'], 'utf-8')
    name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + username + "|" + name + "]]"


def total(row, result, index):
    # get total action for every users
    pass


tables.add_table("delete_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "delete_count"), ])
tables.add_table("restore_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "restore_count"), ])
tables.add_table("revision_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "revision_count"), ])
tables.add_table("event_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "event_count"), ])
tables.add_table("protect_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "protect_count"), ])
tables.add_table("unprotect_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "unprotect_count"), ])
tables.add_table("modify_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "modify_count"), ])
tables.add_table("block_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "block_count"), ])
tables.add_table("unblock_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "unblock_count"), ])
tables.add_table("reblock_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "reblock_count"), ])
tables.add_table("rights_count_table",
                 [("الرقم", None, index), ("المستخدم", None, username), ("العدد", "rights_count"), ])

columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("حذف", "delete_count"),
    ("استرجاع", "restore_count"),
    ("إخفاء نسخة", "revision_count"),
    ("حماية", "protect_count"),
    ("إزالة الحماية", "unprotect_count"),
    ("تغيير الحماية", "modify_count"),
    ("المنع", "delete_count"),
    ("رفع المنع", "delete_count"),
    ("تغيير مدة المنع", "delete_count"),
    ("تغيير صلاحيات", "delete_count"),
    ("المحموع", "delete_count"),

]

tables.add_table("main_table", columns)

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables)
updater.update()
