#!/bin/bash
#set -euo pipefail


. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"
export PYTHONPATH="${PYTHONPATH}:$HOME/repos"


myArrayFiles=( "$HOME"/repos/tasks/statistics/activity_of_bureaucrats.py \
  "$HOME"/repos/tasks/check_usernames/load/load.py \
  "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_revision_edits.py \
  "$HOME"/repos/tasks/statistics/sandboxs_users_need_to_review.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_help_pages_creation_with_bot.py \
  "$HOME"/repos/tasks/statistics/administrators_activity.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_portals_creation.py \
  "$HOME"/repos/tasks/statistics/articles_containing_linked_email_addresses.py \
  "$HOME"/repos/tasks/statistics/pages_that_are_missing_internal_links.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_portals_creation_with_bot.py \
  "$HOME"/repos/tasks/statistics/articles_in_which_there_is_a_link_to_user_pages.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_redirect_creation.py \
  "$HOME"/repos/tasks/statistics/articles_not_found_by_number_of_language_links.py \
  "$HOME"/repos/tasks/statistics/range_blocks.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_redirect_creation_with_bot.py \
  "$HOME"/repos/tasks/statistics/forgotten_articles.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_templates_creation.py \
  "$HOME"/repos/tasks/statistics/inactive_bots.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_templates_creation_with_bot.py \
  "$HOME"/repos/tasks/statistics/inactive_users.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_article_creation.py \
  "$HOME"/repos/tasks/statistics/list_of_portals_by_number_of_articles.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_categories_creation.py \
  "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_edits.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_categories_creation_with_bot.py \
  "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_edits_with_bot.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_help_pages_creation.py \
  "$HOME"/repos/tasks/statistics/categories_not_found_by_number_of_language_links.py \
  "$HOME"/repos/tasks/statistics/latest_arabic_files_on_commons.py \
  "$HOME"/repos/tasks/statistics/templates_not_found_by_number_of_language_links.py \
  "$HOME"/repos/tasks/statistics/Articles_by_size.py \
  "$HOME"/repos/tasks/statistics/featured_articles_by_size.py \
  "$HOME"/repos/tasks/statistics/good_articles_by_size.py \
  "$HOME"/repos/tasks/statistics/pages_with_most_revisions.py \
  "$HOME"/repos/tasks/statistics/talk_pages_by_size.py \
  "$HOME"/repos/tasks/statistics/bot_wars.py \
  "$HOME"/repos/tasks/statistics/abuse_filter/filters_blow_in_the_last_week.py \
  "$HOME"/repos/tasks/statistics/abuse_filter/indefinitely_blocked_ips.pys \
  "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_files_uploaded.py \
  "$HOME"/repos/tasks/statistics/unusually_long_ip_blocks.py \
  "$HOME"/repos/tasks/statistics/unusually_long_user_blocks.py \

)

run_file() {
    python3 "$1"  || (echo "Error running file $1" && false)
}

for file in "${myArrayFiles[@]}"; do
    run_file "$file"
done

# Exit the script after running all the Python files
exit 0
