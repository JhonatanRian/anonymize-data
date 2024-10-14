import re


def handler_anonymize_string(value: str, size_anonymization: float, **kwargs) -> str:
    total_to_mask = int(len(value) * size_anonymization)
    string_sliced = value[:total_to_mask] if total_to_mask > 0 else value[total_to_mask:]
    pattern = re.escape(string_sliced)
    modified = re.sub(pattern, '*' * abs(total_to_mask), value, count=1)
    return modified
