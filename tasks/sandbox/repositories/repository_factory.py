from enum import Enum, auto
from tasks.sandbox.use_cases.page_repository import PageRepository
from tasks.sandbox.repositories.pywikibot_page_repository import PywikibotPageRepository


class RepositoryType(Enum):
    PYWIKIBOT = auto()
    # Can add more repository types here like:
    # MWCLIENT = auto()
    # API = auto()


class RepositoryFactory:
    @staticmethod
    def create_repository(repo_type: RepositoryType) -> PageRepository:
        """
        Create a repository instance based on the specified type.
        
        Args:
            repo_type (RepositoryType): The type of repository to create.
            
        Returns:
            PageRepository: An instance of the requested repository type.
            
        Raises:
            ValueError: If the repository type is not supported.
        """
        if repo_type == RepositoryType.PYWIKIBOT:
            return PywikibotPageRepository()
        
        raise ValueError(f"Unsupported repository type: {repo_type}") 