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
from typing import Any

from validate_docbr import CNPJ, CPF, PIS
from anonymizer_data.core.config import Config
from .dispatch import MaskDispatch


def _handle_invalid_doc(doc: str, doc_name: str, **kwargs: Any) -> str:
    """Helper to handle invalid documents according to Config."""
    if Config.strict_mode:
        raise ValueError(f"Invalid {doc_name}: {doc}")
    if Config.fallback_masking:
        return anonymize_all_string(doc, **kwargs)
    return doc


@MaskDispatch.register("string")
def anonymize_string(value: str, size_anonymization: float, **kwargs: Any) -> str:
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
    """
    if size_anonymization == 0:
        return value

    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    total_to_mask = 1 if len(value) == 1 else int(len(value) * size_anonymization)
    string_sliced = (
        value[:total_to_mask] if total_to_mask > 0 else value[total_to_mask:]
    )
    pattern = re.escape(string_sliced)
    modified = re.sub(pattern, mask_char * abs(total_to_mask), value, count=1)
    return modified


@MaskDispatch.register("email", "mail")
def anonymize_email(email: str, **kwargs: Any) -> str:
    """
    Anonymize an email address by masking the username part.

    This function takes an email address as input and replaces the username part
    (the part before the '@') with a masked version, while keeping the domain part intact.
    The level of anonymization for the username can be adjusted using additional parameters.

    Parameters:
        email (str): The original email address to be anonymized.

    Returns:
        str: The masked version of the email address.
    """
    if not isinstance(email, str) or "@" not in email:
        return _handle_invalid_doc(str(email), "Email", **kwargs)

    username, domain = email.split("@", 1)
    if not username or not domain:
        return _handle_invalid_doc(str(email), "Email", **kwargs)

    masked_username = anonymize_string(username, size_anonymization=0.9, **kwargs)

    return f"{masked_username}@{domain}"


@MaskDispatch.register(
    "phone",
    "smartphone",
    "cell_phone_number",
    "cell_phone",
    "celular",
    "telefone",
    "telefone_fixo",
)
def anonymize_phone_number(phone: str, **kwargs: Any) -> str:
    """
    Anonymize a phone number by masking parts of it while preserving its format.

    This function takes a phone number as input, removes any non-numeric characters,
    and returns a masked version of the phone number. The format is preserved, with
    specific parts masked according to the rules defined.

    Parameters:
        phone (str): The original phone number to be anonymized, which may include non-numeric characters.

    Returns:
        str: The masked version of the phone number.
    """
    if not isinstance(phone, str):
        return _handle_invalid_doc(str(phone), "Phone", **kwargs)

    phone_digits = re.findall(r"\d", phone)

    if len(phone_digits) < 3:
        return _handle_invalid_doc(phone, "Phone", **kwargs)

    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    last_three = phone_digits[-3:]
    anonymized = [mask_char] * (len(phone_digits) - 3)

    replace_iter = iter(anonymized + last_three)

    def to_replace(match):
        return next(replace_iter)

    phone_anonymized = re.sub(r"\d", to_replace, phone)
    return phone_anonymized


def mask_string_part(
    string: str, start: int, end: int, occurrences: int = 1, **kwargs: Any
) -> str:
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
    """
    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    pattern = re.escape(string[start:end])
    return re.sub(pattern, mask_char * (end - start), string, count=occurrences)


@MaskDispatch.register("numero", "number")
def anonymize_numeric_digits(string: str, **kwargs: Any) -> str:
    """
    Anonymize all numeric digits in a string by replacing them with asterisks.

    This function scans the input string and replaces every numeric digit (0-9)
    with an asterisk (*), effectively anonymizing any sensitive numerical information.

    Parameters:
        string (str): The original string containing numeric digits to be anonymized.

    Returns:
        str: The modified string with all numeric digits replaced by asterisks.
    """
    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    return re.sub(r"\d", mask_char, str(string))


