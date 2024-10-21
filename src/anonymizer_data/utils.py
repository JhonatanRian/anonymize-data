"""
Functions:
    anonymize_string: Anonymize a string by masking a specified portion of it.
    anonymize_email: Anonymize an email address by masking the username part.
    anonymize_phone_number: Anonymize a phone number by masking parts of it while preserving its format.
    mask_string_part: Mask a specific part of a string with asterisks.
    anonymize_numeric_digits: Anonymize all numeric digits in a string by replacing them with asterisks.
    anonymize_substring: Anonymize a specified substring in the main text by replacing it with asterisks.
    anonymize_cpf: Anonymize a Brazilian CPF (Cadastro de Pessoas Físicas) number by masking parts of it.
    anonymize_cnpj: Anonymize a Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica) number by masking parts of it.
    anonymize_rg: Anonymize a Brazilian RG (Registro Geral) number by masking parts of it.
    anonymize_pis: Anonymize a Brazilian PIS (Programa de Integração Social) number by masking parts of it.
"""

import re

from validate_docbr import CNPJ, CPF, PIS


def anonymize_string(value: str, size_anonymization: float, **kwargs) -> str:
    """
    Anonymize a string by masking a specified portion of it.

    This function takes a string and replaces a portion of its characters with asterisks (*).
    The extent of the masking is determined by the `size_anonymization` parameter, which
    specifies the fraction of the string to be masked.

    Parameters:
        value (str): The original string to be anonymized.
        size_anonymization (float): A float value between 0 and 1 indicating the proportion of the string to mask. For example, 0.5 will mask half of the characters in the string.

    Returns:
        str: The masked version of the input string. If `size_anonymization` is set such that no characters are masked, the original string will be returned.

    Examples:
        >>> anonymize_string("Hello World", 0.5)
        '***** World'

        >>> anonymize_string("SensitiveData", 0.8)
        '***********ata'

        >>> anonymize_string("A", 1)
        '*'

        >>> anonymize_string("Test", 0)
        'Test'
    """
    if size_anonymization == 0:
        return value

    total_to_mask = 1 if len(value) == 1 else int(len(value) * size_anonymization)
    string_sliced = (
        value[:total_to_mask] if total_to_mask > 0 else value[total_to_mask:]
    )
    pattern = re.escape(string_sliced)
    modified = re.sub(pattern, "*" * abs(total_to_mask), value, count=1)
    return modified


