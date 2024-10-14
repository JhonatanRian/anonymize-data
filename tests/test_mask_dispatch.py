import unittest

from anonymizer.string_mask import MaskDispatch


class TestMaskDispatch(unittest.TestCase):

    def setUp(self):
        self.dispatch = MaskDispatch()

    def test_add_handler(self):
        self.assertIn('string', self.dispatch._handlers)
        self.assertEqual(self.dispatch._handlers['string']("Test", 1.0), "****")

    def test_mask_with_valid_handler(self):
        result = self.dispatch.mask('string', 'SensitiveData', size_anonymization=1.0)
        self.assertEqual(result, '*************')


if __name__ == '__main__':
    unittest.main()
