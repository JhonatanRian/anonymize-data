import unittest

from anonymizer.anonymizer import MaskList
from anonymizer.mask_dispatch import MaskDispatch


class TestMaskList(unittest.TestCase):

    def setUp(self):
        self.valid_list = ["SensitiveData1", "SensitiveData2"]
        self.valid_nested_list = [
            ["SensitiveData1", "SensitiveData2"],
            ["MoreData1", "MoreData2"],
        ]
        self.mask_dispatch = MaskDispatch()
        self.mask_list = MaskList(self.valid_list, string_mask=self.mask_dispatch)

    def test_create_mask_list_valid(self):
        mask_list = MaskList(self.valid_list, string_mask=self.mask_dispatch)
        self.assertEqual(mask_list.view(), self.valid_list)

    def test_create_mask_list_no_anonymized(self):
        mask_list = MaskList(
            self.valid_list, string_mask=self.mask_dispatch, anonymize_string=False
        )
        self.assertEqual(list(mask_list), self.valid_list)
        self.assertEqual(mask_list.__list__, self.valid_list)

    def test_create_mask_list_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            MaskList(123, string_mask=self.mask_dispatch)
        self.assertEqual(str(context.exception), "Value 123 is not valid")

    def test_anonymize(self):
        mask_list = MaskList(self.valid_list, string_mask=self.mask_dispatch)
        result = mask_list.anonymize()
        expected_result = ["*********Data1", "*********Data2"]
        self.assertEqual(result, expected_result)

    def test_empty_list(self):
        mask_list = MaskList([], string_mask=self.mask_dispatch)
        result = mask_list.anonymize()
        self.assertEqual(result, [])

    def test_anonymize_with_extra_kwargs(self):
        mask_list = MaskList(
            self.valid_list, string_mask=self.mask_dispatch, size_anonymization=0.5
        )
        result = mask_list.anonymize()

        expected_result = ["*******veData1", "*******veData2"]
        self.assertEqual(result, expected_result)

    def test_anonymize_nested_list(self):
        mask_list = MaskList(self.valid_nested_list, string_mask=self.mask_dispatch)
        result = mask_list.anonymize()

        expected_result = [
            ["*********Data1", "*********Data2"],
            ["******ta1", "******ta2"],
        ]
        self.assertEqual(result, expected_result)

    def test_getitem(self):
        self.assertEqual(self.mask_list[0], "SensitiveData1")
        self.assertEqual(self.mask_list[1], "SensitiveData2")

    def test_len(self):
        self.assertEqual(len(self.mask_list), 2)

    def test_iter(self):
        elements = [item for item in self.mask_list]
        self.assertEqual(elements, self.valid_list)

    def test_str(self):
        expected_str = str(self.valid_list)
        self.assertEqual(str(self.mask_list), expected_str)

    def test_eq_with_list(self):
        self.assertEqual(self.mask_list, self.valid_list)

    def test_eq_with_masklist(self):
        another_mask_list = MaskList(self.valid_list, string_mask=self.mask_dispatch)
        self.assertEqual(self.mask_list, another_mask_list)

    def test_not_equal_with_different_list(self):
        different_list = ["DifferentData1", "DifferentData2"]
        self.assertNotEqual(self.mask_list, different_list)

    def test_not_equal_with_different_masklist(self):
        different_mask_list = MaskList(
            ["DifferentData11", "DifferentData22"], string_mask=self.mask_dispatch
        )
        self.assertNotEqual(self.mask_list, different_mask_list)

    def test_equal_with_different_object(self):
        class Test:
            def __init__(self):
                self.title = "test"

        obj_test = Test()

        different_mask_list = MaskList(
            ["DifferentData11", obj_test], string_mask=self.mask_dispatch
        )
        different_mask_list.anonymize()
        self.assertNotEqual(["*********Data11", obj_test], different_mask_list)
        self.assertNotEqual(obj_test, different_mask_list)


if __name__ == "__main__":
    unittest.main()
