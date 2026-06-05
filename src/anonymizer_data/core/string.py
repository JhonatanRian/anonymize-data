from typing import Any

from anonymizer_data.handlers.dispatch import MaskDispatch

from .base import MaskBase


class MaskStr(MaskBase[str]):
    """
    Class to anonymize strings.

    Attributes:
        value (str): The string to anonymize.
        type_mask (Optional[str]): The type mask to anonymize. Default is "string".
        anonymize_string (Optional[bool]): If false the string will never be anonymized. default is True.
        size_anonymization (Optional[float]): The size of the anonymized string.
        string_masker (Optional[MaskDispatch]): Dispatcher of the string to anonymize.

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
        type_mask: str | None = None,
        anonymize_string: bool = True,
        string_masker: MaskDispatch | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(value)

        self._type_mask: str = type_mask or self._type_mask_default
        self._string_masker: MaskDispatch = string_masker or MaskDispatch()
        self.__anonymize_string: bool = anonymize_string

        self._extra: dict[str, Any] = kwargs.copy()

        if "size_anonymization" in self._extra:
            self._validate_size_anonymization(self._extra["size_anonymization"])
        elif self._type_mask == self._type_mask_default:
            self._extra["size_anonymization"] = 0.7
            self._validate_size_anonymization(0.7)

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
