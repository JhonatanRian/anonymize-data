# Contributing to anonymizer-data

Thank you for considering contributing to `anonymizer-data`! This guide will help you set up your development environment and outline the contribution process.

---

## Development Environment Setup

This project uses [uv](https://github.com/astral-sh/uv) as the package and project manager.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JhonatanRian/anonymize.git
   cd anonymize
   ```

2. **Install dependencies**:
   ```bash
   uv sync --dev
   ```

3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On Linux/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

---

## Development Workflow

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/your-bug-name
   ```

2. **Make your changes**. Ensure you follow the project's coding style guidelines.

3. **Run tests & coverage**:
   ```bash
   uv run coverage run -m unittest
   ```

4. **Lint and Format**:
   We use `ruff` for linting and formatting.
   ```bash
   uv run ruff format .
   uv run ruff check . --fix
   ```

5. **Type Checking**:
   ```bash
   uv run pyright src
   ```

6. **Documentation**:
   To preview the documentation locally:
   ```bash
   uv run mkdocs serve
   ```

---

## Pull Request Process

1. Ensure all tests and type checks pass.
2. Update the user documentation in the `docs/` folder if you change or add any functionality.
3. Submit a Pull Request targeting the `main` branch.
4. Provide a clear description of your changes and link any related issues.

---

## Commit Message Style

We follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` for new features.
- `fix:` for bug fixes.
- `docs:` for documentation changes.
- `refactor:` for code changes that neither fix a bug nor add a feature.
- `perf:` for performance improvements.
- `test:` for adding missing tests.
- `chore:` for updating build tasks, package manager configs, etc.

---

By contributing, you agree that your contributions will be licensed under the [MIT License](../LICENSE).
