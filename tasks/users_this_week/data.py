"""
list_page_sub_pages is a list of dictionaries representing data for creating a subpage for a week's worth of activity for a particular activity on a wiki. Each dictionary in the list has the following keys:

"competition_page": a string representing the title of the main page for the week's worth of activity.
"title_of_page": a string representing the title of the subpage for the activity.
"summary": a string representing the summary to be used when saving the subpage.
"activity": a string representing the activity being recorded on the subpage (e.g. "articles", "article reviews").
"team": a string representing the top performers for the activity (e.g. "top 5 article creators").
"template_stub": a string representing the stub of a template to be used when sending a notification to a user.
"query": a string representing a SQL query to be used to retrieve data for the subpage.
"""
list_page_sub_pages = [
    {
        "competition_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
        "send_alert": True,
        "title_of_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER/مقالات",
        "summary": "بوت:تحديث [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
        "team": "المستخدمون الـ5 الأوائل في إنشاء المقالات",
        "activity": "مقالات",
        "template_stub": "{{وسام كاتب الأسبوع|WEEK_NUMBER YEAR_NUMBER|RANK|بعدد إنشاء المقالات|USER_NAME}}",
        'query': """SELECT actor_name as name, COUNT(*) as score
    FROM revision r
    INNER JOIN actor ON r.rev_actor = actor.actor_id
    INNER JOIN page p on r.rev_page = p.page_id
    WHERE p.page_namespace=0
    and p.page_is_redirect=0
    and r.rev_timestamp between START_WEEK_DATE and END_WEEK_DATE
    and r.rev_parent_id=0
     and ucase(actor_name) not like ucase("%BOT") COLLATE utf8mb4_general_ci
  and actor_name not like "%بوت%" collate utf8mb4_general_ci
  and actor_name Not IN (SELECT user_name
                         FROM user_groups
                                  INNER JOIN user ON user_id = ug_user
                         WHERE ug_group = "bot")
                         and actor_name not in (SELECT replace(pl_title,"_"," ")
FROM pagelinks
where pagelinks.pl_from = 7352181
and pl_namespace = 2)
    GROUP BY actor_name
    having COUNT(*) > 1
    ORDER BY score DESC,name
    LIMIT 10;"""
    },
    {
        "competition_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
        "send_alert": True,
        "title_of_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER/مراجعة المقالات",
        "summary": "بوت:تحديث [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
        "activity": "مراجعة للمقالات",
        "team": "أكثر 5 مستخدمين مراجعة للمقالات",
        "template_stub": "{{وسام مراجع مقالات الأسبوع|WEEK_NUMBER YEAR_NUMBER|RANK|بعدد مراجعة المقالات|USER_NAME}}",
        'query': """select
  actor_name as name,
  COUNT(*) as score
from
  logging
  INNER JOIN actor ON log_actor = actor.actor_id
where
  log_timestamp BETWEEN START_WEEK_DATE and END_WEEK_DATE
  and ucase(actor_name) not like ucase("%BOT") COLLATE utf8mb4_general_ci
  and actor_name not like "%بوت%" collate utf8mb4_general_ci
  and actor_name Not IN (SELECT user_name
                         FROM user_groups
                                  INNER JOIN user ON user_id = ug_user
                         WHERE ug_group = "bot")
  and log_action = "approve-i"
  and log_namespace = 0
  and actor_name not in (SELECT replace(pl_title,"_"," ")
FROM pagelinks
where pagelinks.pl_from = 7352181
and pl_namespace = 2)
group by actor_name
having COUNT(*) > 1
ORDER BY score DESC,name
LIMIT 10;"""

    },
    {
        "competition_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
        "send_alert": True,
        "title_of_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER/إدارة",
        "summary": "بوت:تحديث [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
        "activity": "أفعال إدارية",
        "team": "الإداريون الذين أجروا أكبر عدد من الأعمال الإدارية",
        "template_stub": "{{وسام إداري الأسبوع|WEEK_NUMBER YEAR_NUMBER|RANK|بعدد الأعمال الإدارية يدويا|USER_NAMEً}}",
        'query': """select actor_name as name, COUNT(*) as score
from logging
INNER JOIN actor on logging.log_actor = actor_id
where log_timestamp BETWEEN START_WEEK_DATE AND END_WEEK_DATE
and log_type in ("block", "protect", "delete", "rights")
and actor_name IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = 'sysop')
and actor_name not in (SELECT replace(pl_title,"_"," ")
and actor_user not null
FROM pagelinks
where pagelinks.pl_from = 7352181
and pl_namespace = 2)
group by logging.log_actor
having COUNT(*)>1
ORDER BY score DESC,name
LIMIT 10;"""

    },
    {
        "competition_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
        "send_alert": True,
        "title_of_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER/إضافة نصوص",
        "summary": "بوت:تحديث [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
        "team": "المستخدمون الـ 5 الأوائل في إضافة نصوص",
        "template_stub": "{{وسام الأسبوع 2|WEEK_NUMBER YEAR_NUMBER|RANK|بإضافة النصوص|USER_NAME}}",
        "activity": "إضافة نصوص",
        'query': """SELECT actor_name as name, SUM(CAST(rev.rev_len as signed)-CAST(parent.rev_len as signed)) AS score, COUNT(rev.rev_id) as edit_count
FROM revision rev
INNER JOIN actor on rev.rev_actor = actor_id
JOIN revision parent
ON rev.rev_parent_id = parent.rev_id
INNER JOIN comment_revision on rev.rev_comment_id = comment_id
JOIN page
ON page_id = parent.rev_page
WHERE page_namespace = 0
and comment_text not like "%رجوع%"
and comment_text not like "%استرجاع%"
AND rev.rev_timestamp BETWEEN START_WEEK_DATE AND END_WEEK_DATE
AND parent.rev_timestamp BETWEEN START_WEEK_DATE AND END_WEEK_DATE
  and ucase(actor_name) not like ucase("%BOT") COLLATE utf8mb4_general_ci
  and actor_name not like "%بوت%" collate utf8mb4_general_ci
  and actor_name Not IN (SELECT user_name
                         FROM user_groups
                                  INNER JOIN user ON user_id = ug_user
                         WHERE ug_group = "bot")
and actor_name IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = 'editor' or 'autoreview')
and actor_name not in (SELECT replace(pl_title,"_"," ")
and actor_user not null
FROM pagelinks
where pagelinks.pl_from = 7352181
and pl_namespace = 2)
GROUP BY actor_name
having score > 0
ORDER BY score DESC,name
LIMIT 10;"""

    },
    {
        "competition_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
        "send_alert": True,
        "title_of_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER/مراجعة التعديلات",
        "summary": "بوت:تحديث [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
        "activity": "مراجعة للتعديلات",
        "team": "أكثر 5 مستخدمين مراجعة للتعديلات",
        "template_stub": "{{وسام مراجع تعديلات الأسبوع|WEEK_NUMBER YEAR_NUMBER|RANK|بعدد مراجعة التعديلات المعلقة|USER_NAME}}",
        'query': """select actor_name as name, COUNT(*) as score
    from logging
    INNER JOIN actor ON actor.actor_id = logging.log_actor
    where log_timestamp BETWEEN START_WEEK_DATE AND END_WEEK_DATE
    and log_action = "approve"
    and log_namespace = 0

    and actor_name Not IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = 'bot')
     and ucase(actor_name) not like ucase("%BOT") COLLATE utf8mb4_general_ci
  and actor_name not like "%بوت%" collate utf8mb4_general_ci
and actor_name not in (SELECT replace(pl_title,"_"," ")
and actor_user not null
FROM pagelinks
where pagelinks.pl_from = 7352181
and pl_namespace = 2)
    group by logging.log_actor
    having COUNT(*)>1
    ORDER BY score DESC,name
	LIMIT 10;"""

    },
    {
        "competition_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
        "send_alert": True,
        "title_of_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER/تعديلات",
        "summary": "بوت:تحديث [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
        "team": "المستخدمون الـ5 الأوائل بعدد التعديلات",
        "template_stub": "{{وسام الأسبوع 1|WEEK_NUMBER YEAR_NUMBER|RANK|بعدد التعديلات هذا الأسبوع|USER_NAME}}",
        "activity": "تعديلات",
        'query': """SELECT actor_name as name, COUNT(rev.rev_id) as score
FROM revision rev
INNER JOIN actor on rev.rev_actor = actor_id
INNER JOIN comment_revision on rev.rev_comment_id = comment_id
JOIN page ON page_id = rev.rev_page
AND comment_text NOT LIKE ucase ("%[[ميدياويكي:Gadget-Cat-a-lot|تعديل تصنيفات]]%") collate utf8mb4_general_ci
    AND comment_text NOT LIKE ucase ("%[[Project:أوب|أوب]]%") collate utf8mb4_general_ci
    AND comment_text NOT LIKE ucase ("%[[ويكيبيديا:أوب|أوب]]%") collate utf8mb4_general_ci
AND rev.rev_timestamp BETWEEN START_WEEK_DATE AND END_WEEK_DATE
AND ucase(actor_name) NOT LIKE ucase("%BOT") COLLATE utf8mb4_general_ci
AND actor_name NOT LIKE "%بوت%" collate utf8mb4_general_ci
AND actor_name NOT IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = "bot")
and actor_name not in (SELECT replace(pl_title,"_"," ")
and actor_user not null
FROM pagelinks
where pagelinks.pl_from = 7352181
and pl_namespace = 2)
GROUP BY actor_name
HAVING score > 0
ORDER BY score DESC,name
LIMIT 10;"""
    },
    {
        "competition_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
        "send_alert": True,
        "title_of_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER/جدد",
        "summary": "بوت:تحديث [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
        "activity": "تعديلات",
        "team": "أنشط 5 مستخدمين بين المستخدمين الواعدين",
        "template_stub": "{{وسام الأسبوع 3|WEEK_NUMBER YEAR_NUMBER|RANK|بعدد التعديلات لحديثي التسجيل|USER_NAME}}",
        'query': """SELECT actor_name as name, COUNT(revision.rev_id) AS score
FROM user
INNER JOIN actor ON user_id = actor_user
INNER JOIN revision ON rev_actor = actor_id
INNER JOIN page ON page.page_id = revision.rev_page
LEFT JOIN ipblocks ON actor_user = ipb_user
WHERE rev_timestamp BETWEEN START_WEEK_DATE AND END_WEEK_DATE
AND user_registration BETWEEN DATE_BEFORE_30_DAYS and START_WEEK_DATE
AND page.page_namespace = 0
AND ipb_user IS NULL
AND ucase(actor_name) NOT LIKE ucase("%BOT") COLLATE utf8mb4_general_ci
AND actor_name NOT LIKE "%بوت%" collate utf8mb4_general_ci
and actor_name NOT IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = 'editor' or 'autoreview' or 'bot')
and actor_name not in (SELECT replace(pl_title,"_"," "
and actor_user not null
FROM pagelinks
where pagelinks.pl_from = 7352181
and pl_namespace = 2)
GROUP BY actor_name
ORDER BY score DESC,name
LIMIT 10;
"""
    },
    {
        "competition_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
        "send_alert": False,
        "title_of_page": "DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER/بوتات",
        "summary": "بوت:تحديث [[ويكيبيديا:مستخدمو الأسبوع الأكثر نشاطا|مشروع مستخدمو الأسبوع الأكثر نشاطًا]] (V1.1.0)",
        "team": "البوتات الـ5 الأوائل بعدد التعديلات",
        "template_stub": "{{وسام الأسبوع 1|WEEK_NUMBER YEAR_NUMBER|RANK|بعدد التعديلات هذا الأسبوع|USER_NAME}}",
        "activity": "تعديلات",
        'query': """SELECT actor_name as name, COUNT(rev.rev_id) as score
FROM revision rev
INNER JOIN actor on rev.rev_actor = actor_id
WHERE rev_timestamp BETWEEN START_WEEK_DATE AND END_WEEK_DATE
AND actor_name  IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = "bot")
and actor_name not in (SELECT replace(pl_title,"_"," ") FROM pagelinks where pagelinks.pl_from = 7352181 and pl_namespace = 2)
and actor_name not in (
	"New user message",
  	"MediaWiki message delivery",
  	"Flow talk page manager"
)
GROUP BY actor_name
HAVING score > 0
ORDER BY score DESC,name
LIMIT 15;"""
    },
]
