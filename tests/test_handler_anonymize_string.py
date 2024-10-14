import unittest
from anonymizer.handlers_anonymize import handler_anonymize_string


class TestHandlerAnonymizeString(unittest.TestCase):

    def test_anonymize_complete(self):
        result = handler_anonymize_string("SensitiveData", size_anonymization=1.0)
        self.assertEqual(result, "*************")

    def test_anonymize_partial(self):
        result = handler_anonymize_string("SensitiveData", size_anonymization=0.5)
        self.assertEqual(result, "******iveData")

    def test_empty_string(self):
        result = handler_anonymize_string("", size_anonymization=0.5)
        self.assertEqual(result, "")

    def test_size_above_one(self):
        result = handler_anonymize_string("SensitiveData", size_anonymization=1.5)
        self.assertEqual(result, "*******************")

    def test_negative_size_anonymization(self):
        result = handler_anonymize_string("SensitiveData", size_anonymization=-0.5)
        self.assertEqual(result, "Sensiti******")

    def test_default_size_anonymization(self):
        with self.assertRaises(TypeError):
            handler_anonymize_string("SensitiveData")

if __name__ == '__main__':
    unittest.main()
