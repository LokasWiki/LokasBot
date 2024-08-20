import os
from datetime import datetime

import pywikibot
import requests

# Configuration
site = pywikibot.Site('ar', 'wikipedia')  # Change 'ar' to your language code if needed
tool_name = os.getenv('LOGNAME', 'غير متوفر')  # Fetch the tool name from environment variables
talk_page_title = f'مستخدم:CI-CD log/LokasBot'  # Page title to post the message
bot_version = '1.0.0'  # Replace with your bot version

# GitHub repository details
repo_owner = 'LokasWiki'
repo_name = 'LokasBot'
branch_name = 'main'
github_api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch_name}'
contributors_api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contributors'

# Get the current date and time
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Fetch the latest commit message and time from GitHub
try:
    response = requests.get(github_api_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    branch_data = response.json()
    commit_sha = branch_data['commit']['sha']

    # Fetch commit details using the commit SHA
    commit_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}'
    commit_response = requests.get(commit_url)
    commit_response.raise_for_status()
    commit_data = commit_response.json()
    commit_message = commit_data['commit']['message']
    commit_date = commit_data['commit']['committer']['date']
    commit_html_url = commit_data['html_url']  # URL to the commit on GitHub
    last_commit_author = commit_data['commit']['committer']['name']  # Name of the last commit author
except Exception as e:
    commit_message = 'غير متوفر'
    commit_date = 'غير متوفر'
    commit_html_url = 'غير متوفر'
    last_commit_author = 'غير متوفر'
    print(f'Error fetching commit data: {e}')

# Fetch the list of contributors from GitHub
try:
    response = requests.get(contributors_api_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    contributors_data = response.json()

    # Extract contributor names and their contributions
    contributors = []
    for contributor in contributors_data:
        name = contributor['login']
        contributions = contributor['contributions']
        contributors.append(f'{name} ({contributions} مساهمة)')

except Exception as e:
    contributors = ['غير متوفر']
    print(f'Error fetching contributors data: {e}')

# Format the list of contributors
contributors_list = '\n'.join(f'* {contributor}' for contributor in contributors)

# Message to be posted with wiki template
message = f'''\
== إشعار تحديث البوت ({tool_name}) ==
مرحبًا!

نود إبلاغكم بأن البوت قد تم تحديثه وهو يعمل الآن للمرة الأولى بعد سحب التحديثات الجديدة.

=== تفاصيل التحديث ===
{{| class="wikitable sortable mw-collapsible"
|+ تفاصيل التحديث
|-
! القسم !! التفاصيل
|-
| اسم الأداة || {tool_name}
|-
| نسخة البوت || {bot_version}
|-
| آخر تحديث || {commit_message}
|-
| رابط التحديث || [رابط التحديث]({commit_html_url})
|-
| تاريخ ووقت آخر تحديث || {commit_date}
|-
| تاريخ ووقت التشغيل || {now}
|-
|}}

=== المساهمون ===
{contributors_list}

=== ملاحظات ===
* نشكر جميع المساهمين في هذا التحديث.
* لمزيد من المعلومات أو المساعدة، يمكنكم زيارة [مستندات الدعم](https://example.com/support).

مع أطيب التحيات،
~~~~
'''

# Post the message to the specified talk page
talk_page = pywikibot.Page(site, talk_page_title)
talk_page.text = message
talk_page.save(summary='إعلام البوت: التشغيل للمرة الأولى بعد سحب التحديثات')
print("Message posted to the talk page.")
