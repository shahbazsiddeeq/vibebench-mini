# src/solution.py

def build_cmd(base, args):
    if isinstance(base, str):
        cmd = [base]
    elif isinstance(base, list):
        cmd = base[:]
    else:
        raise ValueError("Base must be a string or a list of strings.")

    if not isinstance(args, dict):
        raise ValueError("Args must be a dictionary.")

    if 'verbose' in args:
        if not isinstance(args['verbose'], bool):
            raise ValueError("Verbose must be a boolean.")
        if args['verbose']:
            cmd.append("--verbose")

    if 'timeout' in args:
        if not isinstance(args['timeout'], int) or args['timeout'] <= 0:
            raise ValueError("Timeout must be a strictly positive integer.")
        cmd.append("--timeout")
        cmd.append(str(args['timeout']))

    if 'output' in args:
        if not isinstance(args['output'], str) or '\0' in args['output'] or '\n' in args['output'] or '\r' in args['output']:
            raise ValueError("Output must be a string without NUL, newline, or carriage-return characters.")
        cmd.append("--output")
        cmd.append(args['output'])

    return cmd
