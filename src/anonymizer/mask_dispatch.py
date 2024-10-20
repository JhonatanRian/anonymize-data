from typing import Callable, Dict, Any

from anonymizer.utils import (
    anonymize_cpf,
    anonymize_string,
    anonymize_cnpj,
    anonymize_rg,
    anonymize_cep,
    anonymize_pis,
    anonymize_phone_number,
    anonymize_email,
    anonymize_all_string,
    anonymize_numeric_digits,
)


class MaskDispatch:
    """Class responsible for managing anonymization handlers."""

    _handlers: Dict[str, Callable[[Any, Any], Any]] = {}

    @classmethod
    def add_handler(cls, type_mask: str, handler: Callable) -> None:
        """Adds a handler for a specific mask type."""
        cls._handlers[type_mask] = handler

    def mask(self, type_mask: str, data: Any, **kwargs: Any) -> Any:
        """Applies the appropriate mask to the given data if the type exists."""
        if type_mask not in self._handlers:
            return data
        return self._handlers[type_mask](data, **kwargs)


MaskDispatch.add_handler("string", handler=anonymize_string)
MaskDispatch.add_handler("cpf", handler=anonymize_cpf)
MaskDispatch.add_handler("cpfs", handler=anonymize_cpf)
MaskDispatch.add_handler("cnpj", handler=anonymize_cnpj)
MaskDispatch.add_handler("rg", handler=anonymize_rg)
MaskDispatch.add_handler("cep", handler=anonymize_cep)
MaskDispatch.add_handler("pis", handler=anonymize_pis)

MaskDispatch.add_handler("phone", handler=anonymize_phone_number)
MaskDispatch.add_handler("smartphone", handler=anonymize_phone_number)
MaskDispatch.add_handler("cell_phone_number", handler=anonymize_phone_number)
MaskDispatch.add_handler("cell_phone", handler=anonymize_phone_number)
MaskDispatch.add_handler("celular", handler=anonymize_phone_number)
MaskDispatch.add_handler("telefone", handler=anonymize_phone_number)
MaskDispatch.add_handler("telefone_fixo", handler=anonymize_phone_number)

MaskDispatch.add_handler("email", handler=anonymize_email)
MaskDispatch.add_handler("mail", handler=anonymize_email)

MaskDispatch.add_handler("username", handler=anonymize_all_string)
MaskDispatch.add_handler("first_name", handler=anonymize_all_string)
MaskDispatch.add_handler("name", handler=anonymize_all_string)
MaskDispatch.add_handler("nome", handler=anonymize_all_string)
MaskDispatch.add_handler("numero", handler=anonymize_numeric_digits)
MaskDispatch.add_handler("number", handler=anonymize_numeric_digits)
MaskDispatch.add_handler("endereco", handler=anonymize_all_string)
MaskDispatch.add_handler("endereço", handler=anonymize_all_string)
MaskDispatch.add_handler("address", handler=anonymize_all_string)
MaskDispatch.add_handler("bairro", handler=anonymize_all_string)
MaskDispatch.add_handler("neighborhood", handler=anonymize_all_string)
MaskDispatch.add_handler("district", handler=anonymize_all_string)
MaskDispatch.add_handler("suburb", handler=anonymize_all_string)
MaskDispatch.add_handler("quarter", handler=anonymize_all_string)
MaskDispatch.add_handler("sexo", handler=anonymize_all_string)
MaskDispatch.add_handler("sex", handler=anonymize_all_string)
MaskDispatch.add_handler("gender", handler=anonymize_all_string)
MaskDispatch.add_handler("raça", handler=anonymize_all_string)
MaskDispatch.add_handler("raca", handler=anonymize_all_string)
MaskDispatch.add_handler("race", handler=anonymize_all_string)
MaskDispatch.add_handler("cor", handler=anonymize_all_string)
MaskDispatch.add_handler("color", handler=anonymize_all_string)
MaskDispatch.add_handler("senha", handler=anonymize_all_string)
MaskDispatch.add_handler("password", handler=anonymize_all_string)
MaskDispatch.add_handler("tipo_sanguineo", handler=anonymize_all_string)
MaskDispatch.add_handler("blood_type", handler=anonymize_all_string)
