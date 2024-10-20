from unittest import TestCase

from anonymizer.utils import anonymize_rg


class TestAnonymizeRG(TestCase):

    def test_anonymize_valid_rg_with_format(self):
        self.assertEqual(anonymize_rg("12.345.678-9"), "**.345.***-**")

    def test_anonymize_valid_rg_without_format(self):
        self.assertEqual(anonymize_rg("123456789"), "******789")

    def test_anonymize_invalid_rg(self):
        self.assertEqual(anonymize_rg("invalid-rg"), "invalid-rg")

    def test_anonymize_short_rg(self):
        self.assertEqual(anonymize_rg("123"), "123")

    def test_anonymize_empty_string(self):
        self.assertEqual(anonymize_rg(""), "")
