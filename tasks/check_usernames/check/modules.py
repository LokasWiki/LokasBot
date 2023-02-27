import pywikibot
import wikitextparser as wtp
import pywikibot.flow


class ReadUsers:
    def __init__(self, site, page_title):
        self.site = site
        self.page_title = page_title
        self.text = None
        self.users = []

    def load_page(self):
        self.page = pywikibot.Page(self.site, self.page_title)
        self.text = self.page.text
        self.parsed = wtp.parse(str(self.text))

    def parse_table(self):
        table = self.parsed.tables[0].data()
        for row in table:
            reason = row[4]
            status = row[3]
            user = row[2]
            if status.strip().lower() == "نعم".strip().lower():
                t = wtp.Template(user)
                user_dic = {
                    "reason": reason,
                    "has_reason": not (str(reason).strip().lower() == ""),
                    "user_template": user,
                    "username": t.arguments[0].value.strip()
                }
                self.users.append(user_dic)

    def start_send_alert(self):
        for user in self.users:
            if str(user['username']).strip().lower() == "Lokas7755".strip().lower():

                self.send_alert(user['username'], user['has_reason'], user['reason'])

    def send_alert(self, user_name, has_reason, reason):

        # Retrieve the user talk page
        user = pywikibot.User(self.site, user_name)

        # Get the user page for the user
        talk_page = user.getUserTalkPage()

        if talk_page.is_flow_page():
            board = pywikibot.flow.Board(talk_page)

            # Add a new section to the page
            title = 'اسم المستخدم مخالف'
            if has_reason:
                content = "{{نسخ:تنبيه اسم مستخدم|REASON}}".replace("REASON",str(reason).strip())
            else:
                content = "{{نسخ:تنبيه اسم مستخدم}}"

            try:
                topic = board.new_topic(title, content)

            except Exception as error:
                print(f'Error saving page: {error}')

        else:
            pass
            # Add a new section to the page
            text = talk_page.text
            text += '\n'
            if has_reason:
                text += "{{نسخ:تنبيه اسم مستخدم|REASON}}----[[مستخدم:Dr-Taher|Dr-Taher]] ([[نقاش المستخدم:Dr-Taher|نقاش]]) {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)".replace("REASON",str(reason).strip())
            else:
                text += "{{نسخ:تنبيه اسم مستخدم}}----[[مستخدم:Dr-Taher|Dr-Taher]] ([[نقاش المستخدم:Dr-Taher|نقاش]]) {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)"

            try:
                # Save the edited page

                talk_page.text = text

                # Save the page
                talk_page.save(summary="بوت:تنبيه اسم مخالف",minor=False)
            except Exception as error:
                print(f'Error saving page: {error}')


