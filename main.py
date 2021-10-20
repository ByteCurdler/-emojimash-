import operator

code = """
🔢123🔢🖨️🔢2🔢🧮➕🖨️🗑💬text💬📜wahoo📜🖨️
"""


class chars:
    number = "🔢"
    string = "📜"
    string_escape = "❕"
    math = "🧮"
    math_ops = {
        "➕": (operator.add, 2),
        "➖": (operator.sub, 2),
        "✖️": (operator.mul, 2),
        "➗": (operator.truediv, 2),
        "⤴️": (operator.pow, 2),
        "🟰": (operator.eq, 2),
        "=": (operator.eq, 2),
        "🔄": (operator.neg, 1),
        "‼️": (operator.not_, 1),
    }
    makelist = "📝"
    makedict = "📙"
    getitem = "🔍"
    print = "🖨"
    delete = "🗑"
    comment = "💬"
    label = "📛"


def lexify(text):
    inp = list(text)
    code = []
    labels = {}
    while inp:
        symbol = inp.pop(0)
        symname = [i for i in dir(chars) if getattr(chars, i) == symbol]
        if symname:
            symname = symname[0]
        else:
            symname = None
        # print(symbol, symname)
        if symname == "number":
            ind = inp.index(chars.number)
            buffer = "".join(inp[:ind])
            inp = inp[ind+1:]
            code.append(("push", int(buffer)))
        if symname == "string":
            buffer = ""
            while (char := inp.pop(0)) != chars.string:
                if char == chars.string_escape:
                    char2 = inp.pop(0)
                    if char2 in (chars.string, chars.string_escape):
                        buffer += char2
                    else:
                        buffer += char + char2
                else:
                    buffer += char
            code.append(("push", buffer))
        if symname == "math":
            op = inp.pop(0)
            if op in chars.math_ops:
                code.append(("math", op))
        if symname in ("list", "dict", "getitem", "print", "delete"):
            code.append((symname,))
        if symname in ("comment", "label"):
            ind = inp.index(symbol)
            buffer = "".join(inp[:ind])
            inp = inp[ind+1:]
        if symname == "label":
            labels[buffer] = len(code)
    return code, labels


def run(code, labels):
    pc = 0
    stack = []
    while pc < len(code):
        cmd, *args = code[pc]
        if cmd == "push":
            stack.append(args[0])
        if cmd == "math":
            op, numargs = chars.math_ops[args[0]]
            items = [stack.pop() for _ in range(numargs)]
            stack.append(op(*items))
        if cmd == "list":
            pass
        if cmd == "dict":
            pass
        if cmd == "getitem":
            pass
        if cmd == "print":
            pass
        if cmd == "delete":
            pass


print(lexify(code))
