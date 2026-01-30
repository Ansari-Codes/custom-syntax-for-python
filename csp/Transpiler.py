# import re

# def transpile(code: str) -> str:
#     # 1. UNIVERSAL STRING EXTRACTION (Handling \`)
#     strings = []
    
#     def save_string(match):
#         # match.group(1) contains the content inside the backticks
#         content = match.group(1)
        
#         # Unescape the backticks for Python: \` -> `
#         content = content.replace(r'\`', '`')
        
#         # Escape quotes to ensure they work inside Python's triple quotes
#         content = content.replace('"', '\\"').replace("'", "\\'")
        
#         placeholder = f"__STR_VAL_{len(strings)}__"
#         strings.append(f'"""{content}"""')
#         return placeholder

#     # REGEX EXPLANATION:
#     # `             : Match opening backtick
#     # (             : Start capture group
#     #   (?:         : Non-capturing group for choices
#     #     \\.       : Match any escaped character (e.g., \`)
#     #     |         : OR
#     #     [^`]      : Match any character that is NOT a backtick
#     #   )* : Repeat zero or more times
#     # )             : End capture group
#     # `             : Match closing backtick
#     backtick_pattern = r'`((?:\\.|[^`])*)`'
    
#     code_hidden = re.sub(backtick_pattern, save_string, code, flags=re.DOTALL)

#     py_lines = []
#     skip_multiline = False
    
#     for line in code_hidden.splitlines():
#         raw_line = line.rstrip()
#         line_stripped = raw_line.strip()

#         # Handle % comments
#         if line_stripped.startswith("%"):
#             if line_stripped.endswith("%") and len(line_stripped) > 1:
#                 continue
#             else:
#                 skip_multiline = not skip_multiline
#                 continue
#         if skip_multiline or line_stripped.startswith(("//", "#")):
#             continue

#         indent = re.match(r'\s*', raw_line).group()
#         line = line_stripped

#         # --- Standard Logic Transpilation ---
#         if line.startswith(":") and line.endswith(":") and line != ":":
#             line = "elif " + line[1:-1].strip() + ":"
#         elif line == ":":
#             line = "else:"

#         line = re.sub(r'^\$(\w+)\[(.*)\]:$', r'def \1(\2):', line)
#         line = re.sub(r'^>>\s*(.+):$', r'while \1:', line)
#         line = re.sub(r'^=>\s*(\w+)\s*:\s*(.+):$', r'for \1 in \2:', line)
#         line = re.sub(r'(\w+)\s*<-\s*(.+)', r'\1 = \2', line)
#         line = re.sub(r'^->\s*(.+)', r'return \1', line)

#         if line.endswith(":") and not line.startswith(("if ", "elif ", "else:", "while ", "for ", "def ")):
#             line = "if " + line[:-1].strip() + ":"

#         py_lines.append(indent + line)

#     final_python = "\n".join(py_lines)

#     # 2. RESTORE STRINGS
#     for i, s in enumerate(strings):
#         final_python = final_python.replace(f"__STR_VAL_{i}__", s)

#     return final_python

###############################################
# VERSION 0.1.3: New Transpiler Function below!
###############################################

import re

def transpile(code: str) -> str:
    # 1. UNIVERSAL STRING EXTRACTION
    strings = []
    def save_string(match):
        content = match.group(1).replace(r'\`', '`').replace('"', '\\"').replace("'", "\\'")
        placeholder = f"__STR_VAL_{len(strings)}__"
        strings.append(f'"""{content}"""')
        return placeholder

    backtick_pattern = r'`((?:\\.|[^`])*)`'
    code_hidden = re.sub(backtick_pattern, save_string, code, flags=re.DOTALL)

    py_lines = []
    skip_multiline = False
    in_function_header = False
    header_buffer = ""
    
    PY_BLOCK_STARTERS = {"try", "except", "finally", "with", "match", "case", "if", "elif", "else", "for", "while", "def", "class", "async", "pass", "return"}

    def find_main_colon(s):
        """Finds the first colon not inside brackets, braces, or parentheses."""
        depth = 0
        for i, char in enumerate(s):
            if char in "([{": depth += 1
            elif char in ")]}": depth -= 1
            elif char == ":" and depth == 0:
                return i
        return -1

    def process_logic(line):
        line = line.strip()
        if not line: return ""

        # Shorthands
        line = re.sub(r'(\w+)\s*<-\s*(.+)', r'\1 = \2', line)
        line = re.sub(r'->\s*(.+)', r'return \1', line)

        # 1. Functions ($name[args]: body)
        if line.startswith("$"):
            header, _, body = line.partition("]:")
            header = header[1:]; name, _, args = header.partition("[")
            return f"def {name}({args.strip()}): {process_logic(body)}"

        # 2. While Loops (>> cond: body)
        if line.startswith(">>"):
            idx = find_main_colon(line)
            if idx != -1:
                cond = line[2:idx].strip(); body = line[idx+1:].strip()
                return f"while {cond}: {process_logic(body)}"

        # 3. For Loops (=> var:iterable: body)
        if line.startswith("=>"):
            first_c = line.find(":")
            var = line[2:first_c].strip(); rest = line[first_c+1:]
            sec_c = find_main_colon(rest)
            if sec_c != -1:
                iterable = rest[:sec_c].strip(); body = rest[sec_c+1:].strip()
                return f"for {var} in {iterable}: {process_logic(body)}"

        # 4. Conditionals (:cond: body or : body)
        if line.startswith(":"):
            # Check for a second colon at depth 0
            second_c_idx = find_main_colon(line[1:])
            
            if second_c_idx != -1:
                # Pattern: :condition:body
                cond = line[1:second_c_idx+1].strip()
                body = line[second_c_idx+2:].strip()
                if not cond: # It was just ': : body'
                    return f"else: {process_logic(body)}"
                return f"elif {cond}: {process_logic(body)}"
            else:
                # Pattern: :condition: (ends with colon) OR :body
                if line.endswith(":") and line != ":":
                    return f"elif {line[1:-1].strip()}:"
                else:
                    return f"else: {process_logic(line[1:].strip())}"

        # 5. Implicit If Detection
        c_idx = find_main_colon(line)
        if c_idx != -1:
            prefix = line[:c_idx].strip(); body = line[c_idx+1:].strip()
            first = prefix.split()[0] if prefix else ""
            if first not in PY_BLOCK_STARTERS:
                return f"if {prefix}: {process_logic(body)}"

        return line

    for raw_line in code_hidden.splitlines():
        line_stripped = raw_line.strip()
        indent = re.match(r'\s*', raw_line).group()
        if line_stripped.startswith("%"):
            if not (line_stripped.endswith("%") and len(line_stripped) > 1): skip_multiline = not skip_multiline
            continue
        if skip_multiline or line_stripped.startswith(("//", "#")) or not line_stripped:
            py_lines.append(raw_line if not skip_multiline else ""); continue
        if line_stripped.startswith("$") and "]:" not in line_stripped:
            in_function_header = True; header_buffer = line_stripped; continue
        if in_function_header:
            header_buffer += " " + line_stripped
            if "]:" in line_stripped:
                in_function_header = False; py_lines.append(indent + process_logic(header_buffer)); header_buffer = ""
            continue
        py_lines.append(indent + process_logic(line_stripped))

    final_python = "\n".join(py_lines)
    for i, s in enumerate(strings): final_python = final_python.replace(f"__STR_VAL_{i}__", s)
    return final_python
