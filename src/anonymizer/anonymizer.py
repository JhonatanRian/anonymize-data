from abc import abstractmethod
from typing import Any


class MaskerBase:
    allowed_type: type

    def __init__(self, value) -> None:
        if not self.check_value(value):
            raise ValueError(f'Value {value} is not valid')

        self.__value = value
        self.__value_anonymized = None

    def check_value(self, value) -> bool:
        return isinstance(value, self.allowed_type)

    def view(self) -> Any:
        return self.__value

    @abstractmethod
    def anonymize(self):
        pass

    @abstractmethod
    def __anonymize(self, value):
        pass


