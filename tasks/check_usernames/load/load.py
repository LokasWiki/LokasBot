from core.utils.wikidb import Database

db = Database()
db.query = """select log_title from logging
where log_type in ("newusers")
#todo: make it 24 only
and log_timestamp > DATE_SUB(NOW(), INTERVAL 1 day)"""
db.get_content_from_database()
names = []
for row in db.result:
    name = str(row['log_title'], 'utf-8')
    names.append(name)
