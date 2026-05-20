import unittest

from anonymizer_data.core.dispatcher import dispatch_value_mask
from anonymizer_data.core.dict_strategy import (
    DefaultDictAnonymizationStrategy,
    KeyAsTypeMaskDictAnonymizationStrategy,
    KeyBasedDictAnonymizationStrategy,
)


class TestDictAnonymizationStrategy(unittest.TestCase):
    def setUp(self):
        self.data = {"key1": "value1", "key2": "value2"}

    def test_default_strategy(self):
        strategy = DefaultDictAnonymizationStrategy(dispatch_value_mask)
        result = strategy.anonymize(self.data)
        self.assertEqual(result, {"key1": "****e1", "key2": "****e2"})

    def test_key_based_strategy(self):
        strategy = KeyBasedDictAnonymizationStrategy(["key1"], dispatch_value_mask)
        result = strategy.anonymize(self.data)
        self.assertEqual(result, {"key1": "****e1", "key2": "value2"})

    def test_key_as_type_mask_strategy(self):
        strategy = KeyAsTypeMaskDictAnonymizationStrategy(dispatch_value_mask)
        result = strategy.anonymize(self.data)
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})
