from abc import abstractmethod
from typing import Any
import re
from anonymizer.mask_settings import StringMaskSettings


class MaskerBase:
    allowed_type: type

    def __init__(self, value, setting=None) -> None:
        if not self.check_value(value):
            raise ValueError(f'Value {value} is not valid')

        self.__value = value
        self.__value_anonymized = None
        self.config_mask = setting

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


class MaskerString(MaskerBase):
    allowed_type = str

    def __init__(self, value: str, setting: StringMaskSettings) -> None:
        super().__init__(value, setting)

    def __str__(self) -> str:
        return self.anonymize()

    def __anonymize(self, value) -> str:
        total_to_mask = len(value) * self.config_mask.size_anonymization
        pattern = re.escape(value[:total_to_mask])
        modified = re.sub(pattern, '*' * total_to_mask, value, count=1)
        return modified

    def anonymize(self) -> str:
        if self.__value_anonymized is None:
            self.__value_anonymized = self.__anonymize(self.__value)
        return self.__value_anonymized

