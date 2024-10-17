from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Optional, TypeVar, Dict, List, Union

from anonymizer.string_mask import MaskDispatch

T = TypeVar("T")


def dispatch_value_mask(value: Any, **extra: Any) -> Any:
    match type(value).__name__:
        case "list":
            return MaskList(value, **extra).anonymize()
        case "dict":
            return MaskDict(value, **extra).anonymize()
        case "str":
            return MaskString(value, **extra).anonymize()
        case _:
            return value


class MaskBase(ABC):
    _allowed_type: type

    def __init__(self, value: T) -> None:
        if not self.check_value(value):
            raise ValueError(f"Value {value} is not valid")

        self._value: T = value
        self._value_anonymized: Optional[Union[str, list, dict]] = None

    def check_value(self, value: Any) -> bool:
        return isinstance(value, self._allowed_type)

    def view(self) -> Any:
        return self._value

    def anonymize(self):
        """Returns and persists the anonymized value"""
        if self._value_anonymized is None:
            self._value_anonymized = self._anonymize(self._value)
        return self._value_anonymized or self._anonymize(self._value)

    @abstractmethod
    def _anonymize(self, value: Any) -> str:
        pass


class MaskString(MaskBase):
    """
    Class to anonymize strings.

    Attributes:
        value (str): The string to anonymize.
        type_mask (Optional[str]): The type mask to anonymize. Default is "string".
        string_mask (bool): If false the string will never be anonymized. default is True.
        size_anonymization (float): The size of the anonymized string.

    Examples:
        >>> string = MaskString("Hello world")
        >>> print(string)
        Hello world
        >>> string.anonymize()
        '*******ord'
        >>> print(string)
        *******ord
        >>> string.view()  # View original string
        Hello Word

    Returns:
        MaskString: A object MaskString.

    Raises:
        ValueError: The 'size_anonymization' field must be between 0 and 1.
    """

    _allowed_type = str
    _type_mask_default: str = "string"

    def __init__(
        self,
        value: str,
        type_mask: Optional[str] = None,
        string_mask: Optional[MaskDispatch] = None,
        anonymize_string: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(value)

        self._type_mask: str = type_mask or self._type_mask_default
        self._string_mask: MaskDispatch = string_mask or MaskDispatch()
        self.__anonymize_string: bool = anonymize_string

        if self._type_mask == self._type_mask_default:
            size_anonymization = kwargs.get("size_anonymization", 0.7)
            self._validate_size_anonymization(size_anonymization)
            kwargs["size_anonymization"] = size_anonymization

        self._extra: Dict[str, Any] = kwargs

    def __str__(self) -> str:
        return self._value_anonymized or self._value

    def __repr__(self):
        return f"<MaskString>"

    def _anonymize(self, value: str) -> str:
        if not self.__anonymize_string:
            return value
        return self._string_mask.mask(self._type_mask, value, **self._extra)

    @staticmethod
    def _validate_size_anonymization(size_anonymization: float) -> None:
        """Validates the size_anonymization parameter."""
        if not isinstance(size_anonymization, float):
            raise ValueError("The 'size_anonymization' must be a float.")

        size_anonymization = round(size_anonymization, 1)

        if not (0 < abs(size_anonymization) <= 1):
            raise ValueError("The 'size_anonymization' field must be between 0 and 1.")


class MaskList(MaskBase):
    """
    Class to anonymize strings.\n

    Note:
        The "size_anonymization" parameter will be passed to MaskString for each string contained in "value" as well as
        the other parameters, keeping this in mind be aware that if you pass an invalid value a ValueError may occur
        when calling the "anonymize" method.

    Attributes:
        value (str): The string to anonymize.
        type_mask (Optional[str]): The type mask to anonymize. Default is "string".
        string_mask (bool): If false the string will never be anonymized. default is True.
        size_anonymization (float): The size of the anonymized string.

    Examples:
        >>> mask_list = MaskList(["Hello world", "Hello Python"])
        >>> print(mask_list)
        ["Hello world", "Hello Python"]
        >>> mask_list.anonymize()
        ['*******orld', '********thon']
        >>> mask_list = MaskList(["Hello world", "Hello Python"], size_anonymization=0.5)  # anonymizing by half
        >>> print(mask_list.anonymize())
        ['***** world', '******Python']
        >>> mask_list.view()  # View original list
        ["Hello world", "Hello Python"]

    Returns:
        MaskList: A object MaskList.

    """

    _allowed_type = list

    def __init__(self, value: List[T], **kwargs: Any) -> None:
        super().__init__(value)

        self._extra: Dict[str, Any] = kwargs

    def _anonymize(self, value: list) -> list:
        return [dispatch_value_mask(item, **self._extra) for item in value]

    @property
    def __list__(self) -> list:
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
            return value_compare == list(other)
        return False


class MaskDict(MaskBase):
    _allowed_type = dict

    def __init__(
        self,
        value: Dict[str, Any],
        key_with_type_mask: bool = False,
        selected_keys: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(value)
        self.__key_with_type_mask: bool = key_with_type_mask
        self.__selected_keys: List[str] = selected_keys or []

        self._extra: Dict[str, Any] = kwargs
        self._extra["selected_keys"] = self.__selected_keys
        self._extra["key_with_type_mask"] = self.__key_with_type_mask

        if len(self.__selected_keys) > 0:
            self._extra["anonymize_string"] = True

        if self.__key_with_type_mask:
            self._extra.pop("type_mask", None)

    def _anonymize(self, value: dict) -> dict:
        dict_anonymized = {}
        for k, v in value.items():
            extra_data = deepcopy(self._extra)

            if len(self.__selected_keys) > 0 and k not in self.__selected_keys:
                extra_data["anonymize_string"] = False

            if self.__key_with_type_mask:
                extra_data["type_mask"] = k

            value_anonymized = dispatch_value_mask(v, **extra_data)
            dict_anonymized[k] = value_anonymized
        return dict_anonymized

    @property
    def __dict__(self) -> dict:
        return self._value_anonymized or self._value

    def __getitem__(self, key):
        value_dict = self._value_anonymized or self._value
        return value_dict[key]

    def __len__(self):
        return len(self._value_anonymized or self._value)

    def __iter__(self):
        if self._value_anonymized:
            return iter(self._value_anonymized.items())
        return iter(self._value.items())

    def __str__(self) -> str:
        return str(self._value_anonymized or self._value)
