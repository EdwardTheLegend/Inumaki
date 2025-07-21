# Inumaki Error Handling Documentation

The Inumaki interpreter now features enhanced error handling with structured exception types, descriptive messages, and actionable suggestions to help developers debug their code more effectively.

## Error Categories

### Syntax Errors (`InumakiSyntaxError`)
These errors occur during the lexical analysis phase when invalid characters or malformed tokens are encountered.

**Examples:**
- Invalid characters: `Tuna x = 5` (single `=` is not allowed)
- Unterminated strings: `Tuna message Tuna "Hello`
- Non-printable characters in source code

**Error message format:**
```
InumakiSyntaxError: [Description]
  at line [N], column [N]
  Suggestion: [Helpful tip]
```

### Parse Errors (`InumakiParseError`)
These errors occur when the parser encounters unexpected tokens or invalid syntax structure.

**Examples:**
- Missing keywords: `Tuna x 5` (missing second `Tuna`)
- Unexpected tokens: Using identifiers where keywords are expected
- Invalid control structure syntax

**Error message format:**
```
InumakiParseError: Expected '[expected]', but got '[actual]'
  at line [N], column [N]
  Suggestion: [Context-specific advice]
```

### Runtime Errors
Runtime errors occur during code execution and are categorized into specific types:

#### Name Errors (`InumakiNameError`)
Raised when trying to access undefined variables or functions.

**Example:**
```inumaki
Tuna_Tuna(undefined_variable)
```

**Error message:**
```
InumakiNameError: Undefined variable: 'undefined_variable'
  Suggestion: Make sure 'undefined_variable' is defined before use. Use 'Tuna undefined_variable Tuna <value>' to define it
```

#### Arithmetic Errors (`InumakiArithmeticError`)
Raised for mathematical errors like division by zero.

**Example:**
```inumaki
Tuna result Tuna 10 / 0
```

**Error message:**
```
InumakiArithmeticError: Division by zero
  Suggestion: Check that the divisor is not zero before performing division
```

#### Function Errors (`InumakiFunctionError`)
Raised when there are issues with function calls or definitions.

**Examples:**
- Calling undefined functions
- Incorrect function arguments
- Errors within function execution

#### Type Errors (`InumakiTypeError`)
Raised for type-related errors and invalid operators.

**Example:**
```inumaki
Tuna result Tuna x InvalidOperator y
```

#### Cursed Speech Overload (`CursedSpeechOverloadError`)
A special error unique to Inumaki that occurs when too many cursed words are used.

**Error message:**
```
CursedSpeechOverloadError: Throat irritation from excessive cursed speech usage! (120/100)
  Suggestion: Use 'Cough_Syrup' to reset cursed speech counter and soothe the throat
```

## Error Message Components

All enhanced errors include:

1. **Error Type**: The specific exception class name (e.g., `InumakiSyntaxError`)
2. **Description**: A clear explanation of what went wrong
3. **Location**: Line and column information when available
4. **Suggestion**: Actionable advice on how to fix the issue

## Interactive Shell Behavior

When using the Inumaki interactive shell (`python inumaki.py`), errors are displayed immediately and the shell continues running, allowing for quick testing and debugging.

**Example session:**
```
$ python inumaki.py
Inumaki Interactive Shell
Enter Inumaki code (Ctrl+C or Ctrl+D to exit)
inumaki> Tuna x 5
InumakiParseError: Expected 'Keyword', but got 'Number'
  at line 1, column 8
  Suggestion: Expected a keyword like 'Tuna', 'Mustard_Leaf', etc. Check the language syntax
inumaki> Tuna x Tuna 5
inumaki> Tuna_Tuna(x)
5.0
inumaki> 
```

## File Execution Behavior

When running Inumaki files, errors are displayed with the filename for context:

```
$ python inumaki.py myprogram.inu
Error in myprogram.inu:
InumakiArithmeticError: Division by zero
  Suggestion: Check that the divisor is not zero before performing division
```

## Common Error Scenarios and Solutions

### 1. Missing Keywords
**Error:** `Expected 'Keyword', but got 'Number'`
**Solution:** Add the required keyword (usually `Tuna`) in the correct position

**Wrong:** `Tuna x 5`
**Right:** `Tuna x Tuna 5`

### 2. Undefined Variables
**Error:** `Undefined variable: 'varname'`
**Solution:** Define the variable before using it

**Solution:** `Tuna varname Tuna some_value`

### 3. Unterminated Strings
**Error:** `Unterminated string literal`
**Solution:** Add the closing quote

**Wrong:** `Tuna message Tuna "Hello`
**Right:** `Tuna message Tuna "Hello"`

### 4. Division by Zero
**Error:** `Division by zero`
**Solution:** Check the divisor value or add a conditional check

**Example fix:**
```inumaki
Mustard_Leaf Tuna divisor != 0 Tuna {
    Tuna result Tuna numerator / divisor
} Explode {
    Tuna_Tuna("Cannot divide by zero!")
}
```

### 5. Cursed Speech Overload
**Error:** `Throat irritation from excessive cursed speech usage!`
**Solution:** Use `Cough_Syrup` to reset the cursed counter

**Example:**
```inumaki
Kelp Reset cursed speech counter
Cough_Syrup
```

## Technical Implementation

The error handling system is implemented in `inu_exceptions.py` and integrated throughout the interpreter components:

- **Lexer** (`inu_lexer.py`): Enhanced character and token validation
- **Parser** (`inu_parser.py`): Improved syntax structure validation  
- **Interpreter** (`inu_interpreter.py`): Runtime error detection and reporting
- **Main Entry Point** (`inumaki.py`): Unified error display and handling

This provides a consistent, user-friendly error experience across all phases of code execution.