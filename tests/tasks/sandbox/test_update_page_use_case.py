import unittest
from unittest.mock import Mock, call

from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.use_cases.update_page_use_case import UpdatePageUseCase
from tasks.sandbox.use_cases.update_strategies import (
    ReplaceContentStrategy,
    AppendContentStrategy,
    PrependContentStrategy
)


class TestUpdatePageUseCase(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.repository = Mock()
        self.use_case = UpdatePageUseCase(self.repository)
        self.page = PageEntity(
            title="Test Title",
            text="New Content",
            summary="Test Summary"
        )
        self.existing_page = PageEntity(
            title="Test Title",
            text="Existing Content",
            summary=""
        )

    def test_execute_with_replace_strategy(self):
        """Test page update with replace strategy"""
        self.repository.get_page.return_value = self.existing_page
        self.use_case.set_strategy(ReplaceContentStrategy())
        self.use_case.execute(self.page)
        
        self.repository.save_page.assert_called_once()
        saved_page = self.repository.save_page.call_args[0][0]
        self.assertEqual(saved_page.text, "New Content")

    def test_execute_with_append_strategy(self):
        """Test page update with append strategy"""
        self.repository.get_page.return_value = self.existing_page
        self.use_case.set_strategy(AppendContentStrategy())
        self.use_case.execute(self.page)
        
        self.repository.save_page.assert_called_once()
        saved_page = self.repository.save_page.call_args[0][0]
        self.assertEqual(saved_page.text, "Existing Content\nNew Content")

    def test_execute_with_prepend_strategy(self):
        """Test page update with prepend strategy"""
        self.repository.get_page.return_value = self.existing_page
        self.use_case.set_strategy(PrependContentStrategy())
        self.use_case.execute(self.page)
        
        self.repository.save_page.assert_called_once()
        saved_page = self.repository.save_page.call_args[0][0]
        self.assertEqual(saved_page.text, "New Content\nExisting Content")

    def test_observers_notification(self):
        """Test that observers are notified of updates"""
        observer1 = Mock()
        observer2 = Mock()
        self.use_case.add_observer(observer1)
        self.use_case.add_observer(observer2)
        
        self.repository.get_page.return_value = self.existing_page
        self.use_case.execute(self.page)
        
        observer1.update.assert_called_once_with(self.page)
        observer2.update.assert_called_once_with(self.page)

    def test_execute_with_nonexistent_page(self):
        """Test update when page doesn't exist"""
        self.repository.get_page.side_effect = Exception("Page not found")
        self.use_case.execute(self.page)
        
        self.repository.save_page.assert_called_once()
        saved_page = self.repository.save_page.call_args[0][0]
        self.assertEqual(saved_page.text, "New Content")


if __name__ == "__main__":
    unittest.main()
