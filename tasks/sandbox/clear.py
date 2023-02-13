import pywikibot

page_text = "{{عنوان الملعب}}\n<!-- مرحبا! خذ راحتك في تجربة مهارتك في التنسيق والتحرير أسفل هذا السطر. هذه الصفحة لتجارب التعديل ، سيتم تفريغ هذه الصفحة كل 12 ساعة. -->"
page_summary = "بوت:افراغ الصفحة تلقائيا!"
page_title = "ويكيبيديا:ملعب"


def main(*args: str) -> int:
    site = pywikibot.Site()
    page = pywikibot.Page(site, page_title)
    page.text = page_text
    page.save(summary=page_summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
