"""Script security validator and input validators.

Uses Python's ``ast`` module to parse uploaded scripts and reject
code that uses dangerous operations (file I/O, subprocess, imports
of forbidden modules, etc.).

Also provides username and password validation helpers used by
the authentication service.
"""

import ast
import re
from typing import Any

from app.errors import ScriptValidationError, ValidationError

# ---------------------------------------------------------------------------
# Block-lists
# ---------------------------------------------------------------------------

FORBIDDEN_IMPORTS: set[str] = {
    "os",
    "subprocess",
    "shutil",
    "sys",
    "ctypes",
    "multiprocessing",
    "threading",
    "socket",
    "http.server",
    "importlib",
    "pickle",
    "shelve",
    "tempfile",
}

FORBIDDEN_FUNCTIONS: set[str] = {
    "eval",
    "exec",
    "compile",
    "open",
    "execfile",
    "__import__",
    "input",
}

FORBIDDEN_ATTRS: set[str] = {
    "__builtins__",
    "__class__",
    "__subclasses__",
    "__globals__",
    "__code__",
}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate_script(source_code: str) -> None:
    """Validate a Python script for security concerns.

    Parses *source_code* into an AST and walks it, rejecting any
    forbidden imports, function calls, or attribute accesses.

    Args:
        source_code: The raw Python source code string.

    Raises:
        ScriptValidationError: If the script fails any security check.
    """
    # TODO: Implement script validation
    #   - Parse source_code with ast.parse(source_code)
    #   - Walk the AST with _ScriptValidator
    #   - If any violations found, raise ScriptValidationError with
    #     details of the first violation.
    ...


# ---------------------------------------------------------------------------
# Input validators (used by AuthService)
# ---------------------------------------------------------------------------


def validate_username(username: str) -> str:
    """Validate a username and return the stripped value.

    Rules:
      - Must be 3-64 characters after stripping.
      - Allowed characters: letters, digits, underscores, hyphens.

    Args:
        username: Raw username string.

    Returns:
        Stripped username.

    Raises:
        ValidationError: If the username fails any validation rule.
    """
    cleaned = username.strip()
    if len(cleaned) < 3:
        raise ValidationError("用户名至少 3 个字符")
    if len(cleaned) > 64:
        raise ValidationError("用户名最多 64 个字符")
    if not re.match(r"^[a-zA-Z0-9_-]+$", cleaned):
        raise ValidationError("用户名只能包含字母、数字、下划线和连字符")
    return cleaned


def validate_password(password: str) -> None:
    """Validate password strength.

    Rules:
      - Minimum 8 characters.
      - Must contain at least one letter AND one digit.

    Args:
        password: Plain-text password to validate.

    Raises:
        ValidationError: If the password fails any strength check.
    """
    if len(password) < 8:
        raise ValidationError("密码长度至少 8 位，且需包含字母和数字")
    if not re.search(r"[a-zA-Z]", password):
        raise ValidationError("密码长度至少 8 位，且需包含字母和数字")
    if not re.search(r"\d", password):
        raise ValidationError("密码长度至少 8 位，且需包含字母和数字")


# ---------------------------------------------------------------------------
# Internal AST visitor
# ---------------------------------------------------------------------------


class _ScriptValidator(ast.NodeVisitor):
    """AST visitor that checks for forbidden constructs."""

    def __init__(self):
        self.errors: list[str] = []

    def visit_Import(self, node: ast.Import) -> Any:
        """Check for forbidden top-level imports."""
        # TODO: Implement import checking
        #   - For each alias in node.names:
        #   -   If alias.name in FORBIDDEN_IMPORTS (or is a parent
        #         of a forbidden module):
        #         self.errors.append(...)
        #   - self.generic_visit(node)
        ...

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """Check for forbidden ``from ... import ...`` statements."""
        # TODO: Implement from-import checking
        #   - If node.module name (or its top-level parent) is
        #     in FORBIDDEN_IMPORTS, record error
        #   - self.generic_visit(node)
        ...

    def visit_Call(self, node: ast.Call) -> Any:
        """Check for calls to forbidden built-in functions."""
        # TODO: Implement call checking
        #   - If node.func is an ast.Name and node.func.id in
        #     FORBIDDEN_FUNCTIONS, record error
        #   - self.generic_visit(node)
        ...

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        """Check for access to forbidden attributes."""
        # TODO: Implement attribute checking
        #   - Walk the attribute chain and check if any part
        #     matches a FORBIDDEN_ATTRS entry
        #   - self.generic_visit(node)
        ...
