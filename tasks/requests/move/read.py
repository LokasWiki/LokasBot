import traceback

import pywikibot
from sqlalchemy.orm import Session

from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request_Move_Page
from tasks.requests.move.bot.models import TaskDescription, TaskOption, BotRunner, WikipediaTaskReader, \
    LastUserEditRoleChecker, WikiListFormatChecker

# Create an instance of the RequestsPage class
site = pywikibot.Site()

try:

    page_name = "ويكيبيديا:طلبات نقل عبر البوت/ملخص التعديل"
    default_description = "بوت:نقل ([[ويكيبيديا:طلبات نقل عبر البوت]])"
    option_page_name = "ويكيبيديا:طلبات نقل عبر البوت/خيارات البوت"
    default_template_name = "ويكيبيديا:طلبات نقل عبر البوت/خيارات البوت/قالب"
    bot_runner_page_name = "ويكيبيديا:طلبات نقل عبر البوت/تشغيل البوت"

    task_page = pywikibot.Page(site, "ويكيبيديا:طلبات نقل عبر البوت")

    task_description = TaskDescription(site=site, page_title=page_name, default_description=default_description)
    task_option = TaskOption(site=site, page_title=option_page_name, template_name=default_template_name)
    bot_runner = BotRunner(site=site, page_title=bot_runner_page_name)
    last_user_edit_role_page = pywikibot.Page(site, bot_runner_page_name)
    last_user_edit_role = LastUserEditRoleChecker(page=last_user_edit_role_page, role="editor")
    wiki_text_list = WikiListFormatChecker()
    wiki_text_list.set_wiki_text(task_page.text)

    wikipediataskreader = WikipediaTaskReader(
        site=site,
        description=task_description,
        option=task_option,
        task_stats=bot_runner,
        last_user_edit_role=last_user_edit_role,
        wiki_text_list=wiki_text_list
    )

    emptry_page = False
    if wikipediataskreader.can_read():
        try:
            with Session(engine) as session:
                for order in wikipediataskreader.get_list():
                    request_model = Request_Move_Page(
                        from_title=order.source,
                        from_namespace=order.from_ns,
                        to_title=order.description,
                        to_namespace=order.to_ns,
                        task_description=order.description,
                        task_options=str(order.options)
                    )
                    session.add(request_model)
                session.commit()
                emptry_page = True
        except Exception as e:
            session.rollback()
            print("An error occurred while committing the changes:", e)
            just_the_string = traceback.format_exc()
            print(just_the_string)

    if emptry_page:
        # wikipediataskreader.move_to_talk_page()
        pass
    else:
        print("no reqtest found")

except Exception as e:
    print(f"An error occurred: {e}")
    just_the_string = traceback.format_exc()
    print(just_the_string)
