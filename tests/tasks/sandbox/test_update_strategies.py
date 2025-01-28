import unittest

from tasks.sandbox.use_cases.update_strategies import (
    ReplaceContentStrategy,
    AppendContentStrategy,
    PrependContentStrategy
)


class TestUpdateStrategies(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.current_content = "Current Content"
        self.new_content = "New Content"

    def test_replace_strategy(self):
        """Test replace content strategy"""
        strategy = ReplaceContentStrategy()
        result = strategy.prepare_content(self.current_content, self.new_content)
        self.assertEqual(result, "New Content")

    def test_append_strategy(self):
        """Test append content strategy"""
        strategy = AppendContentStrategy()
        result = strategy.prepare_content(self.current_content, self.new_content)
        self.assertEqual(result, "Current Content\nNew Content")

    def test_prepend_strategy(self):
        """Test prepend content strategy"""
        strategy = PrependContentStrategy()
        result = strategy.prepare_content(self.current_content, self.new_content)
        self.assertEqual(result, "New Content\nCurrent Content")

    def test_strategies_with_empty_current_content(self):
        """Test strategies with empty current content"""
        empty_content = ""
        
        replace = ReplaceContentStrategy()
        self.assertEqual(
            replace.prepare_content(empty_content, self.new_content),
            "New Content"
        )
        
        append = AppendContentStrategy()
        self.assertEqual(
            append.prepare_content(empty_content, self.new_content),
            "\nNew Content"
        )
        
        prepend = PrependContentStrategy()
        self.assertEqual(
            prepend.prepare_content(empty_content, self.new_content),
            "New Content\n"
        )

    def test_strategies_with_empty_new_content(self):
        """Test strategies with empty new content"""
        empty_content = ""
        
        replace = ReplaceContentStrategy()
        self.assertEqual(
            replace.prepare_content(self.current_content, empty_content),
            ""
        )
        
        append = AppendContentStrategy()
        self.assertEqual(
            append.prepare_content(self.current_content, empty_content),
            "Current Content\n"
        )
        
        prepend = PrependContentStrategy()
        self.assertEqual(
            prepend.prepare_content(self.current_content, empty_content),
            "\nCurrent Content"
        )


if __name__ == "__main__":
    unittest.main() 