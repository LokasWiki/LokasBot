import os
import unittest
import unittest.mock

from core.utils.lua_to_python import LuaToPython, save_lue_table, get_lue_table


class TestMain(unittest.TestCase):
    def setUp(self):
        # Create test file
        self.test_file = os.path.join(os.path.expanduser("~"), "test_lue_table.txt")
        with open(self.test_file, "w") as f:
            f.write("Test content")

    def test_save_lue_table(self):
        # Save test content
        content = "New test content"
        save_lue_table("test_lue_table.txt", content)

        # Read the file to verify that the content was saved
        with open(self.test_file) as f:
            file_content = f.read()

        self.assertEqual(content, file_content)

    def test_get_lue_table(self):
        # Read the test file
        content = get_lue_table("test_lue_table.txt")

        self.assertEqual(content, "Test content")

    def test_save_lue_table_with_special_characters(self):
        # Save content with special characters
        content = "This is a test\nwith some special characters: &<>"
        save_lue_table("test_lue_table.txt", content)

        # Read the file to verify that the content was saved
        with open(self.test_file) as f:
            file_content = f.read()

        self.assertEqual(content, file_content)

    def test_save_lue_table_with_empty_content(self):
        # Save empty content
        content = ""
        save_lue_table("test_lue_table.txt", content)

        # Read the file to verify that the content was saved
        with open(self.test_file) as f:
            file_content = f.read()

        self.assertEqual(content, file_content)

    def test_get_lue_table_with_missing_file(self):
        # Test reading a non-existent file
        with self.assertRaises(FileNotFoundError):
            get_lue_table("nonexistent_file.txt")

    def test_get_lue_table_with_special_characters(self):
        # Test reading content with special characters
        with open(self.test_file, "w") as f:
            f.write("This is a test\nwith some special characters: &<>")

        content = get_lue_table("test_lue_table.txt")
        expected_content = 'This is a test\nwith some special characters: &<>'

        self.assertEqual(content, expected_content)

    def test_get_lue_table_with_empty_content(self):
        # Test reading an empty file
        with open(self.test_file, "w") as f:
            f.write("")

        content = get_lue_table("test_lue_table.txt")
        expected_content = ""

        self.assertEqual(content, expected_content)

    def tearDown(self):
        # Remove test file
        os.remove(self.test_file)

    def test_simple_parse(self):
        text = """
            return {
                ["كرة القدم في إفريقيا"] = {
                    "كرة القدم في أفريقيا"
                },
                ["تاريخ إفريقيا"] = {
                    "تاريخ أفريقيا"
                },
                ["الآشوريون والسريان والكلدان"] = {
                    "آشوريون - سريان - كلدان",
                    "كلدان",
                    "سريان",
                    "آشوريون",
                    "آشوريون/سريان/كلدان"
                },
                ["آيسلندا"] = {
                    "أيسلندا"
                },
        """
        valid = {'كرة القدم في إفريقيا': ['كرة القدم في أفريقيا'], 'تاريخ إفريقيا': ['تاريخ أفريقيا'],
                 'الآشوريون والسريان والكلدان': ['آشوريون - سريان - كلدان', 'كلدان', 'سريان', 'آشوريون',
                                                 'آشوريون/سريان/كلدان'], 'آيسلندا': ['أيسلندا']}
        ltp = LuaToPython(text)
        self.assertDictEqual(ltp.data, valid)
        self.assertCountEqual(ltp.data, valid)
        self.assertEqual(ltp.search("سريان"), "الآشوريون والسريان والكلدان")
        self.assertEqual(ltp.search("آشوريون"), "الآشوريون والسريان والكلدان")
        self.assertEqual(ltp.search("الآشوريون والسريان والكلدان"), "الآشوريون والسريان والكلدان")
        self.assertEqual(ltp.search("أيسلندا"), "آيسلندا")
        self.assertEqual(ltp.search("آيسلندا"), "آيسلندا")
        self.assertIsNone(ltp.search("test"))
        self.assertEqual(text, ltp.input_lua)


if __name__ == "__main__":
    unittest.main()
