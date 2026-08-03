import re
import math

def safe_eval(expr: str) -> float:
    """
    Safely evaluates an arithmetic expression.

    The expression can contain only numeric literals, the binary operators
    +, -, *, /, **, unary + and -, and parentheses.
    Any other syntax raises ValueError. Division by zero raises ZeroDivisionError.
    A power operation whose exponent has magnitude greater than 1000 raises ValueError.

    Args:
        expr: The arithmetic expression string.

    Returns:
        The result of the evaluation as a float.

    Raises:
        ValueError: If the expression contains invalid syntax, mismatched parentheses,
                    or a power operation with an excessively large exponent.
        ZeroDivisionError: If division by zero occurs.
    """
    if not isinstance(expr, str):
        raise TypeError("Expression must be a string.")

    # Tokenization
    # This regex handles numbers (integers and floats), operators, and parentheses.
    # It also handles unary operators by allowing them to be preceded by nothing or an opening parenthesis.
    # We'll handle unary operators more robustly during parsing.
    token_pattern = re.compile(
        r"(\d+\.\d*|\.\d+|\d+)|"  # Floats and integers
        r"(\*\*|//|==|!=|<=|>=|<>|<<|>>|&|\||\^|~)|"  # Disallowed operators (catch them early)
        r"([+\-*/%()])"  # Allowed operators and parentheses
    )

    tokens = []
    last_token_type = None # None, 'number', 'operator', 'paren_open', 'paren_close'
    i = 0
    while i < len(expr):
        match = token_pattern.match(expr, i)
        if not match:
            # Check for whitespace and skip
            if expr[i].isspace():
                i += 1
                continue
            # If not whitespace and not a valid token, it's an error
            raise ValueError(f"Invalid character or syntax at position {i}: '{expr[i]}'")

        num_str, disallowed_op, allowed_op_or_paren = match.groups()

        if disallowed_op:
            raise ValueError(f"Disallowed operator '{disallowed_op}' found in expression.")

        if num_str is not None:
            tokens.append(float(num_str))
            last_token_type = 'number'
        elif allowed_op_or_paren:
            token = allowed_op_or_paren
            if token == '-':
                # Heuristic for unary minus: if it's at the beginning or after an opening paren or another operator
                if last_token_type is None or last_token_type in ('operator', 'paren_open'):
                    tokens.append('UNARY_MINUS')
                else:
                    tokens.append(token)
            elif token == '+':
                # Heuristic for unary plus: similar logic
                if last_token_type is None or last_token_type in ('operator', 'paren_open'):
                    tokens.append('UNARY_PLUS')
                else:
                    tokens.append(token)
            else:
                tokens.append(token)

            if token == '(':
                last_token_type = 'paren_open'
            elif token == ')':
                last_token_type = 'paren_close'
            else:
                last_token_type = 'operator'
        else:
            # This case should ideally not be reached if the regex is comprehensive
            raise ValueError(f"Unexpected parsing error at position {i}.")

        i = match.end()

    # Shunting-yard algorithm for converting infix to postfix (RPN)
    output_queue = []
    operator_stack = []
    precedence = {'+': 1, '-': 1, 'UNARY_PLUS': 3, 'UNARY_MINUS': 3, '*': 2, '/': 2, '**': 3}
    # Right-associativity for **
    associativity = {'+': 'left', '-': 'left', '*': 'left', '/': 'left', '**': 'right',
                     'UNARY_PLUS': 'right', 'UNARY_MINUS': 'right'}

    for token in tokens:
        if isinstance(token, float):
            output_queue.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError("Mismatched parentheses.")
            operator_stack.pop()  # Pop the '('
        elif token in precedence:  # It's an operator
            while (operator_stack and operator_stack[-1] != '(' and
                   ((associativity[token] == 'left' and precedence[token] <= precedence.get(operator_stack[-1], 0)) or
                    (associativity[token] == 'right' and precedence[token] < precedence.get(operator_stack[-1], 0)))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
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
            if token in ('UNARY_PLUS', 'UNARY_MINUS'):
                if not operand_stack:
                    raise ValueError("Invalid expression: not enough operands for unary operator.")
                operand = operand_stack.pop()
                if token == 'UNARY_MINUS':
                    operand_stack.append(-operand)
                else:  # UNARY_PLUS
                    operand_stack.append(operand)
            else: # Binary operator
                if len(operand_stack) < 2:
                    raise ValueError("Invalid expression: not enough operands for operator.")
                right = operand_stack.pop()
                left = operand_stack.pop()

                if token == '+':
                    operand_stack.append(left + right)
                elif token == '-':
                    operand_stack.append(left - right)
                elif token == '*':
                    operand_stack.append(left * right)
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero.")
                    operand_stack.append(left / right)
                elif token == '**':
                    # Resource exhaustion check for power operations
                    if abs(right) > 1000 and left not in (0, 1, -1):
                        raise ValueError("Exponent magnitude too large to prevent resource exhaustion.")
                    try:
                        operand_stack.append(left ** right)
                    except OverflowError:
                        raise ValueError("Result of power operation is too large to represent.")
                else:
                    raise ValueError(f"Unknown operator: {token}")

    if len(operand_stack) != 1:
        raise ValueError("Invalid expression: too many operands or operators.")

    result = operand_stack[0]
    if not math.isfinite(result):
        raise ValueError("Result is not a finite number (e.g., infinity or NaN).")

    return result
