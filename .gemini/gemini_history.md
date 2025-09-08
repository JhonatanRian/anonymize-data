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