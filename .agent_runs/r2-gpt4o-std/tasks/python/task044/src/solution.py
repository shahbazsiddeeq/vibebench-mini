def to_snake(s):
    result = []
    i = 0
    while i < len(s):
        if s[i].isupper():
            start = i
            while i < len(s) and s[i].isupper():
                i += 1
            if i < len(s) and s[i].islower():
                result.append(s[start:i-1].lower())
                result.append('_')
                result.append(s[i-1].lower())
            else:
                result.append(s[start:i].lower())
            if i < len(s):
                result.append('_')
        else:
            result.append(s[i])
            i += 1
    return ''.join(result).rstrip('_')

def to_camel(s):
    parts = s.split('_')
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])

# Example usage:
# print(to_snake("HTMLParser"))  # Should output: "html_parser"
# print(to_camel("my_variable_name"))  # Should output: "myVariableName"
