from tasks.statistics.module import UpdatePage, ArticleTables, index


class IPRangeCalculator:
    def __init__(self, bt_address, bt_range_start, bt_range_end):
        self.bt_address = bt_address
        self.bt_range_start = bt_range_start
        self.bt_range_end = bt_range_end

    def get_ip_range(self):
        # bt_range_start/bt_range_end are hexadecimal:
        # 8 chars for IPv4, 16 chars for IPv6
        start_range_int = int(self.bt_range_start, 16)
        end_range_int = int(self.bt_range_end, 16)
        return end_range_int - start_range_int + 1


# Set the parameters for the update
query = """SELECT
  bt_address,
  bt_range_start,
  bt_range_end,
  actor_name,
  bl_timestamp,
  bl_expiry,
  comment_text
FROM block
inner join block_target bt on block.bl_target = bt.bt_id
inner join actor on actor.actor_id = block.bl_by_actor
inner join comment on comment.comment_id = block.bl_reason_id
WHERE bt_address LIKE '%/%';"""
file_path = 'stub/range_blocks.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/نطاقات الأيبيهات الممنوعة"


def username(row, result, index):
    user_name = str(row['actor_name'], 'utf-8')
    return "[[User talk:" + user_name + "|" + user_name + "]]"


def ipb_address(row, result, index):
    return "{{ipr | 1 = " + str(row['bt_address'], 'utf-8') + "}}"


def get_ip_range(row, result, index):
    bt_address = str(row['bt_address'], 'utf-8')
    bt_range_start = str(row['bt_range_start'], 'utf-8')
    bt_range_end = str(row['bt_range_end'], 'utf-8')
    ip_range_calculator = IPRangeCalculator(bt_address, bt_range_start, bt_range_end)
    return str(ip_range_calculator.get_ip_range())


def ipb_timestamp(row, result, index):
    return "{{نسخ:#time::H:i، j F Y|" + str(row['bl_timestamp'], 'utf-8') + "}}"


columns = [
    ("الرقم", None, index),
    ("النطاق", None, ipb_address),
    ("عدد الأيبيهات", None, get_ip_range),
    ("الإداري", None, username),
    ("تاريخ المنع", None, ipb_timestamp),
    ("تاريخ نهاية المنع", "bl_expiry"),
    ("السبب", "comment_text"),
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
