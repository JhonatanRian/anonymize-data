import unittest

from anonymizer.utils import anonymize_string


class TestHandlerAnonymizeString(unittest.TestCase):

    def test_anonymize_complete(self):
        result = anonymize_string("SensitiveData", size_anonymization=1.0)
        self.assertEqual(result, "*************")

    def test_anonymize_partial(self):
        result = anonymize_string("SensitiveData", size_anonymization=0.5)
        self.assertEqual(result, "******iveData")

    def test_empty_string(self):
        result = anonymize_string("", size_anonymization=0.5)
        self.assertEqual(result, "")

    def test_one_character_in_string(self):
        result = anonymize_string("x", size_anonymization=0.5)
        self.assertEqual(result, "*")

    def test_two_character_in_string(self):
        result = anonymize_string("xy", size_anonymization=0.5)
        self.assertEqual(result, "*y")

    def test_size_above_one(self):
        result = anonymize_string("SensitiveData", size_anonymization=1.5)
        self.assertEqual(result, "*******************")

    def test_negative_size_anonymization(self):
        result = anonymize_string("SensitiveData", size_anonymization=-0.5)
        self.assertEqual(result, "Sensiti******")

    def test_zero_size_anonymization(self):
        result = anonymize_string("SensitiveData", size_anonymization=-0)
        self.assertEqual(result, "SensitiveData")

    def test_default_size_anonymization(self):
        with self.assertRaises(TypeError):
            anonymize_string("SensitiveData")


if __name__ == "__main__":
    unittest.main()
