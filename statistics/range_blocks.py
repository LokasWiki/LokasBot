from module import UpdatePage, ArticleTables, index


class IPRangeCalculator:
    def __init__(self, ipb_address, ipb_range_start, ipb_range_end):
        self.ipb_address = ipb_address
        self.ipb_range_start = ipb_range_start
        self.ipb_range_end = ipb_range_end

    def get_ip_range(self):
        # split the ipb_address into its parts
        ipb_parts = self.ipb_address.split(":")
        # check if the address is an IPv4 or IPv6 address
        if len(ipb_parts) == 8:
            # this is an IPv6 address, we need to convert the start and end range to IPv6 format
            start_range = self.ipb_range_start.split("-")[1]
            end_range = self.ipb_range_end.split("-")[1]
            # convert the start and end range to integers
            start_range_int = int(start_range, 16)
            end_range_int = int(end_range, 16)
            # return the number of IPs in the range
            return end_range_int - start_range_int + 1
        else:
            # this is an IPv4 address, we need to convert the start and end range to IPv4 format
            start_range = self.ipb_range_start.split(".")
            end_range = self.ipb_range_end.split(".")
            # convert the start and end range to integers
            start_range_int = int(start_range[0])(2 ** 24) + int(start_range[1])(216) + int(start_range[2]) * (
                28) + int(start_range[3])
            end_range_int = int(end_range[0])(2 ** 24) + int(end_range[1])(216) + int(end_range[2]) * (28) + int(
                end_range[3])
            # return the number of IPs in the range
        return end_range_int - start_range_int + 1


# Set the parameters for the update
query = """SELECT
  ipb_address,
  ipb_range_start,
  ipb_range_end,
  actor_name,
  ipb_timestamp,
  ipb_expiry,
  comment_text
FROM ipblocks
inner join actor on actor.actor_id = ipblocks.ipb_by_actor
inner join comment on comment.comment_id = ipblocks.ipb_reason_id
WHERE ipb_address LIKE '%/%';"""
file_path = 'stub/range_blocks.txt'
page_name = "ويكيبيديا:إحصاءات/نطاقات الأيبيهات الممنوعة"

# Create an instance of the ArticleTables class
tables = ArticleTables()


def username(row, result, index):
    username = str(row['actor_name'], 'utf-8')
    return "[[User talk:" + username + "|" + username + "]]"


def ipb_address(row, result, index):
    return "{{ipr | 1 = " + str(row['ipb_address'], 'utf-8') + "}}"


def get_ip_range(row, result, index):
    ipb_address = str(row['ipb_address'], 'utf-8')
    ipb_range_start = str(row['ipb_range_start'], 'utf-8')
    ipb_range_end = str(row['ipb_range_end'], 'utf-8')
    ip_range_calculator = IPRangeCalculator(ipb_address, ipb_range_start, ipb_range_end)
    return str(ip_range_calculator.get_ip_range())


def ipb_timestamp(row, result, index):
    return "{{نسخ:#time::H:i، j F Y|" + str(row['ipb_timestamp'], 'utf-8') + "}}"


columns = [
    ("الرقم", None, index),
    ("النطاق", None, ipb_address),
    ("عدد الأيبيهات", None, get_ip_range),
    ("الإداري", None, username),
    ("تاريخ المنع", None, ipb_timestamp),
    ("تاريخ نهاية المنع", "ipb_expiry"),
    ("السبب", "comment_text"),
]

tables.add_table("main_table", columns)

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables)
updater.update()
