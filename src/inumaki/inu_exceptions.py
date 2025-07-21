"""
Enhanced exception handling for the Inumaki programming language interpreter.

This module provides structured exception classes with descriptive error messages,
context information, and helpful suggestions for common issues.
"""


class InumakiException(Exception):
    """Base exception class for all Inumaki interpreter errors."""
    
    def __init__(self, message, line=None, column=None, code_snippet=None, suggestion=None):
        self.message = message
        self.line = line
        self.column = column
        self.code_snippet = code_snippet
        self.suggestion = suggestion
        super().__init__(self._format_message())
    
    def _format_message(self):
        """Format the error message with context and suggestions."""
        parts = [f"{self.__class__.__name__}: {self.message}"]
        
        if self.line is not None:
            parts.append(f"  at line {self.line}" + (f", column {self.column}" if self.column else ""))
        
        if self.code_snippet:
            parts.append(f"  Code: {self.code_snippet}")
        
        if self.suggestion:
            parts.append(f"  Suggestion: {self.suggestion}")
        
        return "\n".join(parts)


class InumakiSyntaxError(InumakiException):
    """Raised when there's a syntax error in the source code."""
    pass


class InumakiParseError(InumakiException):
    """Raised when the parser encounters unexpected tokens or structure."""
    pass


class InumakiRuntimeError(InumakiException):
    """Raised when there's a runtime error during execution."""
    pass


class InumakiNameError(InumakiRuntimeError):
    """Raised when trying to access an undefined variable or function."""
    pass


class InumakiTypeError(InumakiRuntimeError):
    """Raised when there's a type-related error during execution."""
    pass


class InumakiArithmeticError(InumakiRuntimeError):
    """Raised when there's an arithmetic error like division by zero."""
    pass


class CursedSpeechOverloadError(InumakiRuntimeError):
    """Raised when the cursed speech threshold is exceeded."""
    
    def __init__(self, cursed_count, threshold=100):
        super().__init__(
            message=f"Throat irritation from excessive cursed speech usage! ({cursed_count}/{threshold})",
            suggestion="Use 'Cough_Syrup' to reset cursed speech counter and soothe the throat"
        )
        self.cursed_count = cursed_count
        self.threshold = threshold


class InumakiFunctionError(InumakiRuntimeError):
    """Raised when there's an error with function calls or definitions."""
    pass


# Helper functions for creating specific error messages
def create_unexpected_token_error(expected, got, line=None, column=None):
    """Create a descriptive error for unexpected tokens."""
    suggestion = None
    if expected == "Keyword" and got in ["Number", "String", "Identifier"]:
        suggestion = "Expected a keyword like 'Tuna', 'Mustard_Leaf', etc. Check the language syntax"
    elif expected in ["Tuna", "Tuna_Mayo"] and got == "Identifier":
        suggestion = f"Did you mean '{expected}' instead of '{got}'?"
    elif expected == "RightBrace" and got == "EOF":
        suggestion = "Missing closing brace '}'. Check for unmatched braces"
    
    return InumakiParseError(
        message=f"Expected '{expected}', but got '{got}'",
        line=line,
        column=column,
        suggestion=suggestion
    )


def create_undefined_variable_error(var_name, line=None, column=None):
    """Create a descriptive error for undefined variables."""
    return InumakiNameError(
        message=f"Undefined variable: '{var_name}'",
        line=line,
        column=column,
        suggestion=f"Make sure '{var_name}' is defined before use. Use 'Tuna {var_name} Tuna <value>' to define it"
    )


def create_division_by_zero_error(line=None, column=None):
    """Create a descriptive error for division by zero."""
    return InumakiArithmeticError(
        message="Division by zero",
        line=line,
        column=column,
        suggestion="Check that the divisor is not zero before performing division"
    )


def create_invalid_operator_error(operator, line=None, column=None):
    """Create a descriptive error for invalid operators."""
    return InumakiTypeError(
        message=f"Unknown or invalid operator: '{operator}'",
        line=line,
        column=column,
        suggestion="Check the operator syntax. Valid operators include: +, -, *, /, %, ==, !=, <, >, <=, >=, And, Or"
    )


def create_function_call_error(func_name, error_detail, line=None, column=None):
    """Create a descriptive error for function call issues."""
    return InumakiFunctionError(
        message=f"Error calling function '{func_name}': {error_detail}",
        line=line,
        column=column,
        suggestion="Check function name, parameters, and that the function is defined"
    )


def create_invalid_character_error(char, line=None, column=None):
    """Create a descriptive error for invalid characters in source code."""
    suggestion = None
    if char in "=!":
        suggestion = f"'{char}' must be part of a comparison operator like '==' or '!='"
    elif char.isascii() and not char.isprintable():
        suggestion = "Remove non-printable characters from the source code"
    
    return InumakiSyntaxError(
        message=f"Invalid character: '{char}'",
        line=line,
        column=column,
        suggestion=suggestion
    )


def create_unterminated_string_error(line=None, column=None):
    """Create a descriptive error for unterminated strings."""
    return InumakiSyntaxError(
        message="Unterminated string literal",
        line=line,
        column=column,
        suggestion="Add a closing quote to terminate the string"
    )