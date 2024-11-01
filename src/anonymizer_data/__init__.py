"""
The anonymize-data library provides functionality to anonymize sensitive data in different formats, such as strings, lists,
and dictionaries. This library is useful for developers who need to ensure data privacy in their applications.

Classes:
    MaskStr: Class for anonymizing string sensitive data
    MaskList: Class for anonymizing list with sensitive data
    MaskDict: Class for anonymizing dict with sensitive data

"""

from .anonymizer_data import MaskDict, MaskList, MaskStr

__all__ = ["MaskStr", "MaskDict", "MaskList"]
