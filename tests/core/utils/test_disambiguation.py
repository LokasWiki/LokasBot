import unittest.mock

from app.core.utils import Disambiguation

list_of_allow_titles = [
        "(disambiguation) تجربه",
        " (disambiguation) تجربه"
        " ( disambiguation) تجربه"
        " ( disambiguation ) تجربه",
        "(disambiguation)تجربه",
        " (disambiguation)تجربه"
        " ( disambiguation)تجربه"
        " ( disambiguation )تجربه",
        "(disAMBIGuation) تجربه",
        " (disambigUAtion) تجربه"
        " ( disambiguATion) تجربه"
        " ( disambiguatiON ) تجربه",
        "(diSAmbiguation)تجربه",
        " (disaMBiguation)تجربه"
        " ( disamBIGuation)تجربه"
        " ( disambigUATion )تجربه",
        "(توضيح) تجربه",
        " (توضيح) تجربه"
        " ( توضيح) تجربه"
        " ( توضيح ) تجربه",
        "(توضيح)تجربه",
        " (توضيح)تجربه"
        " ( توضيح)تجربه"
        " ( توضيح )تجربه",
    ]
list_of_not_allow_titles = [
        "disambiguation) تجربه",
        " disambiguation) تجربه"
        "  disambiguation) تجربه"
        "  disambiguation ) تجربه",
        "disambiguation)تجربه",
        " disambiguation)تجربه"
        "  disambiguation)تجربه"
        "  disambiguation )تجربه",
        "disAMBIGuation) تجربه",
        " disambigUAtion) تجربه"
        "  disambiguATion) تجربه"
        "  disambiguatiON ) تجربه",
        "diSAmbiguation)تجربه",
        " disaMBiguation)تجربه"
        "  disamBIGuation)تجربه"
        "  disambigUATion )تجربه",
        "توضيح) تجربه",
        " توضيح) تجربه"
        "  توضيح) تجربه"
        "  توضيح ) تجربه",
        "توضيح)تجربه",
        " توضيح)تجربه"
        "  توضيح)تجربه"
        "  توضيح )تجربه",
        "(disambiguation تجربه",
        " (disambiguation تجربه"
        " ( disambiguation تجربه"
        " ( disambiguation  تجربه",
        "(disambiguationتجربه",
        " (disambiguationتجربه"
        " ( disambiguationتجربه"
        " ( disambiguation تجربه",
        "(disAMBIGuation تجربه",
        " (disambigUAtion تجربه"
        " ( disambiguATion تجربه"
        " ( disambiguatiON  تجربه",
        "(diSAmbiguationتجربه",
        " (disaMBiguationتجربه"
        " ( disamBIGuationتجربه"
        " ( disambigUATion تجربه",
        "(توضيح تجربه",
        " (توضيح تجربه"
        " ( توضيح تجربه"
        " ( توضيح  تجربه",
        "(توضيحتجربه",
        " (توضيحتجربه"
        " ( توضيحتجربه"
        " ( توضيح تجربه",
    ]
list_of_templates = ["توضيح", "Disambig", "صفحة توضيح", "Disambiguation"]

def test_if_page_is_disambiguation_from_title():

    for title in list_of_allow_titles:
        text = "Some text without The template."

        d = Disambiguation(title, text)

        assert d.page_title == title.lower()
        assert d.page_text == text.lower()

        assert d.check_title() == True
        assert d.check_text() == False

        assert d.check("or") == True
        assert d.check("oR") == True
        assert d.check("OR") == True
        assert d.check("Or") == True

        assert d.check() == False

def test_if_page_is_disambiguation_from_template_with_true_title():
    for title in list_of_allow_titles:
        for template_name in list_of_templates:
            text = """

            '''أنطونيو بلانكو''' يُشير إلى:
*[[أنطونيو بلانكو (رسام)]] (1912–1999)، رسام من أصل إسباني وأمريكي.
*[[أنطونيو بلانكو فريجيرو]] (1923–1991)، عالم آثار ومؤرخ إسباني.
*[[أنطونيو بلانكو (لاعب كرة قدم)]] (مواليد 2000)، لاعب كرة قدم إسباني

            """
            templates = []
            templates.append("{{"+template_name+"}}\n" + text)
            templates.append("{{      " + template_name + "}}\n" + text)
            templates.append("{{      " + template_name + "        }}\n" + text)
            templates.append("{{      " + template_name + "}}\n" + text)
            templates.append("{{ " + template_name + "}}\n" + text)
            templates.append("aaaaaaaaaaa{{ " + template_name + "}}\n" + text)
            templates.append("aaaaaaaaaaa\n{{ " + template_name + "}}\n" + text)

            templates.append(text + "\n{{" + template_name + "}}")
            templates.append(text + "\n{{      " + template_name + "}}")
            templates.append(text + "\n{{      " + template_name + "        }}")
            templates.append(text + "\n{{      " + template_name + " }}")
            templates.append(text + "\n{{  " + template_name + " }}")
            templates.append(text + "\naaaaaaaaaaa{{  " + template_name + " }}")
            templates.append(text + "\naaaaaaaaaaa\n{{  " + template_name + " }}")

            for template in templates:

                d = Disambiguation(title, template)

                assert d.page_title == title.lower()
                assert d.page_text == template.lower()

                assert d.check_title() == True
                assert d.check_text() == True

                assert d.check("or") == True
                assert d.check("oR") == True
                assert d.check("and") == True
                assert d.check() == True


def test_if_page_is_not_disambiguation_from_title():
    page = unittest.mock.Mock()

    for title in list_of_not_allow_titles:
        lot = [title.lower(), title.upper(), title, "11111111" + title.lower(), "11111111" + title.upper(),
               "11111111" + title, "11111111" + title.lower() + "11111123", "11111111" + title.upper() + "11111123",
               "11111111" + title + "11111123"]
        for t in lot:
            text = "Some text without The template."

            d = Disambiguation(t, text)
            assert d.page_title == t.lower()
            assert d.page_text == text.lower()

            assert d.check_title() == False
            assert d.check_text() == False

            assert d.check("or") == False
            assert d.check("oR") == False
            assert d.check("OR") == False
            assert d.check("Or") == False
            assert d.check() == False

