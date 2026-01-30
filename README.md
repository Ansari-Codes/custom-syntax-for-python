![](https://github.com/Ansari-Codes/custom-syntax-for-python/blob/main/statics/banner_transparent.png?raw=true)

# CSPLang – Custom Syntax for Python Language
**GITHUB**: https://github.com/Ansari-Codes/custom-syntax-for-python <br>
**PYPI**: https://pypi.org/project/csp-lang/

**CSPLang** is a high-speed, symbolic syntactic wrapper for Python. It transforms a compact, symbol-heavy DSL into executable Python code. Designed with the principle of **"Write less, do more,"** CSPLang turns Python's keyword-heavy structure into a sleek, streamlined experience.

> **The CSPLang Philosophy:** 
What if you had the full power of the Python ecosystem, but with the minimalist elegance of a functional language?

---

## 🚀 Key Features (v2.0)

* **Recursive One-Liners:** Define functions, loops, and conditions all on a single line.
* **Context-Aware Parsing:** Intelligently distinguishes between logic colons and data colons (like in dictionaries or list slices).
* **Symbolic Identity:** Replaces verbose keywords (`def`, `while`, `return`) with intuitive symbols (`$`, `>>`, `->`).
* **Zero-Overhead Integration:** Use any Python library (`numpy`, `tqdm`, `asyncio`) out of the box.

---

## 🛠 Installation

### Using git

```powershell
# Clone and Install
git clone https://github.com/Ansari-Codes/custom-syntax-for-python.git
cd custom-syntax-for-python
pip install .
```

### Using pip+git

```powershell
pip install git+https://github.com/Ansari-Codes/custom-syntax-for-python.git
```

### From pypi
```powershell
pip install csp-lang
```

---

## 📝 Syntax Overview

### 1. Variables & Assignment

Use the "flow" operator `<-` for assignment.

```python
name <- `Abubakar`
age  <- 19
data <- [1, 2, 3]
```

### 2. Universal Strings

Forget `f""`, `""`, or `''' '''`. Use backticks for everything. They support multiple lines and escaped backticks (`).

```python
msg <- `This is a 
multi-line string with a \`backtick\` inside.`

# F-strings work naturally:
print(f`Hello, {name}!`)
```

### 3. Conditionals (Implicit If)

No need to type `if`. A standalone condition ending in a colon is automatically treated as a conditional.

```python
x <- 10

x > 5:               # This is 'if'
    print(`Large`)
: x == 5:            # This is 'elif'
    print(`Medium`)
:                    # This is 'else'
    print(`Small`)

# NEW: One-liners are now supported!
x == 10: print(`Perfect Score`)
```

### 4. Loops

* **While:** Use `>>`
* **For:** Use `=>` (where `:` replaces `in`)

```python
# While Loop
count <- 3
>> count > 0: 
    print(count) 
    count <- count - 1

# For Loop
=> i:range(3):
    print(f`Iteration {i}`)
```

### 5. Functions & Methods

Defined using `$` and `[]`. The `->` symbol acts as the return.

```python
# Standard definition
$add[a, b]:
    -> a + b

# Works inside classes too!
class Math:
    $cube[self, n]: 
        -> n ** 3
```

---

## ⚡ Extreme Flexibility (v2.0 Stress Test)

Because CSPLang v2.0 uses a **Recursive Split Strategy**, it can handle complex Python constructs mixed with CSP symbols without breaking.

```python
# Slicing and Dictionaries work perfectly!
data <- [10, 20, 30, 40]
subset <- data[1:3]             # Transpiler ignores the slice colon
results <- {`val`: subset[0]}    # Transpiler ignores the dict colon

# Complex nesting and one-lining
$check[n]: 
    >> n > 0: 
        n%2==0:
            print("Even: ", n)
        :n%2!=0: print("Odd: ", n)
        :print(n in [1, 2, 3, 4][:2])
        n <- n - 1
check(10)
```

---

## 💻 CLI Usage

| Command | Description |
| --- | --- |
| `csp run file.csp` | Transpiles and executes immediately. |
| `csp transpile file.csp -o out.py` | Converts CSP to a standalone Python file. |
| `csp test` | Runs the internal test suite. |

---

## 👨‍💻 Developer

I am **Muhammad Abubakar Siddique Ansari**, a 1st-year ICS student at KIPS College, Punjab (Pakistan). I'm passionate about Data Science, AI, and building tools that make developers' lives easier.

**Portfolio:** [ansari-codes.github.io/portfolio](https://ansari-codes.github.io/portfolio)

---

## Logo
![logo](https://github.com/Ansari-Codes/custom-syntax-for-python/blob/main/statics/logo.png?raw=true)
---
