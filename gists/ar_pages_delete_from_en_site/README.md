## خطوات تنفيذ مهمة جلب الصفحات التي تتواجد في النسخة العربية ولها مقابل في النسخة الإنجليزية وتم حذقه هنا

الهدف من هذه المهمة حذف هذه الصفحات أو مراجعتها لأنها غالبا تكون عبارة عن صفحات لا تحتوي علي الملحوظية اللازمة أو أنها من
إنشاء مخرب أو دمية جورب

## الاستعلام

في البداية تقوم بتغشيل الاستعلام  الذي يجلب الصفحات التي تم حذفها من ويكي الانجليزيه ولها مقابل في العربيه عبر ويكي بيانات

```
SELECT
comment.comment_text AS "deleted_page",
revision_userindex.rev_timestamp AS "date_of_delete",
wb_items_per_site.ips_site_page AS "name_of_page"
FROM
(SELECT page_id, page_title FROM page WHERE page_namespace = 0) AS page
JOIN revision_userindex ON page.page_id = revision_userindex.rev_page
JOIN comment ON comment.comment_id = revision_userindex.rev_comment_id
JOIN wb_items_per_site ON wb_items_per_site.ips_item_id = REPLACE(page.page_title, "Q", "")
WHERE
comment.comment_text LIKE "%clientsitelink-remove%"
AND comment.comment_text LIKE "%enwiki%"
#AND rev_timestamp > (NOW() - INTERVAL 1 MONTH)
AND year(rev_timestamp) in (2023)
AND wb_items_per_site.ips_site_id = "arwiki"
AND comment.comment_text LIKE "%Template%"
#AND comment.comment_text NOT LIKE "%Template%"
AND comment.comment_text NOT LIKE "%Category%"
```

هذا هو الاستعلام الاساسي ويتم تعديله حتي تجلب نوع معين حسب المطلوب مثل ان تجلب المقالات والتصنيفات فقط او المقالات
والتصنيفات والقوالب الخ...

```
AND comment.comment_text LIKE "%Template%"
#AND comment.comment_text NOT LIKE "%Template%"
AND comment.comment_text NOT LIKE "%Category%"
```

ملاحظه: الافضل ان تبدا بالمقالات ثم تقوم بتشغيل استعلام اخر حتي تجلب التصفيات والقوالب بالاعتماد علي تغير الشروح الثلاثه
التي في الاعلي

# تجهيز البيانات وحفظها في قاعده بيانات من نوع sql

بعد ان تقوم بتشغيل الاستعلام تقوم بحفظ البيانات علي جهازك الشخصي في شكل ملف .csv حتي يتم التعامل معها في الخطوات التاليه
وهذا شكل البيانات المفترض ان تحصل عليها من الاستعلام الذي في الاعلي

```
deleted_page,date_of_delete,name_of_page
/* clientsitelink-remove:1||enwiki */ Template:Mobile view problem,20231004042649,قالب:Mobile view problem
/* clientsitelink-remove:1||enwiki */ Template:Men's Olympic water polo tournament statistics – best performances of confederations (by tournament),20230215000053,قالب:إحصائيات بطولة كرة الماء الأولمبية للرجال - أفضل أداء للاتحادات القارية
/* clientsitelink-remove:1||enwiki */ Template:Men's Olympic water polo tournament statistics – participating teams,20230215000053,قالب:احصائيات منافسة كرة الماء الأولمبية رجال - الفرق المشاركة
/* clientsitelink-remove:1||enwiki */ Template:Men's Olympic water polo tournament statistics – finishes in top four,20230215000053,قالب:إحصائيات بطولة كرة الماء الأولمبية للرجال - المراكز الأربعة الأولى
/* clientsitelink-remove:1||enwiki */ Template:Men's Olympic water polo tournament statistics – medal table,20230215000053,قالب:إحصائيات بطولة كرة الماء الأولمبية للرجال - جدول الميداليات
```

الان نحتاج الي العمل علي تحليل هذه البيانات حتي نستخرج منها القائمة التي في الاسفل تمهيدلا لاستخدمها في ويكيبيديا العربيه او في عمليات الفحص والمراجعه عبر الاكسيل

| Field                     | Description                                                           |
|---------------------------|-----------------------------------------------------------------------|
| id                        | معرف مميز يستخدم في عمليه البحث والتحليل يبدا من واحد ثم يزاد بعد ذلك |
| en_page                   | اسم الصفحة في النسخة الأجنبية مع النطاق                               |
| date                      | تاريخ الحذف                                                           |
| ar_page                   | اسم الصفحة في النسخة العربية                                          |
| namespace                 | النطاق فقط                                                            |
| exites_in_en              | هل تم إعادة إضافة المقال مرة أخرى إلى النسخة الإنجليزية بعد الحذف     |
| comment                   | سبب الحذف في النسخة الإنجليزية                                        |
| year                      | سنة الحذف                                                             |
| en_page_without_namespace | اسم الصفحة في النسخة الإنجليزية بدون النطاق                           |
| en_first_letter           | أول حرف من اسم الصفحة في النسخة الإنجليزية                            |
| ar_first_letter           | أول حرف من اسم الصفحة في النسخة العربية                               |

## from_cvs_to_db.py

نبدا اولا بتغشيل هذا الاسكريبت والهدف منه عمل تحليل النص وحفظ البيانات في قاعده البيانات لتعامل معها في المستقبل

## exites_in_en.py

ثم هذا الملف الذي يتاكد من ان الصفحه تم انشاءها من جديد او ارجاعها بعد الحذف ام لا

## get_logs.py

ثم هذا الملف حتي يجلب سبب الحذف

## save_page.py

ثم هذا الملف حتي يقوم بحفظ الصفحات في ويكيبديا
او يمكنك تحويل قاعده البيانات الي ملف شيت حتي يمكن استخدمه مع الاكسيل او جوجل شيت 
