import unittest

from tasks.copypatrol.domain.entities.copyright_case import CopyrightCase


class TestCopyrightCase(unittest.TestCase):
    def test_copyright_case_creation(self):
        # Act
        case = CopyrightCase(id=1, lang='ar', project='wikipedia', status=None)

        # Assert
        self.assertEqual(case.id, 1)
        self.assertEqual(case.lang, 'ar')
        self.assertEqual(case.project, 'wikipedia')
        self.assertIsNone(case.status)


if __name__ == '__main__':
    unittest.main()
