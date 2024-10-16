from unittest import TestCase

from anonymizer.handlers_anonymize import handler_anonymize_type_cpf
from tests.conftest import fake


class AnonymizeCPFTestCase(TestCase):
    def test_string_cpf_valid(self):
        cpf = fake.cpf()
        cpf_anonymized = f"***.{cpf[4:7]}.***-**"

        result = handler_anonymize_type_cpf(cpf)
        self.assertEqual(result, cpf_anonymized)
        self.assertEqual(type(result), str)

    def test_list_cpf_valid(self):
        cpf = fake.cpf()
        cpf_two = fake.cpf().replace('.', '').replace('-', '')
        cpfs = [cpf, cpf_two]
        cpfs_anonymized = [f"***.{cpf[4:7]}.***-**", f"*******{cpf_two[7:]}"]

        result = handler_anonymize_type_cpf(cpfs)
        self.assertEqual(result, cpfs_anonymized)
        self.assertEqual(type(result), list)

    def test_invalid_cpf(self):
        cpf = "12345678910"

        result = handler_anonymize_type_cpf(cpf)
        self.assertEqual(result, cpf)

    def test_unsupported_type_data(self):
        cpf = 12345678910

        result = handler_anonymize_type_cpf(cpf)
        self.assertEqual(result, cpf)