def anonymize_email(email: str, **kwargs) -> str:
    """
    Anonymize an email address by masking the username part.

    This function takes an email address as input and replaces the username part
    (the part before the '@') with a masked version, while keeping the domain part intact.
    The level of anonymization for the username can be adjusted using additional parameters.

    Parameters:
        email (str): The original email address to be anonymized.

    Returns:
        str: The masked version of the email address. If the input email is not valid, it returns the original email.

    Examples:
        >>> anonymize_email("user@example.com")
        '***r@example.com'

        >>> anonymize_email("john.doe@gmail.com")
        '*******e@gmail.com'

        >>> anonymize_email("invalid-email")
        'invalid-email'
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return email
    username, domain = email.split("@", 1)
    masked_username = anonymize_string(username, size_anonymization=0.9, **kwargs)

    return f"{masked_username}@{domain}"


def anonymize_phone_number(phone: str, **kwargs) -> str:
    """
    Anonymize a phone number by masking parts of it while preserving its format.

    This function takes a phone number as input, removes any non-numeric characters,
    and returns a masked version of the phone number. The format is preserved, with
    specific parts masked according to the rules defined.

    Parameters:
        phone (str): The original phone number to be anonymized, which may include non-numeric characters.

    Returns:
        str: The masked version of the phone number.

    Examples:
        >>> anonymize_phone_number("+55 (11) 91234-5678")
        '+** (**) *****-*678'

        >>> anonymize_phone_number("123-456-7890")
        '***-***-*890'

        >>> anonymize_phone_number("9876543210")
        '*******210'
    """
    phone_digits = re.findall(r"\d", phone)

    if len(phone_digits) < 3:
        return phone

    last_three = "".join(phone_digits[-3:])

    anonymized = "*" * (len(phone_digits) - 3)

    index_digit = 0

    def to_replace(match):
        nonlocal index_digit
        if index_digit < len(anonymized):
            result = anonymized[index_digit]
            index_digit += 1
            return result
        else:
            index_digit += 1
            return last_three[(index_digit - 1) - len(anonymized)]

    phone_anonymized = re.sub(r"\d", to_replace, phone)

    return phone_anonymized


def mask_string_part(string: str, start: int, end: int, occurrences=1, **kwargs) -> str:
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


def anonymize_numeric_digits(string: str, **kwargs) -> str:
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


def anonymize_substring(
    main_text: str, substring: str, occurrences: int = 1, **kwargs
) -> str:
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


def anonymize_cpf(cpf: str, **kwargs) -> str:
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

    validate_cpf = CPF()
    if type(cpf) != str or not validate_cpf.validate(cpf):
        return cpf

    pattern = re.sub(r"[^0-9]", "", cpf)

    if "." in cpf and "-" in cpf:
        return f"***.{pattern[3:6]}.***-**"
    return mask_string_part(pattern, start=0, end=9)


def anonymize_cnpj(cnpj: str, **kwargs) -> str:
    """
    Anonymize a Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica) number by masking parts of it.

    This function takes a CNPJ number as input, removes any non-numeric characters,
    and returns a masked version of the CNPJ. If the input CNPJ is formatted with dots, slashes,
    and a dash, it will mask the first two digits and the last four digits, while revealing the
    middle digits. If the CNPJ is provided without formatting, it will mask all but the last four digits.

    Parameters:
        cnpj (str): The original CNPJ number to be anonymized, which may include non-numeric characters.

    Returns:
        str: The masked version of the CNPJ number.

    Examples:
        >>> anonymize_cnpj("12.345.678/0001-95")
        '**.***.678/****-**'

        >>> anonymize_cnpj("12345678000195")
        '*******00195'
    """
    validate_cnpj = CNPJ()
    if not validate_cnpj.validate(cnpj):
        return cnpj

    pattern = re.sub(r"[^0-9]", "", cnpj)

    if "." in cnpj and "-" in cnpj and "-" in cnpj:
        return f"**.***.{pattern[5:8]}/****-**"
    return mask_string_part(pattern, start=0, end=9)


def anonymize_rg(rg: str, **kwargs) -> str:
    """
    Anonymize a Brazilian RG (Registro Geral) number by masking parts of it.

    This function takes an RG number as input, removes any non-numeric characters,
    and returns a masked version of the RG. If the input RG is formatted with dots and a dash,
    it will mask the first two digits and the last two digits, while revealing the middle digits.
    If the RG is provided without formatting, it will mask all but the last four digits.

    Parameters:
        rg (str): The original RG number to be anonymized, which may include non-numeric characters.

    Returns:
        str: The masked version of the RG number.

    Examples:
        >>> anonymize_rg("12.345.678-9")
        '**.345.***-**'

        >>> anonymize_rg("123456789")
        '*****6789'
    """

    if not re.match(r"^(?:\d{9}|\d{2}\.\d{3}\.\d{3}-\d)$", rg):
        return rg

    pattern = re.sub(r"[^0-9]", "", rg)

    if "." in rg and "-" in rg:
        return f"**.{pattern[2:5]}.***-**"
    return mask_string_part(pattern, start=0, end=6)


def anonymize_cep(cep: str, **kwargs) -> str:
    """
    Anonymize a Brazilian CEP (Código de Endereçamento Postal) by masking parts of it.

    This function takes a CEP number as input, removes any non-numeric characters,
    and returns a masked version of the CEP. If the input CEP is formatted with a hyphen,
    it will mask the first five digits while revealing the last three digits.
    If the CEP is provided without formatting, it will mask all but the last three digits.

    Parameters:
        cep (str): The original CEP number to be anonymized, which may include non-numeric characters.

    Returns:
        str: The masked version of the CEP number.

    Examples:
        >>> anonymize_cep("12345-678")
        '*****-678'

        >>> anonymize_cep("12345678")
        '*****678'
    """
    if not re.match(r"^\d{5}-?\d{3}$", cep):
        return cep

    pattern = re.sub(r"[^0-9]", "", cep)

    if "-" in cep:
        return f"*****-{cep[6:]}"
    return mask_string_part(pattern, start=0, end=5)


def anonymize_pis(pis: str, **kwargs) -> str:
    """
    Anonymize a Brazilian PIS (Programa de Integração Social) number by masking parts of it.

    This function takes a PIS number as input, removes any non-numeric characters,
    and returns a masked version of the PIS. If the input PIS is formatted with a hyphen,
    it will mask the first five digits and the last two digits, while revealing the middle digits.
    If the PIS is provided without formatting, it will mask all but the last four digits.

    Parameters:
        pis (str): The original PIS number to be anonymized, which may include non-numeric characters.

    Returns:
        str: The masked version of the PIS number.

    Examples:
        >>> anonymize_pis("123.45678.90-1")
        '***.**678.**-*'

        >>> anonymize_pis("12345678901")
        '*******901'

    Note:
        Data validation is performed by the [validate_docbr](https://pypi.org/project/validate-docbr) lib. If the data passed is not valid, it is returned without changes.
    """

    validate_pis = PIS()

    if not validate_pis.validate(pis):
        return pis

    pattern = re.sub(r"[^0-9]", "", pis)

    if "-" in pis:
        return f"***.**{pattern[5:8]}.**-*"
    return mask_string_part(pattern, start=0, end=8)


anonymize_all_string = lambda string, **kwargs: anonymize_string(
    string, size_anonymization=1, **kwargs
)
