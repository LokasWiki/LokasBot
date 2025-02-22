# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.17.2] - 2025-02-21

### Changed
- Improved database performance:
  - Updated queries to use `linktarget` table for better link resolution (#415)
  - Enhanced database queries in add_category task
  - Optimized portal distribution queries
  - Improved remove request query performance
- Re-enabled multiple Python scripts in toolforge job configuration (#415)


## [1.17.1] - 2025-02-09

### Added
- Full code implementation of Missing Topics Task (originally added in v1.0.0)
  - Added clean architecture implementation with complete test coverage
  - Implemented all planned features with proper documentation
  - Added comprehensive logging system
  - Integrated with required external services

### Changed
- Implemented Repository Pattern for flexible data source management
- Added Configuration Pattern for centralized API and database settings
- Introduced Command Pattern for operation encapsulation
- Enhanced logging system with structured format and multiple handlers

### Technical
- Added support for Python 3.6+
- Integrated with pywikibot for wiki operations
- Implemented pymysql for database connections
- Added requests library for API interactions
- Integrated wikitextparser for text processing

### Fixed
- إصلاح الأخطاء الإملائية
### Changed
- تحديث بوت (مهمة ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص) ليعمل علي النسخه الجديده من الموديل ([#141](https://github.com/LokasWiki/LokasBot/pull/141))  

### Added
 - اضافة استلام (اضافة استعلام بوت الصيانة - مقالات بحاجة لإضافة وسم يتيمة) حتي يجلب قائمة الصفحات ويضعها في البوت ([تم كتابه الاستلام الاساسي بواسطه الزميل ASammour](https://quarry.wmcloud.org/query/72149)) ([#140](https://github.com/LokasWiki/LokasBot/pull/140)) 



## [1.4.1] - 2023-03-18
### Fixed
-  تم إصلاح مشكلة عدم حذف الصفحات بعد إجراء الفحص عليها   ([#136](https://github.com/LokasWiki/LokasBot/pull/136)) ([#137](https://github.com/LokasWiki/LokasBot/pull/137))


## [1.4.0] - 2023-03-17

### Fixed
- إصلاح الأخطاء الإملائية  ([#123](https://github.com/LokasWiki/LokasBot/pull/123))

### Added

- بوت إضافة/إزالة قالب بذرة (مهمة الصيانة)  ([#127](https://github.com/LokasWiki/LokasBot/pull/127)) ([#130](https://github.com/LokasWiki/LokasBot/pull/130))

### Changed
- حذف كود sqlite واستخدام مكتبة sqlalchemy 
- أصبح كود مهمة الصيانة وأرشفة المراجع يعتمد علي قاعدة بيانات mysql بدلا من sqlite لحل مشكلة الاتصالات المتعددة
- تم تعديل  طريقة  جلب الصفحات الجديدة بالاعتماد علي آخر موعد تم إجراء البحث السابق فيه لحل مشكلة تكرر الصفحات ولزيادة أداء البوت وتقليل النطاق الترددي


## [1.3.0] - 2023-03-13
### Added
- إضافة قالب لا للوصلات قليلة لتخطي مهمة (إضافة/ إزالة قالب وصلات قليلة) (مهمة الصيانة)  ([#116](https://github.com/LokasWiki/LokasBot/pull/116))
- إضافة تعريب الوسائط بالاعتماد علي (ويكيبيديا:AutoWikiBrowser/Rename template parameters) (مهمة الصيانة)  ([#125](https://github.com/LokasWiki/LokasBot/pull/125))
- إضافة (مستخدم:LokasBot/تجاهل مهمة صيانة المقالات) لحل مشكل تضارب البوتات (مهمة الصيانة)  ([#120](https://github.com/LokasWiki/LokasBot/pull/120))
- إضافة التحديث التلقائي لمهمة (ويكيبيديا:مصادر موثوقة/معاجم وقواميس وأطالس/إحصائيات) حسب طلب الزميل مشيل  ([#117](https://github.com/LokasWiki/LokasBot/pull/117))

### Changed
- تغير وصف بوت:إحصاءات حتي يشمل رقم الإصدار لمزيد من التتبع
### Fixed
- حل مشكلة عدم تحديث (ويكيبيديا:إحصاءات/نشاط الإداريين) بعد آخر إصدار
- (مهمة الصيانة) إصلاح بعض الأخطاء من سجلات البوت
## [1.2.0] - 2023-03-7
### Added
- إضافة جدول جديد للبوتات ولكن بدون توزيع الأوسمة (مهمة مستخدمو الأسبوع الأكثر نشاطا)  ([#112](https://github.com/LokasWiki/LokasBot/pull/112))
- -إعادة تفعيل بوت (إضافة/إزالة قالب وصلات قليلة) بعد إعادة كتابة كود البوت من جديد (مهمة الصيانة)  ([#113](https://github.com/LokasWiki/LokasBot/pull/113))
- إضافة مهمة استبدال القوالب بالاعتماد علي (ويكيبيديا:AutoWikiBrowser/Template redirects) (تعمل كمهمة إضافية)(مهمة الصيانة)  ([#114](https://github.com/LokasWiki/LokasBot/pull/114))

## [1.1.0] - 2023-03-6
### Added
-  إعادة تفعيل بوت (إضافة/إزالة قالب نهاية مسدودة) بعد إعادة كتابة كود البوت من جديد  ([#101](https://github.com/LokasWiki/LokasBot/pull/101))
### Changed
- تم تعديل بوت (ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص) بحيث يبقي المستخدمين الذين تم إضافتهم أمس إلي القائمة في حالة عدم الفحص  ([#98](https://github.com/LokasWiki/LokasBot/pull/98))
- تم تحديث بوت الصيانة عبر تعديل الاستعلام الذي يجلب قائمة المقالات غير المراجعة عبر استخدام استعلام الزميل ASammour  ([#100](https://github.com/LokasWiki/LokasBot/pull/100))
- تعديل مواعيد عمل طلبات البوت إلي وقت أقل
- جعل بوت الأرشفة يؤرشف حتي ٢٠ رابط في المرة الواحدة
- تحسين أكواد مهام بوت الصيانة عبر حذف أكواد regex واستخدام wikitextparser
- إضافة الترتيب الصحيح للقوالب في حالة وجود قوالب البذور
### Fixed
- إصلاح مشكلة تجاهل بعض قوالب الاستشهاد
- تجاهل الصفحات التي تم إنشاؤها قبل ثلاث ساعات من الآن لتحسين النتائج
- دمج الأكواد المكررة بين مهمة أرشفة المصادر ومهمة الصيانة

## [1.0.3] - 2023-03-2
### Changed
- تم تعديل نص بوت مهمة (ويكيبيديا:مصادر موثوقة/معاجم وقواميس وأطالس/إحصائيات)
### Added
- تم إضافة الإصدار الأول من بوت (ويكيبيديا:إحصاءات الشهر)  ([#96](https://github.com/LokasWiki/LokasBot/pull/96))
### Fixed
- تم تحديث الكود بوت (مهمة صيانة المقالات) الي الإصدار  (v4.4.9) (تم تجاهل صفحات التواريخ من مهمة (إضافة/ إزالة قالب لا مصدر) عن طريق تجاهل جميع صفحات بوابة (بوابة تقويم)) ([#97](https://github.com/LokasWiki/LokasBot/pull/97))

## [1.0.2] - 2023-02-28
### Changed
- تم تحديث الكود بوت (ويكيبيديا: إخطار الإداريين/ أسماء مستخدمين للفحص) إلي الإصدار  (v1.3) حتي يجعل صفحة (ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/تشغيل البوت) فارغة عند التحديث ([#95](https://github.com/LokasWiki/LokasBot/pull/95))


## [1.0.1] - 2023-02-27
### Fixed
- تم تحديث الكود بوت (ويكيبيديا: إخطار الإداريين/ أسماء مستخدمين للفحص) لمنع التشغيل التلقائي للكود عند استيراد المكتبات ([#94](https://github.com/LokasWiki/LokasBot/pull/94))

## [1.0.0] - 2023-02-27
### Added
- تم إضافة الإصدار الأول من بوت (ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص)  ([#92](https://github.com/LokasWiki/LokasBot/pull/92))
- Missing Topics Task: Initial design and planning
  - Clean Architecture design with Entities, Use Cases, Repositories, and Observers
  - Support for identifying articles missing in Arabic Wikipedia that exist in English Wikipedia
  - Dynamic bot name configuration and batch processing capabilities
  - Rate limiting and performance optimization features
  - Comprehensive logging system with multiple levels
  - Multiple observer pattern support for progress monitoring
  - Configurable database connections for different wikis
  - Type hints for better IDE support
  - Real-time timestamp updates
  - Extensive test suite planning

### Technical (Planned)
- Python 3.6+ support
- Integration with pywikibot for wiki operations
- Database connections via pymysql
- HTTP requests via requests library
- Text processing with wikitextparser
