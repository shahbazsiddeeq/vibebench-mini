# src/solution.py

import ast
import operator

class SafeEvalVisitor(ast.NodeVisitor):
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
            return
        raise ValueError("Unsupported operation")

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, (ast.UAdd, ast.USub)):
            return
        raise ValueError("Unsupported operation")

    def visit_Num(self, node):
        return

    def visit_Expr(self, node):
        self.generic_visit(node)

    def visit_Paren(self, node):
        self.generic_visit(node)

    def visit(self, node):
        if isinstance(node, (ast.Module, ast.Expression)):
            self.generic_visit(node)
        else:
            raise ValueError("Invalid syntax")

def safe_eval(expr: str) -> float:
    try:
        tree = ast.parse(expr, mode='eval')
        visitor = SafeEvalVisitor()
        visitor.visit(tree)
        
        # Evaluate the expression safely
        result = eval(compile(tree, filename='', mode='eval'), {"__builtins__": None}, {})
        
        if isinstance(result, (int, float)):
            return float(result)
        raise ValueError("Invalid result type")
    except ZeroDivisionError:
        raise ZeroDivisionError("Division by zero")
    except ValueError as e:
        raise ValueError("Invalid expression") from e
    except OverflowError:
        raise ValueError("Exponent too large")
