from typing import Callable

from anonymizer.handlers_anonymize import handler_anonymize_string


class MaskDispatch:
    _handlers: dict = {}

    @classmethod
    def add_handler(cls, type_mask: str, handler: Callable):
        cls._handlers[type_mask] = handler

    def mask(self, type_mask: str, data, **kwargs):
        if type_mask not in self._handlers:
            return
        return self._handlers[type_mask](data, **kwargs)


MaskDispatch.add_handler('string', handler=handler_anonymize_string)
