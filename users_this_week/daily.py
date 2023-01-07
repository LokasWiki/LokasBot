from module import SubPage,MainPage
from data import list_page_sub_pages

for page_data in list_page_sub_pages:
    obj = SubPage(input_dict=page_data)
    obj.save_page()

main_page = MainPage(
    title_of_page="DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا",
    summary="update",
    stub="stub/main_page.txt",
)
main_page.read_file()
main_page.save_page()

archive_page = MainPage(
    title_of_page="DOMAIN_NAMEمستخدمو الأسبوع الأكثر نشاطا/الأسبوع الWEEK_NUMBER YEAR_NUMBER",
    summary="update",
    stub="stub/archive.txt",
)
archive_page.read_file()
archive_page.save_page()
