from unittest import TestCase

from anonymizer_data.utils import anonymize_cpf
from tests.conftest import fake


class AnonymizeCPFTestCase(TestCase):
    def test_string_cpf_valid(self):
        cpf = fake.cpf()
        cpf_anonymized = f"***.{cpf[4:7]}.***-**"

        result = anonymize_cpf(cpf)
        self.assertEqual(result, cpf_anonymized)
        self.assertEqual(type(result), str)

    def test_invalid_cpf(self):
        cpf = "12345678910"

        result = anonymize_cpf(cpf)
        self.assertEqual(result, cpf)

    def test_unsupported_type_data(self):
        cpf = 12345678910

        result = anonymize_cpf(cpf)
        self.assertEqual(result, cpf)
