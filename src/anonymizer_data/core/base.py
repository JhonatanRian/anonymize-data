from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, Union

T = TypeVar("T")


class MaskBase(ABC, Generic[T]):
    _allowed_type: type

    def __init__(self, value: T) -> None:
        if not self.check_value(value):
            raise ValueError(f"Value {value} is not valid")

        self._value: T = value
        self._value_anonymized: Optional[Union[str, list, dict]] = None

    def check_value(self, value: T) -> bool:
        return isinstance(value, self._allowed_type)

    def view(self) -> T:
        return self._value

    def anonymize(self) -> T:
        """Returns and persists the anonymized value"""
        if self._value_anonymized is None:
            self._value_anonymized = self._anonymize(self._value)
        return self._value_anonymized or self._anonymize(self._value)

    @abstractmethod
    def _anonymize(self, value: T) -> T:
        pass

    def __str__(self) -> str:
        return str(self._value_anonymized or self._value)

    def __len__(self) -> int:
        return len(self._value_anonymized or self._value)

    def __iter__(self):
        return iter(self._value_anonymized or self._value)
