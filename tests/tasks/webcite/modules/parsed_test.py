import unittest
from tasks.webcite.modules.parsed import Parsed


class MyTestCase(unittest.TestCase):

    def test_if_cite_template_found(self):
        text = "text"
        summary = "Test summary"
        pobj = Parsed(text,summary)
        new_text, new_summary = pobj.__call__()
        self.assertEqual(text, new_text)

    def test_extract_cites_web_from_text(self):
        text = """
{{قرية مصرية
| اللون =
| الاسم = برنشت
<!-- صورة -->
| صورة =
| عنوان الصورة =
|البلد = {{علم مصر}}
| محافظة ={{علم محافظة الجيزة}}
| خريطة = مركز العياط.png
| عنوان الخريطة = موقع القرية داخل المركز
<!-- معلومات -->
| لقب =
| مدينة =
| مركز = [[العياط (مركز)|العياط]]
| تأسيس =
| وحدة محلية =«وحدة برنشت»
| رئيس الوحدة =طارق سعيد سيد<ref>{{استشهاد ويب
| url = https://www.youm7.com/story/2022/7/19/محافظ-الجيزة-يصدر-قراراً-بحركة-رؤساء-الوحدات-المحلية-48-قيادة/5841922
| title = محافظ الجيزة يصدر قراراً بحركة رؤساء الوحدات المحلية..48 قيادة بالمراكز والمدن
| date = 2022-7-19
| موقع = اليوم السابع
| لغة = ar
| accessdate = 2023-2-16
}}</ref>
| عمدة =
| مساحة =
| عدد السكان = 18296 نسمة
| سنة التعداد = 2006
| الرقم البريدي =12927
| الموقع الرسمي =
}}

'''قرية برنشت''' هي إحدى القرى التابعة لمركز [[العياط (مركز)|العياط]] في [[محافظة الجيزة]] في [[مصر|جمهورية مصر العربية]]. حسب إحصاءات سنة 2006، بلغ إجمالي السكان في برنشت 18296 نسمة، منهم 9880 رجل و8416 امرأة.<ref>{{استشهاد ويب
| مسار = http://www.msrintranet.capmas.gov.eg/pls/census/cnsest_a_sex_ama?LANG=1
| عنوان = البيانات السكانية لمدينة أو قرية حسب تقديرات السكان 2006
| ناشر = الجهاز المصري المركزي للإحصاء
| لغة = العربية
| تاريخ الوصول = 12 أغسطس 2012
| مسار أرشيف = https://web.archive.org/web/20181101175745/http://www.webcitation.org/69rYPjwRN
| تاريخ أرشيف = 1 نوفمبر 2018
| url-status = dead
}}</ref>

== طالع أيضا ==

* [[محافظة الجيزة]]
* [[قائمة قرى محافظة الجيزة]]

== المصادر ==
{{مراجع}}

{{العياط}}
{{شريط بوابات|محافظة الجيزة|تجمعات سكانية|مصر}}
{{بذرة محافظة الجيزة}}

[[تصنيف:قرى العياط]]

"""
        summary = "Test summary"
        pobj = Parsed(text, summary)
        new_text, new_summary = pobj.__call__()
        self.assertEqual(text, new_text)
        self.assertTrue(len(pobj.cite_templates),2)

if __name__ == '__main__':
    unittest.main()
