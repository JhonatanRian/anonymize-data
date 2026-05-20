from typing import Any, Callable

class MaskDispatch:
    """Class responsible for managing anonymization handlers."""

    _handlers: dict[str, Callable[..., Any]] = {}

    @classmethod
    def register(cls, *type_masks: str) -> Callable:
        """Decorator to register a handler for specific mask types."""
        def decorator(handler: Callable) -> Callable:
            for type_mask in type_masks:
                cls.add_handler(type_mask, handler)
            return handler
        return decorator

    @classmethod
    def add_handler(cls, type_mask: str, handler: Callable) -> None:
        """Adds a handler for a specific mask type."""
        cls._handlers[type_mask] = handler

    def mask(self, type_mask: str, data: Any, **kwargs: Any) -> Any:
        """Applies the appropriate mask to the given data if the type exists."""
        if type_mask not in self._handlers:
            return data
        return self._handlers[type_mask](data, **kwargs)
