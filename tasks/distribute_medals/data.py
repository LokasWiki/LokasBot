list_of_distribute_medals = [
    {
        "number": 500,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 1000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 2000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 3000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 5000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 10000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 20000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 30000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 40000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 50000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 60000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 70000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 80000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 90000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 100000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 125000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 150000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 175000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 200000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 225000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 250000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 275000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 300000,
        "query": """SELECT actor_name,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) AS sum_yc,
       (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) AS sum_tc
FROM actor
WHERE (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp < START_DATE) < NUMBER_COUNT
AND (SELECT COUNT(*) FROM revision_userindex WHERE rev_actor = actor_id AND rev_timestamp <= END_DATE) >= NUMBER_COUNT
and actor_name not in (select REPLACE(lt_title as "pl_title, '_', ' ') from pagelinks inner join linktarget ON lt_id = pl_target_id where  pl_from = 7519882);""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
]