def anonymize_substring(
    main_text: str, substring: str, occurrences: int = 1, **kwargs: Any
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
    """
    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    escaped_substring = re.escape(substring)
    anonymized_text = re.sub(
        escaped_substring, mask_char * len(substring), str(main_text), count=occurrences
    )
    return anonymized_text


@MaskDispatch.register("cpf", "cpfs")
def anonymize_cpf(cpf: str, **kwargs: Any) -> str:
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
    """
    validate_cpf = CPF()
    if not isinstance(cpf, str) or not validate_cpf.validate(cpf):
        return _handle_invalid_doc(str(cpf), "CPF", **kwargs)

    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    pattern = re.sub(r"[^0-9]", "", cpf)

    if "." in cpf and "-" in cpf:
        return f"{mask_char*3}.{pattern[3:6]}.{mask_char*3}-{mask_char*2}"
    return mask_string_part(pattern, start=0, end=9, **kwargs)


@MaskDispatch.register("cnpj")
def anonymize_cnpj(cnpj: str, **kwargs: Any) -> str:
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
    """
    validate_cnpj = CNPJ()
    if not isinstance(cnpj, str) or not validate_cnpj.validate(cnpj):
        return _handle_invalid_doc(str(cnpj), "CNPJ", **kwargs)

    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    pattern = re.sub(r"[^0-9]", "", cnpj)

    if (
        "." in cnpj and "-" in cnpj and "/" in cnpj
    ):  # Original had a bug `"-" in cnpj and "-" in cnpj`. Let's fix that too.
        return f"{mask_char*2}.{mask_char*3}.{pattern[5:8]}/{mask_char*4}-{mask_char*2}"
    return mask_string_part(pattern, start=0, end=9, **kwargs)


@MaskDispatch.register("rg")
def anonymize_rg(rg: str, **kwargs: Any) -> str:
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
    """
    if not isinstance(rg, str) or not re.match(
        r"^(?:\d{9}|\d{2}\.\d{3}\.\d{3}-\d)$", rg
    ):
        return _handle_invalid_doc(str(rg), "RG", **kwargs)

    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    pattern = re.sub(r"[^0-9]", "", rg)

    if "." in rg and "-" in rg:
        return f"{mask_char*2}.{pattern[2:5]}.{mask_char*3}-{mask_char*2}"
    return mask_string_part(pattern, start=0, end=6, **kwargs)


@MaskDispatch.register("cep")
def anonymize_cep(cep: str, **kwargs: Any) -> str:
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
    """
    if not isinstance(cep, str) or not re.match(r"^\d{5}-?\d{3}$", cep):
        return _handle_invalid_doc(str(cep), "CEP", **kwargs)

    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    pattern = re.sub(r"[^0-9]", "", cep)

    if "-" in cep:
        return f"{mask_char*5}-{cep[6:]}"
    return mask_string_part(pattern, start=0, end=5, **kwargs)


@MaskDispatch.register("pis")
def anonymize_pis(pis: str, **kwargs: Any) -> str:
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
    """
    validate_pis = PIS()

    if not isinstance(pis, str) or not validate_pis.validate(pis):
        return _handle_invalid_doc(str(pis), "PIS", **kwargs)

    mask_char = kwargs.get("mask_char", Config.default_mask_char)
    pattern = re.sub(r"[^0-9]", "", pis)

    if "-" in pis:
        return f"{mask_char*3}.{mask_char*2}{pattern[5:8]}.{mask_char*2}-{mask_char}"
    return mask_string_part(pattern, start=0, end=8, **kwargs)


@MaskDispatch.register(
    "username",
    "first_name",
    "name",
    "nome",
    "endereco",
    "endereço",
    "address",
    "bairro",
    "neighborhood",
    "district",
    "suburb",
    "quarter",
    "sexo",
    "sex",
    "gender",
    "raça",
    "raca",
    "race",
    "cor",
    "color",
    "senha",
    "password",
    "tipo_sanguineo",
    "blood_type",
)
def anonymize_all_string(string: str, **kwargs: Any) -> str:
    """Anonymize all characters of a string."""
    return anonymize_string(str(string), size_anonymization=1.0, **kwargs)
