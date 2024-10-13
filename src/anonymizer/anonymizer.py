from abc import abstractmethod
from typing import Any
import re
from anonymizer.mask_settings import StringMaskSettings


class MaskBase:
    allowed_type: type

    def __init__(self, value, setting=None) -> None:
        if not self.check_value(value):
            raise ValueError(f'Value {value} is not valid')

        self._value = value
        self._value_anonymized = None
        self.config_mask = setting

    def check_value(self, value) -> bool:
        return isinstance(value, self.allowed_type)

    def view(self) -> Any:
        return self._value

    def anonymize(self) -> str:
        if self._value_anonymized is None:
            self._value_anonymized = self._anonymize(self._value)
        return self._value_anonymized

    @abstractmethod
    def _anonymize(self, value):
        pass


class MaskString(MaskBase):
    allowed_type = str

    def __init__(self, value: str, setting: StringMaskSettings = None) -> None:
        if setting is None:
            setting = StringMaskSettings()

        super().__init__(value, setting)

    def __str__(self) -> str:
        return self.anonymize()

    def _anonymize(self, value) -> str:
        total_to_mask = int(len(value) * self.config_mask.size_anonymization)
        pattern = re.escape(value[:total_to_mask])
        modified = re.sub(pattern, '*' * total_to_mask, value, count=1)
        return modified


#
# class MaskerList(MaskerAbstract):
#
#     def anonymize(self) -> str:
#         # Anonimiza cada item da lista
#         return [MaskerString(item).anonymize() for item in self._MaskerAbstract_value]
#
#     def view(self) -> List[Any]:
#         return self._MaskerAbstract_value
#
#
# class MaskerDict(MaskerAbstract):
#
#     def anonymize(self) -> str:
#         # Anonimiza cada valor do dicionário
#         return {key: MaskerString(value).anonymize() for key, value in self._MaskerAbstract_value.items()}
#
#     def view(self) -> Dict[str, Any]:
#         return self._MaskerAbstract_value

class Anonymizer:
    ...
