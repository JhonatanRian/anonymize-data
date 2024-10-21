<div style="display: flex; justify-content: center">
<img src="docs/assets/logo.png" width=100>
</div>

# Anonymize

[![Documentation Status](https://readthedocs.org/projects/anonymize/badge/?version=latest)](https://anonymize.readthedocs.io/en/latest/?badge=latest)


The Anonymize library provides functionality to anonymize sensitive data in different formats, such as strings, lists, and dictionaries. This library is useful for developers who need to ensure data privacy in their applications.

## Quickstart

### Installation

#### pip

```shell
pip install anonymize
```

#### uv

```
uv add anonymize
```

### Anonymize strings

To anonymize strings in your project you can use the `MaskStr` class.

Example:
```python
from anonymizer_data import MaskStr
string = MaskStr("Hello Word")
string.anonymize()
print(string)  # result: *******ord
```

You can control how much percent the string will be anonymized relative to its length via the `size_anonymization` parameter. You can pass a value from 0 to 1.  
You can also pass a negative value to reverse the anonymization.

Example:
```python
from anonymizer_data import MaskStr
string = MaskStr("Hello Word", size_anonymization=0.5)
string.anonymize()
print(string)  # result: ***** Word
MaskStr("Hello Word", size_anonymization=0.5).anonymize()  # result: Hello*****
```

### Anonymize lists

List anonymization is done by the `MaskList` class.

Example:
```python
from anonymizer_data import MaskList
list_data = MaskList(['1234435', '98765432', '24295294', 'Jhon Doe'])
list_data.anonymize()
print(list_data)  # result: ['****435', '*****432', '*****294', '*****Doe']
```

### Anonymize dict

Dictionary's anonymization is done by the `MaskList` class.

Example:
```python
from anonymizer_data import MaskDict
dict_data = MaskDict(
    {
        "username": "JhonDoe",
        "password": "123Change",
        "roles": ['Admin', 'developer'],
        "contact": {
            "number": "+55 (99) 99999-9999"
        }
    }
)
dict_data.anonymize()
print(dict_data)  # result: {'username': '****Doe', 'password': '******nge', 'roles': ['***in', '******per'], 'contact': {'number': '*************9-9999'}}
```

> **Note:** Dictionary anonymization brings with it other advantages such as: choosing which keys in the dictionary should be anonymized;
enabling exclusive anonymization based on the key. For example, `jhondue@example.com` would become `******e@example.com`.
To learn more, access the [tutorial](tutorials.md)

### cli

You can anonymize strings from the command line.
For this you need to have uv installed.

Exemple:
```shell
{{ commands.run }} "Hello Word"
*******ord
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
