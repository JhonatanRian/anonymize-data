<div style="display: flex; justify-content: center">
<img src="https://anonymize.readthedocs.io/en/latest/assets/logo.png" width=100>
</div>

# anonymize-data

[![Documentation Status](https://readthedocs.org/projects/anonymize/badge/?version=latest)](https://anonymize.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/anonymize-data.svg)](https://badge.fury.io/py/anonymize-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**anonymize-data** is a powerful, flexible, and extensible Python library designed to sanitize and anonymize sensitive data. It provides seamless anonymization for strings, lists, and dictionaries, ensuring data privacy in your applications and logs.

---

## Key Features

- **Multi-Type Support**: Easily mask primitive strings, nested lists, and complex dictionaries.
- **Fluent API**: Chain methods for elegant dictionary manipulation (e.g., `.with_keys(['cpf', 'password'])`).
- **Global Configuration**: Centrally manage default mask characters and security policies.
- **Strict Data Privacy**: Built-in fallback protection masks invalid sensitive data entirely to prevent silent data leaks.
- **Extensible Architecture**: Customize behavior easily thanks to an underlying Registry Pattern.
- **Command-Line Interface (CLI)**: Quickly anonymize text right from your terminal.

## Quickstart

### Installation

Choose your preferred package manager:

**pip**:
```bash
pip install anonymize-data
```

**uv**:
```bash
uv add anonymize-data
```

### Basic Usage

Anonymize data with just a few lines of code:

```python
from anonymizer_data import MaskStr, MaskDict

# String Anonymization
string_mask = MaskStr("Hello World")
print(string_mask.anonymize())  # Output: *******orld

# Dictionary Anonymization with Fluent API
user_data = {
    "username": "JhonDoe",
    "password": "123Change",
    "roles": ['Admin', 'developer'],
    "contact": {
        "number": "+55 (99) 99999-9999"
    }
}

masked_dict = MaskDict(user_data).with_keys(['password', 'number'])
print(masked_dict.anonymize())
# Output: {'username': 'JhonDoe', 'password': '*********', 'roles': ['Admin', 'developer'], 'contact': {'number': '*******************'}}
```

> **Note:** Dictionary anonymization allows for exclusive targeting based on keys. For example, specific sensitive fields like emails or phone numbers can be mapped to specialized masking functions under the hood.

## Command-Line Interface (CLI)

You can anonymize strings directly from your terminal using `uv`:

```bash
uv run anonymize "Hello World"
# Output: *******orld

uv run anonymize --help
```

## Documentation

For comprehensive guides, advanced usage, global configurations, and API reference, please visit our [Official Documentation](https://anonymize.readthedocs.io/en/latest/).
