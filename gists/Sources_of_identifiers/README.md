## [اكود مهمة إزالة استشهادات خاطئة](https://ar.wikipedia.org/wiki/%D9%88%D9%8A%D9%83%D9%8A%D8%A8%D9%8A%D8%AF%D9%8A%D8%A7:%D8%A7%D9%84%D9%85%D9%8A%D8%AF%D8%A7%D9%86/%D8%AA%D9%82%D9%86%D9%8A%D8%A9/2023/%D9%8A%D9%88%D9%86%D9%8A%D9%88#%D8%A5%D8%B2%D8%A7%D9%84%D8%A9_%D8%A7%D8%B3%D8%AA%D8%B4%D9%87%D8%A7%D8%AF%D8%A7%D8%AA_%D8%AE%D8%A7%D8%B7%D8%A6%D8%A9)

# الاستعلام المستخدم في حصر التعديلات

```sql

SELECT page.page_id,
       page.page_namespace,
       page.page_title,
       revision_userindex.rev_id                            AS "main_edit",
       (SELECT MAX(rev_id)
        FROM revision_userindex AS prev_edit
        WHERE prev_edit.rev_page = page.page_id
          AND prev_edit.rev_id < revision_userindex.rev_id) AS "prev_edit",
       comment_text
FROM revision_userindex
         INNER JOIN page ON page.page_id = revision_userindex.rev_page
         inner join comment on revision_userindex.rev_comment_id = comment.comment_id
WHERE revision_userindex.rev_actor = 8
  and page.page_namespace = 0
  and page.page_is_redirect = 0
  and page.page_id not in (select categorylinks.cl_from
                           from categorylinks
                           where categorylinks.cl_to like "جميع_المقالات_بدون_مصدر"
                             and categorylinks.cl_type = "page")
  and (
            comment_text like "%بوت:إضافة مصدر (1)%"
        or comment_text like "%بوت:إضافة مصدر (1.1)%"
        or comment_text like "%بوت:إضافة مصدر (1.2)%" #or comment_text like "%بوت:إضافة مراجع معادلة%"
 # or comment_text like "%بوت:إصلاح مرجع%"
  or comment_text like "%بوت:إضافة مصدر من ويكي الإنجليزية أو الفرنسية (تجريبي)%"
  or comment_text like "%بوت:إضافة مصدر من ويكي الإنجليزية (تجريبي)%"
 or comment_text like "بوت:إضافة مصدر" #or comment_text like "إضافة مراجع"
    )
  and comment_text not like "%كووورة%"
ORDER BY revision_userindex.rev_id

```

عدد الصفوف:  111512

## from_csv_to_sqlite.py

يقوم بتحويل البيانات التي تم جلبها عبر الاستعلام السابق ونخزينها في قاعده بيانات

## load_diff.py

يجلب الفرق (الروابط التي تم اضافتها وليس فرق النص) بين النسخه القديمة والجديدة حتي يتم استخدمه في العمليه الاخصاء وعمليه
الاستبدال القادمة (المهمة نفسها)