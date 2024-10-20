from unittest import TestCase

from anonymizer.utils import anonymize_email


class TestAnonymizeEmail(TestCase):

    def test_anonymize_valid_email(self):
        self.assertEqual(anonymize_email("user@example.com"), "***r@example.com")

    def test_anonymize_invalid_email(self):
        self.assertEqual(anonymize_email("invalid-email"), "invalid-email")

    def test_anonymize_short_email(self):
        self.assertEqual(anonymize_email("a@b.com"), "*@b.com")

    def test_anonymize_empty_email(self):
        self.assertEqual(anonymize_email(""), "")


if __name__ == "__main__":
    unittest.main()
