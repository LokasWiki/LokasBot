import unittest
from unittest.mock import MagicMock, Mock
from unittest.mock import patch
from tasks.maintenance.bots.unreferenced import Unreferenced


class MyTestCase(unittest.TestCase):

    def test_run_if_no_refs_template_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "Some text without the template."
        summary = "Test summary"
        pb = Unreferenced(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "{{لا مصدر|تاريخ ={{نسخ:شهر وسنة}}}}\nSome text without the template.")
        self.assertEqual(new_summary, 'Test summary، أضاف  وسم [[ويكيبيديا:الاستشهاد بمصادر|لا مصدر]]')

    def test_run_if_have_refs_template_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = """Some text without the template.<ref>{{استشهاد بكتاب
| عنوان = إمارة الزبير بين هجرتين الجزء الثاني
| مؤلف = عبد الرزاق الصانع وعبد العزيز العلي
| مسار = https://books.google.com.sa/books?id=X_rkAAAAMAAJ&q=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&dq=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&hl=en&sa=X&ved=2ahUKEwiZ9aO09a35AhVM4BoKHX3HBS4Q6AF6BAgCEAI
| صفحة = 141، 202
|مسار أرشيف= https://web.archive.org/web/20220804200533/https://books.google.com.sa/books?id=X_rkAAAAMAAJ&q=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&dq=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&hl=en&sa=X&ved=2ahUKEwiZ9aO09a35AhVM4BoKHX3HBS4Q6AF6BAgCEAI|تاريخ أرشيف=2022-08-04}}</ref>"""
        summary = "Test summary"
        pb = Unreferenced(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, text)
        self.assertEqual(new_summary, 'Test summary')

    def test_run_if_have_refs_template_no_ref_template_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = """{{مصدر|تاريخ=ديسمبر 2018}}\nSome text without the template.<ref>{{استشهاد بكتاب
| عنوان = إمارة الزبير بين هجرتين الجزء الثاني
| مؤلف = عبد الرزاق الصانع وعبد العزيز العلي
| مسار = https://books.google.com.sa/books?id=X_rkAAAAMAAJ&q=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&dq=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&hl=en&sa=X&ved=2ahUKEwiZ9aO09a35AhVM4BoKHX3HBS4Q6AF6BAgCEAI
| صفحة = 141، 202
|مسار أرشيف= https://web.archive.org/web/20220804200533/https://books.google.com.sa/books?id=X_rkAAAAMAAJ&q=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&dq=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&hl=en&sa=X&ved=2ahUKEwiZ9aO09a35AhVM4BoKHX3HBS4Q6AF6BAgCEAI|تاريخ أرشيف=2022-08-04}}</ref>"""
        summary = "Test summary"
        pb = Unreferenced(page, text, summary)
        new_text, new_summary = pb.__call__()
        output_text = """\nSome text without the template.<ref>{{استشهاد بكتاب
| عنوان = إمارة الزبير بين هجرتين الجزء الثاني
| مؤلف = عبد الرزاق الصانع وعبد العزيز العلي
| مسار = https://books.google.com.sa/books?id=X_rkAAAAMAAJ&q=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&dq=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&hl=en&sa=X&ved=2ahUKEwiZ9aO09a35AhVM4BoKHX3HBS4Q6AF6BAgCEAI
| صفحة = 141، 202
|مسار أرشيف= https://web.archive.org/web/20220804200533/https://books.google.com.sa/books?id=X_rkAAAAMAAJ&q=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&dq=%22%D9%81%D9%8A+%D8%A7%D9%84%D9%82%D8%B1%D9%8A%D8%B7%D9%8A%D8%A7%D8%AA%22&hl=en&sa=X&ved=2ahUKEwiZ9aO09a35AhVM4BoKHX3HBS4Q6AF6BAgCEAI|تاريخ أرشيف=2022-08-04}}</ref>"""
        self.assertEqual(new_text, output_text)
        self.assertEqual(new_summary, 'Test summary، حذف  وسم [[ويكيبيديا:الاستشهاد بمصادر|لا مصدر]]')


if __name__ == '__main__':
    unittest.main()
