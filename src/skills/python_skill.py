

PYTHON_SKILL = """
---
name: tyler-python-skill
description: Apply these whenever writing Python code for Tyler. These conventions override standard PEP where they differ.
license: none
---

## Function Signatures

### Inline args (≤4 args)
```python
def some_function(arg1: int, arg2: str = 'default', arg3: bool = False) -> None:
    "Short concise function description"

    return None
```

### Multi-line args (>4 args or long signatures)
- Return type goes on the **same line as the closing paren**, with one space before `)`
- Whitespace line between signature and docstring
```python
def some_function(
        arg1: int,
        arg2: str = 'default',
        arg3: bool = False ) -> None:
    "Short concise function description"

    return None
```

### ❌ Do NOT use standard PEP closing style
```python
# BAD - closing paren on its own line, no whitespace before docstring
def some_function(
        arg1: int,
        arg2: str = 'default',
        arg3: bool = False
) -> None:
    "Super verbose long function description"
    return None
```

---

## Type Hints

### Use union syntax, not Optional
```python
# GOOD
some_type: str | None = None

# BAD - legacy/magic
some_other_type: Optional[str] = None
```

- `str | None` is preferred over `Optional[str]` — it's explicit and modern
- Apply this to function args, return types, and variable annotations

---

## Spacing & Formatting

### Two blank lines between functions (standard, but enforced)

### Single newline before return statements
```python
def example() -> str:
    "Does something"

    result = "hello"

    return result
```

### Column-align related variable assignments
```python
# GOOD
related_val_A   = 0
related_B       = 0
related         = 0
relatedC        = 0
related_D       = 0

# BAD
related_val_A = 0
related_B = 0
related = 0
relatedC = 0
related_D = 0
```

---

## Docstrings & Body Whitespace

- Keep docstrings **short and concise** — one line when possible

### With docstring → blank lines surround it
A blank line **after** the docstring (before the body). This applies to both functions and classes.
```python
def some_function(arg1: int) -> str:
    "Short concise description."

    result = do_something(arg1)

    return result


class SomeClassWithDocstring:
    "Short concise description."

    name: str
    value: int
```

### Without docstring → no blank line
When there is no docstring, the body starts immediately on the next line with **no** blank line after the signature/colon.
```python
def helper(x: int) -> int:
    return x + 1


class SomeDataHolder:
    name: str
    value: int
```

### ❌ Do NOT add whitespace when there is no docstring
```python
# BAD - blank line with no docstring
def helper(x: int) -> int:

    return x + 1


# BAD - blank line with no docstring
class SomeDataHolder:

    name: str
    value: int
```

---

## Architecture & Organization

### Dataclasses
- **Never** define dataclasses in the same file as a class
- Use `_dataclasses/` subdirectory inside modular directory structures
- OR use a single `dataclasses/` directory at the project root with one dataclass per file
- Always use `@dataclass` decorator

### Custom Errors / Exceptions
- **Never** define custom exceptions in the same file as a class
- Use `_errors/` subdirectory inside modular directory structures
- OR use a single `errors/` directory at the project root with one exception per file
- Follow the same pattern as dataclasses separation

### Single Responsibility
- A class should own one *cohesive responsibility* — not one function, but one purpose
- If a class is handling two unrelated concerns, split it

---

## Summary of Deviations from PEP

| Convention                    | PEP                               | Tyler                               |
|-------------------------------|-----------------------------------|-------------------------------------|
| Multi-line closing paren      | Own line, col-aligned             | Same line as last arg with space    |
| Return type placement         | After closing paren on new line   | Same line as closing paren          |
| Optional types                | `Optional[str]`                   | `str | None`                       |
| Whitespace around docstring   | No blank lines                    | Blank line after                    |
| No docstring whitespace       | N/A                               | No blank line after signature       |
| Related var alignment         | No alignment                      | Column-aligned `=` signs            |
| Newline before return         | Not required                      | Always one blank line               |
| Dataclass placement           | Same file OK                      | Separate `_dataclasses/` dir        |
| Exception placement           | Same file OK                      | Separate `_errors/` dir             |
|-------------------------------|-----------------------------------| ----------------------------------- |
"""

def get_python_skill() -> str:
    return PYTHON_SKILL