from abc import ABC, abstractmethod
from typing import Any, Optional

from anonymizer.exceptions import KeyMaskError
from anonymizer.string_mask import MaskDispatch


def dispatch_value_mask(value, save_mask, **extra):
    match type(value).__name__:
        case 'list':
            return MaskList(value, save_mask=save_mask, **extra).anonymize()
        case 'dict':
            return MaskDict(value, save_mask=save_mask, **extra).anonymize()
        case 'str':
            return MaskString(value, save_mask=save_mask, **extra).anonymize()
        case _:
            return value


class MaskBase(ABC):
    allowed_type: type

    def __init__(self, value: Any, save_mask: bool) -> None:
        if not self.check_value(value):
            raise ValueError(f'Value {value} is not valid')

        self._value = value
        self._value_anonymized = None
        self._save_mask = save_mask

    def check_value(self, value: Any) -> bool:
        return isinstance(value, self.allowed_type)

    def view(self) -> Any:
        return self._value

    def anonymize(self):
        if self._value_anonymized is None and self._save_mask:
            self._value_anonymized = self._anonymize(self._value)
        return self._value_anonymized or self._anonymize(self._value)

    @abstractmethod
    def _anonymize(self, value: Any) -> str:
        pass


class MaskString(MaskBase):
    allowed_type = str
    _type_mask_default: str = "string"

    def __init__(self, value: str, type_mask: Optional[str] = None,
                 string_mask: Optional[MaskDispatch] = None, save_mask: bool = True,
                 anonymize_string: bool = True, **kwargs) -> None:
        super().__init__(value, save_mask)

        self._type_mask = type_mask or self._type_mask_default
        self._string_mask = string_mask or MaskDispatch()
        self.__anonymize_string = anonymize_string

        if self._type_mask == self._type_mask_default:
            size_anonymization = kwargs.get("size_anonymization", 0.7)
            self.validate_size_anonymization(size_anonymization)
            kwargs['size_anonymization'] = size_anonymization

        self._extra = kwargs

    def __str__(self) -> str:
        return self.anonymize()

    def _anonymize(self, value: str) -> str:
        if not self.__anonymize_string:
            return value
        return self._string_mask.mask(self._type_mask, value, **self._extra)

    @staticmethod
    def validate_size_anonymization(size_anonymization: float) -> None:
        """Validates the size_anonymization parameter."""
        if not isinstance(size_anonymization, float):
            raise ValueError("The 'size_anonymization' must be a float.")

        size_anonymization = round(size_anonymization, 1)

        if not (0 <= size_anonymization <= 1):
            raise ValueError("The 'size_anonymization' field must be between 0 and 1.")


class MaskList(MaskBase):
    allowed_type = list

    def __init__(self, value: list, save_mask: bool = True, **kwargs) -> None:
        super().__init__(value, save_mask)

        self._extra = kwargs

    def _anonymize(self, value: list) -> list:
        return [dispatch_value_mask(
            item, save_mask=False, **self._extra
        ) for item in value]

    def list(self) -> list:
        return self._value_anonymized or self._value

    def __getitem__(self, index):
        value_list = self._value_anonymized or self._value
        return value_list[index]

    def __len__(self):
        return len(self._value_anonymized or self._value)

    def __iter__(self):
        return iter(self._value_anonymized or self._value)

    def __str__(self) -> str:
        return str(self._value_anonymized or self._value)

    def __eq__(self, other):
        value_compare = self._value_anonymized or self._value
        if isinstance(other, list):
            return value_compare == other
        elif isinstance(other, MaskList):
            return value_compare == other.list()
        return False


class MaskDict(MaskBase):
    allowed_type = dict

    def __init__(self, value: dict, save_mask: bool = True, key_with_type_mask: bool = False, **kwargs) -> None:
        super().__init__(value, save_mask)
        self.__key_with_type_mask = key_with_type_mask

        if key_with_type_mask and kwargs.get('type_mask', False):
            raise KeyMaskError('Only one of these parameters can be true, not both. "key_with_type_mask" | "type_mask"')

        self._extra = kwargs

    def _anonymize(self, value: dict) -> dict:
        dict_anonymized = {}
        for key, value in value.items():
            if self.__key_with_type_mask:
                value_anonymized = dispatch_value_mask(
                    value, save_mask=False, type_mask=key, **self._extra
                )
            else:
                value_anonymized = dispatch_value_mask(
                    value, save_mask=False, **self._extra
                )
            dict_anonymized[key] = value_anonymized
        return dict_anonymized

    def dict(self) -> dict:
        return self._value_anonymized

    def __getitem__(self, key):
        value_dict = self._value_anonymized or self._value
        return value_dict[key]

    def __len__(self):
        return len(self._value_anonymized or self._value)

    def __iter__(self):
        return iter(self._value_anonymized or self._value)

    def __str__(self) -> str:
        return str(self._value_anonymized or self._value)
