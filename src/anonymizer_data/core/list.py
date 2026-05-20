from typing import Any, Dict, List

from .base import MaskBase, T


class MaskList(MaskBase[List[T]]):
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
        >>> from anonymizer_data.core import MaskList
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
        from .dispatcher import dispatch_value_mask
        return [dispatch_value_mask(item, **self._extra) for item in value]

    @property
    def __list__(self) -> list:
        return self._value_anonymized or self._value

    def __getitem__(self, index: int) -> T:
        value_list = self._value_anonymized or self._value
        return value_list[index]

    def __eq__(self, other: object) -> bool:
        value_compare = self._value_anonymized or self._value
        if isinstance(other, list):
            return value_compare == other
        elif isinstance(other, MaskList):
            return value_compare == list(other)
        return False
