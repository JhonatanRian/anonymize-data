# Gemini Code Assistant Context

## Project Overview

This project is a Python library called `anonymize-data`. Its purpose is to provide a flexible and easy-to-use way to anonymize sensitive data in various formats, including strings, lists, and dictionaries. The library is designed to be used in applications where data privacy is a concern.

The core of the library is built around a set of "masking" classes (`MaskStr`, `MaskList`, `MaskDict`) that handle the anonymization of different data types. A `MaskDispatch` class is used to map specific data types (e.g., "cpf", "email", "phone") to their corresponding anonymization functions. This allows for a high degree of customization and extensibility.

The project uses `typer` for its command-line interface (CLI), `rich` for formatted output, and `validate-docbr` for validating Brazilian documents like CPF and CNPJ.

## Building and Running

The project is managed using `hatch` and `uv`.

### Dependencies

- **Main dependencies**: `rich`, `typer`, `validate-docbr`
- **Development dependencies**: `coverage`, `faker`, `jinja2`, `mkdocs-macros-plugin`, `mkdocs-material`, `mkdocs`, `mkdocstrings-python`, `mkdocstrings`, `ruff`

### Running the linter

To run the linter, use the following command:

```bash
uv run ruff check .
```

### Running tests

To run the tests, use the following command:

```bash
uv run coverage run -m unittest
```

### Running the CLI

The project provides a CLI for anonymizing strings directly from the command line.

```bash
uv run anonymize "Hello Word"
```

## Development Conventions

- **Code Style**: The project uses `black` for code formatting with a line length of 88 characters.
- **Linting**: `ruff` is used for linting.
- **Testing and Coverage**: Before and after any code change, all tests must pass (`uv run coverage run -m unittest`). New functionality requires new tests, and a high test coverage percentage is non-negotiable. Unnecessary tests should be removed.
- **Documentation**: The project uses `mkdocs` with `mkdocs-material` for generating documentation. Docstrings are written in a way that they can be parsed by `mkdocstrings`.
- **Mandatory Documentation Updates**: Any addition, removal, or change in functionality *must* be reflected in the `docs/` directory to keep the user documentation up-to-date. This is non-negotiable.
- **Commits**: Commit messages should be clear and concise, and should explain the "why" behind the changes, not just the "what".

## Project History

All significant changes to the project, including new features, refactorings, and bug fixes, must be documented in the `.gemini/gemini_history.md` file. This file serves as a changelog and helps the AI assistant understand the project's evolution.

When making any changes to the codebase, please add an entry to `.gemini/gemini_history.md` following the format specified in that file.

## Main Idea and Core Anonymization Rules

The primary goal of this project is to provide a flexible and robust way to anonymize sensitive data within strings, lists, and dictionaries.

### Strings

Strings are the fundamental data type for anonymization. The core rules are:

- **Default Behavior:** By default, a portion of the string is masked, typically leaving only the end of the string visible. For example, `"Hello World"` becomes `"*******orld"`.
- **Customization:** Developers can control the anonymization by:
  - Specifying the percentage of the string to mask (e.g., `0.5` for 50%).
  - Reversing the masking direction to hide the end of the string instead of the beginning.

### Lists

When given a list, the library will iterate through it and apply the configured string anonymization rules to each string element within the list.

### Dictionaries

Anonymizing dictionaries is designed for scenarios like cleaning sensitive data from log messages or API responses. The logic is key-based:

- **Key-based Masking:** The library identifies and anonymizes values associated with sensitive keys (e.g., `"cpf"`, `"rg"`, `"credit_card_number"`).
- **Extensibility:**
  - **Custom Keys:** Developers can register new sensitive keys to be anonymized.
  - **Fine-grained Control:** It's possible to define which keys should always be anonymized and which should be ignored (whitelisted).
  - **Toggle Anonymization:** Key-based anonymization can be enabled or disabled as needed.
- **Hybrid Approach:** This method combines dictionary-specific rules with the standard string anonymization techniques for the values that are being masked.