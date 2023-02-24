from datetime import datetime


class DateFormatter:
    """
    Utility class for formatting timestamps into human-readable dates.

    Args:
        language (str): Optional. The language of the formatted date string. Defaults to 'en'.

    Attributes:
        language (str): The language of the formatted date string.

    Methods:
        format_timestamp(timestamp: str) -> str:
            Formats a timestamp string into a human-readable date string according to the specified
            language. The timestamp string should be in the format 'YYYYMMDDHHMMSS'.

    Example usage:
        >>> formatter = DateFormatter()
        >>> formatter.format_timestamp('20220101000000')
        '01 January 2022'
    """

    def __init__(self, language: str = 'en'):
        self.language = language

    def format_timestamp(self, timestamp: str) -> str:
        """
        Formats a timestamp string into a human-readable date string according to the specified
        language.

        Args:
            timestamp (str): A timestamp string in the format 'YYYYMMDDHHMMSS'.

        Returns:
            str: A human-readable date string.

        Raises:
            ValueError: If the timestamp string is not in the correct format.
        """
        dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        if self.language == 'ar':
            month_names = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                           'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
            month_name = month_names[dt.month - 1]
            formatted_date = f"{dt.day} {month_name} {dt.year}"
        else:
            formatted_date = dt.strftime('%d %B %Y')
        return formatted_date
