from unittest import TestCase

from anonymizer.utils import anonymize_cnpj


class TestAnonymizeCNPJ(TestCase):

    def test_anonymize_valid_cnpj_with_format(self):
        self.assertEqual(anonymize_cnpj("12.345.678/0001-95"), "**.***.678/****-**")

    def test_anonymize_valid_cnpj_without_format(self):
        self.assertEqual(anonymize_cnpj("12345678000195"), "*********00195")

    def test_anonymize_invalid_cnpj(self):
        self.assertEqual(anonymize_cnpj("invalid-cnpj"), "invalid-cnpj")

    def test_anonymize_short_cnpj(self):
        self.assertEqual(anonymize_cnpj("123"), "123")

    def test_anonymize_empty_string(self):
        self.assertEqual(anonymize_cnpj(""), "")
