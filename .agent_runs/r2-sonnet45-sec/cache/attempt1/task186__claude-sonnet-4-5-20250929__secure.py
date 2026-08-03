import ast
from typing import List, Tuple


def compute_complexity(source: str) -> List[Tuple[str, int, int]]:
    """
    Compute cyclomatic complexity for all function definitions in Python source.
    
    Args:
        source: Python source code as a string
        
    Returns:
        List of tuples (function_name, lineno, complexity) sorted by (lineno, function_name)
        
    Raises:
        ValueError: If source is not valid Python
    """
    # Validate input
    if not isinstance(source, str):
        raise ValueError("Source must be a string")
    
    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}")
    
    results = []
    
    # Visitor to find all function definitions and calculate complexity
    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None
            self.complexity = 0
            
        def visit_FunctionDef(self, node):
            self._visit_function(node)
            
        def visit_AsyncFunctionDef(self, node):
            self._visit_function(node)
            
        def _visit_function(self, node):
            # Save the current function context
            old_function = self.current_function
            old_complexity = self.complexity
            
            # Start measuring this function
            self.current_function = node
            self.complexity = 1  # Base complexity
            
            # Visit the function body, but stop at nested functions/classes
            for child in node.body:
                self._visit_body_node(child)
            
            # Record the result
            results.append((node.name, node.lineno, self.complexity))
            
            # Restore context
            self.current_function = old_function
            self.complexity = old_complexity
            
        def _visit_body_node(self, node):
            """Visit a node but don't descend into nested functions/classes/lambdas"""
            # Don't visit nested function definitions or classes
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # But we do need to process the nested function itself
                self.visit(node)
                return
            
            # For other nodes, calculate complexity and recurse
            if isinstance(node, ast.If):
                self.complexity += 1
                # Visit all parts of the if statement
                for child in node.body:
                    self._visit_body_node(child)
                for child in node.orelse:
                    self._visit_body_node(child)
                    
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                self.complexity += 1
                for child in node.body:
                    self._visit_body_node(child)
                for child in node.orelse:
                    self._visit_body_node(child)
                    
            elif isinstance(node, ast.Try):
                # Try itself doesn't add complexity, but handlers do
                for child in node.body:
                    self._visit_body_node(child)
                for handler in node.handlers:
                    self.complexity += 1  # Each except handler adds 1
                    for child in handler.body:
                        self._visit_body_node(child)
                for child in node.orelse:
                    self._visit_body_node(child)
                for child in node.finalbody:
                    self._visit_body_node(child)
                    
            elif isinstance(node, ast.IfExp):
                # Ternary expression
                self.complexity += 1
                self._visit_body_node(node.test)
                self._visit_body_node(node.body)
                self._visit_body_node(node.orelse)
                
            elif isinstance(node, ast.BoolOp):
                # and/or adds (number of operands - 1)
                self.complexity += len(node.values) - 1
                for child in node.values:
                    self._visit_body_node(child)
                    
            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                # Comprehensions: count if-clauses
                for generator in node.generators:
                    self.complexity += len(generator.ifs)
                    # Don't descend into the iterator or filters as they might contain lambdas
                    self._visit_body_node(generator.iter)
                    for if_clause in generator.ifs:
                        self._visit_body_node(if_clause)
                # Visit the element expression(s)
                if isinstance(node, ast.DictComp):
                    self._visit_body_node(node.key)
                    self._visit_body_node(node.value)
                else:
                    self._visit_body_node(node.elt)
                    
            else:
                # For all other nodes, recursively visit children
                for child in ast.iter_child_nodes(node):
                    self._visit_body_node(child)
    
    visitor = ComplexityVisitor()
    visitor.visit(tree)
    
    # Sort by (lineno, function_name)
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results
