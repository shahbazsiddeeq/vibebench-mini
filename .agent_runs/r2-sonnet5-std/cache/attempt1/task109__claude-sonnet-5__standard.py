def pipeline(*fns):
    def run(x):
        for fn in fns:
            x = fn(x)
        return x
    return run
