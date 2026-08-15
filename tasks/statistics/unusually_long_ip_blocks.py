from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """
SELECT
  bt_address,
  actor_name,
  bl_timestamp,
  bl_expiry,
  comment_text
FROM
  block
  INNER JOIN block_target bt ON block.bl_target = bt.bt_id
  INNER JOIN actor ON actor.actor_id = block.bl_by_actor
  INNER JOIN comment ON comment.comment_id = block.bl_reason_id
WHERE
  bl_expiry > DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 1 month), '%Y%m%d%H%i%s')
  AND bl_expiry != "infinity"
  AND bt_user IS NULL
  AND INSTR(LOWER(comment_text), 'proxy') = 0
  AND INSTR(LOWER(comment_text), 'بروكسيات مفتوحة') = 0
  AND INSTR(LOWER(comment_text), 'webhost') = 0;"""
file_path = 'stub/unusually_long_ip_blocks.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/عناوين IP المحظورة لمدة طويلة بشكل غير عادي"


def ipb_addres(row, result, index):
    ip = str(row['bt_address'], 'utf-8')
    return "{{IPvandal| 1 = " + ip + "}}"


def user_name(row, result, index):
    user_name = str(row['actor_name'], 'utf-8')
    name = user_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + user_name + "|" + name + "]]"


def ipb_timestamp(row, result, index):
    return "{{نسخ:#time::H:i، j F Y|" + str(row['bl_timestamp'], 'utf-8') + "}}"


columns = [
    ("الرقم", None, index),
    ("عنوان الip", None, ipb_addres),
    ("المستخدم الذي قام بعملية المنع", None, user_name),
    ("تاريخ المنع", None, ipb_timestamp),
    ("سبب المنع", None, lambda row, result, index: str(row['comment_text'], 'utf-8')),
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
