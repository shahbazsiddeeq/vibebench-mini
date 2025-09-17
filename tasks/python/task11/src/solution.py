from typing import Dict, List, Union

ALLOWED = {
    "verbose": ("--verbose", "bool"),
    "timeout": ("--timeout", "int"),
    "output": ("--output", "str"),
}


def _sanitize_str(v: str) -> str:
    if any(ch in v for ch in ("\x00", "\n", "\r")):
        raise ValueError("invalid string")
    return v


def build_cmd(base: Union[str, List[str]], args: Dict[str, object]) -> List[str]:
    cmd = [base] if isinstance(base, str) else list(base)
    for k, v in args.items():
        if k not in ALLOWED:
            raise ValueError(f"unknown key: {k}")
        flag, typ = ALLOWED[k]
        if typ == "bool":
            if not isinstance(v, bool):
                raise ValueError("verbose must be bool")
            if v:
                cmd.append(flag)
        elif typ == "int":
            if not (isinstance(v, int) and v > 0):
                raise ValueError("timeout must be positive int")
            cmd.extend([flag, str(v)])
        elif typ == "str":
            if not isinstance(v, str):
                raise ValueError("output must be str")
            cmd.extend([flag, _sanitize_str(v)])
    return cmd
