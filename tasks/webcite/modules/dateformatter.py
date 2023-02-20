from datetime import datetime


class DateFormatter:
    def __init__(self, language: str = 'en'):
        self.language = language

    def format_timestamp(self, timestamp: str) -> str:

        dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        if self.language == 'ar':
            month_names = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                           'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
            month_name = month_names[dt.month - 1]
            formatted_date = f"{dt.day} {month_name} {dt.year}"
        else:
            formatted_date = dt.strftime('%d %B %Y')
        return formatted_date
