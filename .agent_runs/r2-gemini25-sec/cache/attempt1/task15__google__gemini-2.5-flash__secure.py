import operator
import re

def safe_eval(expr: str) -> float:
    """
    Safely evaluates an arithmetic expression.

    The expression can contain only numeric literals, the binary operators
    +, -, *, /, **, unary + and -, and parentheses.
    Any other syntax raises ValueError.
    Division by zero raises ZeroDivisionError.
    A power operation whose exponent has magnitude greater than 1000 raises ValueError.

    Args:
        expr: The arithmetic expression string.

    Returns:
        The result of the evaluation as a float.

    Raises:
        ValueError: If the expression contains invalid syntax, names,
                    attribute access, function calls, subscripts, comprehensions,
                    lambdas, or if a power operation has an exponent with
                    magnitude greater than 1000.
        ZeroDivisionError: If division by zero occurs.
    """
    # Remove all whitespace for easier parsing
    expr = expr.replace(" ", "")

    # Regex to validate the entire expression.
    # It allows numbers (integers and floats), +, -, *, /, **, (, ).
    # It explicitly disallows any letters, underscores, or other symbols.
    # This is a strict whitelist approach.
    if not re.fullmatch(r"[\d\.\+\-\*\/\(\)]+", expr):
        raise ValueError("Invalid characters or syntax in expression.")

    # Check for common disallowed patterns that might slip through simple regex
    # (e.g., function calls like 'func()', variable names 'x', attribute access 'obj.attr')
    # This is a secondary check, as the fullmatch regex should catch most.
    # However, it's good to be explicit about what's forbidden.
    if re.search(r"[a-zA-Z_]", expr):
        raise ValueError("Names, function calls, or other disallowed syntax detected.")

    # Tokenize the expression
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isdigit() or (expr[i] == '.' and i + 1 < len(expr) and expr[i+1].isdigit()):
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
        elif expr[i] in ('+', '-', '*', '/', '(', ')'):
            tokens.append(expr[i])
            i += 1
        elif expr[i:i+2] == '**':
            tokens.append('**')
            i += 2
        else:
            raise ValueError(f"Unexpected character or sequence: {expr[i:]}")

    # Infix to Postfix conversion (Shunting-yard algorithm)
    output_queue = []
    operator_stack = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3}
    # Right-associativity for **
    associativity = {'+': 'left', '-': 'left', '*': 'left', '/': 'left', '**': 'right'}

    # Handle unary operators by transforming them into a distinct token or by
    # treating them as part of the number for the parser.
    # For simplicity, we'll handle them during evaluation or by context.
    # A common approach is to replace unary minus with '0 -' or a special token.
    # Here, we'll rely on the parsing logic to differentiate.
    # For example, `-(3)` becomes `0 - (3)` effectively.
    # `+3` is just `3`.

    # A more robust way to handle unary operators:
    processed_tokens = []
    expect_operand = True # True if the next token should be an operand (number or '(')
    for i, token in enumerate(tokens):
        if token == '-' and expect_operand:
            # Unary minus. Prepend a '0' to make it binary subtraction.
            # This simplifies the shunting-yard algorithm.
            processed_tokens.append('0')
            processed_tokens.append('-')
            expect_operand = False # After '0 -', we expect an operand
        elif token == '+' and expect_operand:
            # Unary plus. Just ignore it, as it doesn't change the value.
            # Or, if we want to be strict, we could treat it like unary minus
            # and prepend '0 +'. For now, ignoring is simpler and correct.
            pass
        elif token in ('+', '-', '*', '/', '**', '('):
            processed_tokens.append(token)
            expect_operand = True
        elif token == ')':
            processed_tokens.append(token)
            expect_operand = False # After ')', we expect an operator
        else: # Number
            processed_tokens.append(token)
            expect_operand = False

    tokens = processed_tokens

    for token in tokens:
        if token.replace('.', '', 1).isdigit():  # It's a number
            output_queue.append(float(token))
        elif token in precedence:  # It's an operator
            while (operator_stack and operator_stack[-1] != '(' and
                   (precedence.get(operator_stack[-1], 0) > precedence[token] or
                    (precedence.get(operator_stack[-1], 0) == precedence[token] and associativity[token] == 'left'))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError("Mismatched parentheses.")
            operator_stack.pop()  # Pop the '('
        else:
            raise ValueError(f"Unexpected token during parsing: {token}")

    while operator_stack:
        op = operator_stack.pop()
        if op == '(':
            raise ValueError("Mismatched parentheses.")
        output_queue.append(op)

    # Evaluate Postfix expression
    operand_stack = []
    for token in output_queue:
        if isinstance(token, float):
            operand_stack.append(token)
        else:  # It's an operator
            if len(operand_stack) < 2:
                raise ValueError("Invalid expression: not enough operands for operator.")
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()

            if token == '+':
                operand_stack.append(operand1 + operand2)
            elif token == '-':
                operand_stack.append(operand1 - operand2)
            elif token == '*':
                operand_stack.append(operand1 * operand2)
            elif token == '/':
                if operand2 == 0:
                    raise ZeroDivisionError("Division by zero.")
                operand_stack.append(operand1 / operand2)
            elif token == '**':
                # Security check for large exponents
                if abs(operand2) > 1000:
                    raise ValueError("Exponent magnitude exceeds 1000 to prevent resource exhaustion.")
                operand_stack.append(operand1 ** operand2)
            else:
                raise ValueError(f"Unknown operator: {token}")

    if len(operand_stack) != 1:
        raise ValueError("Invalid expression: too many operands or operators.")

    return operand_stack[0]
