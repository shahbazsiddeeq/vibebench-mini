# src/solution.py

def pipeline(*fns):
    def composed_function(x):
        for fn in fns:
            x = fn(x)
        return x
    return composed_function
