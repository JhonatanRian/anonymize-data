import re

def mask_string_part(string: str, start: int, end: int, occurrences=1):
    pattern = re.escape(string[start:end])
    return re.sub(pattern, '*' * (end - start), string, count=occurrences)


def anonymize_numeric_digits(string: str) -> str:
    return re.sub(r'\d', '*', string)


def anonymize_substring(main_text: str, substring: str, occurrences: int = 1) -> str:
    escaped_substring = re.escape(substring)

    anonymized_text = re.sub(escaped_substring, '*' * len(substring), main_text, count=occurrences)
    return anonymized_text


def anonymize_cpf(cpf: str) -> str:
    patern = re.sub(r'[^0-9]', '', cpf)

    if "." in cpf and "-" in cpf:
        return f"***.{patern[3:6]}.***-**"
    return f"*******{patern[7:]}"
