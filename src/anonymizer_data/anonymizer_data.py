from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Optional, TypeVar, Dict, List, Union

from anonymizer_data.mask_dispatch import MaskDispatch

T = TypeVar("T")


def dispatch_value_mask(
    value: Any, **extra: Any
) -> Union["MaskStr", "MaskList", "MaskDict", Any]:
    match type(value).__name__:
        case "list":
            return MaskList(value, **extra).anonymize()
        case "dict":
            return MaskDict(value, **extra).anonymize()
        case "str":
            return MaskStr(value, **extra).anonymize()
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

    def __str__(self) -> str:
        return str(self._value_anonymized or self._value)

    def __len__(self):
        return len(self._value_anonymized or self._value)

    def __iter__(self):
        return iter(self._value_anonymized or self._value)


class MaskStr(MaskBase):
    """
    Class to anonymize strings.

    Attributes:
        value (str): The string to anonymize.
        type_mask (Optional[str]): The type mask to anonymize. Default is "string".
        anonymize_string (Optional[bool]): If false the string will never be anonymized. default is True.
        size_anonymization (Optional[float]): The size of the anonymized string.
        string_masker (Optional[MaskDispatch]): Dispatcher of the string to anonymize.

    Returns:
        MaskStr: A object MaskStr.

    Examples:
        >>> string = MaskStr("Hello world")
        >>> print(string)
        Hello world
        >>> string.anonymize()
        '*******ord'
        >>> print(string)
        *******ord
        >>> string.view()  # View original string
        Hello Word

    Raises:
        ValueError: The 'size_anonymization' field must be between 0 and 1.
        ValueError: The 'size_anonymization' must be a float.
        ValueError: Value {value} is not valid.
    """

    _allowed_type = str
    _type_mask_default: str = "string"

    def __init__(
        self,
        value: str,
        type_mask: Optional[str] = None,
        anonymize_string: bool = True,
        string_masker: Optional[MaskDispatch] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(value)

        self._type_mask: str = type_mask or self._type_mask_default
        self._string_masker: MaskDispatch = string_masker or MaskDispatch()
        self.__anonymize_string: bool = anonymize_string

        if self._type_mask == self._type_mask_default:
            size_anonymization = kwargs.get("size_anonymization", 0.7)
            self._validate_size_anonymization(size_anonymization)
            kwargs["size_anonymization"] = size_anonymization

        self._extra: Dict[str, Any] = kwargs

    def __repr__(self):
        return f"<MaskStr>"

    def _anonymize(self, value: str) -> str:
        if not self.__anonymize_string:
            return value
        return self._string_masker.mask(self._type_mask, value, **self._extra)

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
    This class anonymizes data contained in lists. Just like `MaskDict`, it can be data of type `str`, `dict` or `list`.

    Attributes:
        value (str): The string to anonymize.
        type_mask (Optional[str]): The type mask to anonymize. Default is "string".
        string_masker (bool): If false the string will never be anonymized. default is True.
        size_anonymization (float): The size of the anonymized string.

    Note:
        The "size_anonymization" parameter will be passed to MaskStr for each string contained in "value" as well as
        the other parameters, keeping this in mind be aware that if you pass an invalid value a ValueError may occur
        when calling the "anonymize" method.

    Returns:
        MaskList: A object MaskList.

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

    Raises:
        ValueError: Value {value} is not valid.
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

    def __eq__(self, other):
        value_compare = self._value_anonymized or self._value
        if isinstance(other, list):
            return value_compare == other
        elif isinstance(other, MaskList):
            return value_compare == list(other)
        return False


class MaskDict(MaskBase):
    """
    This class performs dictionary anonymization. For string values it will use the `MaskStr` class, for lists it
    will use the `MaskList` class and for dictionaries it will use `MaskDict`. This allows mass masking to occur.
    Knowing this, remember that parameters such as `size_anonymization` or `type_mask` are passed to the anonymizations
    that occur in cascade.

    You can also choose which keys should be anonymized, or choose to use dictionary keys as `type_mask` so that they
    are dispatched to data type handlers.

    Attributes:
        value (str): The string to anonymize.
        type_mask (Optional[str]): The type mask to anonymize. Default is "string".
        size_anonymization (Optional[float]): The size of the anonymized string.
        selected_keys (Optional[list[str]]): A list of selected keys that should be anonymized only.
        key_with_type_mask (Optional[bool]): If True it passes the keys as key_mask to the value when being anonymized.

    Returns:
        MaskStr: A object MaskStr.

    Examples:
        >>> dictionary = MaskDict({"key": "value_common", "key2": "value_common2"})
        >>> print(dictionary)
        {"key": "value_common", "key2": "value_common2"}
        >>> dictionary.anonymize()
        '*******ord'
        >>> print(dictionary)
        {'key': '********mmon', 'key2': '*********mon2'}
        >>> dictionary.view()  # View original string
        {"key": "value_common", "key2": "value_common2"}

    Raises:
        ValueError: Value {value} is not valid.

    Note:
        You should pay attention to the order of preference of these parameters. You can pass them all but one will
        always have more preference than the other, the order is: `size_anonymization` < `type_mask` < `selected_keys` < `key_with_type_mask`
    """

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

    def __iter__(self):
        if self._value_anonymized:
            return iter(self._value_anonymized.items())
        return iter(self._value.items())
