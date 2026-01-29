import re

def transpile(code: str) -> str:
    # 1. UNIVERSAL STRING EXTRACTION (Handling \`)
    strings = []
    
    def save_string(match):
        # match.group(1) contains the content inside the backticks
        content = match.group(1)
        
        # Unescape the backticks for Python: \` -> `
        content = content.replace(r'\`', '`')
        
        # Escape quotes to ensure they work inside Python's triple quotes
        content = content.replace('"', '\\"').replace("'", "\\'")
        
        placeholder = f"__STR_VAL_{len(strings)}__"
        strings.append(f'"""{content}"""')
        return placeholder

    # REGEX EXPLANATION:
    # `             : Match opening backtick
    # (             : Start capture group
    #   (?:         : Non-capturing group for choices
    #     \\.       : Match any escaped character (e.g., \`)
    #     |         : OR
    #     [^`]      : Match any character that is NOT a backtick
    #   )* : Repeat zero or more times
    # )             : End capture group
    # `             : Match closing backtick
    backtick_pattern = r'`((?:\\.|[^`])*)`'
    
    code_hidden = re.sub(backtick_pattern, save_string, code, flags=re.DOTALL)

    py_lines = []
    skip_multiline = False
    
    for line in code_hidden.splitlines():
        raw_line = line.rstrip()
        line_stripped = raw_line.strip()

        # Handle % comments
        if line_stripped.startswith("%"):
            if line_stripped.endswith("%") and len(line_stripped) > 1:
                continue
            else:
                skip_multiline = not skip_multiline
                continue
        if skip_multiline or line_stripped.startswith(("//", "#")):
            continue

        indent = re.match(r'\s*', raw_line).group()
        line = line_stripped

        # --- Standard Logic Transpilation ---
        if line.startswith(":") and line.endswith(":") and line != ":":
            line = "elif " + line[1:-1].strip() + ":"
        elif line == ":":
            line = "else:"

        line = re.sub(r'^\$(\w+)\[(.*)\]:$', r'def \1(\2):', line)
        line = re.sub(r'^>>\s*(.+):$', r'while \1:', line)
        line = re.sub(r'^=>\s*(\w+)\s*:\s*(.+):$', r'for \1 in \2:', line)
        line = re.sub(r'(\w+)\s*<-\s*(.+)', r'\1 = \2', line)
        line = re.sub(r'^->\s*(.+)', r'return \1', line)

        if line.endswith(":") and not line.startswith(("if ", "elif ", "else:", "while ", "for ", "def ")):
            line = "if " + line[:-1].strip() + ":"

        py_lines.append(indent + line)

    final_python = "\n".join(py_lines)

    # 2. RESTORE STRINGS
    for i, s in enumerate(strings):
        final_python = final_python.replace(f"__STR_VAL_{i}__", s)

    return final_python
