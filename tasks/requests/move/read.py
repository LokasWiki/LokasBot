import logging

import pywikibot

from tasks.requests.move.bot.models import TaskDescription, TaskOption, BotRunner, WikipediaTaskReader, \
    LastUserEditRoleChecker

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 9

try:

    page_name = "ويكيبيديا:طلبات نقل عبر البوت/ملخص التعديل"
    site = pywikibot.Site("ar", "wikipedia")
    default_description = "بوت:نقل ([[ويكيبيديا:طلبات نقل عبر البوت]])"
    task_description = TaskDescription(site=site, page_title=page_name, default_description=default_description)
    print(task_description.get_description())

    option_page_name = "ويكيبيديا:طلبات نقل عبر البوت/خيارات البوت"
    default_template_name = "ويكيبيديا:طلبات نقل عبر البوت/خيارات البوت/قالب"
    task_option = TaskOption(site=site, page_title=option_page_name, template_name=default_template_name)
    print(task_option.get_options())

    bot_runner_page_name = "ويكيبيديا:طلبات نقل عبر البوت/تشغيل البوت"
    bot_runner = BotRunner(site=site, page_title=bot_runner_page_name)
    print(bot_runner.can_run())

    task_page = pywikibot.Page(site, "ويكيبيديا:طلبات نقل عبر البوت")

    last_user_edit_role = LastUserEditRoleChecker(page=task_page, role="editor")

    wikipediataskreader = WikipediaTaskReader(
        site=site,
        description=task_description,
        option=task_option,
        task_stats=bot_runner,
        last_user_edit_role=last_user_edit_role
    )
    if wikipediataskreader.can_bot_run() and wikipediataskreader.check_user_role():
        print("can run page status has true value")


except Exception as e:
    print(f"An error occurred: {e}")
    logging.error(e)

#
# try:
#
#     requests_page = RequestsPage(site)
#     requests_page.title = "ويكيبيديا:طلبات توزيع قالب تصفح"
#     requests_page.header_text = "{{/ترويسة}}"
#
#     requests_page.load_page()
#
#     if requests_page.check_user_edits(3000):
#         scanner = RequestsScanner()
#         scanner.pattern = r"\*\s*\[\[قالب:(?P<source>.*)\]\](?P<extra>.*)"
#         scanner.scan(requests_page.get_page_text())
#
#         if scanner.have_requests:
#             requests_page.start_request()
#             try:
#                 with Session(engine) as session:
#                     for request in scanner.requests:
#                         # source_page = pywikibot.Page(site, f"{request['source']}",ns=0)
#                         # destination_page = pywikibot.Page(site, f"{request['destination']}",ns=0)
#                         # if source_page.exists() and destination_page.exists() and source_page.namespace() == 0 and destination_page.namespace() == 0:
#                         # todo:add check if template exists with send content to talk page
#                         request_model = Request(
#                             from_title=request['source'],
#                             from_namespace=10,
#                             request_type=type_of_request,
#                             extra=request['extra']
#                         )
#                         session.add(request_model)
#                     session.commit()
#             except Exception as e:
#                 session.rollback()
#                 print("An error occurred while committing the changes:", e)
#
#         else:
#             print("no reqtest found")
#             requests_page.move_to_talk_page()
#     else:
#         print("not allow for user")
#         requests_page.move_to_talk_page()
#     # Get the page text after removing the header text
# except Exception as e:
#     print(f"An error occurred: {e}")
