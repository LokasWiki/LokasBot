from module import SendTemplate
from data import list_page_sub_pages

for page_data in list_page_sub_pages:
    obj = SendTemplate(input_dict=page_data)
    obj.send()
