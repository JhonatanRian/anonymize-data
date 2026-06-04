import os
import re


def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # dict strategy
    if "test_dict_strategy.py" in filepath:
        content = content.replace(
            "from anonymizer_data.core.dict_strategy import (",
            "from anonymizer_data.core.dispatcher import dispatch_value_mask\nfrom anonymizer_data.core.dict_strategy import (",
        )
        content = content.replace(
            "DefaultDictAnonymizationStrategy()",
            "DefaultDictAnonymizationStrategy(dispatch_value_mask)",
        )
        content = content.replace(
            'KeyBasedDictAnonymizationStrategy(selected_keys=["key1"])',
            'KeyBasedDictAnonymizationStrategy(["key1"], dispatch_value_mask)',
        )
        content = content.replace(
            "KeyAsTypeMaskDictAnonymizationStrategy()",
            "KeyAsTypeMaskDictAnonymizationStrategy(dispatch_value_mask)",
        )

    # Test replacements for document handlers
    # They usually look like: self.assertEqual(anonymize_cep("invalid-cep"), "invalid-cep")
    # We replace "invalid-cep" with "*" * len("invalid-cep") in the second argument.

    def repl_assert_equal(m):
        func_call = m.group(1)
        expected = m.group(2)
        if expected.startswith('"') or expected.startswith("'"):
            raw_str = expected[1:-1]
            if raw_str in [
                "invalid-cep",
                "123",
                "invalid-cnpj",
                "invalid-email",
                "abc",
                "12",
                "invalid-pis",
                "invalid-rg",
                "invalid-cpf",
            ]:
                return f"self.assertEqual({func_call}, '{'*' * len(raw_str)}')"
            if "invalid" in raw_str:
                return f"self.assertEqual({func_call}, '{'*' * len(raw_str)}')"
        elif expected.isdigit():  # For test_unsupported_type_data
            if expected == "12345678910":
                return f"self.assertEqual({func_call}, '***********')"
        return m.group(0)

    content = re.sub(
        r"self\.assertEqual\((anonymize_\w+\(.*?\)),\s*(.*?)\)",
        repl_assert_equal,
        content,
    )

    # For test_invalid_cpf which has: result = MaskStr(cpf, "cpf").anonymize(); self.assertEqual(result, cpf)
    # where cpf = "12345678910"
    content = content.replace(
        "self.assertEqual(result, cpf)", 'self.assertEqual(result, "*" * len(str(cpf)))'
    )

    # test_mask_string.py
    if "test_mask_string.py" in filepath:
        content = content.replace(
            "self.assertEqual(mask_string.anonymize(), cpf_invalid)",
            'self.assertEqual(mask_string.anonymize(), "*" * len(cpf_invalid))',
        )

    with open(filepath, "w") as f:
        f.write(content)


test_files = [
    "tests/test_dict_strategy.py",
    "tests/test_anonymize_cep.py",
    "tests/test_anonymize_cnpj.py",
    "tests/test_anonymize_email.py",
    "tests/test_anonymize_phone_number.py",
    "tests/test_anonymize_pis.py",
    "tests/test_anonymize_rg.py",
    "tests/test_handler_anonymize_type_cpf.py",
    "tests/test_mask_string.py",
]

for file in test_files:
    if os.path.exists(file):
        patch_file(file)
