import unittest
from anonymizer import MaskString
from anonymizer.string_mask import MaskDispatch

class TestMaskString(unittest.TestCase):

    def setUp(self):
        self.valid_string = "SensitiveData"
        self.mask_dispatch = MaskDispatch()

    def test_create_mask_string_valid(self):
        mask_string = MaskString(self.valid_string, string_mask=self.mask_dispatch)
        self.assertEqual(mask_string.view(), self.valid_string)

    def test_create_mask_string_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            MaskString(123, string_mask=self.mask_dispatch)
        self.assertEqual(str(context.exception), 'Value 123 is not valid')

    def test_anonymize_complete(self):
        mask_string = MaskString(self.valid_string, string_mask=self.mask_dispatch, size_anonymization=1.0)
        result = mask_string.anonymize()
        self.assertEqual(result, "*************")
        self.assertEqual(str(mask_string), "*************")

    def test_not_anonymize(self):
        mask_string = MaskString(self.valid_string, string_mask=self.mask_dispatch, size_anonymization=1.0,
                                 anonymize_string=False)
        result = mask_string.anonymize()
        self.assertEqual(result, self.valid_string)

    def test_size_anonymization_validation(self):
        with self.assertRaises(ValueError) as context:
            MaskString(self.valid_string, size_anonymization="invalid")
        self.assertEqual(str(context.exception), "The 'size_anonymization' must be a float.")

        with self.assertRaises(ValueError) as context:
            MaskString(self.valid_string, size_anonymization=1.5)
        self.assertEqual(str(context.exception), "The 'size_anonymization' field must be between 0 and 1.")

    def test_default_size_anonymization(self):
        mask_string = MaskString(self.valid_string, string_mask=self.mask_dispatch)
        result = mask_string.anonymize()
        self.assertEqual(result, '*********Data')


if __name__ == '__main__':
    unittest.main()
