from typing import Callable, Dict, Any

from anonymizer.handlers_anonymize import (
    handler_anonymize_string,
    handler_anonymize_type_cpf,
)


class MaskDispatch:
    """Class responsible for managing anonymization handlers."""

    _handlers: Dict[str, Callable[[Any, Any], Any]] = {}

    @classmethod
    def add_handler(cls, type_mask: str, handler: Callable[[Any, Any], Any]) -> None:
        """Adds a handler for a specific mask type."""
        cls._handlers[type_mask] = handler

    def mask(self, type_mask: str, data: Any, **kwargs: Any) -> Any:
        """Applies the appropriate mask to the given data if the type exists."""
        if type_mask not in self._handlers:
            return data
        return self._handlers[type_mask](data, **kwargs)


MaskDispatch.add_handler("string", handler=handler_anonymize_string)
MaskDispatch.add_handler("cpf", handler=handler_anonymize_type_cpf)
MaskDispatch.add_handler("cpfs", handler=handler_anonymize_type_cpf)
