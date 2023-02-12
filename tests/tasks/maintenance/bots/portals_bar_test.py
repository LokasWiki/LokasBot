import re
import unittest.mock

from tasks.maintenance.bots.portals_bar import PortalsBar


# check if template found or not

def test_add_template():
    page = unittest.mock.Mock()
    page.title.return_value = "Example Page"

    text = "Some text without the template."
    summary = "Test summary"
    pb = PortalsBar(page, text, summary)
    new_text, new_summary = pb.__call__()

    assert new_text != text
    assert new_summary != summary
    assert re.search(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*", new_text) is not None
    assert "، أضاف وسم مقالات بحاجة لشريط بوابات" in new_summary


def test_add_above_category_template():
    page = unittest.mock.Mock()
    page.title.return_value = "Example Page"

    text = """
== وصلات خارجية ==
{{روابط شقيقة}}
* [http://www.altafsir.com/Quran.asp?SoraNo=13&Ayah=1&NewPage=1&LanguageID=1 سورة الرعد: تجويد-تفسير] - موقع Altafsir.com
{{فهرس سور القرآن}}
{{ضبط استنادي}}
[[تصنيف:سور|رعد]]
[[تصنيف:سور مدنية]]
"""
    summary = "Test summary"
    pb = PortalsBar(page, text, summary)
    new_text, new_summary = pb.__call__()

    assert new_text != text
    assert new_summary != summary
    assert re.search(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*", new_text) is not None
    assert new_text ==  """
== وصلات خارجية ==
{{روابط شقيقة}}
* [http://www.altafsir.com/Quran.asp?SoraNo=13&Ayah=1&NewPage=1&LanguageID=1 سورة الرعد: تجويد-تفسير] - موقع Altafsir.com
{{فهرس سور القرآن}}
{{ضبط استنادي}}
{{مقالات بحاجة لشريط بوابات}}
[[تصنيف:سور|رعد]]
[[تصنيف:سور مدنية]]
"""
    assert "، أضاف وسم مقالات بحاجة لشريط بوابات" in new_summary


def test_remove_template_if_no_templates_found():
    page = unittest.mock.Mock()
    page.title.return_value = "Example Page"

    text = "Some text with the template.\n{{مقالات بحاجة لشريط بوابات}}"
    summary = "Test summary"
    pb = PortalsBar(page, text, summary)
    new_text, new_summary = pb.__call__()

    assert new_text == text
    assert new_summary == summary
    assert re.search(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*", new_text) is not None


def test_remove_template_if_page_type_is_disambiguation():
    page = unittest.mock.Mock()
    page.title.return_value = "Example Page (disambiguation)"

    text = "Some text with the template.\n{{مقالات بحاجة لشريط بوابات}}"
    summary = "Test summary"
    pb = PortalsBar(page, text, summary)
    new_text, new_summary = pb.__call__()

    assert new_text == text
    assert new_summary == summary
    assert re.search(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*", new_text) is not None


def test_remove_template_if_template_found():
    page = unittest.mock.Mock()
    page.title.return_value = "Example Page"

    list_of_template = [
        "صندوق بوابات",
        "Portal box",
        "مجموعة بوابات",
        "Portail",
        "وصلة بوابة",
        "صندوق بوابة",
        "Portal bar",
        "شب",
        "شريط بوابة",
        "شريط البوابات",
        "بوابة",
        "Portal"
    ]

    for template in list_of_template:
        text = "Some text with the template.{{" + template + "|مصر}}\n{{مقالات بحاجة لشريط بوابات}}"
        summary = "Test summary"
        pb = PortalsBar(page, text, summary)
        new_text, new_summary = pb.__call__()

        assert new_text != text
        assert new_summary != summary
        assert re.search(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*", new_text) is None
        assert "، حذف وسم مقالات بحاجة لشريط بوابات" in new_summary

        text = "Some text with the template.{{" + template + "|مصر|اسيا|يمين=نعم}}\n{{مقالات بحاجة لشريط بوابات}}"
        summary = "Test summary"
        pb = PortalsBar(page, text, summary)
        new_text, new_summary = pb.__call__()

        assert new_text != text
        assert new_summary != summary
        assert re.search(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*", new_text) is None
        assert "، حذف وسم مقالات بحاجة لشريط بوابات" in new_summary


def test_remove_template_if_template_found_but_have_not_correct_parms():
    list_of_template = [
        "صندوق بوابات",
        "Portal box",
        "مجموعة بوابات",
        "Portail",
        "وصلة بوابة",
        "صندوق بوابة",
        "Portal bar",
        "شب",
        "شريط بوابة",
        "شريط البوابات",
        "بوابة",
        "Portal"
    ]

    page = unittest.mock.Mock()
    page.title.return_value = "Example Page"

    for template in list_of_template:

        lot = [
            # "{{شريط          بوابات|}}",
            "{{" + template + "|           }}",
            "{{" + template + "}}"
                              "{{" + template + "|\n}}",
            "{{" + template + "|       \n  \n  }}",
            "{{          " + template + "         }}"
        ]

        for item in ["نمط", "حد", "قد", "عرض", "فاصل"]:
            lot.append("{{" + template + "|" + item + "=قائمة}}", )
        for template_name in lot:
            text = "Some text with the template." + template_name + "\n{{مقالات بحاجة لشريط بوابات}}"
            summary = "Test summary"
            pb = PortalsBar(page, text, summary)
            new_text, new_summary = pb.__call__()

            assert new_text != text
            assert new_summary != summary

            assert re.search(r"\s*{{\s*مقالات\s+بحاجة\s+لشريط\s+بوابات\s*}}\s*", new_text) is not None
            assert template_name not in new_text
            assert "، أضاف وسم مقالات بحاجة لشريط بوابات" in new_summary
