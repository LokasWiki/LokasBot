#!/bin/bash
#set -euo pipefail


. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"


myArrayFiles=( "$HOME"/repos/tasks/statistics/activity_of_bureaucrats.py \
  "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_revision_edits.py \
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
  "$HOME"/repos/tasks/statistics/users_by_the_number_of_pages_created.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_article_creation_with_bot.py \
  "$HOME"/repos/tasks/statistics/users_with_bots_by_the_number_of_pages_created.py \
  "$HOME"/repos/tasks/statistics/list_of_portals_by_number_of_articles.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_categories_creation.py \
  "$HOME"/repos/tasks/statistics/wikipedians_without_permission.py \
  "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_edits.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_categories_creation_with_bot.py \
  "$HOME"/repos/tasks/statistics/list_of_wikipedians_by_number_of_edits_with_bot.py \
  "$HOME"/repos/tasks/statistics/users_by_number_of_help_pages_creation.py \
  "$HOME"/repos/tasks/statistics/categories_not_found_by_number_of_language_links.py \
  "$HOME"/repos/tasks/statistics/latest_arabic_files_on_commons.py \

)

run_file() {
    python3 "$1"  || (echo "Error running file $1" && false)
}

for file in "${myArrayFiles[@]}"; do
    run_file "$file"
done

# Exit the script after running all the Python files
exit 0
