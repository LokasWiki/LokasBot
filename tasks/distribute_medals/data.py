list_of_distribute_medals = [
    {
        "number": 500,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 1000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 2000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 3000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 5000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 10000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 20000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 30000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 40000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 50000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 60000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 70000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 80000,
        "query": """WITH revision_counts AS (
            SELECT 
                rev_actor,
                SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
                SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
            FROM revision_userindex
            GROUP BY rev_actor
            HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
        ),
        excluded_actors AS (
            SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
            FROM pagelinks 
            INNER JOIN linktarget ON lt_id = pl_target_id 
            WHERE pl_from = 7519882
        )
        SELECT 
            a.actor_name, 
            rc.sum_yc, 
            rc.sum_tc
        FROM 
            actor a
        JOIN 
            revision_counts rc ON a.actor_id = rc.rev_actor
        LEFT JOIN 
            excluded_actors ea ON a.actor_name = ea.pl_title
        WHERE 
            ea.pl_title IS NULL;
        """,
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 90000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 100000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 125000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 150000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 175000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 200000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 225000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 250000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 275000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
    {
        "number": 300000,
        "query": """WITH revision_counts AS (
    SELECT 
        rev_actor,
        SUM(CASE WHEN rev_timestamp < START_DATE THEN 1 ELSE 0 END) AS sum_yc,
        SUM(CASE WHEN rev_timestamp <= END_DATE THEN 1 ELSE 0 END) AS sum_tc
    FROM revision_userindex
    GROUP BY rev_actor
    HAVING sum_yc < NUMBER_COUNT AND sum_tc >= NUMBER_COUNT
),
excluded_actors AS (
    SELECT REPLACE(lt_title, '_', ' ') AS pl_title 
    FROM pagelinks 
    INNER JOIN linktarget ON lt_id = pl_target_id 
    WHERE pl_from = 7519882
)
SELECT 
    a.actor_name, 
    rc.sum_yc, 
    rc.sum_tc
FROM 
    actor a
JOIN 
    revision_counts rc ON a.actor_id = rc.rev_actor
LEFT JOIN 
    excluded_actors ea ON a.actor_name = ea.pl_title
WHERE 
    ea.pl_title IS NULL;
""",
        "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
    },
]
