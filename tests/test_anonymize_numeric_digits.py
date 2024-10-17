import unittest

from anonymizer.utils import anonymize_numeric_digits


class TestAnonymizeNumericDigits(unittest.TestCase):

    def test_anonymize_digits(self):
        result = anonymize_numeric_digits("My phone number is 1234567890")
        self.assertEqual(result, "My phone number is **********")

    def test_no_digits(self):
        result = anonymize_numeric_digits("No digits here!")
        self.assertEqual(result, "No digits here!")

    def test_mixed_characters(self):
        result = anonymize_numeric_digits("abc123xyz")
        self.assertEqual(result, "abc***xyz")


if __name__ == "__main__":
    unittest.main()
