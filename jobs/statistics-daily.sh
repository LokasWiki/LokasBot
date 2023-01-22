#!/bin/bash
set -euo pipefail


. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"

python3 "$HOME"/repos/tasks/statistics/activity_of_bureaucrats.py
python3 "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_revision_edits.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_help_pages_creation_with_bot.py
python3 "$HOME"/repos/tasks/statistics/administrators_activity.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_portals_creation.py
python3 "$HOME"/repos/tasks/statistics/articles_containing_linked_email_addresses.py
python3 "$HOME"/repos/tasks/statistics/pages_that_are_missing_internal_links.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_portals_creation_with_bot.py
python3 "$HOME"/repos/tasks/statistics/articles_in_which_there_is_a_link_to_user_pages.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_redirect_creation.py
python3 "$HOME"/repos/tasks/statistics/articles_not_found_by_number_of_language_links.py
python3 "$HOME"/repos/tasks/statistics/range_blocks.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_redirect_creation_with_bot.py
python3 "$HOME"/repos/tasks/statistics/forgotten_articles.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_templates_creation.py
python3 "$HOME"/repos/tasks/statistics/inactive_bots.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_templates_creation_with_bot.py
python3 "$HOME"/repos/tasks/statistics/inactive_users.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_article_creation.py
python3 "$HOME"/repos/tasks/statistics/users_by_the_number_of_pages_created.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_article_creation_with_bot.py
python3 "$HOME"/repos/tasks/statistics/users_with_bots_by_the_number_of_pages_created.py
python3 "$HOME"/repos/tasks/statistics/list_of_portals_by_number_of_articles.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_categories_creation.py
python3 "$HOME"/repos/tasks/statistics/wikipedians_without_permission.py
python3 "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_edits.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_categories_creation_with_bot.py
python3 "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_edits_with_bot.py
python3 "$HOME"/repos/tasks/statistics/users_by_number_of_help_pages_creation.py

