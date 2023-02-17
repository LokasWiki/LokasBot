import pywikibot
from tasks.webcite.modules.parsed import Parsed

site = pywikibot.Site()

titles = [
    "1._FC_Union_Berlin",
    "100_امرأة_(بي_بي_سي)",
    "1455_هـ",
    "1934_في_إسبانيا",
    "1966",
    "1973_في_ألمانيا",
    "1975_في_مصر",
    "2002_في_سوريا",
    "2004",
    "2022",
    "2023_في_العراق",
    "3_رجال_سيئين",
    "50000_كواور",
    "90_دقيقة",
    "Cartography",
    "Convention_on_Nuclear_Safety",
    "List_of_administrators_of_Allied-occupied_Germany",
    "UNAF",
    "آتيس_ضيوف",
    "آدم_رجايبي",
    "آدم_نيومان",
    "آر_تي_الألمانية",
    "آراء_دينية_حول_الاستمناء",
    "آرتور_بوكا",
    "آرثر_تشارلز_هاردي",
    "آرون_بور",
    "آرييل_نغوكام",
    "آصف_علي_زرداري",
    "آفة_النبيذ_الفرنسي_الكبرى",
    "آل_جور",
    "آلان_إيوبو",
    "آلان_الريس",
    "آلان_بونو",
    "آلان_ميندي",
    "آنا_بورغراس",
    "آنا_ريتا_سيركويرا",
    "آي_بي_تي_في",
    "آيات_القرمزي",
    "آيت_عبد_الله",
    "آيت_عبد_الله_(آيت_عبد_الله)",
    "آيت_عبد_الله_(الحمام)",
    "أبافنجين",
    "أبراهام_شارب",
    "أبرشية_آسيا",
    "أبرشية_إفريقيا",
    "أبرشية_البنطس",
    "أبرشية_الغال",
    "أبرشية_بانونيا",
    "أبرشية_ثراسيا",
    "أبرشية_داسيا",
    "أبرشية_فيينا",
    "أبرشية_مقدونيا",
    "أبو_الحسن_الهاشمي_القرشي",
    "أبو_العرقان",
    "أبو_بكر_أومارو",
    "أبو_بكر_الصنوبري",
    "أبو_ذؤيب_السعدي",
    "أبو_زيد_الهلالي",
    "أبو_شوشة_(الرملة)",
    "أبو_عنان_فارس",
    "أبو_غالب_(الجيزة)",
    "أبو_لؤلؤة_المجوسي",
    "أبو_موسى_الأشعري",
    "أبو_يعقوب_يوسف_بن_عبد_المؤمن",
    "أبوت_لويل_كامينغز",
    "أبولا_إديل",
    "أبيل_كامبوس",
    "أتريس",
    "أتمتة_خلوية",
    "أتيميس",
    "أحداث_الأزمة_السورية",
    "أحلام_الشامسي",
    "أحلام_اليقظة_المفرطة",
    "أحلام_عمرنا_(فيلم)",
    "أحمد_الحران",
    "أحمد_العش",
    "أحمد_العنزي_(لاعب_كرة_قدم_سعودي)",
    "أحمد_باحسين",
    "أحمد_حسين_(سياسي)",
    "أحمد_عقل",
    "أحمد_عقل_(ممثل)",
    "أحمد_نغويامزا",
    "أحياء_أم_درمان",
    "أداما_سار",
    "أدب_جاهلي",
    "أدب_صدر_الإسلام",
    "أدلاي_ستيفنسون_الأول",
    "أرارات_(فيلم)",
    "أرتميس",
    "أرتور_أندروس",
    "أرتور_هيرنيك_أوياما",
    "أردلانيون",
    "أرز_أطلسي",
    "أرسينيو_بينيتيز",
    "أرسينيو_سيباستياو",
    "أرشد_الصالحي",
    "أرشيف_عصبة_الأمم",
    "أرشيف_مانشستر_للموسيقى_الرقمية",
    "أرشيف_وثائق_صناعة_الأدوية",
    "أرض_أرض_(فيلم)"
]

for page_name in titles:
    page = pywikibot.Page(site, page_name)
    if page.exists():
        summary = ""

        bot = Parsed(page.text, summary)
        new_text, new_summary = bot()

        if new_text != page.text:
            page.text = new_text
            page.save(new_summary)
