def write_config(path, config):
    lines = []
    for section, pairs in config.items():
        lines.append("[{}]\n".format(section))
        for key, value in pairs.items():
            if "\n" in value or "\r" in value:
                raise ValueError(
                    "Value for {}.{} contains a line break".format(section, key)
                )
            lines.append("{}={}\n".format(key, value))
        lines.append("\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
