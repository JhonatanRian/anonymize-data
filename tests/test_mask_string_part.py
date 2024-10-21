import unittest

from anonymizer_data.utils import mask_string_part


class TestMaskStrPart(unittest.TestCase):

    def test_mask_part(self):
        result = mask_string_part("SensitiveData", 0, 8)
        self.assertEqual(result, "********eData")

    def test_mask_part_with_occurrences(self):
        result = mask_string_part("SensitiveDataSensitiveData", 0, 8, occurrences=1)
        self.assertEqual(result, "********eDataSensitiveData")

    def test_mask_part_no_occurrences_and_occurrences_negative(self):
        result = mask_string_part("SensitiveData", 0, 8, occurrences=0)
        self.assertEqual(result, "********eData")

        result = mask_string_part("SensitiveData", 0, 8, occurrences=-1)
        self.assertEqual(result, "SensitiveData")


if __name__ == "__main__":
    unittest.main()
