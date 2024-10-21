from unittest import TestCase

from anonymizer_data.utils import anonymize_cep


class TestAnonymizeCEP(TestCase):

    def test_anonymize_valid_cep_with_format(self):
        self.assertEqual(anonymize_cep("12345-678"), "*****-678")

    def test_anonymize_valid_cep_without_format(self):
        self.assertEqual(anonymize_cep("12345678"), "*****678")

    def test_anonymize_invalid_cep(self):
        self.assertEqual(anonymize_cep("invalid-cep"), "invalid-cep")

    def test_anonymize_short_cep(self):
        self.assertEqual(anonymize_cep("123"), "123")

    def test_anonymize_empty_string(self):
        self.assertEqual(anonymize_cep(""), "")
