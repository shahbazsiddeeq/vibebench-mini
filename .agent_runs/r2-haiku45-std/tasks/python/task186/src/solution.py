import ast
from typing import List, Tuple


def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    """
    Compute cyclomatic complexity for all functions in the given source code.
    
    Returns a list of tuples (function_name, lineno, complexity) sorted by
    (lineno, function_name).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python source: {e}")
    
    results = []
    
    def visit_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Visit a function definition and compute its complexity."""
        complexity = 1  # Base complexity
        
        # Walk through the function's own body (not nested functions/classes)
        for child in ast.walk(node):
            # Skip nested function/class definitions
            if child is not node and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue
            
            # Check if this node is directly in the function's body
            if not is_in_function_body(node, child):
                continue
            
            # Count decision points
            if isinstance(child, ast.If):
                complexity += 1
            elif isinstance(child, (ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.While):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.IfExp):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                # Each BoolOp adds (number of operands - 1)
                complexity += len(child.values) - 1
        
        # Count if-clauses in comprehensions
        for child in ast.walk(node):
            if child is not node and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue
            if not is_in_function_body(node, child):
                continue
            
            if isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in child.generators:
                    complexity += len(generator.ifs)
        
        results.append((node.name, node.lineno, complexity))
    
    def is_in_function_body(func_node: ast.FunctionDef | ast.AsyncFunctionDef, target: ast.AST) -> bool:
        """
        Check if target node is directly in func_node's body,
        not in a nested function/class/lambda.
        """
        if target is func_node:
            return False
        
        # Walk through the function body, stopping at nested definitions
        for node in ast.walk(func_node):
            if node is target:
                # Now check if target is nested inside a function/class/lambda
                # by walking from func_node and checking parents
                return not is_nested_in_definition(func_node, target)
        
        return False
    
    def is_nested_in_definition(func_node: ast.FunctionDef | ast.AsyncFunctionDef, target: ast.AST) -> bool:
        """Check if target is nested inside a function/class/lambda within func_node."""
        class NestedChecker(ast.NodeVisitor):
            def __init__(self):
                self.found = False
                self.in_nested = False
            
            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                if node is func_node:
                    self.generic_visit(node)
                else:
                    old_in_nested = self.in_nested
                    self.in_nested = True
                    self.generic_visit(node)
                    self.in_nested = old_in_nested
            
            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                if node is func_node:
                    self.generic_visit(node)
                else:
                    old_in_nested = self.in_nested
                    self.in_nested = True
                    self.generic_visit(node)
                    self.in_nested = old_in_nested
            
            def visit_ClassDef(self, node: ast.ClassDef) -> None:
                old_in_nested = self.in_nested
                self.in_nested = True
                self.generic_visit(node)
                self.in_nested = old_in_nested
            
            def visit_Lambda(self, node: ast.Lambda) -> None:
                old_in_nested = self.in_nested
                self.in_nested = True
                self.generic_visit(node)
                self.in_nested = old_in_nested
            
            def generic_visit(self, node: ast.AST) -> None:
                if node is target:
                    self.found = True
                    if self.in_nested:
                        return
                super().generic_visit(node)
        
        checker = NestedChecker()
        checker.visit(func_node)
        return checker.found and checker.in_nested
    
    # Simpler approach: collect all functions, then for each function,
    # count complexity only in its direct body
    class FunctionCollector(ast.NodeVisitor):
        def __init__(self):
            self.functions = []
        
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.functions.append(node)
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.functions.append(node)
            self.generic_visit(node)
    
    collector = FunctionCollector()
    collector.visit(tree)
    
    for func_node in collector.functions:
        complexity = compute_function_complexity(func_node)
        results.append((func_node.name, func_node.lineno, complexity))
    
    results.sort(key=lambda x: (x[1], x[0]))
    return results


def compute_function_complexity(func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    """Compute complexity for a single function, excluding nested definitions."""
    complexity = 1
    
    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.complexity = 0
        
        def visit_If(self, node: ast.If) -> None:
            self.complexity += 1
            self.generic_visit(node)
        
        def visit_For(self, node: ast.For) -> None:
            self.complexity += 1
            self.generic_visit(node)
        
        def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
            self.complexity += 1
            self.generic_visit(node)
        
        def visit_While(self, node: ast.While) -> None:
            self.complexity += 1
            self.generic_visit(node)
        
        def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
            self.complexity += 1
            self.generic_visit(node)
        
        def visit_IfExp(self, node: ast.IfExp) -> None:
            self.complexity += 1
            self.generic_visit(node)
        
        def visit_BoolOp(self, node: ast.BoolOp) -> None:
            self.complexity += len(node.values) - 1
            self.generic_visit(node)
        
        def visit_ListComp(self, node: ast.ListComp) -> None:
            for generator in node.generators:
                self.complexity += len(generator.ifs)
            self.generic_visit(node)
        
        def visit_SetComp(self, node: ast.SetComp) -> None:
            for generator in node.generators:
                self.complexity += len(generator.ifs)
            self.generic_visit(node)
        
        def visit_DictComp(self, node: ast.DictComp) -> None:
            for generator in node.generators:
                self.complexity += len(generator.ifs)
            self.generic_visit(node)
        
        def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
            for generator in node.generators:
                self.complexity += len(generator.ifs)
            self.generic_visit(node)
        
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            # Don't visit nested functions
            pass
        
        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            # Don't visit nested functions
            pass
        
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            # Don't visit nested classes
            pass
        
        def visit_Lambda(self, node: ast.Lambda) -> None:
            # Don't visit lambdas
            pass
    
    visitor = ComplexityVisitor()
    for stmt in func_node.body:
        visitor.visit(stmt)
    
    return complexity + visitor.complexity
