"""
This script sends a template message to the talk pages of users that are listed in the list_page_sub_pages data. It iterates through the list of dictionaries in list_page_sub_pages and for each dictionary, it creates an instance of the SendTemplate class and passes in the dictionary as the input_dict argument. The send method of the SendTemplate instance is then called to send the template message to the appropriate user talk pages.

The SendTemplate class is responsible for querying a database using the query provided in the input_dict argument, and then iterating through the results of the query to send the template message to the user talk pages of each user listed in the query results. It does this by creating a new section on the user talk page and adding the template message to it. If the user talk page is a flow page, the Board class is used to create a new topic on the page with the template message as the content. If the user talk page is a regular wikitext page, the template message is simply appended to the end of the page. The template message is then saved to the user talk page.
"""

from module import SendTemplate
from data import list_page_sub_pages


def main(*args: str) -> int:
    # Iterate through each page data in list_page_sub_pages
    for page_data in list_page_sub_pages:
        try:
            # Create a SendTemplate object with the page data
            obj = SendTemplate(input_dict=page_data)
            # Send the template to the user
            obj.send()
        except Exception as e:
            print(f"An error occurred while processing : {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
