from typing import Any, Dict, List, Optional

from .base import MaskBase
from .dict_strategy import (
    DefaultDictAnonymizationStrategy,
    DictAnonymizationStrategy,
    KeyAsTypeMaskDictAnonymizationStrategy,
    KeyBasedDictAnonymizationStrategy,
)

type DataDict = Dict[str, Any]


class MaskDict(MaskBase[DataDict]):
    _allowed_type = dict

    def __init__(
        self,
        value: DataDict,
        key_with_type_mask: bool = False,
        selected_keys: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(value)
        self._extra = kwargs
        self._strategy: DictAnonymizationStrategy = self._get_strategy(
            key_with_type_mask, selected_keys, **kwargs
        )

    def _get_strategy(
        self,
        key_with_type_mask: bool,
        selected_keys: Optional[List[str]],
        **kwargs: Any,
    ) -> DictAnonymizationStrategy:
        from .dispatcher import dispatch_value_mask
        if key_with_type_mask:
            return KeyAsTypeMaskDictAnonymizationStrategy(dispatch_value_mask, **kwargs)
        if selected_keys:
            return KeyBasedDictAnonymizationStrategy(selected_keys, dispatch_value_mask, **kwargs)
        return DefaultDictAnonymizationStrategy(dispatch_value_mask, **kwargs)

    def with_keys(self, keys: List[str]) -> "MaskDict":
        """Reconfigures the dictionary mask to use only the specified keys."""
        from .dispatcher import dispatch_value_mask
        self._strategy = KeyBasedDictAnonymizationStrategy(keys, dispatch_value_mask, **self._extra)
        return self

    def _anonymize(self, value: DataDict) -> DataDict:
        return self._strategy.anonymize(value)

    @property
    def __dict__(self) -> DataDict:
        return self._value_anonymized or self._value

    def __getitem__(self, key: str) -> Any:
        value_dict = self._value_anonymized or self._value
        return value_dict[key]

    def __iter__(self):
        if self._value_anonymized:
            return iter(self._value_anonymized.items())
        return iter(self._value.items())