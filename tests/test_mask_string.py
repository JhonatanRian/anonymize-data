import unittest
from anonymizer import MaskStr
from anonymizer.mask_dispatch import MaskDispatch
from tests.conftest import fake


class TestMaskStr(unittest.TestCase):

    def setUp(self):
        self.valid_string = "SensitiveData"
        self.mask_dispatch = MaskDispatch()

    def test_create_mask_string_valid(self):
        mask_string = MaskStr(self.valid_string, string_mask=self.mask_dispatch)
        self.assertEqual(mask_string.view(), self.valid_string)

    def test_create_mask_string_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            MaskStr(123, string_mask=self.mask_dispatch)
        self.assertEqual(str(context.exception), "Value 123 is not valid")

    def test_anonymize_complete(self):
        mask_string = MaskStr(
            self.valid_string, string_mask=self.mask_dispatch, size_anonymization=1.0
        )
        result = mask_string.anonymize()
        self.assertEqual(result, "*************")
        self.assertEqual(str(mask_string), "*************")

    def test_not_anonymize(self):
        mask_string = MaskStr(
            self.valid_string,
            string_mask=self.mask_dispatch,
            size_anonymization=1.0,
            anonymize_string=False,
        )
        result = mask_string.anonymize()
        self.assertEqual(result, self.valid_string)

    def test_size_anonymization_validation(self):
        with self.assertRaises(ValueError) as context:
            MaskStr(self.valid_string, size_anonymization="invalid")
        self.assertEqual(
            str(context.exception), "The 'size_anonymization' must be a float."
        )

        with self.assertRaises(ValueError) as context:
            MaskStr(self.valid_string, size_anonymization=1.5)
        self.assertEqual(
            str(context.exception),
            "The 'size_anonymization' field must be between 0 and 1.",
        )

    def test_default_size_anonymization(self):
        mask_string = MaskStr(self.valid_string, string_mask=self.mask_dispatch)
        result = mask_string.anonymize()
        self.assertEqual(result, "*********Data")

    def test_magic_method_repr(self):
        mask_string = MaskStr(self.valid_string, string_mask=self.mask_dispatch)
        mask_string.anonymize()
        self.assertEqual(repr(mask_string), "<MaskStr>")

    def test_enter_type_mask_cpf_valid(self):

        cpf = fake.cpf()
        cpf_clean = cpf.replace(".", "").replace("-", "")

        mask_string = MaskStr(cpf, type_mask="cpf")
        self.assertEqual(mask_string.anonymize(), f"***.{cpf_clean[3:6]}.***-**")

        mask_string = MaskStr(cpf_clean, type_mask="cpf")
        self.assertEqual(mask_string.anonymize(), f"*********{cpf_clean[9:]}")

    def test_enter_type_mask_cpf_invalid(self):
        cpf_invalid = "123.456.789-20"
        cpf_invalid_clean = "12345678920"

        mask_string = MaskStr(cpf_invalid, type_mask="cpf")
        self.assertEqual(mask_string.anonymize(), cpf_invalid)

        mask_string = MaskStr(cpf_invalid_clean, type_mask="cpf")
        self.assertEqual(mask_string.anonymize(), cpf_invalid_clean)


if __name__ == "__main__":
    unittest.main()
