import re
import pywikibot
import difflib

# قم بجلب جميع الصفحات من تصنيف الحذف
# قم بالبحث عن النسخه التي تم وضع القالب بها
# قم بجلب اسم المستخدم
# قم بالذهاب الي صفحه نطاق اسم المستخدم وتاكد من ان التنبيه لم يصل له
# اذا كان المستخدم يستخدم نقاشات flow قم بااضافه التنبيه له بعد اجراء عمليه الفحص بي طريقه مختلف
# في النهايه ضع معرفه الصفحه الي قاعده البيانات حتي لا يتم المرور عليها مره اخري
# قم بحذف الصفحات من قاعده البيانات بعد ٢٤ ساعه
# قم بتحويل الكود الي oop

site = pywikibot.Site()
# cat name of page
cat_name = "تصنيف:صفحات للحذف السريع"
# regex to found page
pattern = r"{{شطب[^}]*}}"

cat_page = pywikibot.Category(site,cat_name)

# start get list of sub pages
for p in list(cat_page.articles()):
    # init temp page
    print(p.title())
    page = pywikibot.Page(site,p.title())
    # revision that in it template of delete was added
    delete_revision = None
    # start get all revisions of temp page from old to new
    for revision in page.revisions(reverse=True):
        # get revision id
        revid = revision['revid']
        # get text of revision
        text = page.getOldVersion(revid)
        # start check if template found
        match = re.search(pattern, text)
        if match:
            delete_revision = revision
            break
    # timestamp of delete revision
    delete_revision_timestamp = delete_revision['timestamp']
    # get first user that create page
    user = pywikibot.User(site, page.oldest_revision.user)
    # check if user in not ip
    if not user.isAnonymous():
        user_talk_page = user.getUserTalkPage()
        prev_text = ""
        # start to get all revisions of user talk page to check if user not get alert
        for ut_revision in user_talk_page.revisions(starttime=delete_revision_timestamp, reverse=True):
            # get revision id
            revid = ut_revision['revid']
            # get text of revision
            text = user_talk_page.getOldVersion(revid)
            diff = difflib.unified_diff(prev_text.splitlines(), text.splitlines())
            added_text = '\n'.join(list(filter(lambda line: line.startswith('+'), diff)))
            if added_text:
                print(added_text)
                print("-----------------------")
            prev_text = text







