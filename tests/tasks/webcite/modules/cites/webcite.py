import unittest
import wikitextparser as wtp

from tasks.webcite.modules.cites.webcite import WebCite


class MyTestCase(unittest.TestCase):
    def test_simple(self):
        template = """{{استشهاد ويب
| url = https://www.youm7.com/story/2022/7/19/محافظ-الجيزة-يصدر-قراراً-بحركة-رؤساء-الوحدات-المحلية-48-قيادة/5841922
| title = محافظ الجيزة يصدر قراراً بحركة رؤساء الوحدات المحلية..48 قيادة بالمراكز والمدن
| date = 2022-7-19
| موقع = اليوم السابع
| لغة = ar
| accessdate = 2023-2-16
}}"""
        parser = wtp.Template(template)
        obj = WebCite(parser)
        self.assertIs(obj.is_archived(), False)
        self.assertEqual(len(obj.archive_url_args_found), 0)
        self.assertEqual(len(obj.arguments_after_clean), 6)
        self.assertEqual(parser.get_arg("url").name.strip().lower(),obj.url().name.strip().lower())
        self.assertEqual(parser.get_arg("url").value.strip().lower(),obj.url().value.strip().lower())

    def test_simple_with_empty_arg(self):
        template = """{{استشهاد ويب
| url = https://www.youm7.com/story/2022/7/19/محافظ-الجيزة-يصدر-قراراً-بحركة-رؤساء-الوحدات-المحلية-48-قيادة/5841922
| title = محافظ الجيزة يصدر قراراً بحركة رؤساء الوحدات المحلية..48 قيادة بالمراكز والمدن
| date = 2022-7-19
| موقع = اليوم السابع
| url2 =
| title =
| uvfd =
| لغة = ar
| accessdate = 2023-2-16
}}"""
        parser = wtp.Template(template)
        obj = WebCite(parser)
        self.assertIs(obj.is_archived(), False)
        self.assertEqual(len(obj.archive_url_args_found), 0)
        self.assertEqual(len(obj.arguments_after_clean), 6)
        self.assertEqual(parser.get_arg("url").name.strip().lower(), obj.url().name.strip().lower())
        self.assertEqual(parser.get_arg("url").value.strip().lower(), obj.url().value.strip().lower())

    def test_simple_with_one_arg_url(self):
        template = """{{استشهاد ويب
| مسار = http://www.alarabiya.net/ar/sport/saudi-sport/2017/09/05/%D8%A7%D9%84%D8%A3%D8%AE%D8%B6%D8%B1-%D9%8A%D9%86%D9%87%D9%8A-%D8%BA%D9%8A%D8%A7%D8%A8%D9%87-%D8%A7%D9%84%D8%B7%D9%88%D9%8A%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D9%85%D9%88%D9%86%D8%AF%D9%8A%D8%A7%D9%84-%D9%88%D9%8A%D9%82%D8%B7%D8%B9-%D8%AA%D8%B0%D9%83%D8%B1%D8%A9-%D9%85%D9%88%D8%B3%D9%83%D9%88.html
| عنوان = السعودية تتأهل إلى نهائيات كأس العالم 2018
| موقع = www.alarabiya.net
| لغة = ar
| تاريخ الوصول = 2017-11-11| مسار أرشيف = https://web.archive.org/web/20180216041626/http://www.alarabiya.net/ar/sport/saudi-sport/2017/09/05/الأخضر-ينهي-غيابه-الطويل-عن-المونديال-ويقطع-تذكرة-موسكو.html | تاريخ أرشيف = 16 فبراير 2018 }}"""
        parser = wtp.Template(template)
        obj = WebCite(parser)
        self.assertIs(obj.is_archived(), True)
        self.assertEqual(len(obj.archive_url_args_found), 1)
        self.assertEqual(len(obj.arguments_after_clean), 7)
        self.assertEqual(parser.get_arg("مسار").name.strip().lower(), obj.url().name.strip().lower())
        self.assertEqual(parser.get_arg("مسار").value.strip().lower(), obj.url().value.strip().lower())

    def test_simple_with_none_arg_url(self):
        template = """{{استشهاد ويب
        | عنوان = السعودية تتأهل إلى نهائيات كأس العالم 2018
        | موقع = www.alarabiya.net
        | لغة = ar
        | تاريخ الوصول = 2017-11-11| مسار أرشيف = https://web.archive.org/web/20180216041626/http://www.alarabiya.net/ar/sport/saudi-sport/2017/09/05/الأخضر-ينهي-غيابه-الطويل-عن-المونديال-ويقطع-تذكرة-موسكو.html | تاريخ أرشيف = 16 فبراير 2018 }}"""
        parser = wtp.Template(template)
        obj = WebCite(parser)
        self.assertIs(obj.is_archived(), True)
        self.assertEqual(len(obj.archive_url_args_found), 1)
        self.assertEqual(len(obj.arguments_after_clean), 6)
        self.assertIsNone(obj.url())


    def test_simple_with_empty_arg_url(self):
        template = """{{استشهاد ويب
        | عنوان = السعودية تتأهل إلى نهائيات كأس العالم 2018
        | موقع = www.alarabiya.net
        | url =
        | تاريخ الوصول = 2017-11-11| مسار أرشيف = https://web.archive.org/web/20180216041626/http://www.alarabiya.net/ar/sport/saudi-sport/2017/09/05/الأخضر-ينهي-غيابه-الطويل-عن-المونديال-ويقطع-تذكرة-موسكو.html | تاريخ أرشيف = 16 فبراير 2018 }}"""
        parser = wtp.Template(template)
        obj = WebCite(parser)
        self.assertIs(obj.is_archived(), True)
        self.assertEqual(len(obj.archive_url_args_found), 1)
        self.assertEqual(len(obj.arguments_after_clean), 5)
        self.assertIsNone(obj.url())

    def test_simple_with_replace_arg_url(self):
        template = """{{استشهاد ويب
        | عنوان = السعودية تتأهل إلى نهائيات كأس العالم 2018
        | موقع = www.alarabiya.net
        | url = http://temburong.gov.bn/SitePages/MUKIM%20BOKOK.aspx
        | تاريخ الوصول = 2017-11-11| مسار أرشيف = https://web.archive.org/web/20180216041626/http://www.alarabiya.net/ar/sport/saudi-sport/2017/09/05/الأخضر-ينهي-غيابه-الطويل-عن-المونديال-ويقطع-تذكرة-موسكو.html | تاريخ أرشيف = 16 فبراير 2018 }}"""
        parser = wtp.Template(template)
        obj = WebCite(parser)
        self.assertIs(obj.is_archived(), True)
        self.assertEqual(len(obj.archive_url_args_found), 1)
        self.assertEqual(len(obj.arguments_after_clean), 6)
        self.assertIsNotNone(obj.url())
        obj.replace_to(obj.url_args,"مسار")
        self.assertEqual(obj.template.has_arg("url"),False)
        self.assertEqual(obj.template.has_arg("مسار"),True)
        self.assertEqual(obj.template.get_arg("مسار").value.strip().lower(),"http://temburong.gov.bn/SitePages/MUKIM%20BOKOK.aspx".strip().lower())


if __name__ == '__main__':
    unittest.main()
