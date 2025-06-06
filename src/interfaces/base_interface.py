from abc import ABC, abstractmethod

class BaseInterface(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def get_user_input(self):
        pass

    @abstractmethod
    def show_response(self, response):
        pass

    @abstractmethod
    def prompt_for_parameters(self):
        pass