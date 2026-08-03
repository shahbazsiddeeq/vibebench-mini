import ast
from typing import List, Tuple


def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    """
    Compute cyclomatic complexity for all function definitions in Python source code.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of tuples (function_name, lineno, complexity) sorted by (lineno, function_name)
        
    Raises:
        ValueError: If source is not valid Python
    """
    if not isinstance(source, str):
        raise ValueError("Source must be a string")
    
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax") from e
    
    results = []
    
    def analyze_function(node, parent_is_class=False):
        """Analyze a function definition node and return its complexity."""
        complexity = 1  # Base complexity
        
        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 0
                
            def visit_If(self, node):
                # Each if/elif adds 1
                self.complexity += 1
                # Continue visiting children
                self.generic_visit(node)
                
            def visit_For(self, node):
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_AsyncFor(self, node):
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_While(self, node):
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_ExceptHandler(self, node):
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_IfExp(self, node):
                # Ternary expression
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_BoolOp(self, node):
                # and/or: add (number of operands - 1)
                self.complexity += len(node.values) - 1
                self.generic_visit(node)
                
            def visit_comprehension(self, node):
                # Each if clause in a comprehension adds 1
                self.complexity += len(node.ifs)
                self.generic_visit(node)
                
            def visit_FunctionDef(self, node):
                # Don't visit nested function bodies
                pass
                
            def visit_AsyncFunctionDef(self, node):
                # Don't visit nested async function bodies
                pass
                
            def visit_Lambda(self, node):
                # Don't visit lambda bodies
                pass
                
            def visit_ClassDef(self, node):
                # Don't visit class bodies
                pass
        
        visitor = ComplexityVisitor()
        
        # Visit only the direct body of this function
        for stmt in node.body:
            visitor.visit(stmt)
            
        complexity += visitor.complexity
        return complexity
    
    def traverse(node, parent_is_class=False):
        """Traverse AST and collect all function definitions."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = node.name
            lineno = node.lineno
            complexity = analyze_function(node, parent_is_class)
            results.append((func_name, lineno, complexity))
            
            # Also traverse the body to find nested functions
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    traverse(child, False)
                elif isinstance(child, ast.ClassDef):
                    # Traverse class to find methods
                    for class_child in child.body:
                        traverse(class_child, True)
                        
        elif isinstance(node, ast.ClassDef):
            # Traverse class body to find methods
            for child in node.body:
                traverse(child, True)
                
        elif isinstance(node, ast.Module):
            # Traverse module body
            for child in node.body:
                traverse(child, False)
    
    traverse(tree)
    
    # Sort by (lineno, function_name)
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results
