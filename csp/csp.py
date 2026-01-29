#!/usr/bin/env python3
import argparse
from pathlib import Path
from .Transpiler import transpile
from .Transpiler import transpile

def test():
    sources = [
        "x <- 5\ny <- x + 2\nz <- y * 3\nprint(x, y, z)",
        "_var <- 10\nanotherVar <- _var + 5\nprint(anotherVar)",
        "x <- 2\nx > 0:\n    print('x>0')\n: x == 2:\n        print('x==2')\n:\n        print('other')",
        "y <- 5\ny < 5:\n    print('y<5')\n:\n    print('y>=5')",
        "x <- 3\n>> x > 0:\n    print(x)\n    x <- x - 1",
        "y <- 2\n>> y > 0:\n    z <- y * 2\n    print(z)\n    y <- y - 1",
        "=> i:[]:\n    print(i)",
        "=> j:[1,2,3]:\n    print(j)",
        "=> k:range(3):\n    print(k)",
        "$add[a, b]:\n    -> a + b\nprint(add(2,3))",
        "$default_args[a=1, b=2]:\n    -> a * b\nprint(default_args())\nprint(default_args(3,4))",
        "x <- 2\n>> x > 0:\n    y <- x\n    >> y > 0:\n        print(x, y)\n        y <- y - 1\n    x <- x - 1",
        "a <- 3\na > 0:\n    print('outer')\n: a == 3:\n    print('middle')\n    >> i in [1,2]:\n        print(i)\n:\n        print('other')",
        "% This is a\nmultiline comment\n%\nx <- 10\n// single line comment\ny <- 5\n# another comment\nprint(x + y)",
        "$compute[a, b]:\n    result <- a + b\n    -> result\nprint(compute(2,5))",
        "_x <- 1\n_y_2 <- 3\nz3 <- _x + _y_2\nprint(z3)",
        "% Complex test %\nx <- 5\n>> x > 0:\n    y <- x\n    y > 2:\n        print('y>2')\n    :\n        print('y<=2')\n    x <- x - 1\n$func[a=1, b=2]:\n    -> a*b\nprint(func())\nprint(func(3,4))",
        "x <- 3\n>> x > 0:\n    y <- x\n    >> y > 0:\n        y % 2 == 0:\n            print(x, y, 'even')\n        else:\n            print(x, y, 'odd')\n        y <- y - 1\n    x <- x - 1",
        "$sum_squares[a=1, b=3]:\n    total <- 0\n    => i:range(a, b+1):\n        total <- total + i*i\n    -> total\nprint(sum_squares())\nprint(sum_squares(2,4))",
        "n <- 5\nn > 0:\n    n == 5:\n        print('five')\n    : n == 4:\n        print('four')\n    :\n        print('other')\nelse:\n    print('zero or negative')",
        "$factorial[n]:\n    result <- 1\n    >> n > 1:\n        result <- result * n\n        n <- n - 1\n    -> result\nprint(factorial(5))",
        "% This is a\nmultiline comment\n%\nx <- 2\n% single-line comment %\ny <- 3\nprint(x + y)",
        "$matrix_sum[matrix]:\n    total <- 0\n    => row:matrix:\n        => val:row:\n            total <- total + val\n    -> total\nprint(matrix_sum([[1,2],[3,4]]))",
        "nums <- [1,2,3,4,5]\n=> n:nums:\n    n % 2 == 0:\n        print(n, 'even')\n    :\n        print(n, 'odd')",
        "$square[x]:\n    -> x*x\n$square_sum[a, b]:\n    -> square(a) + square(b)\nprint(square_sum(2,3))",
        "x <- 5\n>> x > 0:\n    x % 2 == 0:\n        pass\n    :\n        print(x)\n    x <- x - 1",
        "a <- 2\n>> a > 0:\n    b <- 2\n    >> b > 0:\n        a == b:\n            print('match')\n        :\n            print('no match')\n        b <- b - 1\n    a <- a - 1",
        "print(f`This \nis {type(3)} \nmutliline\nWhile Loop:\nx <- 0\n>> x < 10:\n    print(x)\n    x <- x + 1`)",
        "x <- `outer \`inner\` value`\nprint(x)", # type: ignore
        "% This is mutliline without close\nprint(10)"
    ]

    passed = 0
    failed = []
    print("===== Starting Test =====")
    for i, source in enumerate(sources):
        print(f"-------- Test #{i + 1} -------- ")
        print(source)
        python_code = transpile(source)
        print("--- Generated Python:\n")
        print(python_code)
        print("\n--- Output:\n")
        try:
            g = {}
            exec(python_code, g)
            passed += 1
            print("Successful!")
        except Exception as e:
            print("Error!", str(e))
            failed.append(i + 1)
    print(f"Total Passed (out of {len(sources)}):", passed)
    print("Failed Tests:", failed)

def cmd_run(file_path: str):
    """Transpile CSP file and execute as Python"""
    path = Path(file_path)
    if not path.is_file():
        print(f"Error: file '{file_path}' not found.")
        return
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    py_code = transpile(code)
    try:
        exec(py_code, globals())
    except Exception as e:
        print(f"Runtime Error: {e}")

def cmd_transpile(file_path: str, output: str):
    path = Path(file_path)
    if not path.is_file():
        print(f"Error: file '{file_path}' not found.")
        return
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    py_code = transpile(code)
    out_path = Path(output)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(py_code)
    print(f"Transpiled Python written to {out_path}")

def main():
    parser = argparse.ArgumentParser(description="CSP - Custom Syntax for Python")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run a CSP program directly")
    run_parser.add_argument("file", help="CSP source file (.csp)")
    transpile_parser = subparsers.add_parser("transpile", help="Transpile CSP (*.csp) to Python (*.py)")
    transpile_parser.add_argument("file", help="CSP source file (.csp)")
    transpile_parser.add_argument("-o", "--output", required=True, help="Output Python file (.py)")
    subparsers.add_parser("test", help="Runs mutliple tests of CSP")
    args, unknown = parser.parse_known_args()
    if args.command is None and len(unknown) == 1:
        cmd_run(unknown[0])
    elif args.command == "test":
        test()
    elif args.command == "run":
        cmd_run(args.file)
    elif args.command == "transpile":
        cmd_transpile(args.file, args.output)
    else:
        parser.print_help()
