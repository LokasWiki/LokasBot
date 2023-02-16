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
        self.assertEqual(len(obj.arguments_after_clean),6)

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
        self.assertEqual(len(obj.archive_url_args_found),0)
        self.assertEqual(len(obj.arguments_after_clean),6)

if __name__ == '__main__':
    unittest.main()
