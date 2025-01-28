import unittest

from tasks.sandbox.repositories.repository_factory import RepositoryFactory, RepositoryType
from tasks.sandbox.repositories.pywikibot_page_repository import PywikibotPageRepository


class TestRepositoryFactory(unittest.TestCase):
    def test_create_pywikibot_repository(self):
        """Test creating a Pywikibot repository"""
        repository = RepositoryFactory.create_repository(RepositoryType.PYWIKIBOT)
        self.assertIsInstance(repository, PywikibotPageRepository)

    def test_create_invalid_repository(self):
        """Test creating an invalid repository type raises ValueError"""
        # Create a mock enum value that doesn't exist in RepositoryType
        class MockRepositoryType:
            def __str__(self):
                return "INVALID"
        
        with self.assertRaises(ValueError) as context:
            RepositoryFactory.create_repository(MockRepositoryType())
        
        self.assertIn("Unsupported repository type", str(context.exception))

    def test_repository_type_enum(self):
        """Test RepositoryType enum values"""
        self.assertTrue(hasattr(RepositoryType, 'PYWIKIBOT'))
        self.assertIsInstance(RepositoryType.PYWIKIBOT, RepositoryType)


if __name__ == "__main__":
    unittest.main() 