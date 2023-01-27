from data import list_of_distribute_medals
from module import SendTemplate


def main(*args: str) -> int:
    # Iterate through each page data in list_page_sub_pages
    for page_data in list_of_distribute_medals:
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
