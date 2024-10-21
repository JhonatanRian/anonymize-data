from unittest import TestCase

from anonymizer_data.utils import anonymize_phone_number


class TestAnonymizePhoneNumber(TestCase):

    def test_anonymize_valid_phone_with_country_code(self):
        self.assertEqual(
            anonymize_phone_number("+55 (11) 91234-5678"), "+** (**) *****-*678"
        )

    def test_anonymize_valid_phone_with_dashes(self):
        self.assertEqual(anonymize_phone_number("123-456-7890"), "***-***-*890")

    def test_anonymize_valid_phone_without_format(self):
        self.assertEqual(anonymize_phone_number("9876543210"), "*******210")

    def test_anonymize_short_phone(self):
        self.assertEqual(anonymize_phone_number("12"), "12")

    def test_anonymize_invalid_phone(self):
        self.assertEqual(anonymize_phone_number("abc"), "abc")

    def test_anonymize_empty_string(self):
        self.assertEqual(anonymize_phone_number(""), "")
