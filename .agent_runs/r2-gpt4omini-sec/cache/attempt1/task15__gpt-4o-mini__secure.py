# src/solution.py

import ast
import operator

class SafeEvalVisitor(ast.NodeVisitor):
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
            return
        raise ValueError("Invalid operation")

    def visit_UnaryOp(self, node):
        if not isinstance(node.op, (ast.UAdd, ast.USub)):
            raise ValueError("Invalid operation")
        self.generic_visit(node)

    def visit_Num(self, node):
        return

    def visit_Expr(self, node):
        self.generic_visit(node)

    def visit_Paren(self, node):
        self.generic_visit(node)

    def visit(self, node):
        if not isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Num, ast.Expression)):
            raise ValueError("Invalid syntax")
        return super().visit(node)

def safe_eval(expr: str) -> float:
    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
        visitor = SafeEvalVisitor()
        visitor.visit(tree.body)

        # Evaluate the expression safely
        result = eval(compile(tree, filename='', mode='eval'), {"__builtins__": None}, {})
        
        if isinstance(result, (int, float)):
            return float(result)
        raise ValueError("Invalid result type")
    except ZeroDivisionError:
        raise ZeroDivisionError("Division by zero")
    except Exception:
        raise ValueError("Invalid expression")
