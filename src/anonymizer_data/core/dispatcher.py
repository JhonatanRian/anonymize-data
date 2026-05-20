from typing import Any, Callable, Dict

Masker = Any
MaskerFactory = Callable[..., Masker]


DEFAULT_MASKERS: Dict[str, MaskerFactory] = {}


def dispatch_value_mask(value: Any, **extra: Any) -> Masker:
    """Factory that contains the logic for choosing the correct masker for each type of data."""
    from .list import MaskList
    from .string import MaskStr
    from .dict import MaskDict

    DEFAULT_MASKERS.update(
        {
            "list": lambda value, **kwargs: MaskList(value, **kwargs).anonymize(),
            "dict": lambda value, **kwargs: MaskDict(value, **kwargs).anonymize(),
            "str": lambda value, **kwargs: MaskStr(value, **kwargs).anonymize(),
        }
    )

    type_name = type(value).__name__
    masker_factory = DEFAULT_MASKERS.get(type_name)

    if masker_factory:
        return masker_factory(value, **extra)

    if extra.get("type_mask"):
        return MaskStr(str(value), **extra).anonymize()

    return value
