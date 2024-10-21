from unittest import TestCase
from unittest.mock import patch

from anonymizer_data.anonymizer_data import MaskBase


class TestMaskBase(TestCase):
    class MaskBaseImplementation(MaskBase):
        _allowed_type = str

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

    def test_anonymize_multiple_calls(self):
        masker = TestMaskBase.MaskBaseImplementation("test")
        first_call = masker.anonymize()
        second_call = masker.anonymize()
        self.assertEqual(first_call, second_call)

    def test_str_method(self):
        masker = TestMaskBase.MaskBaseImplementation("example")
        self.assertEqual(str(masker), "example")

        masker.anonymize()
        self.assertEqual(str(masker), "*******")

    def test_len_method(self):
        masker = TestMaskBase.MaskBaseImplementation("example")
        self.assertEqual(len(masker), 7)

        masker.anonymize()
        self.assertEqual(len(masker), 7)

    def test_iter_method(self):
        masker = TestMaskBase.MaskBaseImplementation("abc")
        original_chars = [char for char in masker]
        self.assertEqual(original_chars, ["a", "b", "c"])

        masker.anonymize()
        anonymized_chars = [char for char in masker]
        self.assertEqual(anonymized_chars, ["*", "*", "*"])

    @patch.multiple(MaskBase, __abstractmethods__=set())
    def test_abstract_method_anonymize(self):
        MaskBase._allowed_type = str
        masker = MaskBase("abc")

        masker._anonymize("test")
