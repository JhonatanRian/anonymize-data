from unittest import TestCase

from src.anonymizer.anonymizer import MaskerString


class TestMasker(TestCase):
    def test_masker(self):
        string_name = "Jhon Doe"
        string_name_anonymized = "******oe"
        result = MaskerString(string_name)
        self.assertNotEqual(result, string_name_anonymized)
        self.assertEqual(str(result), string_name_anonymized)

    def test_view_string_not_masker(self):
        string_name = "Jhon Doe"
        result = MaskerString(string_name)
        self.assertTrue(isinstance(result, 'view_string'))
        self.assertEqual(result.view_string(), string_name)
