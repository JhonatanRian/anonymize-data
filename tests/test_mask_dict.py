import time
import unittest

from anonymizer_data.core import MaskDict
from tests.payloads import COMPLEX_DICT


class TestMaskDict(unittest.TestCase):

    def setUp(self):
        self.valid_dict = {"key1": "SensitiveData1", "key2": "SensitiveData2"}
        self.valid_nested_dict = {
            "outer_key": {
                "inner_key1": "SensitiveData1",
                "inner_key2": "SensitiveData2",
            }
        }
        self.valid_complex_dict = COMPLEX_DICT
        self.mask_dict = MaskDict(self.valid_dict)

    def test_create_mask_dict_valid(self):
        mask_dict = MaskDict(self.valid_dict)
        self.assertEqual(mask_dict.view(), self.valid_dict)

    def test_create_mask_dict_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            MaskDict(123)
        self.assertEqual(str(context.exception), "Value 123 is not valid")

    def test_anonymize(self):
        mask_dict = MaskDict(self.valid_dict)
        result = mask_dict.anonymize()
        expected_result = {"key1": "*********Data1", "key2": "*********Data2"}
        self.assertEqual(result, expected_result)

    def test_anonymize_nested_dict(self):
        mask_dict = MaskDict(self.valid_nested_dict)
        result = mask_dict.anonymize()

        expected_result = {
            "outer_key": {
                "inner_key1": "*********Data1",
                "inner_key2": "*********Data2",
            }
        }
        self.assertEqual(result, expected_result)

    def test_special_characters(self):
        special_dict = {"@key!": "SensitiveData!", "#key$": "MoreData$"}
        mask_dict = MaskDict(special_dict)
        result = mask_dict.anonymize()

        expected_result = {"@key!": "*********Data!", "#key$": "******ta$"}
        self.assertEqual(result, expected_result)

    def test_performance_large_nested_dict(self):
        large_nested_dict = {
            f"outer_{i}": {f"inner_{j}": f"SensitiveData{i}{j}" for j in range(100)}
            for i in range(100)
        }

        mask_dict = MaskDict(large_nested_dict)

        start_time = time.time()

        result = mask_dict.anonymize()

        end_time = time.time()

        self.assertIsNotNone(result)
        print(f"Performance test completed in {end_time - start_time:.4f} seconds.")

    def test_dict(self):
        expected_result = {"key1": "*********Data1", "key2": "*********Data2"}
        self.mask_dict.anonymize()
        self.assertEqual(dict(self.mask_dict), expected_result)
        self.assertEqual(self.mask_dict.__dict__, expected_result)

    def test_getitem(self):
        self.mask_dict.anonymize()
        self.assertEqual(self.mask_dict["key1"], "*********Data1")
        self.assertEqual(self.mask_dict["key2"], "*********Data2")

    def test_len(self):
        self.assertEqual(len(self.mask_dict), 2)

    def test_iter(self):
        keys = [key_value for key_value in self.mask_dict]
        self.assertEqual(keys, [("key1", "SensitiveData1"), ("key2", "SensitiveData2")])

    def test_str(self):
        expected_str = str({"key1": "*********Data1", "key2": "*********Data2"})
        self.mask_dict.anonymize()
        self.assertEqual(str(self.mask_dict), expected_str)
