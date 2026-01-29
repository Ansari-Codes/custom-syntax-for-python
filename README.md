# CSPLang – Custom Syntax for Python Language

**CSPLang** is a compact custom syntax designed for Python. It’s a toy language that works by transforming each line of CSP code into Python code, then executing it. The focus is on **writing less code but doing more work**.

Think about it this way: 
> What if you run real python, but write it in a bit different way?

Basically, CSP doesn’t block you from using Python’s full ecosystem; it just gives you a syntactic sugar wrapper so your loops, functions, conditionals, and variables can be written in a shorter or more “DSL-like” style.

---

## Developer

I am **Muhammad Abubakar Siddique Ansari**, a passionate developer in **Data Science and AI**. I love creating utilities, exploring new programming ideas, and building simple yet powerful tools.

I am currently (2026) a **1st-year ICS student at KIPS College**, Punjab – Pakistan.
Portfolio: [https://ansari-codes.github.io/portfolio](https://ansari-codes.github.io/portfolio)

---

## Installation

1. Clone the repo:
```powershell
git clone https://github.com/Ansari-Codes/custom-syntax-for-python.git
cd custom-syntax-for-python
pip install -e .
```

2. Via pip:
```powershell
pip install csp_lang
```

3. Pip installation using git:
```powershell
pip install git+https://github.com/Ansari-Codes/custom-syntax-for-python.git
```

---

## Key Principles

1. **Compact Syntax:** Write less code for the same Python functionality.
2. **Readable & Straightforward:** Easy to understand even if you are new to Python.
3. **Direct Python Integration:** Most Python functions, utilities, and modules work without changes.

---

## Syntax Overview

### 1. Comments

Single-line and multi-line comments are supported:

```python
# Single-line comment

% 
This is a
multi-line comment
%
```

### 2. Built-in Python Functions

Python functions and utilities work as-is.

```python
print(10)       # Works exactly like Python
len([1,2,3])    # Python’s len function
```

### 3. Variables

Use `<-` as the assignment operator:

```r
name <- "Muhammad"
age <- 15
x <- 5 + 3
```

### 4. Conditionals

CSP replaces `if`, `elif`, and `else` with a simple, readable syntax:

```python
x <- 5

%
IMPORTANT: Don;t use comments after colon of the conditions
EXAMPLE:
    1. Correct code:
    x>0:
    2. Buggy code:
    x>0: #comment
%

# if x > 0
x > 0:
    print("x is positive")
# elif x == 5
: x == 5:
    print("x is exactly 5")
# else
:
    print("other")
```

> The `:` indicates the start of a condition block, and `:` alone is treated as `else`.

### 5. Loops

#### While Loop

Use `>>` for while loops:

```python

%
IMPORTANT: Don;t use comments after colon of the condition
EXAMPLE:
    1. Correct code:
    x > 0:
    2. Buggy code:
    x > 0: #comment
%

x <- 3
>> x > 0:
    print(x)
    x <- x - 1
```

#### For Loop

Use `=>` with `:` replacing `in`:

```python

%
IMPORTANT: Don;t use comments after colon of the i:iterable:
EXAMPLE:
    1. Correct code:
    x:range(5):

    2. Buggy code:
    x:range(5): #comment
%

=> i:[1,2,3]:
    print(i)

=> j:range(5):
    print(j)
```

> `i` is the loop variable, and `iterable` can be any Python iterable.

### 6. Functions

Functions are defined using `$` and `[]` instead of `def` and `()`:

```python

%
IMPORTANT: Don;t use comments after colon of the functio definition
EXAMPLE:
    1. Correct code:
    $add[a, b]:

    2. Buggy code:
    $add[a, b]: #comment
%

$add[a, b]:
    -> a + b   # return statement

$greet[name="User"]:
    print(f"Hello {name}")
print(add(1, 1))
```

Call functions normally:

```python
print(add(2, 3))
greet()
greet("Muhammad")
```

### 7. Imports

Import modules as in Python:

```python
import math as mt
from math import sqrt
```

If you have tqdm installed, for example:
```python
from tqdm import tqdm
from time import sleep
=> i:tqdm(range(30)):
    sleep(0.1)
```

> Currently, importing other `.csp` files is not supported.

---

## File Format

CSP files use the `.csp` extension.

---

## CLI Usage

You can run CSP programs or transpile them to Python:

```bash
# Run directly
csp run program.csp

# Transpile to Python file
csp transpile program.csp -o program.py
python program.py

# run tests
csp test
```

---

## Example Program

```python
x <- 3
$fun[a]:
    print(f"Start {a}")
    >> a > 0:
        => i:[1,2]:
            print("Loop", i)
        a <- a - 1
    -> "done"

print(fun(x))
```

Output:

```
Start 3
Loop 1
Loop 2
Loop 1
Loop 2
Loop 1
Loop 2
done
```