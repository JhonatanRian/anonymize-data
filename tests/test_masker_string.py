import re
from unittest import TestCase

from anonymizer.mask_settings import StringMaskSettings
from src.anonymizer.anonymizer import MaskString


class TestMaskString(TestCase):

    def test_anonymize_string(self):
        masker = MaskString("banana", StringMaskSettings(0.5))
        anonymized = masker.anonymize()
        expected_pattern = r"^\*\*\*ana$"
        self.assertRegex(anonymized, expected_pattern)

    def test_anonymize_with_full_mask(self):
        masker = MaskString("banana", StringMaskSettings(1.0))
        anonymized = masker.anonymize()
        self.assertEqual(anonymized, "******")

    def test_anonymize_partial(self):
        masker = MaskString("banana", StringMaskSettings(0.3))
        anonymized = masker.anonymize()

        possible_patterns = [r"^\*anana$", r"^\*\*nana$", r"^\*\*anana$"]

        self.assertTrue(
            any(re.match(pattern, anonymized) for pattern in possible_patterns),
            f"Anonymized output '{anonymized}' did not match any expected patterns."
        )

    def test_anonymize_no_mask(self):
        masker = MaskString("banana", StringMaskSettings(0.0))
        anonymized = masker.anonymize()
        self.assertEqual(anonymized, "banana")

    def test_str_method(self):
        masker = MaskString("apple", StringMaskSettings(0.5))
        self.assertEqual(str(masker), masker.anonymize())
