## 2026-05-20: Security and Architecture Improvements

- **Refactored `MaskDispatch` to use a Registry Pattern (`@MaskDispatch.register`).**
- **Created a `Config` class (`core.config`) for global configurations like `strict_mode`, `fallback_masking` and `default_mask_char`.**
- **Implemented a Fluent API in `MaskDict` to allow `.with_keys(['key'])` chaining.**
- **Fixed circular imports between `dispatcher.py`, `dict_strategy.py` and `list.py` by applying Dependency Injection.**
- **Improved Security and Data Privacy:**
  - Masking now defaults to total blackout (`fallback_masking=True`) for malformed PII/sensitive data instead of returning it unmasked (preventing Silent Failures and Data Leaks).
  - Replaced vulnerable ReDoS Regex in email anonymization with `split`.
- **Added PEP 561 compliance (`py.typed`).**
- **Updated `tests/` with the new expected fallback behavior and 100% pass rate.**
- **Overhauled Documentation:** Rewrote `README.md`, `docs/index.md`, and `docs/tutorials.md` to be highly professional, objective, and concise. Included Tabs component for MkDocs and fixed all typos.

## 2025-09-08: Refactoring and Project Structure Improvement

- **Refactored the project to apply SOLID principles and improve the overall structure.**
  - The project was restructured into `core` and `handlers` modules to better separate concerns.
  - The `MaskDict` class was refactored to use a strategy pattern, making it more flexible and extensible.
  - The `dispatch_value_mask` function was moved to its own module to break a circular dependency.
- **Modernized the typing to use Python 3.12 features.**
  - Replaced `Any` with more specific types where possible.
  - Used `type` for type aliasing.
- **Updated the documentation to reflect the changes.**
  - The `docs/api` directory was updated to reflect the new structure.
  - The `mkdocs.yml` file was updated to match the new documentation structure.
- **Updated `GEMINI.md` to reflect the current state of the project.**