import unittest

from anonymizer_data.utils import anonymize_substring


class TestAnonymizeSubstring(unittest.TestCase):

    def test_anonymize_substring(self):
        result = anonymize_substring("Hello world!", "world", occurrences=1)
        self.assertEqual(result, "Hello *****!")

    def test_anonymize_multiple_occurrences(self):
        result = anonymize_substring(
            "Hello world! Welcome to the world!", "world", occurrences=2
        )
        self.assertEqual(result, "Hello *****! Welcome to the *****!")

    def test_anonymize_nonexistent_substring(self):
        result = anonymize_substring("Hello world!", "notfound", occurrences=1)
        self.assertEqual(result, "Hello world!")

    def test_anonymize_substring_empty(self):
        result = anonymize_substring("Hello world!", "", occurrences=1)
        self.assertEqual(result, "Hello world!")


if __name__ == "__main__":
    unittest.main()
