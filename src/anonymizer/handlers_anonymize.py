import re


def handler_anonymize_string(value: str, size_anonymization: float, **kwargs) -> str:
    total_to_mask = int(len(value) * size_anonymization)
    pattern = re.escape(value[:total_to_mask])
    modified = re.sub(pattern, '*' * abs(total_to_mask), value, count=1)
    return modified
