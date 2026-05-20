![Logo](assets/logo.png){ width="200" .center }

# anonymize-data

The **anonymize-data** library provides functionality to anonymize sensitive data in different formats, such as strings, lists, and dictionaries. This library is ideal for developers who need to ensure strict data privacy and sanitization in their Python applications.

---

## Quickstart

### Installation

{% include 'templates/install.md' %}

### Basic Usage

Below you can find how to anonymize different types of data using the library. 

=== "Strings"

    To anonymize strings in your project you can use the `MaskStr` class.

    ```python
    from anonymizer_data import MaskStr
    
    # Basic masking
    string = MaskStr("Hello World")
    print(string.anonymize())  # result: *******orld
    
    # Partial masking (50%)
    string_half = MaskStr("Hello World", size_anonymization=0.5)
    print(string_half.anonymize())  # result: ***** World
    ```

=== "Lists"

    List anonymization is done by the `MaskList` class. It iterates over the items and masks them appropriately.

    ```python
    from anonymizer_data import MaskList
    
    list_data = MaskList(['1234435', '98765432', '24295294', 'Jhon Doe'])
    list_data.anonymize()
    
    print(list_data) 
    # result: ['****435', '*****432', '*****294', '*****Doe']
    ```

=== "Dictionaries"

    Dictionary anonymization is handled by the `MaskDict` class. It provides a Fluent API to easily select which keys should be anonymized.

    ```python
    from anonymizer_data import MaskDict
    
    dict_data = MaskDict({
        "username": "JhonDoe",
        "password": "123Change",
        "roles": ['Admin', 'developer'],
        "contact": {
            "number": "+55 (99) 99999-9999"
        }
    }).with_keys(['password', 'number'])
    
    dict_data.anonymize()
    print(dict_data)  
    # result: {'username': 'JhonDoe', 'password': '*********', 'roles': ['Admin', 'developer'], 'contact': {'number': '*******************'}}
    ```
    
    !!! info
        Dictionary anonymization brings powerful advantages, enabling exclusive anonymization based on specific keys. For example, a key `"email"` holding `jhondoe@example.com` will be correctly parsed and masked. To learn more, check the [Advanced Usage](tutorials.md).

---

## Global Configuration

You can configure global settings such as the default mask character (`mask_char`), strict mode, and fallback behavior for invalid sensitive data (e.g. malformed CPF/CNPJ).

```python
from anonymizer_data.core.config import Config

Config.setup(
    mask_char="X",         # Default is "*"
    strict_mode=False,     # If True, raises ValueError on invalid formats
    fallback_masking=True  # If True, entirely masks invalid formats to avoid data leaks
)
```

---

## Command-Line Interface (CLI)

You can anonymize strings from the command line.
For this you need to have `uv` installed.

Example:
```shell
{{ commands.run }} "Hello World"
*******orld
```

```shell
{{ commands.run }} --help
Usage: anonymize [OPTIONS] VALUE [TYPE_MASK] [SIZE_ANONYMIZATION]                                                                                            
                                                                                                                                                              
 cli anonymization string                                                                                                                                     
                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    value                   TEXT                  The string you want to anonymize [default: None] [required]                                             │
│      type_mask               [TYPE_MASK]           The type mask to use [default: string]                                                                  │
│      size_anonymization      [SIZE_ANONYMIZATION]  The size anonymization factor [default: 0.7]                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                    │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                             │
│ --help                        Show this message and exit.                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
