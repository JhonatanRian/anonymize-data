import re
from typing import Union

from validate_docbr import CPF

from anonymizer.utils import anonymize_cpf


def handler_anonymize_string(value: str, size_anonymization: float, **kwargs) -> str:
    total_to_mask = 1 if len(value) == 1 else int(len(value) * size_anonymization)
    string_sliced = (
        value[:total_to_mask] if total_to_mask > 0 else value[total_to_mask:]
    )
    pattern = re.escape(string_sliced)
    modified = re.sub(pattern, "*" * abs(total_to_mask), value, count=1)
    return modified


def handler_anonymize_type_cpf(
    value: Union[list[str], str], **kwargs
) -> Union[list[str], str]:
    cpf = CPF()

    if isinstance(value, list) and cpf.validate_list(value):
        value_map = map(lambda c: anonymize_cpf(c), value)
        return list(value_map)
    elif isinstance(value, str) and cpf.validate(value):
        return anonymize_cpf(value)
    else:
        return value
