from unittest import TestCase

from anonymizer import MaskString


class TestMaskBase(TestCase):

    class MaskBaseImplementation(MaskString):
        allowed_type = str

        def _anonymize(self, value):
            return "*" * len(value)

    def test_value_type_check(self):
        with self.assertRaises(ValueError):
            TestMaskBase.MaskBaseImplementation(123)

    def test_valid_value(self):
        masker = TestMaskBase.MaskBaseImplementation("valid")
        self.assertEqual(masker.view(), "valid")

    def test_anonymize_method(self):
        masker = TestMaskBase.MaskBaseImplementation("test")
        self.assertEqual(masker.anonymize(), "****")
