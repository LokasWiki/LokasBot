from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, id, user_name, created_at):
        self.id = id
        self.user_name = user_name
        self.created_at = created_at

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def set_id(self, id):
        pass

    @abstractmethod
    def get_user_name(self):
        pass

    @abstractmethod
    def set_user_name(self, user_name):
        pass

    @abstractmethod
    def get_created_at(self):
        pass

    @abstractmethod
    def set_created_at(self, created_at):
        pass
