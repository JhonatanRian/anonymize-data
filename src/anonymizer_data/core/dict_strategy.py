from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, List

from .dispatcher import dispatch_value_mask


class DictAnonymizationStrategy(ABC):
    def __init__(self, **kwargs: Any) -> None:
        self._extra = kwargs

    @abstractmethod
    def anonymize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class DefaultDictAnonymizationStrategy(DictAnonymizationStrategy):
    def anonymize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        anonymized_dict = {}
        for key, value in data.items():
            anonymized_dict[key] = dispatch_value_mask(value, **self._extra)
        return anonymized_dict


class KeyBasedDictAnonymizationStrategy(DictAnonymizationStrategy):
    def __init__(self, selected_keys: List[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._selected_keys = selected_keys

    def anonymize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        anonymized_dict = {}
        for key, value in data.items():
            extra_data = deepcopy(self._extra)
            if self._selected_keys and key not in self._selected_keys:
                extra_data["anonymize_string"] = False
            anonymized_dict[key] = dispatch_value_mask(value, **extra_data)
        return anonymized_dict


class KeyAsTypeMaskDictAnonymizationStrategy(DictAnonymizationStrategy):
    def anonymize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        anonymized_dict = {}
        for key, value in data.items():
            extra_data = deepcopy(self._extra)
            extra_data["type_mask"] = key
            anonymized_dict[key] = dispatch_value_mask(value, **extra_data)
        return anonymized_dict
