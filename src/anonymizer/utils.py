"""
Functions:
    mask_string_part: Mask a specific part of a string with asterisks.
    anonymize_numeric_digits: Anonymize all numeric digits in a string by replacing them with asterisks.
    anonymize_substring: Anonymize a specified substring in the main text by replacing it with asterisks.
    anonymize_cpf: Anonymize a Brazilian CPF (Cadastro de Pessoas Físicas) number by masking parts of it.
"""

import re


def mask_string_part(string: str, start: int, end: int, occurrences=1) -> str:
    """
    Mask a specific part of a string with asterisks.

    This function replaces a substring of the provided string, defined by the start and end indices,
    with asterisks. The number of occurrences to replace can be specified.

    Parameters:
        string (str): The original string in which the substring will be masked.
        start (int): The starting index of the substring to be masked.
        end (int): The ending index of the substring to be masked.
        occurrences (Optional[int]): The number of times to replace the substring with asterisks (default is 1).

    Returns:
        str: The modified string with the specified substring replaced by asterisks.

    Examples:
        >>> mask_string_part('Hello Word!', 6, 10)
        'Hello, *****!'

        >>> mask_string_part('the monkey hit the monkey', 4, 10, 2)
        'the ****** hit the ******'
    """
    pattern = re.escape(string[start:end])
    return re.sub(pattern, "*" * (end - start), string, count=occurrences)


def anonymize_numeric_digits(string: str) -> str:
    """
    Anonymize all numeric digits in a string by replacing them with asterisks.

    This function scans the input string and replaces every numeric digit (0-9)
    with an asterisk (*), effectively anonymizing any sensitive numerical information.

    Parameters:
        string (str): The original string containing numeric digits to be anonymized.

    Returns:
        str: The modified string with all numeric digits replaced by asterisks.

    Examples:
        >>> anonymize_numeric_digits("My phone number is 123-456-7890.")
        'My phone number is ***-***-****.'

        >>> anonymize_numeric_digits("The price is $100.50.")
        'The price is $***.**.'
    """

    return re.sub(r"\d", "*", string)


def anonymize_substring(main_text: str, substring: str, occurrences: int = 1) -> str:
    """
    Anonymize a specified substring in the main text by replacing it with asterisks.

    This function searches for the given substring within the main text and replaces
    it with asterisks. The number of occurrences to replace can be specified.

    Parameters:
        main_text (str): The original text in which the substring will be anonymized.
        substring (str): The substring to be replaced with asterisks.
        occurrences (Optional[int]): The number of times to replace the substring with asterisks (default is 1).

    Returns:
        str: The modified text with the specified substring replaced by asterisks.

    Examples:
        >>> anonymize_substring("Hello, my password is secret123.", "password")
        'Hello, my ******** is secret123.'

        >>> anonymize_substring("This is a test. Test this test.", "test", occurrences=2)
        'This is a ****. Test this ****.'
    """
    escaped_substring = re.escape(substring)

    anonymized_text = re.sub(
        escaped_substring, "*" * len(substring), main_text, count=occurrences
    )
    return anonymized_text


def anonymize_cpf(cpf: str) -> str:
    """
    Anonymize a Brazilian CPF (Cadastro de Pessoas Físicas) number by masking parts of it.

    This function takes a CPF number as input, removes any non-numeric characters,
    and returns a masked version of the CPF. If the input CPF is formatted with dots and a dash,
    it will mask the first three digits and the last two digits, while revealing the middle digits.
    If the CPF is provided without formatting, it will mask all but the last four digits.

    Parameters:
        cpf (str): The original CPF number to be anonymized, which may include non-numeric characters.

    Returns:
        str: The masked version of the CPF number.

    Examples:
        >>> anonymize_cpf("123.456.789-09")
        '***.456.***-**'

        >>> anonymize_cpf("12345678909")
        '*******09'
    """
    patern = re.sub(r"[^0-9]", "", cpf)

    if "." in cpf and "-" in cpf:
        return f"***.{patern[3:6]}.***-**"
    return f"*******{patern[7:]}"
