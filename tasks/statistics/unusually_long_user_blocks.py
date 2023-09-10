from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """
SELECT
  ipb_address,
  actor_name,
  ipb_timestamp,
  ipb_expiry,
  comment_text
FROM
  ipblocks
  INNER JOIN actor_ipblocks ON ipb_by_actor = actor_id
  INNER JOIN comment_ipblocks ON ipb_reason_id = comment_id
WHERE
  ipb_expiry > DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 1 month), '%Y%m%d%H%i%s')
  AND ipb_expiry != "infinity"
  AND ipb_user != 0;
"""
file_path = 'stub/unusually_long_user_blocks.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/مستخدمين محظورين لمدة طويلة بشكل غير عادي"


def ipb_addres(row, result, index):
    ip = str(row['ipb_address'], 'utf-8')
    return "{{IPvandal| 1 = " + ip + "}}"


def user_name(row, result, index):
    user_name = str(row['actor_name'], 'utf-8')
    name = user_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + user_name + "|" + name + "]]"


def ipb_timestamp(row, result, index):
    return "{{نسخ:#time::H:i، j F Y|" + str(row['ipb_timestamp'], 'utf-8') + "}}"


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
