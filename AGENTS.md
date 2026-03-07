# AGENTS.md — Dice Roller

Guidelines for agentic coding agents working in this repository.

## Project Overview

A Python 3 dice notation evaluator with a CLI (`roll`) and an optional Flask web
interface (`web/app.py`). The core logic lives in `dice.py` at the repo root and
is shared by both interfaces. The CLI has zero runtime dependencies (standard
library only); the web interface requires Flask (installed via the `web`
dependency group).

- **Language:** Python 3
- **Core module:** `dice.py` (shared dice-rolling logic)
- **CLI entry point:** `roll` (executable script at repo root)
- **Web entry point:** `web/app.py` (Flask application)
- **License:** GPLv3

---

## Build, Install, and Run Commands

This project uses **[uv](https://docs.astral.sh/uv/)** for environment and dependency management.

### Set up the development environment
```bash
uv sync          # creates .venv and installs all dev dependencies
```

### Run directly (no install required)
```bash
uv run python roll 2d8+6
uv run python roll stats
uv run python roll dir
uv run python roll -h

# or activate the venv first:
source .venv/bin/activate
python roll 2d8+6
```

### Run via Docker
```bash
# Build image
docker build -f container/Dockerfile -t dice-roller .

# Run
docker run dice-roller 2d8+6
```

### Add / remove dependencies
```bash
uv add <package>            # runtime dependency
uv add --dev <package>      # dev-only dependency
uv remove <package>
```

---

## Testing

**There is currently no test suite in this project.** pytest is included as a dev
dependency and ready to use.

```bash
# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_roll.py

# Run a single test function
uv run pytest tests/test_roll.py::test_dice_roller_basic

# Run with verbose output
uv run pytest -v tests/test_roll.py::test_dice_roller_basic
```

Place tests in a `tests/` directory, naming files `test_<module>.py` and test
functions `test_<description>`.

---

## Linting and Formatting

flake8, black, and mypy are included as dev dependencies. No config is currently
enforced, but follow PEP 8 when contributing.

```bash
# Lint
uv run flake8 roll

# Format
uv run black roll

# Type check
uv run mypy roll
```

---

## CI/CD

The project uses **GitLab CI** (`.gitlab-ci.yml`). There is no `.github/workflows/`
directory. The pipeline currently uses the legacy `setup.py` workflow and should be
updated to use `uv` when CI is next touched.

---

## Code Style Guidelines

### General

- Target **Python 3** exclusively. The shebang line must be `#!/usr/bin/env python3`.
- Include the encoding declaration on line 2: `# coding: utf-8`.
- Core dice-rolling logic lives in `dice.py`; the CLI (`roll`) and web interface
  (`web/app.py`) both import from it. Keep this separation.
- Follow **PEP 8**: 4-space indentation, max line length ~79 characters, two blank
  lines between top-level definitions.

### Imports

- Use only the **Python standard library** unless adding a dependency is explicitly
  required. Current imports: `sys`, `re`, `random`.
- Group imports as per PEP 8: standard library only (no third-party or local groups
  currently apply). One import per line.
- Do not use wildcard imports (`from module import *`).

### Naming Conventions

| Construct | Convention | Example |
|---|---|---|
| Functions | `snake_case` | `dice_roller`, `stats_roll` |
| Variables | `snake_case` | `input_text`, `dice_split` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_SIDES` |
| Script entry | `main()` + `if __name__` guard | (see existing pattern) |

- Use descriptive but terse names. Avoid single-letter variables except in tight
  loops where the meaning is obvious.

### Types and Type Hints

- The existing code has **no type hints**. When adding new functions, add type
  annotations for all parameters and return values:
  ```python
  def dice_roller(input_text: str) -> tuple[int, list[str]]:
      ...
  ```
- Avoid using `Any` unless unavoidable.

### Comments and Docstrings

- The existing style uses short inline `# comment` lines above or beside code.
- New functions should include a **one-line docstring** at minimum:
  ```python
  def stats_roll() -> str:
      """Roll 4d6 drop-lowest six times and return formatted results."""
      ...
  ```
- Avoid over-commenting; code should be self-explanatory where possible.

### Error Handling

- Use `sys.exit(2)` for user-facing errors (invalid input, bad syntax).
- Use `sys.exit(0)` for successful early exits.
- Catch only **specific** exception types — never bare `except:` or `except Exception:`.
- Print a helpful usage message before exiting on error (see `error()` and `info()`).
- Warn users about degraded behavior with `warnings.warn(...)` rather than silently
  falling back.

### Known Anti-Patterns to Fix

The existing code contains several Python 3 anti-patterns. Do not repeat them in
new code, and fix them when touching the surrounding lines:

| Anti-pattern | Correct alternative |
|---|---|
| `len(sys.argv) is 1` | `len(sys.argv) == 1` |
| `dice_split[0] is not ''` | `dice_split[0] != ''` |
| `eval()` on user-controlled input | Parse the expression explicitly |
| String concatenation in loops | Use `str.join()` or a list |

### Security

- **Do not use `eval()`** on any data derived from user input. The current
  implementation does this and it is a known issue — replace it with an explicit
  arithmetic parser if refactoring `dice_roller`.
- Use `random.SystemRandom()` for all random number generation (already done at the
  top of `roll`). Do not use `random.random()` or `random.randint()` directly.

---

## Architecture Notes

- All logic lives in **module-level functions** — no classes. Keep it that way unless
  complexity justifies a class.
- The `roll_dice` nested function inside `dice_roller` captures the outer `rolls` list
  as a side effect. This is intentional; maintain the same contract when refactoring.
- Each individual die result is stored in the format `"value/sides"` (e.g. `"4/6"`).
  The stats roll reads this with `int(min(rolls).split("/")[0])`.
- `dice_roller` returns a `(total, rolls)` tuple: the evaluated integer total and the
  list of `"value/sides"` strings.

---

## Distribution Targets

The project is distributed via:
- **PyPI** (via `twine upload` on tagged releases)
- **Docker Hub** (`metasikander/dice-roller`)
- **AUR** (`dice-roller-git`) — tracked as a git submodule in `.gitmodules`
- **RPM/tarball** — pre-built artifacts in `RPM/packages/`
- **Snap** — `snap/snapcraft.yaml` (core18 base, version 1.9)

When bumping the version, update: `setup.py` (`version=`), `snap/snapcraft.yaml`
(`version:`), and the RPM spec if applicable.

---

## Issue Tracking

This project uses **bd (beads)** for issue tracking.
Run `bd prime` for workflow context, or install hooks (`bd hooks install`) for auto-injection.

**Quick reference:**
- `bd ready` - Find unblocked work
- `bd create "Title" --type task --priority 2` - Create issue
- `bd close <id>` - Complete work
- `bd dolt push` - Push beads to remote

For full workflow details: `bd prime`
