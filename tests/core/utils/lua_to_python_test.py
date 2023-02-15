import unittest
import unittest.mock

from core.utils.lua_to_python import LuaToPython


class TestMain(unittest.TestCase):

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
        valid = {'كرة القدم في إفريقيا': ['كرة القدم في أفريقيا'], 'تاريخ إفريقيا': ['تاريخ أفريقيا'], 'الآشوريون والسريان والكلدان': ['آشوريون - سريان - كلدان', 'كلدان', 'سريان', 'آشوريون', 'آشوريون/سريان/كلدان'], 'آيسلندا': ['أيسلندا']}
        ltp = LuaToPython(text)
        self.assertDictEqual(ltp.data,valid)
        self.assertCountEqual(ltp.data,valid)
        self.assertEqual(ltp.search("سريان"),"الآشوريون والسريان والكلدان")
        self.assertEqual(ltp.search("آشوريون"),"الآشوريون والسريان والكلدان")
        self.assertEqual(ltp.search("الآشوريون والسريان والكلدان"),"الآشوريون والسريان والكلدان")
        self.assertEqual(ltp.search("أيسلندا"),"آيسلندا")
        self.assertEqual(ltp.search("آيسلندا"),"آيسلندا")
        self.assertIsNone(ltp.search("test"))
        self.assertEqual(text,ltp.input_lua)



if __name__ == "__main__":
    unittest.main()
