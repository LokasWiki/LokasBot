list_of_distribute_medals = [
    {
        "number": 500,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 1000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 2000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 3000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 5000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 10000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 20000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 30000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 40000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 50000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 60000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 70000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 80000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 90000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 100000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 125000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 150000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 175000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
    {
        "number": 200000,
        "query" : """SELECT actor_name,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS revisions_until_yesterday,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) AS total_edits
FROM actor
WHERE (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id  AND rev_timestamp > END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(pl_title, '_', ' ') from pagelinks where  pl_from = 7519882)
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE}}"
    },
]
