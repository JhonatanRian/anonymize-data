from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Callable


class DictAnonymizationStrategy(ABC):
    def __init__(self, dispatcher_func: Callable[..., Any], **kwargs: Any) -> None:
        self._dispatcher_func = dispatcher_func
        self._extra = kwargs

    @abstractmethod
    def anonymize(self, data: dict[str, Any]) -> dict[str, Any]:
        pass


class DefaultDictAnonymizationStrategy(DictAnonymizationStrategy):
    def anonymize(self, data: dict[str, Any]) -> dict[str, Any]:
        anonymized_dict = {}
        for key, value in data.items():
            anonymized_dict[key] = self._dispatcher_func(value, **self._extra)
        return anonymized_dict


class KeyBasedDictAnonymizationStrategy(DictAnonymizationStrategy):
    def __init__(
        self,
        selected_keys: list[str],
        dispatcher_func: Callable[..., Any],
        **kwargs: Any,
    ) -> None:
        super().__init__(dispatcher_func, **kwargs)
        self._selected_keys = selected_keys

    def anonymize(self, data: dict[str, Any]) -> dict[str, Any]:
        anonymized_dict = {}
        for key, value in data.items():
            extra_data = deepcopy(self._extra)
            if self._selected_keys and key not in self._selected_keys:
                extra_data["anonymize_string"] = False
            anonymized_dict[key] = self._dispatcher_func(value, **extra_data)
        return anonymized_dict


class KeyAsTypeMaskDictAnonymizationStrategy(DictAnonymizationStrategy):
    def anonymize(self, data: dict[str, Any]) -> dict[str, Any]:
        anonymized_dict = {}
        for key, value in data.items():
            extra_data = deepcopy(self._extra)
            extra_data["type_mask"] = key
            anonymized_dict[key] = self._dispatcher_func(value, **extra_data)
        return anonymized_dict
